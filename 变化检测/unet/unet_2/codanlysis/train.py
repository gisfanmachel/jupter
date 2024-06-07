import sys
import os
from optparse import OptionParser
import numpy as np

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
from torch import optim
from evaluate import evaluate
# from eval import eval_net
from unet.unetmodel import UNet
from utils.utils import split_train_val, batch
from utils.load import get_ids, split_ids, get_imgs_and_masks
# 首先需要安装模块pydensecrf,实现CRF条件随机场的模块：

# (deeplearning) userdeMBP:Pytorch-UNet-master user$ python train.py -h
# Usage: train.py [options]
#
# Options:
#   -h, --help            show this help message and exit
#   -e EPOCHS, --epochs=EPOCHS
#                         number of epochs #指明迭代的次数
#   -b BATCHSIZE, --batch-size=BATCHSIZE
#                         batch size #图像批处理的大小
#   -l LR, --learning-rate=LR
#                         learning rate #使用的学习率
#   -g, --gpu             use cuda #使用GPU进行训练
#   -c LOAD, --load=LOAD  load file model #下载预训练的文件，在该基础上进行训练
#   -s SCALE, --scale=SCALE
#                         downscaling factor of the images #图像的缩小因子
# 复制代码

def train_net(net,
              epochs=5,
              batch_size=1,
              lr=0.1,
              val_percent=0.05,
              save_cp=True,
              gpu=False,
              img_scale=0.5):
    dir_img = 'data/train/'  # 训练图像文件夹
    dir_mask = 'data/train_masks/'  # 图像的结果文件夹
    dir_checkpoint = 'checkpoints/'  # 训练好的网络保存文件夹

    ids = get_ids(dir_img)  # 图片名字的后4位为数字，能作为图片id

    # 得到元祖列表为[(id1,0),(id1,1),(id2,0),(id2,1),...,(idn,0),(idn,1)]
    # 这样的作用是后面重新设置生成器时会通过后面的0,1作为utils.py中get_square函数的pos参数，pos=0的取左边的部分，pos=1的取右边的部分
    # 这样图片的数量就会变成2倍
    ids = split_ids(ids)

    iddataset = split_train_val(ids, val_percent)  # 将数据分为训练集和验证集两份

    print('''
    Starting training:
        Epochs: {}
        Batch size: {}
        Learning rate: {}
        Training size: {}
        Validation size: {}
        Checkpoints: {}
        CUDA: {}
    '''.format(epochs, batch_size, lr, len(iddataset['train']),
               len(iddataset['val']), str(save_cp), str(gpu)))

    N_train = len(iddataset['train'])  # 训练集长度

    optimizer = optim.SGD(net.parameters(),  # 定义优化器
                          lr=lr,
                          momentum=0.9,
                          weight_decay=0.0005)

    criterion = nn.BCELoss()  # 损失函数

    for epoch in range(epochs):  # 开始训练
        print('Starting epoch {}/{}.'.format(epoch + 1, epochs))
        net.train()  # 设置为训练模式

        # reset the generators重新设置生成器
        # 对输入图片dir_img和结果图片dir_mask进行相同的图片处理，即缩小、裁剪、转置、归一化后，将两个结合在一起，返回(imgs_normalized, masks)
        train = get_imgs_and_masks(iddataset['train'], dir_img, dir_mask, img_scale)
        val = get_imgs_and_masks(iddataset['val'], dir_img, dir_mask, img_scale)

        epoch_loss = 0

        for i, b in enumerate(batch(train, batch_size)):
            imgs = np.array([i[0] for i in b]).astype(np.float32)  # 得到输入图像数据
            true_masks = np.array([i[1] for i in b])  # 得到图像结果数据

            imgs = torch.from_numpy(imgs)
            true_masks = torch.from_numpy(true_masks)

            if gpu:
                imgs = imgs.cuda()
                true_masks = true_masks.cuda()

            masks_pred = net(imgs)  # 图像输入的网络后得到结果masks_pred，结果为灰度图像
            masks_probs_flat = masks_pred.view(-1)  # 将结果压扁

            true_masks_flat = true_masks.view(-1)

            loss = criterion(masks_probs_flat, true_masks_flat)  # 对两个结果计算损失
            epoch_loss += loss.item()

            print('{0:.4f} --- loss: {1:.6f}'.format(i * batch_size / N_train, loss.item()))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print('Epoch finished ! Loss: {}'.format(epoch_loss / i))  # 一次迭代后得到的平均损失

        if 1:
            # val_dice = eval_net(net, val, gpu)
            val_dice = evaluate(net, val, gpu)
            print('Validation Dice Coeff: {}'.format(val_dice))

        if save_cp:
            torch.save(net.state_dict(),
                       dir_checkpoint + 'CP{}.pth'.format(epoch + 1))
            print('Checkpoint {} saved !'.format(epoch + 1))


def get_args():
    parser = OptionParser()
    parser.add_option('-e', '--epochs', dest='epochs', default=5, type='int',  # 设置迭代数
                      help='number of epochs')
    parser.add_option('-b', '--batch-size', dest='batchsize', default=10,  # 设置训练批处理数
                      type='int', help='batch size')
    parser.add_option('-l', '--learning-rate', dest='lr', default=0.1,  # 设置学习率
                      type='float', help='learning rate')
    parser.add_option('-g', '--gpu', action='store_true', dest='gpu',  # 是否使用GPU，默认是不使用
                      default=False, help='use cuda')
    parser.add_option('-c', '--load', dest='load',  # 下载之前预训练好的模型
                      default=False, help='load file model')
    parser.add_option('-s', '--scale', dest='scale', type='float',  # 图像的缩小因子,用来重新设置图片大小
                      default=0.5, help='downscaling factor of the images')

    (options, args) = parser.parse_args()
    return options


if __name__ == '__main__':
    args = get_args()  # 得到设置的所有参数信息

    net = UNet(n_channels=3, n_classes=1)

    if args.load:  # 是否加载预先训练好的模型
        net.load_state_dict(torch.load(args.load))
        print('Model loaded from {}'.format(args.load))

    if args.gpu:  # 是否使用GPU，设置为True，则使用
        net.cuda()
        # cudnn.benchmark = True # faster convolutions, but more memory

    try:  # 开始训练
        train_net(net=net,
                  epochs=args.epochs,
                  batch_size=args.batchsize,
                  lr=args.lr,
                  gpu=args.gpu,
                  img_scale=args.scale)
    except KeyboardInterrupt:  # 如果键盘输入ctrl+c停止，则会将结果保存在INTERRUPTED.pth中
        torch.save(net.state_dict(), 'INTERRUPTED.pth')
        print('Saved interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
