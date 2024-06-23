import torch.nn as nn
import torch.nn.functional as F

from functools import partial

from pie.network.backbones.pytorch.resnet import resnet34, resnet101, resnet50
from pie.network.models.weight_utils import load_state_dict_from_s3
from pie.utils.registry import Registry

nonlinearity = partial(F.relu,inplace=True)

class Dblock(nn.Module):
    def __init__(self, channel):
        super(Dblock, self).__init__()
        self.dilate1 = nn.Conv2d(channel, channel, kernel_size=3, dilation=1, padding=1)
        self.dilate2 = nn.Conv2d(channel, channel, kernel_size=3, dilation=2, padding=2)
        self.dilate3 = nn.Conv2d(channel, channel, kernel_size=3, dilation=4, padding=4)
        self.dilate4 = nn.Conv2d(channel, channel, kernel_size=3, dilation=8, padding=8)
        # self.dilate5 = nn.Conv2d(channel, channel, kernel_size=3, dilation=16, padding=16)
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
                if m.bias is not None:
                    m.bias.data.zero_()

    def forward(self, x):
        dilate1_out = nonlinearity(self.dilate1(x))
        dilate2_out = nonlinearity(self.dilate2(dilate1_out))
        dilate3_out = nonlinearity(self.dilate3(dilate2_out))
        dilate4_out = nonlinearity(self.dilate4(dilate3_out))
        # dilate5_out = nonlinearity(self.dilate5(dilate4_out))
        out = x + dilate1_out + dilate2_out + dilate3_out + dilate4_out  # + dilate5_out
        return out


class DecoderBlock(nn.Module):
    def __init__(self, in_channels, n_filters):
        super(DecoderBlock, self).__init__()

        self.conv1 = nn.Conv2d(in_channels, in_channels // 4, 1)
        self.norm1 = nn.BatchNorm2d(in_channels // 4)
        self.relu1 = nonlinearity

        self.deconv2 = nn.ConvTranspose2d(in_channels // 4, in_channels // 4, 3, stride=2, padding=1, output_padding=1)
        self.norm2 = nn.BatchNorm2d(in_channels // 4)
        self.relu2 = nonlinearity

        self.conv3 = nn.Conv2d(in_channels // 4, n_filters, 1)
        self.norm3 = nn.BatchNorm2d(n_filters)
        self.relu3 = nonlinearity

    def forward(self, x):
        x = self.conv1(x)
        x = self.norm1(x)
        x = self.relu1(x)
        x = self.deconv2(x)
        x = self.norm2(x)
        x = self.relu2(x)
        x = self.conv3(x)
        x = self.norm3(x)
        x = self.relu3(x)
        return x

# 测试resnet

class DinkNet(nn.Module):
    def __init__(self, num_classes=1, resnet=resnet34,backbone='resnet34'):
        super(DinkNet, self).__init__()

        if backbone == 'resnet34':
            filters = [64, 128, 256, 512]
            Dblock_channal = 512
        elif backbone == 'resnet50' or backbone == 'resnet101':
            filters = [256, 512, 1024, 2048]
            Dblock_channal = 2048

        # filters = [64, 128, 256, 512]

        self.firstconv = resnet.conv1
        self.firstbn = resnet.bn1
        self.firstrelu = resnet.relu
        self.firstmaxpool = resnet.maxpool
        self.encoder1 = resnet.layer1
        self.encoder2 = resnet.layer2
        self.encoder3 = resnet.layer3
        self.encoder4 = resnet.layer4

        self.dblock = Dblock(Dblock_channal)

        self.decoder4 = DecoderBlock(filters[3], filters[2])
        self.decoder3 = DecoderBlock(filters[2], filters[1])
        self.decoder2 = DecoderBlock(filters[1], filters[0])
        self.decoder1 = DecoderBlock(filters[0], filters[0])

        self.finaldeconv1 = nn.ConvTranspose2d(filters[0], 32, 4, 2, 1)
        self.finalrelu1 = nonlinearity
        self.finalconv2 = nn.Conv2d(32, 32, 3, padding=1)
        self.finalrelu2 = nonlinearity
        self.finalconv3 = nn.Conv2d(32, num_classes, 3, padding=1)

    def forward(self, x):
        # Encoder

        x = self.firstconv(x)
        x = self.firstbn(x)
        x = self.firstrelu(x)
        x = self.firstmaxpool(x)
        e1 = self.encoder1(x)
        e2 = self.encoder2(e1)
        e3 = self.encoder3(e2)
        e4 = self.encoder4(e3)

        # Center
        e4 = self.dblock(e4)

        # Decoder
        d4 = self.decoder4(e4) + e3
        d3 = self.decoder3(d4) + e2
        d2 = self.decoder2(d3) + e1
        d1 = self.decoder1(d2)

        out = self.finaldeconv1(d1)
        out = self.finalrelu1(out)
        out = self.finalconv2(out)
        out = self.finalrelu2(out)
        out = self.finalconv3(out)

        # return F.sigmoid(out)
        return F.log_softmax(out,dim=1)


def _dinknet(num_classes,resnet,model_dir,s3_path,backbone):
    model = DinkNet(num_classes,resnet,backbone)
    if model_dir:
        state_dict = load_state_dict_from_s3(s3_path=s3_path, model_dir=model_dir)
        model.load_state_dict(state_dict)
        print('load weight----------')
    return model

# @Registry.divfun
def dinknet34(num_classes=2,in_channal=3,model_dir=None,s3_path=None):
    print('dinknet34-------------')
    resnet = resnet34(in_chan=in_channal, pretrained=False)
    return _dinknet(num_classes,resnet,model_dir,s3_path,backbone='resnet34')

# @Registry.divfun
def dinknet50(num_classes=2,in_channal=3,model_dir=None,s3_path=None):
    print('dinknet50-------------')
    resnet = resnet50(in_chan=in_channal, pretrained=False)
    return _dinknet(num_classes,resnet,model_dir,s3_path,backbone='resnet50')

# @Registry.divfun
def dinknet101(num_classes=2,in_channal=3,model_dir=None,s3_path=None):
    print('dinknet101-------------')
    resnet = resnet101(in_chan=in_channal, pretrained=False)
    return _dinknet(num_classes,resnet,model_dir,s3_path,backbone='resnet101')