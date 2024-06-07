""" Parts of the U-Net model """

import torch
import torch.nn as nn
import torch.nn.functional as F

#ʵ����ߵĺ�����
class DoubleConv(nn.Module):
    """(convolution => [BN] => ReLU) * 2"""

    def __init__(self, in_channels, out_channels, mid_channels=None):
        super().__init__()
        if not mid_channels:
            mid_channels = out_channels
        self.double_conv = nn.Sequential(
            # �Ե�һ��Ϊ�����н���
            # ����ͨ����in_ch�����ͨ����out_ch���������Ϊkernal_size 3*3��paddingΪ1��strideΪ1��dilation=1
            # ����ͼ��H*W�ܴ�572*572 ��Ϊ 570*570,����Ϊ570 = ((572 + 2*padding - dilation*(kernal_size-1) -1) / stride ) +1
            nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(mid_channels), #��������׼������ѵ��ʱ���ò����ÿ������ľ�ֵ�뷽��������ƶ�ƽ��
            nn.ReLU(inplace=True),#�����
            nn.Conv2d(mid_channels, out_channels, kernel_size=3, padding=1, bias=False),#�ٽ���һ�ξ������570*570��Ϊ 568*568
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.double_conv(x)

# ʵ����ߵ����³ػ��������������һ��ľ��
class Down(nn.Module):
    """Downscaling with maxpool then double conv"""

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels)
        )

    def forward(self, x):
        return self.maxpool_conv(x)

# #ʵ���ұߵ����ϵĲ�������������ɸò���Ӧ�ľ������
class Up(nn.Module):
    """Upscaling then double conv"""

    def __init__(self, in_channels, out_channels, bilinear=True):
        super().__init__()

        # if bilinear, use the normal convolutions to reduce the number of channels
        if bilinear:#����ʹ�õ��ϲ�������Ϊbilinear����˫���Բ�ֵ��Ĭ��ʹ�����ֵ�����㷽��Ϊ floor(H*scale_factor)��������28*28��Ϊ56*56
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
            self.conv = DoubleConv(in_channels, out_channels, in_channels // 2)
        else: #�����ʹ��ת�þ����ʵ���ϲ���������ʽ��Ϊ ��Height-1��*stride - 2*padding -kernal_size +output_padding
            self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)
            self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x1, x2): #x2�����������ȡ������ֵ
        x1 = self.up(x1)#��һ���ϲ�������56*56�����ǻ�û����
        # input is CHW  [0]��batch_size, [1]��ͨ�������������£���Դ�벻ͬ
        diffY = x2.size()[2] - x1.size()[2] #�õ�ͼ��x2��x1��H�Ĳ�ֵ��56-64=-8
        diffX = x2.size()[3] - x1.size()[3] #�õ�ͼ��x2��x1��W��ֵ��56-64=-8
        # �õ�һ���ϲ���Ϊ��,�����ϲ�����Ľ����С���ұߵ������Ľ����С��ͬʱ��ͨ�������ʹx2�Ĵ�С��x1��ͬ
        # ��ͼ��������(-4,-4,-4,-4),�������¶���С4���������ʹ��64*64��Ϊ56*56
        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2])
        # if you have padding issues, see
        # https://github.com/HaiyongJiang/U-Net-Pytorch-Unstructured-Buggy/commit/0e854509c2cea854e247a9c615f175f76fbb2e3a
        # https://github.com/xiaopeng-liao/Pytorch-UNet/commit/8ebac70e633bac59fc22bb5195e513d5832fb3bd
        # ������ϲ����õ���ֵx1�����������ȡ��ֵ����ƴ��,dim=1����ͨ�����Ͻ���ƴ�ӣ���512��Ϊ1024
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)

#ʵ���ұߵ���߲�����ұߵľ��
class OutConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        return self.conv(x)
