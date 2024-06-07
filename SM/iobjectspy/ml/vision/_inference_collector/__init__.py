# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference_collector\__init__.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 525 bytes
from .binary_classification_infer import BinaryClassification, BinaryClassificationWithTile, BinaryClassificationWithNumpy
from .image_classification_infer import ImageClassification, ImageClassificationSingle
from .multi_classification_infer import MultiClassification, MultiClassificationWithTile
from .object_detection_infer import ObjectDetection, ObjectDetectionWithTile
from .scene_classification_infer import SceneClassification, SceneClassificationWithTile
from .object_extraction_infer import ObjectExtraction
