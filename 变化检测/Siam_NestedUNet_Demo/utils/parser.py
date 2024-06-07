import argparse as ag
import json


def get_parser_with_args(metadata_json='metadata.json'):
    parser = ag.ArgumentParser(description='Training change detection network')
    with open(metadata_json, 'r') as fin:
        metadata = json.load(fin)
        parser.set_defaults(**metadata)
        parser.add_argument('-b', '--before', type=str, help='before tif path')
        parser.add_argument('-a', '--after', type=str, help='after tif path')
        parser.add_argument('-t', '--tif', type=str, help='tif save path')
        parser.add_argument('-s', '--shp', type=str, help='shp save path')
        # print(parser.parse_args().foo)
        return parser, metadata

    return None
