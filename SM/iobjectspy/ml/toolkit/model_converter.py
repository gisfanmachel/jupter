# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\toolkit\model_converter.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 5350 bytes
import os, shutil, traceback, warnings, tensorflow as tf
from tensorflow.python.tools import freeze_graph
from tensorflow.python.training import saver as saver_lib
from ._toolkit import get_config_from_yaml

def freeze_model(input_model_path, output_frozen_model_path, output_model_name, is_sdm=True, output_node_names=None, saved_model_tags=None):
    """
    模型转换接口，可将训练工具生成的模型或标准 tensorflow Saved Model模型转换成 Frozen Model。

    可用于基于移动端模型推理

    输入可为训练工具训练得到的带有 sdm 文件的模型，也可为 Saved Model文件夹。

    :param input_model_path: 输入的训练生成的模型，以 .sdm 结尾的路径或 Saved Model 文件夹路径
    :type input_model_path: str
    :param output_frozen_model_path: 输出的模型路径
    :type output_frozen_model_path: str
    :param output_model_name: 输出的模型名
    :type output_model_name: str
    :param is_sdm: 是否为带有 sdm 的模型。输入模型为 Saved Model 需填 False，默认为 True (optional)
    :type is_sdm: bool
    :param output_node_names: 输入模型的输出节点名，默认为 None。若 is_sdm 为 True，该参数无效；若 is_sdm为 True，该参数必填 (optional)
    :type output_node_names: str
    :param saved_model_tags: 输入模型的标签，默认为 None (optional)
    :type output_node_names: str
    :return: 生成的 Frozen Model路径, 失败则为None
    :rtype: str or None
    """
    if not os.path.exists(input_model_path):
        raise IOError("Input Model %s does not exist!" % os.path.abspath(input_model_path))
    else:
        _, ext = os.path.splitext(input_model_path)
        if is_sdm:
            if ext != ".sdm":
                raise ValueError("Please set parm 'input_model_path' with a *.sdm file!")
            real_saved_model_path = os.path.abspath(os.path.join(input_model_path, os.path.pardir))
            if output_node_names is not None:
                warnings.warn("The 'is_sdm' is True, your 'output_node_names' won't be used!")
            config = get_config_from_yaml(input_model_path)
            output_node_names = config.output_node_names
            if saved_model_tags is None:
                saved_model_tags = "serve"
        elif ext == ".sdm":
            raise ValueError("Input Model is SuperMap Deeplearning Model(*.sdm), please set parm 'is_sdm' to True!")
        elif output_model_name is None:
            raise ValueError("Input model isn't SuperMap Deeplearning Model, please set parm 'output_node_names'!")
        if saved_model_tags is None:
            raise ValueError("Input model isn't SuperMap Deeplearning Model, please set parm 'saved_model_tags'!")
        if os.path.isdir(input_model_path):
            real_saved_model_path = input_model_path
        else:
            raise ValueError("Parm 'input_model_path' should be a folder!")
        os.path.exists(output_frozen_model_path) or os.makedirs(output_frozen_model_path)
        print("output_frozen_model_path not exist, create a folder %s" % os.path.abspath(output_frozen_model_path))
    export_path = os.path.join(output_frozen_model_path, output_model_name)
    while os.path.exists(export_path):
        export_path += "_1"

    print("The model will be saved in %s" % os.path.abspath(export_path))
    saved_ckpt = os.path.join(export_path, "saved_ckpt")
    output_frozen_pb_path = os.path.join(export_path, "frozen_model.pb")
    try:
        try:
            with tf.Session() as sess:
                tf.saved_model.loader.load(sess, [saved_model_tags], real_saved_model_path)
                saver = saver_lib.Saver(allow_empty=True)
                checkpoint_path = saver.save(sess, saved_ckpt, global_step=0, latest_filename="checkpoint_state")
                freeze_graph.freeze_graph(None, "", False, checkpoint_path, output_node_names, "save/restore_all", "save/Const:0",
                  output_frozen_pb_path, False, "", input_saved_model_dir=real_saved_model_path)
            if os.path.exists(output_frozen_pb_path):
                if is_sdm:
                    return_path = shutil.copy(input_model_path, os.path.join(export_path, os.path.split(export_path)[-1] + ".sdm"))
                else:
                    return_path = export_path
                print("Convert to frozen model fininshed!")
                return return_path
            shutil.rmtree(export_path)
            print("Convert to frozen model failed!")
            return
        except Exception as e:
            try:
                traceback.print_exc()
                print(e)
            finally:
                e = None
                del e

    finally:
        if os.path.exists(export_path):
            tmp_file_list = [
             'tmp.pb', 'checkpoint_state', 'saved_ckpt-0.meta', 
             'saved_ckpt-0.index', 
             'saved_ckpt-0.data-00000-of-00001']
            for i in tmp_file_list:
                try:
                    os.remove(os.path.join(export_path, i))
                except:
                    pass

        sess.close()
