# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/rpc\worker.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 6839 bytes
import socket, argparse
from ._utils import encode_tile, decode_tile, decode_process_info, read_length_and_bytes, write_length_and_bytes, read_int, write_int
from .process import Tile
import numpy
from .serializes import MapSerializer, DataSerializers
FINISHED_AND_EXIT = -1
PROCESS_NO_VALUE_RETURN = 0
PROCESSING = 2
END_PROCESSING = 3
FETCH_FINAL_RESULT = 4
PROCESS_UPDATE_INFO = 5
PRE_PROCESSING = 6
PROCESS_SET_PARAMETERS = 7
EXECUTE_PROCESS_GT = 10
EXECUTE_PROCESS_PIPE = 20
EXECUTE_PROCESS_TILES = 30
PROCESSING_TILE = 31
PROCESSING_TILES = 32
map_ser = MapSerializer()

def _create_entry_object(infile, outfile):
    process_info_bytes = read_length_and_bytes(infile)
    process_info = decode_process_info(process_info_bytes)
    code = process_info.py_code
    entry_class_name = process_info.entry_class
    exec(compile(code, "", "exec"))
    local_p = locals()
    for key in local_p:
        globals()[key] = local_p[key]

    return (
     locals()[entry_class_name](), process_info.kvargs)


def execute_process_gt(infile, outfile):
    entry_obj, kv_args = _create_entry_object(infile, outfile)
    execute_result = entry_obj.execute(kv_args)
    if execute_result is None:
        result_bytes = None
    else:
        result_bytes = map_ser.encode(execute_result)
    write_length_and_bytes(result_bytes, outfile)
    write_int(END_PROCESSING, outfile)
    command = read_int(infile)
    exit(command)


def execute_process_tiles(infile, outfile):
    entry_obj, kv_args = _create_entry_object(infile, outfile)
    _set_parameters(entry_obj, kv_args)
    if read_int(infile) == PROCESS_UPDATE_INFO:
        _process_update_info(entry_obj, infile, outfile)
    commands = {PROCESS_SET_PARAMETERS: _process_set_parameters, 
     PROCESS_UPDATE_INFO: _process_update_info, 
     PROCESSING_TILE: _process_tile, 
     PROCESSING_TILES: _process_tiles}
    while True:
        write_int(PRE_PROCESSING, outfile)
        command = read_int(infile)
        if command == END_PROCESSING:
            break
        else:
            commands[command](entry_obj, infile, outfile)

    command = read_int(infile)
    if command == FETCH_FINAL_RESULT:
        _get_final_results(entry_obj, infile, outfile)
        command = read_int(infile)
    exit(command)


def _get_final_results(entry_obj, infile, outfile):
    if hasattr(entry_obj, "final_results"):
        execute_result = entry_obj.final_results()
        if execute_result is not None:
            bys = DataSerializers.serialize(execute_result)
            write_length_and_bytes(bys, outfile)
        else:
            write_int(PROCESS_NO_VALUE_RETURN, outfile)
    else:
        write_int(PROCESS_NO_VALUE_RETURN, outfile)


def _set_parameters(entry_obj, params):
    if hasattr(entry_obj, "set_parameters"):
        entry_obj.set_parameters(params)


def _process_set_parameters(entry_obj, infile, outfile):
    params = map_ser.decode(read_length_and_bytes(infile))
    _set_parameters(entry_obj, params)


def _process_tile(entry_obj, infile, outfile):
    pb_bytes = read_length_and_bytes(infile)
    source_tile = decode_tile(pb_bytes)
    execute_result = entry_obj.execute(source_tile.values)
    if execute_result is not None:
        if isinstance(execute_result, numpy.ndarray):
            result_tile = Tile(execute_result, source_tile.no_data_value, source_tile.bands, source_tile.pixel)
            write_length_and_bytes(encode_tile(result_tile), outfile)
        else:
            write_length_and_bytes(DataSerializers.serialize(execute_result), outfile)
    else:
        write_int(PROCESS_NO_VALUE_RETURN, outfile)


def _process_tiles(entry_obj, infile, outfile):
    tile_count = read_int(infile)
    tiles = []
    for i in range(tile_count):
        tiles.append(decode_tile(read_length_and_bytes(infile)))

    arrays = [tile.values for tile in tiles]
    execute_result = entry_obj.execute(arrays)
    if execute_result is not None:
        if isinstance(execute_result, numpy.ndarray):
            source_tile = tiles[0]
            result_tile = Tile(execute_result, source_tile.no_data_value, source_tile.bands, source_tile.pixel)
            write_length_and_bytes(encode_tile(result_tile), outfile)
        else:
            write_length_and_bytes(DataSerializers.serialize(execute_result), outfile)
    else:
        write_int(PROCESS_NO_VALUE_RETURN, outfile)


def _process_obj(entry_obj, infile, outfile):
    input_args = DataSerializers.deserialize(read_length_and_bytes(infile))
    execute_result = entry_obj.execute(input_args)
    if execute_result is not None:
        write_length_and_bytes(DataSerializers.serialize(execute_result), outfile)
    else:
        write_int(PROCESS_NO_VALUE_RETURN, outfile)


def _process_update_info(entry_obj, infile, outfile):
    if hasattr(entry_obj, "get_update_info"):
        raster_info = entry_obj.get_update_info()
        if raster_info is not None:
            result_bytes = map_ser.encode(raster_info)
            if len(result_bytes) > 0:
                write_length_and_bytes(result_bytes, outfile)
            else:
                write_int(PROCESS_NO_VALUE_RETURN, outfile)
        else:
            write_int(PROCESS_NO_VALUE_RETURN, outfile)
    else:
        write_int(PROCESS_NO_VALUE_RETURN, outfile)


def execute_process_pipe(infile, outfile):
    entry_obj, args = _create_entry_object(infile, outfile)
    commands = {PROCESS_SET_PARAMETERS: _process_set_parameters, 
     PROCESS_UPDATE_INFO: _process_update_info, 
     PROCESSING_TILE: _process_tile, 
     PROCESSING_TILES: _process_tiles, 
     PROCESSING: _process_obj}
    while True:
        write_int(PRE_PROCESSING, outfile)
        command = read_int(infile)
        if command == FINISHED_AND_EXIT:
            exit(command)
        commands[command](entry_obj, infile, outfile)


def _main(infile, outfile):
    command = read_int(infile)
    if command == EXECUTE_PROCESS_GT:
        return execute_process_gt(infile, outfile)
    if command == EXECUTE_PROCESS_TILES:
        return execute_process_tiles(infile, outfile)
    if command == EXECUTE_PROCESS_PIPE:
        return execute_process_pipe(infile, outfile)
    print("error input command " + str(command))
    exit(-1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="java server port")
    args = vars(parser.parse_args())
    java_port = args["port"]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", java_port))
    sock_file = sock.makefile("rwb", 65536)
    _main(sock_file, sock_file)
    sock.close()
    exit(-1)
