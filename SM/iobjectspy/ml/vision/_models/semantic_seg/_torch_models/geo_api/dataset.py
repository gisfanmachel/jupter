# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\geo_api\dataset.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 10587 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: dataset.py
@time: 12/23/19 2:07 PM
@desc:
"""
import copy, math, multiprocessing, os, random
from concurrent.futures import ThreadPoolExecutor, wait
import rasterio, numpy as np, cv2
from PIL import Image
from rasterio.windows import Window
from torch.utils.data import Dataset as BaseDataset
from ._toolkit import list_xy_file_fromtxt, to_onehot, get_config_from_yaml, vis_image_mask

class SdaDataset(BaseDataset):
    __doc__ = "CamVid Dataset. Read images, apply augmentation and preprocessing transformations.\n\n    Args:\n        images_dir (str): path to images folder\n        masks_dir (str): path to segmentation masks folder\n        class_values (list): values of classes to extract from segmentation mask\n        augmentation (albumentations.Compose): data transfromation pipeline\n            (e.g. flip, scale, etc.)\n        preprocessing (albumentations.Compose): data preprocessing\n            (e.g. noralization, shape manipulation, etc.)\n\n    "

    def __init__(self, sda_path, data_split='train', augmentation=None, preprocessing=None, aug_postprocessing=None, mix_up=False):
        self.base_dir = os.path.dirname(sda_path)
        self.data_config = get_config_from_yaml(sda_path)
        self.data_split = data_split
        if data_split == "train":
            self.images_fps, self.masks_fps = list_xy_file_fromtxt(os.path.join(self.base_dir, "csv_path", "train.csv"))
        else:
            if data_split == "val":
                self.images_fps, self.masks_fps = list_xy_file_fromtxt(os.path.join(self.base_dir, "csv_path", "val.csv"))
            else:
                if data_split == "train_val":
                    self.images_fps, self.masks_fps = list_xy_file_fromtxt(os.path.join(self.base_dir, "csv_path", "trainval.csv"))
                else:
                    raise Exception("data_split param error")
        self.class_type = self.data_config.dataset.class_type
        self.x_bandnum = self.data_config.dataset.x_bandnum
        self.augmentation = augmentation
        self.preprocessing = preprocessing
        self.aug_postprocessing = aug_postprocessing
        self.mix_up = mix_up

    def __getitem__(self, i):
        if self.images_fps[i].endswith("tif"):
            image = rasterio.open(self.images_fps[i]).read()[(None[:self.x_bandnum], ...)]
            image = np.transpose(image, (1, 2, 0))
        else:
            image = cv2.imread(self.images_fps[i])
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = np.array(Image.open(self.masks_fps[i])) if self.masks_fps[i].strip().endswith("png") else cv2.imread(self.masks_fps[i], 0)
        if len(self.class_type) > 2:
            mask = to_onehot(mask, [num for num in range(len(self.class_type))])
        else:
            mask = np.expand_dims(mask, -1)
        if self.augmentation:
            sample = self.augmentation(image=image, mask=mask)
            image, mask = sample["image"], sample["mask"]
        if self.preprocessing:
            sample = self.preprocessing(image=image, mask=mask)
            image, mask = sample["image"], sample["mask"]
        else:
            return (
             image, mask)

    def random_mixup(self, source_image, source_mask, p=0.5):
        if random.random() > 0.8:
            i = random.randint(0, len(self.images_fps) - 1)
            image = rasterio.open(self.images_fps[i]).read()[(None[:self.x_bandnum], ...)]
            image = np.transpose(image, (1, 2, 0))
            mask = np.array(Image.open(self.masks_fps[i])) if self.masks_fps[i].strip().endswith("png") else cv2.imread(self.masks_fps[i], 0)
            if len(self.class_type) > 2:
                mask = to_onehot(mask, [num for num in range(len(self.class_type))])
            else:
                mask = np.expand_dims(mask, -1)
            if self.augmentation:
                sample = self.augmentation(image=image, mask=mask)
                image, mask = sample["image"], sample["mask"]
            if self.preprocessing:
                sample = self.preprocessing(image=image, mask=mask)
                image, mask = sample["image"], sample["mask"]
            source_image = source_image * 0.8 + image * 0.2
            source_mask = source_mask.astype(np.float32) * 0.8 + mask.astype(np.float32) * 0.2
        return (
         source_image, source_mask)

    def __len__(self):
        return len(self.images_fps)


class BaseInferDataLoader:

    def __init__(self):
        pass

    def __getitem__(self, item):
        raise NotImplementedError

    def write_batch(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class SegInferDataLoader(BaseInferDataLoader):

    def __init__(self, input_path, out_path, block_size, batch_size=1, cut_edge=128, color_map=None, preprocessing_fn=None, band_index=[1, 2, 3]):
        self.block_size = block_size
        self.cut_edge = cut_edge
        self.step_size = block_size - cut_edge * 2
        self.batch_size = batch_size
        self.color_map = color_map
        self.src = rasterio.open(input_path)
        self.width, self.height = self.src.width, self.src.height
        self.dst = rasterio.open(out_path, "w", driver="GTiff", width=(self.src.width), height=(self.src.height), count=1,
          bounds=(self.src.bounds),
          crs=(self.src.crs),
          transform=(self.src.transform),
          dtype=(np.uint8))
        self.dst.write_colormap(1, self.color_map)
        self.blocks = self._compute_blocks()
        self.preprocessing_fn = preprocessing_fn
        self.band_index = band_index if max(band_index) <= self.src.count else [i + 1 for i in range(self.src.count)]

    def _read(self, x, y):
        return self.src.read((self.band_index), window=(Window(x, y, self.block_size, self.block_size)),
          boundless=True)

    def _write(self, data, x, y):
        h, w = data.shape[1[:3]]
        write_x = x + self.cut_edge
        write_y = y + self.cut_edge
        write_h = min(h - 2 * self.cut_edge, self.height - write_y)
        write_w = min(w - 2 * self.cut_edge, self.width - write_x)
        if write_h < 0 or write_w < 0:
            return
        data = data[(None[:None], self.cut_edge[:self.cut_edge + write_h], self.cut_edge[:self.cut_edge + write_w])]
        self.dst.write(data,
          window=(Window(write_x, write_y, write_w, write_h)))

    def read_batch(self, blocks):
        data = []
        new_blocks = copy.deepcopy(blocks)
        blocks = [[x for x, _ in blocks], [y for _, y in blocks]]
        with ThreadPoolExecutor(max_workers=(min(self.batch_size, multiprocessing.cpu_count(), 16))) as pool:
            for r in pool.map(self._read, blocks[0], blocks[1]):
                data.append(r)

        with ThreadPoolExecutor(max_workers=(min(self.batch_size, multiprocessing.cpu_count()))) as pool:
            if self.preprocessing_fn is not None:
                task_list = [pool.submit((self.preprocessing_fn), image=image) for image in data]
                wait(task_list)
                data = [t.result()["image"] for t in task_list]
        arrays = np.stack(data, axis=0)
        return (
         arrays, new_blocks)

    def __getitem__(self, item):
        batch_blocks = self.blocks[(item * self.batch_size)[:min((item + 1) * self.batch_size, len(self.blocks))]]
        return self.read_batch(batch_blocks)

    def __iter__(self):
        pass

    def write_batch(self, data, blocks):
        for (x, y), sample in zip(blocks, data):
            if not np.all(sample == 0):
                self._write(sample, x, y)

    def _compute_blocks(self):
        return [(x, y) for x in range(-self.cut_edge, self.width, self.step_size) for y in iter((range(-self.cut_edge, self.height, self.step_size)))]

    def __len__(self):
        return math.ceil(len(self.blocks) / self.batch_size)

    def close(self):
        self.src.close()
        self.dst.close()
