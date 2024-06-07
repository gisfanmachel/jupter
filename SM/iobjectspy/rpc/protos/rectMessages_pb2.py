# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/rpc\protos\rectMessages_pb2.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 3256 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name="rectMessages.proto",
  package="com.supermap.jsuperpy.protos",
  syntax="proto3",
  serialized_options=None,
  serialized_pb=(_b('\n\x12rectMessages.proto\x12\x1ccom.supermap.jsuperpy.protos"C\n\tProtoRect\x12\x0c\n\x04minx\x18\x01 \x01(\x01\x12\x0c\n\x04maxx\x18\x02 \x01(\x01\x12\x0c\n\x04miny\x18\x03 \x01(\x01\x12\x0c\n\x04maxy\x18\x04 \x01(\x01b\x06proto3')))
_PROTORECT = _descriptor.Descriptor(name="ProtoRect",
  full_name="com.supermap.jsuperpy.protos.ProtoRect",
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name="minx",
   full_name="com.supermap.jsuperpy.protos.ProtoRect.minx",
   index=0,
   number=1,
   type=1,
   cpp_type=5,
   label=1,
   has_default_value=False,
   default_value=(float(0)),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name="maxx",
   full_name="com.supermap.jsuperpy.protos.ProtoRect.maxx",
   index=1,
   number=2,
   type=1,
   cpp_type=5,
   label=1,
   has_default_value=False,
   default_value=(float(0)),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name="miny",
   full_name="com.supermap.jsuperpy.protos.ProtoRect.miny",
   index=2,
   number=3,
   type=1,
   cpp_type=5,
   label=1,
   has_default_value=False,
   default_value=(float(0)),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name="maxy",
   full_name="com.supermap.jsuperpy.protos.ProtoRect.maxy",
   index=3,
   number=4,
   type=1,
   cpp_type=5,
   label=1,
   has_default_value=False,
   default_value=(float(0)),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax="proto3",
  extension_ranges=[],
  oneofs=[],
  serialized_start=52,
  serialized_end=119)
DESCRIPTOR.message_types_by_name["ProtoRect"] = _PROTORECT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
ProtoRect = _reflection.GeneratedProtocolMessageType("ProtoRect", (_message.Message,), dict(DESCRIPTOR=_PROTORECT,
  __module__="rectMessages_pb2"))
_sym_db.RegisterMessage(ProtoRect)
