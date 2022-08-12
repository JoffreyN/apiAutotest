# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Qot_UpdateBasicQot.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import Common_pb2 as Common__pb2
from . import Qot_Common_pb2 as Qot__Common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Qot_UpdateBasicQot.proto',
  package='Qot_UpdateBasicQot',
  syntax='proto3',
  serialized_options=b'\n\021com.cmbi.quote.pb\242\002\022Qot_UpdateBasicQot',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18Qot_UpdateBasicQot.proto\x12\x12Qot_UpdateBasicQot\x1a\x0c\x43ommon.proto\x1a\x10Qot_Common.proto\"1\n\x03S2C\x12*\n\x0c\x62\x61sicQotList\x18\x01 \x03(\x0b\x32\x14.Qot_Common.BasicQot\"b\n\x08Response\x12\x0f\n\x07retType\x18\x01 \x01(\x05\x12\x0e\n\x06retMsg\x18\x02 \x01(\t\x12\x0f\n\x07\x65rrCode\x18\x03 \x01(\x05\x12$\n\x03s2c\x18\x04 \x01(\x0b\x32\x17.Qot_UpdateBasicQot.S2CB(\n\x11\x63om.cmbi.quote.pb\xa2\x02\x12Qot_UpdateBasicQotb\x06proto3'
  ,
  dependencies=[Common__pb2.DESCRIPTOR,Qot__Common__pb2.DESCRIPTOR,])




_S2C = _descriptor.Descriptor(
  name='S2C',
  full_name='Qot_UpdateBasicQot.S2C',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='basicQotList', full_name='Qot_UpdateBasicQot.S2C.basicQotList', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=129,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='Qot_UpdateBasicQot.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='retType', full_name='Qot_UpdateBasicQot.Response.retType', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retMsg', full_name='Qot_UpdateBasicQot.Response.retMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errCode', full_name='Qot_UpdateBasicQot.Response.errCode', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='s2c', full_name='Qot_UpdateBasicQot.Response.s2c', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=229,
)

_S2C.fields_by_name['basicQotList'].message_type = Qot__Common__pb2._BASICQOT
_RESPONSE.fields_by_name['s2c'].message_type = _S2C
DESCRIPTOR.message_types_by_name['S2C'] = _S2C
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

S2C = _reflection.GeneratedProtocolMessageType('S2C', (_message.Message,), {
  'DESCRIPTOR' : _S2C,
  '__module__' : 'Qot_UpdateBasicQot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_UpdateBasicQot.S2C)
  })
_sym_db.RegisterMessage(S2C)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'Qot_UpdateBasicQot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_UpdateBasicQot.Response)
  })
_sym_db.RegisterMessage(Response)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)