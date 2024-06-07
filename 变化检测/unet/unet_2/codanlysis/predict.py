# coding:utf-8
import argparse
import os

import numpy as np
import torch
import torch.nn.functional as F

from PIL import Image

from unet.unetmodel import UNet
from utils.utils import resize_and_crop, normalize, split_img_into_squares, hwc_to_chw, merge_masks
from utils.crf import dense_crf
from utils.data_vis import plot_img_and_mask

from torchvision import transforms
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
                scale_factor=0.5,
                out_threshold=0.5,
                use_dense_crf=True,
                use_gpu=False):
    net.eval()  # 进入网络的验证模式，这时网络已经训练好了
    img_height = full_img.size[1]  # 得到图片的高
    img_width = full_img.size[0]  # 得到图片的宽

    img = resize_and_crop(full_img, scale=scale_factor)  # 在utils文件夹的utils.py中定义的函数，重新定义图像大小并进行切割，然后将图像转为数组np.array
    img = normalize(img)  # 对像素值进行归一化，由[0,255]变为[0,1]

    left_square, right_square = split_img_into_squares(img)  # 将图像分成左右两块，来分别进行判断

    left_square = hwc_to_chw(left_square)  # 对图像进行转置，将(H, W, C)变为(C, H, W),便于后面计算
    right_square = hwc_to_chw(right_square)

    X_left = torch.from_numpy(left_square).unsqueeze(0)  # 将(C, H, W)变为(1, C, H, W)，因为网络中的输入格式第一个还有一个batch_size的值
    X_right = torch.from_numpy(right_square).unsqueeze(0)

    if use_gpu:
        X_left = X_left.cuda()
        X_right = X_right.cuda()

    with torch.no_grad():  # 不计算梯度
        output_left = net(X_left)
        output_right = net(X_right)

        left_probs = output_left.squeeze(0)
        right_probs = output_right.squeeze(0)

        tf = transforms.Compose(
            [
                transforms.ToPILImage(),  # 重新变成图片
                transforms.Resize(img_height),  # 恢复原来的大小
                transforms.ToTensor()  # 然后再变成Tensor格式
            ]
        )

        left_probs = tf(left_probs.cpu())
        right_probs = tf(right_probs.cpu())

        left_mask_np = left_probs.squeeze().cpu().numpy()
        right_mask_np = right_probs.squeeze().cpu().numpy()

    full_mask = merge_masks(left_mask_np, right_mask_np, img_width)  # 将左右两个拆分后的图片合并起来

    # 对得到的结果根据设置决定是否进行CRF处理
    if use_dense_crf:
        full_mask = dense_crf(np.array(full_img).astype(np.uint8), full_mask)

    return full_mask > out_threshold


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='MODEL.pth',  # 指明使用的训练好的模型文件，默认使用MODEL.pth
                        metavar='FILE',
                        help="Specify the file in which is stored the model"
                             " (default : 'MODEL.pth')")
    parser.add_argument('--input', '-i', metavar='INPUT', nargs='+',  # 指明要进行预测的图像文件
                        help='filenames of input images', required=True)

    parser.add_argument('--output', '-o', metavar='INPUT', nargs='+',  # 指明预测后生成的图像文件的名字
                        help='filenames of ouput images')
    parser.add_argument('--cpu', '-c', action='store_true',  # 指明使用CPU
                        help="Do not use the cuda version of the net",
                        default=False)
    parser.add_argument('--viz', '-v', action='store_true',
                        help="Visualize the images as they are processed",  # 当图像被处理时，将其可视化
                        default=False)
    parser.add_argument('--no-save', '-n', action='store_true',  # 不存储得到的预测图像到某图像文件中，和--viz结合使用，即可对预测结果可视化，但是不存储结果
                        help="Do not save the output masks",
                        default=False)
    parser.add_argument('--no-crf', '-r', action='store_true',  # 指明不使用CRF对输出进行后处理
                        help="Do not use dense CRF postprocessing",
                        default=False)
    parser.add_argument('--mask-threshold', '-t', type=float,
                        help="Minimum probability value to consider a mask pixel white",  # 最小概率值考虑掩模像素为白色
                        default=0.5)
    parser.add_argument('--scale', '-s', type=float,
                        help="Scale factor for the input images",  # 输入图像的比例因子
                        default=0.5)

    return parser.parse_args()


def get_output_filenames(args):  # 从输入的选项args值中得到输出文件名
    in_files = args.input
    out_files = []

    if not args.output:  # 如果在选项中没有指定输出的图片文件的名字，那么就会根据输入图片文件名，在其后面添加'_OUT'后缀来作为输出图片文件名
        for f in in_files:
            pathsplit = os.path.splitext(f)  # 将文件名和扩展名分开，pathsplit[0]是文件名,pathsplit[1]是扩展名
            out_files.append("{}_OUT{}".format(pathsplit[0], pathsplit[1]))  # 得到输出图片文件名
    elif len(in_files) != len(args.output):  # 如果设置了output名,查看input和output的数量是否相同，即如果input是两张图，那么设置的output也必须是两个，否则报错
        print("Error : Input files and output files are not of the same length")
        raise SystemExit()
    else:
        out_files = args.output

    return out_files


def mask_to_image(mask):
    return Image.fromarray((mask * 255).astype(np.uint8))  # 从数组array转成Image


if __name__ == "__main__":
    args = get_args()  # 得到输入的选项设置的值
    in_files = args.input  # 得到输入的图像文件
    out_files = get_output_filenames(args)  # 从输入的选项args值中得到输出文件名

    net = UNet(n_channels=3, n_classes=1)  # 定义使用的model为UNet，调用在UNet文件夹下定义的unet_model.py,定义图像的通道为3，即彩色图像，判断类型设为1种

    print("Loading model {}".format(args.model))  # 指定使用的训练好的model

    if not args.cpu:  # 指明使用GPU
        print("Using CUDA version of the net, prepare your GPU !")
        net.cuda()
        net.load_state_dict(torch.load(args.model))
    else:  # 否则使用CPU
        net.cpu()
        net.load_state_dict(torch.load(args.model, map_location='cpu'))
        print("Using CPU version of the net, this may be very slow")

    print("Model loaded !")

    for i, fn in enumerate(in_files):  # 对图片进行预测
        print("\nPredicting image {} ...".format(fn))

        img = Image.open(fn)
        if img.size[0] < img.size[1]:  # (W, H, C)
            print("Error: image height larger than the width")

        mask = predict_img(net=net,
                           full_img=img,
                           scale_factor=args.scale,
                           out_threshold=args.mask_threshold,
                           use_dense_crf=not args.no_crf,
                           use_gpu=not args.cpu)

        if args.viz:  # 可视化输入的图片和生成的预测图片
            print("Visualizing results for image {}, close to continue ...".format(fn))
            plot_img_and_mask(img, mask)

        if not args.no_save:  # 设置为False，则保存
            out_fn = out_files[i]
            result = mask_to_image(mask)  # 从数组array转成Image
            result.save(out_files[i])  # 然后保存

            print("Mask saved to {}".format(out_files[i]))