# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\geo_api\predict_api.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 11261 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: predict_api.py
@time: 12/23/19 2:08 PM
@desc:
"""
import os, shutil, tempfile, time, functools, warnings, rasterio, torch, numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from iobjectspy._logger import log_warning
from .dataset import SegInferDataLoader
from ....... import import_tif, DatasourceConnectionInfo, Datasource, raster_to_vector, EngineType, DatasetType
from _jsuperpy.data._util import get_output_datasource
from ..encoders import preprocess_input, get_preprocessing_fn
from ._toolkit import get_preprocessing
from .base import BaseTorchEstimation

class SegTorchEstimation(BaseTorchEstimation):

    def __init__(self, model_path, config, test_aug=False, gpus=[0], **kwargs):
        self.gpus = gpus
        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(map(str, gpus)) if gpus else ""
        if not isinstance(model_path, str):
            raise TypeError("model_path data type inappropriate ，should be str ")
        if not os.path.exists(model_path):
            raise Exception("model_path  path not exists")
        self.model_input = config.model_input[0]
        self.model_output = config.model_output[0]
        if np.argmin(self.model_input.shape) == 0:
            self.band_order = "first"
            self.seg_size = self.model_input.shape[1]
            self.input_bands = self.model_input.shape[0]
            self.out_width_height = [self.model_output.shape[1], self.model_output.shape[2]]
            self.output_msk_num = self.model_output.shape[0]
            if self.model_input.shape[1] != self.model_input.shape[2]:
                raise ValueError("Model input width and height should be equal!")
        else:
            self.band_order = "last"
            self.seg_size = self.model_input.shape[1]
            self.input_bands = self.model_input.shape[-1]
            self.out_width_height = [self.model_output.shape[0], self.model_output.shape[1]]
            self.output_msk_num = self.model_output.shape[-1]
            if self.model_input.shape[1] != self.model_input.shape[0]:
                raise ValueError("Model input width and height should be equal!")
            else:
                self.class_type = config.class_type
                self.color_map = {c.class_value: tuple(c.class_color) for c in self.class_type}
                self.is_stretch = config.is_stretch
                self.model_path = model_path
                self.torch_model_path = os.path.join(self.model_path, os.path.basename(self.model_path) + ".pth")
                if kwargs.get("device") is None:
                    self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
                else:
                    self.device = torch.device(kwargs.get("device"))
                self.test_aug = test_aug
                self.model_config = config
                self.mean = self.model_config.image_mean
                self.std = self.model_config.image_std
                self.image_min = self.model_config.image_min
                self.image_max = self.model_config.image_max
                self.encoder = self.model_config.encoder
                self.encoder_weights = self.model_config.encoder_weights
                if self.input_bands == 3:
                    if self.encoder_weights is None:
                        warnings.warn("encoder_weights 为None，将使用imagenet权重对数据的预处理方式处理数据")
                        preprocessing_fn = get_preprocessing_fn(self.encoder)
                    else:
                        preprocessing_fn = get_preprocessing_fn(self.encoder, self.encoder_weights)
                else:
                    if len(self.image_min) > 1:
                        preprocessing_fn = (functools.partial)(preprocess_input, mean=self.mean, 
                         std=self.std, input_max=self.image_max, input_min=self.image_min)
                    else:
                        preprocessing_fn = (functools.partial)(preprocess_input, mean=self.mean, std=self.std)
            self.preprocessing = functools.partial(get_preprocessing(preprocessing_fn), False)
            self.load_model(self.torch_model_path)

    def estimate_img(self, input_img, coversize, out_path, out_dataset_name, result_type, **kwargs):
        """

        :param input_img:
        :param coversize:
        :param out_path:
        :param out_dataset_name:
        :param result_type: region or grid
        :param kwargs:
        :return:
        """
        self.half_oversize = coversize
        dsm_dataset = kwargs.get("dsm_dataset")
        if not result_type in ('grid', 'region'):
            raise AssertionError("result_type should be grid or region")
        elif self.output_msk_num > 1:
            self.back_or_no_value = -9999
        else:
            self.back_or_no_value = 0
        try:
            batch_size = len(self.gpus) * kwargs.get("batch_size")
        except:
            batch_size = 1 * kwargs.get("batch_size") if kwargs.get("batch_size") is not None else 1

        result_dataset = self._predict_with_rasterio(input_img, dsm_dataset, out_path, out_dataset_name,
          result_type=result_type, batch_size=batch_size)
        return result_dataset

    def _predict_with_rasterio(self, dom_path, dsm_path, out_ds, dst_name, single_thresold=0.5, result_type='grid', batch_size=1):
        tmp_file = os.path.join(tempfile.mkdtemp(), "tmp.tif")
        seg_dataloader = SegInferDataLoader(input_path=dom_path, out_path=tmp_file, block_size=(self.seg_size), batch_size=batch_size,
          cut_edge=(self.half_oversize),
          color_map=(self.color_map),
          preprocessing_fn=(self.preprocessing),
          band_index=[i + 1 for i in range(self.input_bands)])
        for i in tqdm((range(len(seg_dataloader))), desc="Model Infer:"):
            data, batch_blocks = seg_dataloader[i]
            mask_block = self._predict_on_batch(data)
            if self.output_msk_num > 1:
                mask_int = np.argmax(mask_block, axis=1)[(np.newaxis, None[:None], None[:None])]
            else:
                mask_int = mask_block > single_thresold
            mask_int = mask_int.astype(np.uint8)
            if len(mask_int.shape) < 4:
                out_data = mask_int[(None[:None], np.newaxis, None[:None], None[:None])]
            else:
                out_data = mask_int
            seg_dataloader.write_batch(out_data, batch_blocks)

        seg_dataloader.close()
        if result_type.strip() == "grid":
            out_ds = get_output_datasource(out_ds)
            result = import_tif(tmp_file, output=out_ds, out_dataset_name=dst_name, is_import_as_grid=True)
            shutil.copyfile(tmp_file, os.path.join(os.path.dirname(out_ds.connection_info.server), dst_name + ".tif"))
            result = result[0] if (isinstance(result, list) and len(result) > 0) else result
            os.remove(tmp_file)
        else:
            if result_type.strip() == "region":
                tmp_udb_file = os.path.join(tempfile.mkdtemp(), "tmp.udb")
                tmp_dsc = DatasourceConnectionInfo(server=tmp_udb_file, engine_type=(EngineType.UDB))
                tmp_ds = Datasource().create(tmp_dsc)
                import_tif(tmp_file, output=tmp_ds, out_dataset_name="mask_tmp", is_import_as_grid=True)
                os.remove(tmp_file)
                result = raster_to_vector((tmp_ds["mask_tmp"]), "class_type", out_dataset_type=(DatasetType.REGION), back_or_no_value=(self.back_or_no_value),
                  is_thin_raster=True,
                  out_data=out_ds,
                  out_dataset_name=dst_name)
                result = result[0] if (isinstance(result, list) and len(result) > 0) else result
                tmp_ds.delete_all()
                tmp_ds.close()
            else:
                raise Exception("result_type error")
        return result

    def _predict_tile_local(self, image, visiable=False):
        x_tensor = torch.from_numpy(image).to(self.device).unsqueeze(0)
        if self.test_aug:
            with torch.no_grad():
                pr_mask = self.model.forward(x_tensor)
            pr_mask = pr_mask.squeeze().cpu().detach().numpy()
        else:
            pr_mask = self.model.predict(x_tensor)
            pr_mask = pr_mask.squeeze().cpu().numpy()
        if visiable:
            plt.figure(figsize=(16, 16))
            plt.subplot(121)
            plt.imshow(np.transpose(image, (1, 2, 0)) * 255)
            plt.subplot(122)
            plt.imshow(np.argmax(pr_mask, axis=0))
            plt.show()
        return pr_mask

    @torch.no_grad()
    def _predict_on_batch(self, predict_tiles):
        batch_data = predict_tiles
        x_tensor = torch.from_numpy(batch_data).to(self.device)
        if self.test_aug:
            with torch.no_grad():
                pr_mask = self.model.forward(x_tensor)
            pr_mask = pr_mask.cpu().detach().numpy()
        else:
            with torch.no_grad():
                pr_mask = self.model.forward(x_tensor)
            pr_mask = pr_mask.cpu().detach().numpy()
        return pr_mask

    def load_model(self, model_path):
        self.model = torch.load(model_path, map_location=(self.device))
        if torch.cuda.device_count() > 1:
            self.model = torch.nn.DataParallel(self.model)
        if self.test_aug:
            import ttach as tta
            transforms = tta.Compose([
             tta.Scale(scales=[0.28125, 0.5, 1, 2])])
            self.model = tta.SegmentationTTAWrapper((self.model), transforms, merge_mode="mean")
        if self.model.training:
            self.model.eval()

    def close_model(self):
        try:
            del self.model
            torch.cuda.empty_cache()
        except Exception as e:
            try:
                log_warning("Close model error : {}".format(e))
            finally:
                e = None
                del e
