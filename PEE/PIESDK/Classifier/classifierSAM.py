# -*- coding:utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
from pie.utils.common import find_pie_dir, download_checkpoint, array_to_image,\
    blend_images, vector_to_geojson, coords_to_xy, bbox_to_xy, geojson_to_coords, \
    download_file, raster_to_vector, check_package

class PIEClassifierSAM(object):
    def __init__(
            self,
            model_type=None,
            checkpoint=None,
            automatic=True,
            device=None,
            sam_kwargs=None):
        try:
            from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
        except ImportError:
            raise ImportError("系统依赖库 segment_anything 没有安装")
        try:
            import torch
        except ImportError:
            raise ImportError("系统依赖库 pytorch 没有安装")
        if model_type is None or model_type not in ['vit_h', 'vit_l', 'vit_b']:
            raise ValueError("model_type必须提供且必须是'vit_h', 'vit_l', 'vit_b'之一")
        self.model_type = model_type
        default_path = find_pie_dir()

        if checkpoint is None:
            if model_type == 'vit_h':
                basename = 'sam_vit_h_4b8939.pth'
            elif model_type == 'vit_l':
                basename = 'sam_vit_l_0b3195.pth'
            elif model_type == 'vit_b':
                basename = 'sam_vit_b_01ec64.pth'
            else:
                basename = 'sam_vit_b_01ec64.pth'
            checkpoint = os.path.join(default_path, basename)

        if not os.path.exists(checkpoint):
            print(f"Checkpoint {checkpoint} does not exist.")
            basename = os.path.basename(checkpoint)
            download_checkpoint(url=basename, output=checkpoint)

        self.checkpoint = checkpoint

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            if device == "cuda":
                torch.cuda.empty_cache()

        self.device = device
        self.sam_kwargs = sam_kwargs
        self.image_path = None
        self.source = None  #
        self.image = None  ## 这个source和image 什么关系
        self.masks = None
        self.objects = None
        self.annotations = None

        self.prediction = None
        self.scores = None
        self.logits = None

        self.sam = sam_model_registry[self.model_type](checkpoint=self.checkpoint)
        self.sam.to(device=self.device)
        sam_kwargs = self.sam_kwargs if self.sam_kwargs is not None else {}

        self.mask_generator = SamAutomaticMaskGenerator(self.sam, **sam_kwargs)  # 初始化automaticMaskGenerator
        self.predictor = SamPredictor(self.sam)

    def __call__(
            self,
            image,
            foreground=True,
            erosion_kernel=(3, 3),
            mask_multiplier=255,
            **kwargs,
    ):
        check_package("opencv-python", "cv2")
        import cv2
        h, w, _ = image.shape
        masks = self.mask_generator.generate(image)
        if foreground:  # Extract foreground objects only
            resulting_mask = np.zeros((h, w), dtype=np.uint8)
        else:
            resulting_mask = np.ones((h, w), dtype=np.uint8)
        resulting_borders = np.zeros((h, w), dtype=np.uint8)

        for m in masks:
            mask = (m["segmentation"] > 0).astype(np.uint8)  # 把大于0的地方create mask
            resulting_mask += mask

            # Apply erosion to the mask
            if erosion_kernel is not None:
                mask_erode = cv2.erode(mask, erosion_kernel, iterations=1)
                mask_erode = (mask_erode > 0).astype(np.uint8)
                edge_mask = mask - mask_erode
                resulting_borders += edge_mask

        resulting_mask = (resulting_mask > 0).astype(np.uint8)
        resulting_borders = (resulting_borders > 0).astype(np.uint8)
        resulting_mask_with_borders = resulting_mask - resulting_borders
        return resulting_mask_with_borders * mask_multiplier

    def generate(
            self,
            source,
            output=None,
            foreground=True,
            batch=False,
            erosion_kernel=None,
            mask_multiplier=255,
            unique=True,
            **kwargs,
    ):
        check_package("opencv-python", "cv2")
        import cv2
        if isinstance(source, str):
            if not os.path.exists(source):
                raise ValueError(f"输入图像 {source} 不存在.")
            if not source.endswith('tif'):
                raise TypeError(f"输入图像只支持tif格式.")
            image = cv2.imread(source)
        elif isinstance(source, np.ndarray):
            image = source
        else:
            raise ValueError("Input source must be either a path or a numpy array.")

        self.source = image
        self.masks = self.mask_generator.generate(image)
        self.batch = False

        if output is not None:
            self.save_masks(
                output, foreground, unique, erosion_kernel, mask_multiplier, **kwargs
            )

    def save_masks(
            self,
            output=None,
            foreground=True,
            unique=True,
            erosion_kernel=None,
            mask_multiplier=255,
            **kwargs,
    ):
        check_package("opencv-python", "cv2")
        import cv2
        if self.masks is None:
            raise ValueError("No masks found. Please run generate() first.")

        h, w, _ = self.source.shape
        masks = self.masks

        if len(masks) < 255:
            dtype = np.uint8
        elif len(masks) < 65535:
            dtype = np.uint16
        else:
            dtype = np.uint32

        if unique:
            sorted_masks = sorted(masks, key=(lambda x: x["area"]), reverse=False)

            objects = np.zeros(
                (
                    sorted_masks[0]["segmentation"].shape[0],
                    sorted_masks[0]["segmentation"].shape[1],
                )
            )
            # Assign a unique value to each object
            for index, ann in enumerate(sorted_masks):
                m = ann["segmentation"]
                objects[m] = index + 1

        # Generate a binary mask
        else:
            if foreground:  # Extract foreground objects only
                resulting_mask = np.zeros((h, w), dtype=dtype)
            else:
                resulting_mask = np.ones((h, w), dtype=dtype)
            resulting_borders = np.zeros((h, w), dtype=dtype)

            for m in masks:
                mask = (m["segmentation"] > 0).astype(dtype)
                resulting_mask += mask

                # Apply erosion to the mask
                if erosion_kernel is not None:
                    mask_erode = cv2.erode(mask, erosion_kernel, iterations=1)
                    mask_erode = (mask_erode > 0).astype(dtype)
                    edge_mask = mask - mask_erode
                    resulting_borders += edge_mask

            resulting_mask = (resulting_mask > 0).astype(dtype)
            resulting_borders = (resulting_borders > 0).astype(dtype)
            objects = resulting_mask - resulting_borders
            objects = objects * mask_multiplier

        objects = objects.astype(dtype)
        self.objects = objects

        if output is not None:  # Save the output image
            array_to_image(self.objects, output, self.source, **kwargs)

    def show_masks(self, figsize=(12, 10), cmap="binary_r", axis="off", foreground=True, **kwargs):
        check_package("opencv-python", "cv2")
        import cv2
        if self.batch:
            self.objects = cv2.imread(self.masks)
        else:
            if self.objects is None:
                self.save_masks(foreground=foreground, **kwargs)

        plt.figure(figsize=figsize)
        plt.imshow(self.objects, cmap=cmap)
        plt.axis(axis)
        plt.show()

    def show_anns(
            self,
            figsize=(12, 10),
            axis="off",
            alpha=0.35,
            output=None,
            blend=True,
            **kwargs,
    ):
        anns = self.masks
        if self.image is None:
            print("Please run generate() first.")
            return

        if anns is None or len(anns) == 0:
            return
        plt.figure(figsize=figsize)
        plt.imshow(self.source)

        sorted_anns = sorted(anns, key=(lambda x: x["area"]), reverse=True)

        ax = plt.gca()
        ax.set_autoscale_on(False)

        img = np.ones(
            (
                sorted_anns[0]["segmentation"].shape[0],
                sorted_anns[0]["segmentation"].shape[1],
                4,
            )
        )
        img[:, :, 3] = 0
        for ann in sorted_anns:
            m = ann["segmentation"]
            color_mask = np.concatenate([np.random.random(3), [alpha]])
            img[m] = color_mask
        ax.imshow(img)

        if "dpi" not in kwargs:
            kwargs["dpi"] = 100

        if "bbox_inches" not in kwargs:
            kwargs["bbox_inches"] = "tight"
        plt.axis(axis)
        self.annotations = (img[:, :, 0:3] * 255).astype(np.uint8)
        if output is not None:
            if blend:
                array = blend_images(
                    self.annotations, self.image, alpha=alpha, show=False
                )
            else:
                array = self.annotations
            array_to_image(array, output, self.source)

    def set_image(self, image, image_format="RGB"):
        """Set the input image as a numpy array.

        Args:
            image (np.ndarray): The input image as a numpy array.
            image_format (str, optional): The image format, can be RGB or BGR. Defaults to "RGB".
        """
        check_package("opencv-python", "cv2")
        import cv2
        if isinstance(image, str):
            if image.startswith("http"):
                image_path = download_file(image)
            else:
                image_path = image
            if not os.path.exists(image_path):
                raise ValueError(f"Input path {image_path} does not exist.")
            self.image = image_path
            image_bgr = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            self.predictor.set_image(image_rgb, image_format=image_format)
            print("set_image is finish ... ")
        elif isinstance(image, np.ndarray):
            pass
        else:
            raise ValueError("Input image must be either a path or a numpy array.")


    def save_prediction(
            self,
            output,
            index=None,
            mask_multiplier=255,
            dtype=np.float32,
            vector=None,
            simplify_tolerance=None,
            **kwargs,
    ):
        """Save the predicted mask to the output path.

        Args:
            output (str): The path to the output image.
            index (int, optional): The index of the mask to save. Defaults to None,
                which will save the mask with the highest score.
            mask_multiplier (int, optional): The mask multiplier for the output mask, which is usually a binary mask [0, 1].
            vector (str, optional): The path to the output vector file. Defaults to None.
            dtype (np.dtype, optional): The data type of the output image. Defaults to np.float32.
            simplify_tolerance (float, optional): The maximum allowed geometry displacement.
                The higher this value, the smaller the number of vertices in the resulting geometry.

        """
        if self.scores is None:
            raise ValueError("No predictions found. Please run predict() first.")

        if index is None:
            index = self.scores.argmax(axis=0)
        array = self.masks[index] * mask_multiplier
        self.prediction = array
        array_uint8 = array.astype(np.uint8)
        array_to_image(array_uint8, output, self.image, **kwargs)
        if vector is not None:
            raster_to_vector(output, vector, simplify_tolerance=simplify_tolerance)

    def predict(
            self,
            point_coords=None,
            point_labels=None,
            box=None,
            point_crs=None,
            mask_input=None,
            multimask_output=True,
            return_logits=False,
            output=None,
            index=None,
            mask_multiplier=255,
            dtype=np.float32,
            return_results=False,
            **kwargs,
    ):
        if isinstance(point_coords, str):
            point_coords = vector_to_geojson(point_coords)

        if isinstance(point_coords, dict):
            point_coords = geojson_to_coords(point_coords)

        if hasattr(self, "point_coords"):
            point_coords = self.point_coords

        if hasattr(self, "point_labels"):
            point_labels = self.point_labels
        if point_crs is not None:
            point_coords = coords_to_xy(self.image, point_coords, point_crs)
        if isinstance(point_coords, list):
            point_coords = np.array(point_coords)

        if point_labels is None:
            point_labels = [1] * len(point_coords)
        elif isinstance(point_labels, int):
            point_labels = [point_labels] * len(point_coords)

        if isinstance(point_labels, list):
            if len(point_labels) != len(point_coords):
                if len(point_labels) == 1:
                    point_labels = point_labels * len(point_coords)
                else:
                    raise ValueError(
                        "The length of point_labels must be equal to the length of point_coords."
                    )
            point_labels = np.array(point_labels)

        if isinstance(box, list) and point_crs is not None:
            box = np.array(bbox_to_xy(self.image, box, point_crs))
        masks, scores, logits = self.predictor.predict(
            point_coords, point_labels, box, mask_input, multimask_output, return_logits
        )
        self.masks = masks
        self.scores = scores
        self.logits = logits
        if output is not None:
            self.save_prediction(output, index, mask_multiplier, dtype, **kwargs)

        if return_results:
            return masks, scores, logits


if __name__ == '__main__':
    pass
