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

# 返回信息
# 单张图片：python predict.py -i image.jpg -o output.jpg
# 多张图片：python predict.py -i image1.jpg image2.jpg --viz --no-save？
# 4）如果你的计算机只有CPU，即CPU - only版本，使用选项 - -cpu指定
#
# 5）你可以指定你使用的训练好的模型文件，使用 - -mode MODEL.pth

# 可见crf后处理后，可以将一些不符合事实的判断结果给剔除，使得结果更加精确
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
#                         : 'MODEL.pth')  #指明使用的训练好的模型文件，默认使用MODEL.pth
#   --input INPUT [INPUT ...], -i INPUT [INPUT ...] #指明要进行预测的图像文件，必须要有的值
#                         filenames of input images
#   --output INPUT [INPUT ...], -o INPUT [INPUT ...] #指明预测后生成的图像文件的名字
#                         filenames of ouput images
#   --cpu, -c             Do not use the cuda version of the net #指明使用CPU，默认为false，即默认使用GPU
#   --viz, -v             Visualize the images as they are processed #当图像被处理时，将其可视化，默认为false，即不可以可视化
#   --no-save, -n         Do not save the output masks #不存储得到的预测图像到某图像文件中，和--viz结合使用，即可对预测结果可视化，但是不存储结果，默认为false，即会保存结果
#   --no-crf, -r          Do not use dense CRF postprocessing #指明不使用CRF对输出进行后处理，默认为false，即使用CRF
#   --mask-threshold MASK_THRESHOLD, -t MASK_THRESHOLD
#                         Minimum probability value to consider a mask pixel #最小化考虑掩模像素为白色的概率值，默认为0.5
#                         white
#   --scale SCALE, -s SCALE
#                         Scale factor for the input images #输入图像的比例因子，默认为0.5
def predict_img(net,
                full_img,
                device,
                scale_factor=1,
                out_threshold=0.5):
    net.eval()#进入网络的验证模式，这时网络已经训练好了
    img = torch.from_numpy(BasicDataset.preprocess(full_img, scale_factor, is_mask=False))
    img = img.unsqueeze(0)
    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():#不计算梯度
        output = net(img)

        if net.n_classes > 1:
            probs = F.softmax(output, dim=1)[0]
        else:
            probs = torch.sigmoid(output)[0]

        tf = transforms.Compose([
            transforms.ToPILImage(),#重新变成图片
            transforms.Resize((full_img.size[1], full_img.size[0])),
            transforms.ToTensor()#然后再变成Tensor格式
        ])

        full_mask = tf(probs.cpu()).squeeze()

    if net.n_classes == 1:
        return (full_mask > out_threshold).numpy()
    else:
        return F.one_hot(full_mask.argmax(dim=0), net.n_classes).permute(2, 0, 1).numpy()


def get_args():
    parser = argparse.ArgumentParser(description='Predict masks from input images')
    parser.add_argument('--model', '-m', default='MODEL.pth', metavar='FILE',
                        help='Specify the file in which the model is stored')#指明使用的训练好的模型文件，默认使用MODEL.pth
    parser.add_argument('--input', '-i', metavar='INPUT', nargs='+', help='Filenames of input images', required=True) #指明要进行预测的图像文件
    parser.add_argument('--output', '-o', metavar='INPUT', nargs='+', help='Filenames of output images')#指明预测后生成的图像文件的名字
    parser.add_argument('--viz', '-v', action='store_true',
                        help='Visualize the images as they are processed')#当图像被处理时，将其可视化
    parser.add_argument('--no-save', '-n', action='store_true', help='Do not save the output masks')#不存储得到的预测图像到某图像文件中，和--viz结合使用，即可对预测结果可视化，但是不存储结果
    parser.add_argument('--mask-threshold', '-t', type=float, default=0.5,
                        help='Minimum probability value to consider a mask pixel white')#最小概率值考虑掩模像素为白色
    parser.add_argument('--scale', '-s', type=float, default=0.5,
                        help='Scale factor for the input images')#输入图像的比例因子

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

    net = UNet(n_channels=3, n_classes=2) #定义使用的model为UNet，调用在UNet文件夹下定义的unet_model.py,定义图像的通道为3，即彩色图像，判断类型设为2种

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
