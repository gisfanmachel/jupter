import argparse
import logging
import os

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from utils.data_loading import BasicDataset
from unet import UNet
from utils.utils import plot_img_and_mask

# ������Ϣ
# ����ͼƬ��python predict.py -i image.jpg -o output.jpg
# ����ͼƬ��python predict.py -i image1.jpg image2.jpg --viz --no-save��
# 4�������ļ����ֻ��CPU����CPU - only�汾��ʹ��ѡ�� - -cpuָ��
#
# 5�������ָ����ʹ�õ�ѵ���õ�ģ���ļ���ʹ�� - -mode MODEL.pth

# �ɼ�crf����󣬿��Խ�һЩ��������ʵ���жϽ�����޳���ʹ�ý�����Ӿ�ȷ
# (deeplearning) userdeMBP:Pytorch-UNet-master user$ python predict.py -i image1.jpg image2.jpg --viz --no-save --cpu --no-crf


# (deeplearning) userdeMBP:Pytorch-UNet-master user$ python predict.py -h
# usage: predict.py [-h] [--model FILE] --input INPUT [INPUT ...]
#                   [--output INPUT [INPUT ...]] [--cpu] [--viz] [--no-save]
#                   [--no-crf] [--mask-threshold MASK_THRESHOLD] [--scale SCALE]
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --model FILE, -m FILE
#                         Specify the file in which is stored the model (default
#                         : 'MODEL.pth')  #ָ��ʹ�õ�ѵ���õ�ģ���ļ���Ĭ��ʹ��MODEL.pth
#   --input INPUT [INPUT ...], -i INPUT [INPUT ...] #ָ��Ҫ����Ԥ���ͼ���ļ�������Ҫ�е�ֵ
#                         filenames of input images
#   --output INPUT [INPUT ...], -o INPUT [INPUT ...] #ָ��Ԥ������ɵ�ͼ���ļ�������
#                         filenames of ouput images
#   --cpu, -c             Do not use the cuda version of the net #ָ��ʹ��CPU��Ĭ��Ϊfalse����Ĭ��ʹ��GPU
#   --viz, -v             Visualize the images as they are processed #��ͼ�񱻴���ʱ��������ӻ���Ĭ��Ϊfalse���������Կ��ӻ�
#   --no-save, -n         Do not save the output masks #���洢�õ���Ԥ��ͼ��ĳͼ���ļ��У���--viz���ʹ�ã����ɶ�Ԥ�������ӻ������ǲ��洢�����Ĭ��Ϊfalse�����ᱣ����
#   --no-crf, -r          Do not use dense CRF postprocessing #ָ����ʹ��CRF��������к���Ĭ��Ϊfalse����ʹ��CRF
#   --mask-threshold MASK_THRESHOLD, -t MASK_THRESHOLD
#                         Minimum probability value to consider a mask pixel #��С��������ģ����Ϊ��ɫ�ĸ���ֵ��Ĭ��Ϊ0.5
#                         white
#   --scale SCALE, -s SCALE
#                         Scale factor for the input images #����ͼ��ı������ӣ�Ĭ��Ϊ0.5
def predict_img(net,
                full_img,
                device,
                scale_factor=1,
                out_threshold=0.5):
    net.eval()#�����������֤ģʽ����ʱ�����Ѿ�ѵ������
    img = torch.from_numpy(BasicDataset.preprocess(full_img, scale_factor, is_mask=False))
    img = img.unsqueeze(0)
    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():#�������ݶ�
        output = net(img)

        if net.n_classes > 1:
            probs = F.softmax(output, dim=1)[0]
        else:
            probs = torch.sigmoid(output)[0]

        tf = transforms.Compose([
            transforms.ToPILImage(),#���±��ͼƬ
            transforms.Resize((full_img.size[1], full_img.size[0])),
            transforms.ToTensor()#Ȼ���ٱ��Tensor��ʽ
        ])

        full_mask = tf(probs.cpu()).squeeze()

    if net.n_classes == 1:
        return (full_mask > out_threshold).numpy()
    else:
        return F.one_hot(full_mask.argmax(dim=0), net.n_classes).permute(2, 0, 1).numpy()


def get_args():
    parser = argparse.ArgumentParser(description='Predict masks from input images')
    parser.add_argument('--model', '-m', default='MODEL.pth', metavar='FILE',
                        help='Specify the file in which the model is stored')#ָ��ʹ�õ�ѵ���õ�ģ���ļ���Ĭ��ʹ��MODEL.pth
    parser.add_argument('--input', '-i', metavar='INPUT', nargs='+', help='Filenames of input images', required=True) #ָ��Ҫ����Ԥ���ͼ���ļ�
    parser.add_argument('--output', '-o', metavar='INPUT', nargs='+', help='Filenames of output images')#ָ��Ԥ������ɵ�ͼ���ļ�������
    parser.add_argument('--viz', '-v', action='store_true',
                        help='Visualize the images as they are processed')#��ͼ�񱻴���ʱ��������ӻ�
    parser.add_argument('--no-save', '-n', action='store_true', help='Do not save the output masks')#���洢�õ���Ԥ��ͼ��ĳͼ���ļ��У���--viz���ʹ�ã����ɶ�Ԥ�������ӻ������ǲ��洢���
    parser.add_argument('--mask-threshold', '-t', type=float, default=0.5,
                        help='Minimum probability value to consider a mask pixel white')#��С����ֵ������ģ����Ϊ��ɫ
    parser.add_argument('--scale', '-s', type=float, default=0.5,
                        help='Scale factor for the input images')#����ͼ��ı�������

    return parser.parse_args()


def get_output_filenames(args):
    def _generate_name(fn):
        split = os.path.splitext(fn)
        return f'{split[0]}_OUT{split[1]}'

    return args.output or list(map(_generate_name, args.input))


def mask_to_image(mask: np.ndarray):
    if mask.ndim == 2:
        return Image.fromarray((mask * 255).astype(np.uint8))
    elif mask.ndim == 3:
        return Image.fromarray((np.argmax(mask, axis=0) * 255 / mask.shape[0]).astype(np.uint8))


if __name__ == '__main__':
    args = get_args()
    in_files = args.input
    out_files = get_output_filenames(args)

    net = UNet(n_channels=3, n_classes=2) #����ʹ�õ�modelΪUNet��������UNet�ļ����¶����unet_model.py,����ͼ���ͨ��Ϊ3������ɫͼ���ж�������Ϊ2��

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logging.info(f'Loading model {args.model}')
    logging.info(f'Using device {device}')

    net.to(device=device)
    net.load_state_dict(torch.load(args.model, map_location=device))

    logging.info('Model loaded!')

    for i, filename in enumerate(in_files):
        logging.info(f'\nPredicting image {filename} ...')
        img = Image.open(filename)

        mask = predict_img(net=net,
                           full_img=img,
                           scale_factor=args.scale,
                           out_threshold=args.mask_threshold,
                           device=device)

        if not args.no_save:
            out_filename = out_files[i]
            result = mask_to_image(mask)
            result.save(out_filename)
            logging.info(f'Mask saved to {out_filename}')

        if args.viz:
            logging.info(f'Visualizing results for image {filename}, close to continue...')
            plot_img_and_mask(img, mask)
