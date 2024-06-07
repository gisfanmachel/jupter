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
# ������Ҫ��װģ��pydensecrf,ʵ��CRF�����������ģ�飺

# (deeplearning) userdeMBP:Pytorch-UNet-master user$ python train.py -h
# Usage: train.py [options]
#
# Options:
#   -h, --help            show this help message and exit
#   -e EPOCHS, --epochs=EPOCHS
#                         number of epochs #ָ�������Ĵ���
#   -b BATCHSIZE, --batch-size=BATCHSIZE
#                         batch size #ͼ��������Ĵ�С
#   -l LR, --learning-rate=LR
#                         learning rate #ʹ�õ�ѧϰ��
#   -g, --gpu             use cuda #ʹ��GPU����ѵ��
#   -c LOAD, --load=LOAD  load file model #����Ԥѵ�����ļ����ڸû����Ͻ���ѵ��
#   -s SCALE, --scale=SCALE
#                         downscaling factor of the images #ͼ�����С����
# ���ƴ���

def train_net(net,
              epochs=5,
              batch_size=1,
              lr=0.1,
              val_percent=0.05,
              save_cp=True,
              gpu=False,
              img_scale=0.5):
    dir_img = 'data/train/'  # ѵ��ͼ���ļ���
    dir_mask = 'data/train_masks/'  # ͼ��Ľ���ļ���
    dir_checkpoint = 'checkpoints/'  # ѵ���õ����籣���ļ���

    ids = get_ids(dir_img)  # ͼƬ���ֵĺ�4λΪ���֣�����ΪͼƬid

    # �õ�Ԫ���б�Ϊ[(id1,0),(id1,1),(id2,0),(id2,1),...,(idn,0),(idn,1)]
    # �����������Ǻ�����������������ʱ��ͨ�������0,1��Ϊutils.py��get_square������pos������pos=0��ȡ��ߵĲ��֣�pos=1��ȡ�ұߵĲ���
    # ����ͼƬ�������ͻ���2��
    ids = split_ids(ids)

    iddataset = split_train_val(ids, val_percent)  # �����ݷ�Ϊѵ��������֤������

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

    N_train = len(iddataset['train'])  # ѵ��������

    optimizer = optim.SGD(net.parameters(),  # �����Ż���
                          lr=lr,
                          momentum=0.9,
                          weight_decay=0.0005)

    criterion = nn.BCELoss()  # ��ʧ����

    for epoch in range(epochs):  # ��ʼѵ��
        print('Starting epoch {}/{}.'.format(epoch + 1, epochs))
        net.train()  # ����Ϊѵ��ģʽ

        # reset the generators��������������
        # ������ͼƬdir_img�ͽ��ͼƬdir_mask������ͬ��ͼƬ��������С���ü���ת�á���һ���󣬽����������һ�𣬷���(imgs_normalized, masks)
        train = get_imgs_and_masks(iddataset['train'], dir_img, dir_mask, img_scale)
        val = get_imgs_and_masks(iddataset['val'], dir_img, dir_mask, img_scale)

        epoch_loss = 0

        for i, b in enumerate(batch(train, batch_size)):
            imgs = np.array([i[0] for i in b]).astype(np.float32)  # �õ�����ͼ������
            true_masks = np.array([i[1] for i in b])  # �õ�ͼ��������

            imgs = torch.from_numpy(imgs)
            true_masks = torch.from_numpy(true_masks)

            if gpu:
                imgs = imgs.cuda()
                true_masks = true_masks.cuda()

            masks_pred = net(imgs)  # ͼ������������õ����masks_pred�����Ϊ�Ҷ�ͼ��
            masks_probs_flat = masks_pred.view(-1)  # �����ѹ��

            true_masks_flat = true_masks.view(-1)

            loss = criterion(masks_probs_flat, true_masks_flat)  # ���������������ʧ
            epoch_loss += loss.item()

            print('{0:.4f} --- loss: {1:.6f}'.format(i * batch_size / N_train, loss.item()))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print('Epoch finished ! Loss: {}'.format(epoch_loss / i))  # һ�ε�����õ���ƽ����ʧ

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
    parser.add_option('-e', '--epochs', dest='epochs', default=5, type='int',  # ���õ�����
                      help='number of epochs')
    parser.add_option('-b', '--batch-size', dest='batchsize', default=10,  # ����ѵ����������
                      type='int', help='batch size')
    parser.add_option('-l', '--learning-rate', dest='lr', default=0.1,  # ����ѧϰ��
                      type='float', help='learning rate')
    parser.add_option('-g', '--gpu', action='store_true', dest='gpu',  # �Ƿ�ʹ��GPU��Ĭ���ǲ�ʹ��
                      default=False, help='use cuda')
    parser.add_option('-c', '--load', dest='load',  # ����֮ǰԤѵ���õ�ģ��
                      default=False, help='load file model')
    parser.add_option('-s', '--scale', dest='scale', type='float',  # ͼ�����С����,������������ͼƬ��С
                      default=0.5, help='downscaling factor of the images')

    (options, args) = parser.parse_args()
    return options


if __name__ == '__main__':
    args = get_args()  # �õ����õ����в�����Ϣ

    net = UNet(n_channels=3, n_classes=1)

    if args.load:  # �Ƿ����Ԥ��ѵ���õ�ģ��
        net.load_state_dict(torch.load(args.load))
        print('Model loaded from {}'.format(args.load))

    if args.gpu:  # �Ƿ�ʹ��GPU������ΪTrue����ʹ��
        net.cuda()
        # cudnn.benchmark = True # faster convolutions, but more memory

    try:  # ��ʼѵ��
        train_net(net=net,
                  epochs=args.epochs,
                  batch_size=args.batchsize,
                  lr=args.lr,
                  gpu=args.gpu,
                  img_scale=args.scale)
    except KeyboardInterrupt:  # �����������ctrl+cֹͣ����Ὣ���������INTERRUPTED.pth��
        torch.save(net.state_dict(), 'INTERRUPTED.pth')
        print('Saved interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
