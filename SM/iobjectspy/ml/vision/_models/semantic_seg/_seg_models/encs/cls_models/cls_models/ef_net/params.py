# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\encs\cls_models\cls_models\ef_net\params.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 7998 bytes
import os, re, collections
IMAGENET_WEIGHTS = {'efficientnet-b0':{'name':"efficientnet-b0_imagenet_1000.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b0_imagenet_1000.h5", 
  'md5':"bca04d16b1b8a7c607b1152fe9261af7"}, 
 'efficientnet-b0-notop':{'name':"efficientnet-b0_imagenet_1000_notop.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b0_imagenet_1000_notop.h5", 
  'md5':"45d2f3b6330c2401ef66da3961cad769"}, 
 'efficientnet-b1':{'name':"efficientnet-b1_imagenet_1000.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b1_imagenet_1000.h5", 
  'md5':"bd4a2b82f6f6bada74fc754553c464fc"}, 
 'efficientnet-b1-notop':{'name':"efficientnet-b1_imagenet_1000_notop.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b1_imagenet_1000_notop.h5", 
  'md5':"884aed586c2d8ca8dd15a605ec42f564"}, 
 'efficientnet-b2':{'name':"efficientnet-b2_imagenet_1000.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b2_imagenet_1000.h5", 
  'md5':"45b28b26f15958bac270ab527a376999"}, 
 'efficientnet-b2-notop':{'name':"efficientnet-b2_imagenet_1000_notop.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b2_imagenet_1000_notop.h5", 
  'md5':"42fb9f2d9243d461d62b4555d3a53b7b"}, 
 'efficientnet-b3':{'name':"efficientnet-b3_imagenet_1000.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b3_imagenet_1000.h5", 
  'md5':"decd2c8a23971734f9d3f6b4053bf424"}, 
 'efficientnet-b3-notop':{'name':"efficientnet-b3_imagenet_1000_notop.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b3_imagenet_1000_notop.h5", 
  'md5':"1f7d9a8c2469d2e3d3b97680d45df1e1"}, 
 'efficientnet-b4':{'name':"efficientnet-b4_imagenet_1000.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b4_imagenet_1000.h5", 
  'md5':"01df77157a86609530aeb4f1f9527949"}, 
 'efficientnet-b4-notop':{'name':"efficientnet-b4_imagenet_1000_notop.h5", 
  'url':"https://github.com/qubvel/efficientnet/releases/download/v0.0.1/efficientnet-b4_imagenet_1000_notop.h5", 
  'md5':"e7c3b780f050f8f49c800f23703f285c"}}
GlobalParams = collections.namedtuple("GlobalParams", [
 'batch_norm_momentum', 'batch_norm_epsilon', 'dropout_rate', 'data_format', 
 'num_classes', 
 'width_coefficient', 'depth_coefficient', 
 'depth_divisor', 'min_depth', 
 'drop_connect_rate'])
GlobalParams.__new__.__defaults__ = (None, ) * len(GlobalParams._fields)
BlockArgs = collections.namedtuple("BlockArgs", [
 'kernel_size', 'num_repeat', 'input_filters', 'output_filters', 
 'expand_ratio', 
 'id_skip', 'strides', 'se_ratio'])
BlockArgs.__new__.__defaults__ = (None, ) * len(BlockArgs._fields)

def efficientnet_params(model_name):
    """Get efficientnet params based on model name."""
    params_dict = {
     'efficientnet-b0': (1.0, 1.0, 224, 0.2), 
     'efficientnet-b1': (1.0, 1.1, 240, 0.2), 
     'efficientnet-b2': (1.1, 1.2, 260, 0.3), 
     'efficientnet-b3': (1.2, 1.4, 300, 0.3), 
     'efficientnet-b4': (1.4, 1.8, 380, 0.4), 
     'efficientnet-b5': (1.6, 2.2, 456, 0.4), 
     'efficientnet-b6': (1.8, 2.6, 528, 0.5), 
     'efficientnet-b7': (2.0, 3.1, 600, 0.5)}
    return params_dict[model_name]


class BlockDecoder(object):
    __doc__ = "Block Decoder for readability."

    def _decode_block_string(self, block_string):
        """Gets a block through a string notation of arguments."""
        assert isinstance(block_string, str)
        ops = block_string.split("_")
        options = {}
        for op in ops:
            splits = re.split("(\\d.*)", op)
            if len(splits) >= 2:
                key, value = splits[None[:2]]
                options[key] = value

        if "s" not in options or len(options["s"]) != 2:
            raise ValueError("Strides options should be a pair of integers.")
        return BlockArgs(kernel_size=(int(options["k"])),
          num_repeat=(int(options["r"])),
          input_filters=(int(options["i"])),
          output_filters=(int(options["o"])),
          expand_ratio=(int(options["e"])),
          id_skip=("noskip" not in block_string),
          se_ratio=(float(options["se"]) if "se" in options else None),
          strides=[
         int(options["s"][0]), int(options["s"][1])])

    def _encode_block_string(self, block):
        """Encodes a block to a string."""
        args = [
         "r%d" % block.num_repeat,
         "k%d" % block.kernel_size,
         "s%d%d" % (block.strides[0], block.strides[1]),
         "e%s" % block.expand_ratio,
         "i%d" % block.input_filters,
         "o%d" % block.output_filters]
        if block.se_ratio > 0:
            if block.se_ratio <= 1:
                args.append("se%s" % block.se_ratio)
        if block.id_skip is False:
            args.append("noskip")
        return "_".join(args)

    def decode(self, string_list):
        """Decodes a list of string notations to specify blocks inside the network.

    Args:
      string_list: a list of strings, each string is a notation of block.

    Returns:
      A list of namedtuples to represent blocks arguments.
    """
        assert isinstance(string_list, list)
        blocks_args = []
        for block_string in string_list:
            blocks_args.append(self._decode_block_string(block_string))

        return blocks_args

    def encode(self, blocks_args):
        """Encodes a list of Blocks to a list of strings.

    Args:
      blocks_args: A list of namedtuples to represent blocks arguments.
    Returns:
      a list of strings, each string is a notation of block.
    """
        block_strings = []
        for block in blocks_args:
            block_strings.append(self._encode_block_string(block))

        return block_strings


def efficientnet(width_coefficient=None, depth_coefficient=None, dropout_rate=0.2, drop_connect_rate=0.2):
    """Creates a efficientnet model."""
    blocks_args = [
     'r1_k3_s11_e1_i32_o16_se0.25', 'r2_k3_s22_e6_i16_o24_se0.25', 
     'r2_k5_s22_e6_i24_o40_se0.25', 
     'r3_k3_s22_e6_i40_o80_se0.25', 
     'r3_k5_s11_e6_i80_o112_se0.25', 
     'r4_k5_s22_e6_i112_o192_se0.25', 
     'r1_k3_s11_e6_i192_o320_se0.25']
    global_params = GlobalParams(batch_norm_momentum=0.99,
      batch_norm_epsilon=0.001,
      dropout_rate=dropout_rate,
      drop_connect_rate=drop_connect_rate,
      data_format="channels_last",
      num_classes=1000,
      width_coefficient=width_coefficient,
      depth_coefficient=depth_coefficient,
      depth_divisor=8,
      min_depth=None)
    decoder = BlockDecoder()
    return (decoder.decode(blocks_args), global_params)


def get_model_params(model_name, override_params=None):
    """Get the block args and global params for a given model."""
    if model_name.startswith("efficientnet"):
        width_coefficient, depth_coefficient, input_shape, dropout_rate = efficientnet_params(model_name)
        blocks_args, global_params = efficientnet(width_coefficient, depth_coefficient, dropout_rate)
    else:
        raise NotImplementedError("model name is not pre-defined: %s" % model_name)
    if override_params:
        global_params = (global_params._replace)(**override_params)
    return (
     blocks_args, global_params, input_shape)
