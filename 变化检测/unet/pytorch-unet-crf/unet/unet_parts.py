# sub-parts of the U-Net model

import torch
import torch.nn as nn
import torch.nn.functional as F


# 实现左边的横向卷积
class double_conv(nn.Module):
    '''(conv => BN => ReLU) * 2'''

    def __init__(self, in_ch, out_ch):
        super(double_conv, self).__init__()
        self.conv = nn.Sequential(
            # 以第一层为例进行讲解
            # 输入通道数in_ch，输出通道数out_ch，卷积核设为kernal_size 3*3，padding为1，stride为1，dilation=1
            # 所以图中H*W能从572*572 变为 570*570,计算为570 = ((572 + 2*padding - dilation*(kernal_size-1) -1) / stride ) +1
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),  # 进行批标准化，在训练时，该层计算每次输入的均值与方差，并进行移动平均
            nn.ReLU(inplace=True),  # 激活函数
            nn.Conv2d(out_ch, out_ch, 3, padding=1),  # 再进行一次卷积，从570*570变为 568*568
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        x = self.conv(x)
        return x


# 实现左边第一行的卷积
class inconv(nn.Module):  #
    def __init__(self, in_ch, out_ch):
        super(inconv, self).__init__()
        self.conv = double_conv(in_ch, out_ch)  # 输入通道数in_ch为3， 输出通道数out_ch为64

    def forward(self, x):
        x = self.conv(x)
        return x


# 实现左边的向下池化操作，并完成另一层的卷积
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


# 实现右边的向上的采样操作，并完成该层相应的卷积操作
class up(nn.Module):
    def __init__(self, in_ch, out_ch, bilinear=True):
        super(up, self).__init__()

        #  would be a nice idea if the upsampling could be learned too,
        #  but my machine do not have enough memory to handle all those weights
        if bilinear:  # 声明使用的上采样方法为bilinear——双线性插值，默认使用这个值，计算方法为 floor(H*scale_factor)，所以由28*28变为56*56
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        else:  # 否则就使用转置卷积来实现上采样，计算式子为 （Height-1）*stride - 2*padding -kernal_size +output_padding
            self.up = nn.ConvTranspose2d(in_ch // 2, in_ch // 2, 2, stride=2)

        self.conv = double_conv(in_ch, out_ch)

    def forward(self, x1, x2):  # x2是左边特征提取传来的值
        # 第一次上采样返回56*56，但是还没结束
        x1 = self.up(x1)

        # input is CHW, [0]是batch_size, [1]是通道数，更改了下，与源码不同
        diffY = x1.size()[2] - x2.size()[2]  # 得到图像x2与x1的H的差值，56-64=-8
        diffX = x1.size()[3] - x2.size()[3]  # 得到图像x2与x1的W差值，56-64=-8

        # 用第一次上采样为例,即当上采样后的结果大小与右边的特征的结果大小不同时，通过填充来使x2的大小与x1相同
        # 对图像进行填充(-4,-4,-4,-4),左右上下都缩小4，所以最后使得64*64变为56*56
        x2 = F.pad(x2, (diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2))

        # for padding issues, see
        # https://github.com/HaiyongJiang/U-Net-Pytorch-Unstructured-Buggy/commit/0e854509c2cea854e247a9c615f175f76fbb2e3a
        # https://github.com/xiaopeng-liao/Pytorch-UNet/commit/8ebac70e633bac59fc22bb5195e513d5832fb3bd

        # 将最后上采样得到的值x1和左边特征提取的值进行拼接,dim=1即在通道数上进行拼接，由512变为1024
        x = torch.cat([x2, x1], dim=1)
        x = self.conv(x)
        return x


# 实现右边的最高层的最右边的卷积
class outconv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(outconv, self).__init__()
        self.conv = nn.Conv2d(in_ch, out_ch, 1)

    def forward(self, x):
        x = self.conv(x)
        return x
