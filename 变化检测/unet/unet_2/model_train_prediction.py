#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2022/1/11 13:23
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : model_train_prediction.py
# @Descr   : 模型的构建和训练:基于前期的数据准备，我们可以使用PyTorch构建深度学习卷积网络，进而进行建筑物的提取
# @Software: PyCharm


import os.path
import time
from pathlib import Path
import numpy as np  # linear algebra
import torch
import torchvision.transforms as transforms
from PIL import Image
from skimage import transform
from torch import nn
from torch.utils.data import Dataset, DataLoader
from matplotlib import pyplot as plt
from torchvision.transforms import ToPILImage
root_path = "F:\\Work\\ai_deep_learning\\Unet"
# root_path = "E:\\系统开发\\AI\\ai_deep_learning\\Unet"
base_path = Path(root_path + "\\data\\deeplearn-cities\\dataset\\dataset\\trainning")
train_dl = None
valid_dl = None
model_name = "unet_build_model100epc.pth"
batch_size = 4
# batch_size = 8
num_workers = 8
pin_memory = True


class UNET(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()

        # parameters: in_channels, out_channels, kernel_size, padding
        self.conv1 = self.contract_block(in_channels, 32, 7, 3)
        self.conv2 = self.contract_block(32, 64, 3, 1)
        self.conv3 = self.contract_block(64, 128, 3, 1)

        self.upconv3 = self.expand_block(128, 64, 3, 1)
        self.upconv2 = self.expand_block(64 * 2, 32, 3, 1)
        self.upconv1 = self.expand_block(32 * 2, out_channels, 3, 1)

    # will be call when create instance
    def __call__(self, x):
        # downsampling part
        conv1 = self.conv1(x)
        conv2 = self.conv2(conv1)
        conv3 = self.conv3(conv2)

        upconv3 = self.upconv3(conv3)
        upconv2 = self.upconv2(torch.cat([upconv3, conv2], 1))
        upconv1 = self.upconv1(torch.cat([upconv2, conv1], 1))

        return upconv1

    def contract_block(self, in_channels, out_channels, kernel_size, padding):
        # 以第一层为例进行讲解
        # 输入通道数in_ch，输出通道数out_ch，卷积核设为kernal_size 3*3，padding为1，stride为1，dilation=1
        # 所以图中H*W能从572*572 变为 570*570,计算为570 = ((572 + 2*padding - dilation*(kernal_size-1) -1) / stride ) +1

        contract = nn.Sequential(
            torch.nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=1, padding=padding),
            torch.nn.BatchNorm2d(out_channels),#进行批标准化，在训练时，该层计算每次输入的均值与方差，并进行移动平均
            torch.nn.ReLU(),#激活函数
            torch.nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size, stride=1, padding=padding),#再进行一次卷积，从570*570变为 568*568
            torch.nn.BatchNorm2d(out_channels),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )

        return contract

    def expand_block(self, in_channels, out_channels, kernel_size, padding):
        expand = nn.Sequential(torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=padding),
                               torch.nn.BatchNorm2d(out_channels),
                               torch.nn.ReLU(),
                               torch.nn.Conv2d(out_channels, out_channels, kernel_size, stride=1, padding=padding),
                               torch.nn.BatchNorm2d(out_channels),
                               torch.nn.ReLU(),
                               torch.nn.ConvTranspose2d(out_channels, out_channels, kernel_size=3, stride=2, padding=1,
                                                        output_padding=1)
                               )
        return expand


def build_model():
    unet = UNET(3, 2)
    print(unet)
    # print("test")


class CanopyDataset(Dataset):
    def __init__(self, img_dir, msk_dir, pytorch=True, transforms=None):
        super().__init__()

        # Loop through the files in red folder and combine, into a dictionary, the other bands
        self.files = [self.combine_files(f, img_dir, msk_dir) for f in img_dir.iterdir() if not f.is_dir()]
        self.pytorch = pytorch
        self.transforms = transforms

    def combine_files(self, r_file: Path, img_dir, msk_dir):
        files = {'image': r_file,
                 'mask': msk_dir / r_file.name.replace('naip_tiles',
                                                       'lu_masks')}  # .replace('naip_tiles', 'lu_masks') is not necessary, just in case you have different name

        return files

    def __len__(self):
        return len(self.files)

    def open_as_array(self, idx, invert=False, include_nir=False, augment=False):
        img_pil = Image.open(self.files[idx]['image'])
        # augment the image
        if augment:
            img_pil = self.transforms(img_pil)

        raw_rgb = np.asarray(img_pil).astype(float)
        #         src_raw_rgb = rio.open(self.files[idx]['image'])
        #         raw_rgb = src_raw_rgb.read()
        #         src_raw_rgb.close()

        raw_rgb = transform.resize(raw_rgb, (512, 512, 3))
        if invert:
            raw_rgb = raw_rgb.transpose((2, 0, 1))

        # normalize
        # return (raw_rgb / np.iinfo(raw_rgb.dtype).max)
        return (raw_rgb / 255.0)

    def open_mask(self, idx, add_dims=False, augment=False):
        mask_pil = Image.open(self.files[idx]['mask'])
        # augment the image
        if augment:
            mask_pil = self.transforms(mask_pil)

        raw_mask = np.array(mask_pil).astype(float)
        #         print('The filename is:=======', self.files[idx]['mask'])
        #         src_raw_mask = rio.open(self.files[idx]['mask'])
        #         raw_mask = src_raw_mask.read()
        #         src_raw_mask.close()

        raw_mask = transform.resize(raw_mask, (512, 512))
        raw_mask = np.where(raw_mask == 5, 1,
                            0)  # in the land use map of PHiladelphis, the tree is 1, 5 is for building

        return np.expand_dims(raw_mask, 0) if add_dims else raw_mask

    def __getitem__(self, idx):

        img_pil = Image.open(self.files[idx]['image'])
        mask_pil = Image.open(self.files[idx]['mask'])
        # mask_y = np.array(mask_pil).astype(float)

        ## just the colorization of the raw image, not need to change the mask
        if self.transforms:
            img_pil = self.transforms(img_pil)
            mask_pil = self.transforms(mask_pil)

        image_x = np.asarray(img_pil).astype(float)
        mask_y = np.array(mask_pil).astype(float)

        image_x = transform.resize(image_x, (512, 512, 3))
        mask_y = transform.resize(mask_y, (512, 512))

        image_x = image_x.transpose((2, 0, 1)) / 255.0
        mask_y = np.where(mask_y == 5, 1, 0)  # in the land use map of PHiladelphis, the tree is 1, 5 is for building

        # # 90 degree rotation
        # if np.random.rand()<0.5:
        #     angle = np.random.randint(4) * 90
        #     image_x = ndimage.rotate(image_x, angle,reshape=True)
        #     mask_y = ndimage.rotate(mask_y, angle, reshape=True)

        # # vertical flip
        # if np.random.rand()<0.5:
        #     image_x = np.flip(image_x, 0)
        #     mask_y = np.flip(mask_y, 0)

        # # horizonal flip
        # if np.random.rand()<0.5:
        #     image_x = np.flip(image_x, 1)
        #     mask_y = np.flip(mask_y, 1)

        ## add scale in future

        # x = torch.tensor(self.open_as_array(idx, \
        #                                     invert=self.pytorch, \
        #                                     include_nir=True, \
        #                                     augment=True), \
        #                                     dtype=torch.float32)
        # y = torch.tensor(self.open_mask(idx, add_dims=False, augment=True), \
        #                                 dtype=torch.torch.int64)

        # return x, y

        return torch.tensor(image_x, dtype=torch.float32), torch.tensor(mask_y, dtype=torch.int64)

    def open_as_pil(self, idx):
        arr = 256 * self.open_as_array(idx)

        return Image.fromarray(arr.astype(np.uint8), 'RGB')

    def __repr__(self):
        s = 'Dataset class with {} files'.format(self.__len__())

        return s


def convert_data():
    global train_dl
    global valid_dl
    # this is used to augment the image
    # transform_aug = transforms.Compose([
    #     # transforms.ToPILImage(),
    #     # transforms.Resize((300, 300)),
    #     # transforms.CenterCrop((100, 100)),
    #     # transforms.RandomCrop((80, 80)),
    #     transforms.RandomHorizontalFlip(p=0.5),
    #     transforms.RandomRotation(degrees=(-90, 90)),
    #     transforms.RandomVerticalFlip(p=0.5)
    #     # transforms.ToTensor()
    #     # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    # ])

    # data = CanopyDataset(base_path/'imgs',
    #                     base_path/'labels',
    #                     transforms=transform_aug)

    data = CanopyDataset(base_path / 'imgs',
                         base_path / 'labels')

    # train_ds, valid_ds = torch.utils.data.random_split(data, (2615, 872))
    train_size = int(0.7 * len(data))
    val_size = len(data) - train_size
    train_ds, valid_ds = torch.utils.data.random_split(data, (train_size, val_size))
    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    valid_dl = DataLoader(valid_ds, batch_size=batch_size, shuffle=True)

    # train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=pin_memory)
    # valid_dl = DataLoader(valid_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=pin_memory)

    print('train_dl is:', len(train_dl))
    print('valid_dl is:', len(valid_dl))


def train(model, train_dl, valid_dl, loss_fn, optimizer, acc_fn, epochs=1):
    start = time.time()
    model.cuda()

    train_loss, valid_loss = [], []

    best_acc = 0.0

    for epoch in range(epochs):
        print('Epoch {}/{}'.format(epoch, epochs - 1))
        print('-' * 10)

        for phase in ['train', 'valid']:
            if phase == 'train':
                model.train(True)  # Set trainind mode = true
                dataloader = train_dl
            else:
                model.train(False)  # Set model to evaluate mode
                dataloader = valid_dl

            running_loss = 0.0
            running_acc = 0.0

            step = 0

            # iterate over data
            for x, y in dataloader:
                x = x.cuda()
                y = y.cuda()
                step += 1

                # forward pass
                if phase == 'train':
                    # zero the gradients
                    optimizer.zero_grad()
                    outputs = model(x)
                    loss = loss_fn(outputs, y)

                    # the backward pass frees the graph memory, so there is no
                    # need for torch.no_grad in this training pass
                    loss.backward()
                    optimizer.step()
                    # scheduler.step()

                else:
                    with torch.no_grad():
                        outputs = model(x)
                        loss = loss_fn(outputs, y.long())

                # stats - whatever is the phase
                acc = acc_fn(outputs, y)

                running_acc += acc * dataloader.batch_size
                running_loss += loss * dataloader.batch_size

                if step % 100 == 0:
                    # clear_output(wait=True)
                    print('Current step: {}  Loss: {}  Acc: {}  AllocMem (Mb): {}'.format(step, loss, acc,
                                                                                          torch.cuda.memory_allocated() / 1024 / 1024))
                    # print(torch.cuda.memory_summary())

            epoch_loss = running_loss / len(dataloader.dataset)
            epoch_acc = running_acc / len(dataloader.dataset)

            # clear_output(wait=True)
            print('Epoch {}/{}'.format(epoch, epochs - 1))
            print('-' * 10)
            print('{} Loss: {:.4f} Acc: {}'.format(phase, epoch_loss, epoch_acc))
            print('-' * 10)

            train_loss.append(epoch_loss) if phase == 'train' else valid_loss.append(epoch_loss)

    time_elapsed = time.time() - start
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

    return train_loss, valid_loss


def batch_to_img(xb, idx):
    img = np.array(xb[idx, 0:3])
    return img.transpose((1, 2, 0))


def predb_to_mask(predb, idx):
    p = torch.functional.F.softmax(predb[idx], 0)
    return p.argmax(0).cpu()


def acc_metric(predb, yb):
    return (predb.argmax(dim=1) == yb.cuda()).float().mean()


def train_model():
    unet = UNET(3, 2)

    loss_fn = nn.CrossEntropyLoss()
    opt = torch.optim.Adam(unet.parameters(), lr=0.01)
    train_loss, valid_loss = train(unet, train_dl, valid_dl, loss_fn, opt, acc_metric, epochs=100)
    torch.save(unet.state_dict(), model_name)


def combine_files(r_file: Path, img_dir, msk_dir):
    files = {'image': r_file,
             'mask': msk_dir / r_file.name.replace('naip_tiles', 'lu_masks')}

    # print('r_file is:', r_file)
    # print('msk_dir:', msk_dir)
    # print('r_file.name is:', r_file.name.replace('naip_tiles', 'lu_masks'))
    # print('The mas file is: -----', msk_dir / r_file.name.replace('naip_tiles', 'lu_masks'))

    return files


def recong_building():
    # data = CanopyDataset(base_path/'imgs',
    #                     base_path/'labels')

    img_dir = base_path / 'imgs'
    msk_dir = base_path / 'labels'
    print(img_dir)
    print(msk_dir)

    # Loop through the files in red folder and combine, into a dictionary, the other bands
    self_files = [combine_files(f, img_dir, msk_dir) for f in img_dir.iterdir() if not f.is_dir()]
    # print(self_files)

    # 查看一下影像和对应的标记数据
    from matplotlib import pyplot as plt

    xb, yb = next(iter(train_dl))
    print(xb.shape, yb.shape)

    bs = batch_size
    fig, ax = plt.subplots(bs, 2, figsize=(12, bs * 5))
    for i in range(bs):
        ax[i, 0].imshow(batch_to_img(xb, i))
        ax[i, 1].imshow(yb[i])
    plt.show()
    # 模型预测以及结果比较

    model = UNET(3, 2)

    model_file_path = os.path.join(root_path, model_name)
    model.load_state_dict(torch.load(model_file_path))

    xb, yb = next(iter(train_dl))

    with torch.no_grad():
        predb = model(xb)

    ## batch size
    bs = batch_size
    fig, ax = plt.subplots(bs, 3, figsize=(15, bs * 5))
    for i in range(bs):
        ax[i, 0].imshow(batch_to_img(xb, i))
        ax[i, 1].imshow(yb[i])
        ax[i, 2].imshow(predb_to_mask(predb, i))
    plt.show()

def detect_building(detect_image_path, result_image_path):
    img_jpg = Image.open(detect_image_path)
    raw_rgb = np.asarray(img_jpg).astype(float)
    raw_rgb = transform.resize(raw_rgb, (512, 512, 3))
    to_tensor = transforms.ToTensor()
    old_tensor = to_tensor(raw_rgb)
    # 将(C, H, W)  变为(1, C, H, W)，因为网络中的输入格式第一个还有一个batch_size的值
    img_tensor = old_tensor.reshape(1, 3, 512, 512)
    # img_tensor = old_tensor.reshape(1, 3, 5079, 5079)
    img_tensor = img_tensor.to(torch.float32)

    model = UNET(3, 2)
    with torch.no_grad():
        predb = model(img_tensor)
    p = torch.functional.F.softmax(predb[0], 0)
    result_tensor = p.argmax(0).cpu()
    # fig, ax = plt.subplots(1, 2, figsize=(12, 1 * 5))
    # ax[0].imshow(img_jpg)
    # ax[1].imshow(result_tensor)

    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1) #先是打印输入的图片
    a.set_title('Input image')
    plt.imshow(img_jpg)

    b = fig.add_subplot(1, 2, 2) #然后打印预测得到的结果图片
    b.set_title('Output mask')
    plt.imshow(result_tensor)
    plt.show()

    result_tensor = result_tensor.to(torch.float32)
    result_img = ToPILImage()(result_tensor)
    result_img.save(result_image_path)


if __name__ == "__main__":
    # 1. 卷积神经网络的构建
    build_model()
    # # 2.图像和标记转换为PyTorch可以识别的格式
    convert_data()
    # # 3. 模型训练
    train_model()
    # 4. 模型预测：基于训练的模型进行建筑物提取
    recong_building()
    # # 5. 提取建筑物
    # detect_image_path = "E:\\系统开发\\AI\\ai_deep_learning\\Unet\\data\\deeplearn-cities\\dataset\\row2-col8.tif"
    # # detect_image_path = "E:\\系统开发\\AI\\ai_deep_learning\\Unet\\data\\deeplearn-cities\\dataset\\naip.tif"
    # result_image_path = "E:\\系统开发\\AI\\ai_deep_learning\\Unet\\data\\deeplearn-cities\\dataset\\naip_building.tif"
    # detect_building(detect_image_path, result_image_path)
