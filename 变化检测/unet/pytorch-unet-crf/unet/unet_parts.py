# sub-parts of the U-Net model

import torch
import torch.nn as nn
import torch.nn.functional as F


# ʵ����ߵĺ�����
class double_conv(nn.Module):
    '''(conv => BN => ReLU) * 2'''

    def __init__(self, in_ch, out_ch):
        super(double_conv, self).__init__()
        self.conv = nn.Sequential(
            # �Ե�һ��Ϊ�����н���
            # ����ͨ����in_ch�����ͨ����out_ch���������Ϊkernal_size 3*3��paddingΪ1��strideΪ1��dilation=1
            # ����ͼ��H*W�ܴ�572*572 ��Ϊ 570*570,����Ϊ570 = ((572 + 2*padding - dilation*(kernal_size-1) -1) / stride ) +1
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),  # ��������׼������ѵ��ʱ���ò����ÿ������ľ�ֵ�뷽��������ƶ�ƽ��
            nn.ReLU(inplace=True),  # �����
            nn.Conv2d(out_ch, out_ch, 3, padding=1),  # �ٽ���һ�ξ������570*570��Ϊ 568*568
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        x = self.conv(x)
        return x


# ʵ����ߵ�һ�еľ��
class inconv(nn.Module):  #
    def __init__(self, in_ch, out_ch):
        super(inconv, self).__init__()
        self.conv = double_conv(in_ch, out_ch)  # ����ͨ����in_chΪ3�� ���ͨ����out_chΪ64

    def forward(self, x):
        x = self.conv(x)
        return x


# ʵ����ߵ����³ػ��������������һ��ľ��
class down(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(down, self).__init__()
        self.mpconv = nn.Sequential(
            nn.MaxPool2d(2),
            double_conv(in_ch, out_ch)
        )

    def forward(self, x):
        x = self.mpconv(x)
        return x


# ʵ���ұߵ����ϵĲ�������������ɸò���Ӧ�ľ������
class up(nn.Module):
    def __init__(self, in_ch, out_ch, bilinear=True):
        super(up, self).__init__()

        #  would be a nice idea if the upsampling could be learned too,
        #  but my machine do not have enough memory to handle all those weights
        if bilinear:  # ����ʹ�õ��ϲ�������Ϊbilinear����˫���Բ�ֵ��Ĭ��ʹ�����ֵ�����㷽��Ϊ floor(H*scale_factor)��������28*28��Ϊ56*56
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        else:  # �����ʹ��ת�þ����ʵ���ϲ���������ʽ��Ϊ ��Height-1��*stride - 2*padding -kernal_size +output_padding
            self.up = nn.ConvTranspose2d(in_ch // 2, in_ch // 2, 2, stride=2)

        self.conv = double_conv(in_ch, out_ch)

    def forward(self, x1, x2):  # x2�����������ȡ������ֵ
        # ��һ���ϲ�������56*56�����ǻ�û����
        x1 = self.up(x1)

        # input is CHW, [0]��batch_size, [1]��ͨ�������������£���Դ�벻ͬ
        diffY = x1.size()[2] - x2.size()[2]  # �õ�ͼ��x2��x1��H�Ĳ�ֵ��56-64=-8
        diffX = x1.size()[3] - x2.size()[3]  # �õ�ͼ��x2��x1��W��ֵ��56-64=-8

        # �õ�һ���ϲ���Ϊ��,�����ϲ�����Ľ����С���ұߵ������Ľ����С��ͬʱ��ͨ�������ʹx2�Ĵ�С��x1��ͬ
        # ��ͼ��������(-4,-4,-4,-4),�������¶���С4���������ʹ��64*64��Ϊ56*56
        x2 = F.pad(x2, (diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2))

        # for padding issues, see
        # https://github.com/HaiyongJiang/U-Net-Pytorch-Unstructured-Buggy/commit/0e854509c2cea854e247a9c615f175f76fbb2e3a
        # https://github.com/xiaopeng-liao/Pytorch-UNet/commit/8ebac70e633bac59fc22bb5195e513d5832fb3bd

        # ������ϲ����õ���ֵx1�����������ȡ��ֵ����ƴ��,dim=1����ͨ�����Ͻ���ƴ�ӣ���512��Ϊ1024
        x = torch.cat([x2, x1], dim=1)
        x = self.conv(x)
        return x


# ʵ���ұߵ���߲�����ұߵľ��
class outconv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(outconv, self).__init__()
        self.conv = nn.Conv2d(in_ch, out_ch, 1)

    def forward(self, x):
        x = self.conv(x)
        return x
