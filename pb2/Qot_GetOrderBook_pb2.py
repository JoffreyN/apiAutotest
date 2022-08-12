# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Qot_GetOrderBook.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import Common_pb2 as Common__pb2
from . import Qot_Common_pb2 as Qot__Common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Qot_GetOrderBook.proto',
  package='Qot_GetOrderBook',
  syntax='proto3',
  serialized_options=b'\n\021com.cmbi.quote.pb\242\002\020Qot_GetOrderBook',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16Qot_GetOrderBook.proto\x12\x10Qot_GetOrderBook\x1a\x0c\x43ommon.proto\x1a\x10Qot_Common.proto\"-\n\x03\x43\x32S\x12&\n\x08security\x18\x01 \x01(\x0b\x32\x14.Qot_Common.Security\"\xa3\x01\n\x03S2C\x12&\n\x08security\x18\x01 \x01(\x0b\x32\x14.Qot_Common.Security\x12\"\n\x03\x62uy\x18\x02 \x03(\x0b\x32\x15.Qot_Common.OrderBook\x12#\n\x04sell\x18\x03 \x03(\x0b\x32\x15.Qot_Common.OrderBook\x12\x12\n\nupdateTime\x18\x04 \x01(\t\x12\x17\n\x0fupdateTimestamp\x18\x05 \x01(\x03\"-\n\x07Request\x12\"\n\x03\x63\x32s\x18\x01 \x01(\x0b\x32\x15.Qot_GetOrderBook.C2S\"`\n\x08Response\x12\x0f\n\x07retType\x18\x01 \x01(\x05\x12\x0e\n\x06retMsg\x18\x02 \x01(\t\x12\x0f\n\x07\x65rrCode\x18\x03 \x01(\x05\x12\"\n\x03s2c\x18\x04 \x01(\x0b\x32\x15.Qot_GetOrderBook.S2CB&\n\x11\x63om.cmbi.quote.pb\xa2\x02\x10Qot_GetOrderBookb\x06proto3'
  ,
  dependencies=[Common__pb2.DESCRIPTOR,Qot__Common__pb2.DESCRIPTOR,])




_C2S = _descriptor.Descriptor(
  name='C2S',
  full_name='Qot_GetOrderBook.C2S',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='Qot_GetOrderBook.C2S.security', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=76,
  serialized_end=121,
)


_S2C = _descriptor.Descriptor(
  name='S2C',
  full_name='Qot_GetOrderBook.S2C',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='Qot_GetOrderBook.S2C.security', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='buy', full_name='Qot_GetOrderBook.S2C.buy', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sell', full_name='Qot_GetOrderBook.S2C.sell', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='updateTime', full_name='Qot_GetOrderBook.S2C.updateTime', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='updateTimestamp', full_name='Qot_GetOrderBook.S2C.updateTimestamp', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=124,
  serialized_end=287,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Qot_GetOrderBook.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='c2s', full_name='Qot_GetOrderBook.Request.c2s', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=289,
  serialized_end=334,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='Qot_GetOrderBook.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='retType', full_name='Qot_GetOrderBook.Response.retType', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retMsg', full_name='Qot_GetOrderBook.Response.retMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errCode', full_name='Qot_GetOrderBook.Response.errCode', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='s2c', full_name='Qot_GetOrderBook.Response.s2c', index=3,
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
  serialized_start=336,
  serialized_end=432,
)

_C2S.fields_by_name['security'].message_type = Qot__Common__pb2._SECURITY
_S2C.fields_by_name['security'].message_type = Qot__Common__pb2._SECURITY
_S2C.fields_by_name['buy'].message_type = Qot__Common__pb2._ORDERBOOK
_S2C.fields_by_name['sell'].message_type = Qot__Common__pb2._ORDERBOOK
_REQUEST.fields_by_name['c2s'].message_type = _C2S
_RESPONSE.fields_by_name['s2c'].message_type = _S2C
DESCRIPTOR.message_types_by_name['C2S'] = _C2S
DESCRIPTOR.message_types_by_name['S2C'] = _S2C
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

C2S = _reflection.GeneratedProtocolMessageType('C2S', (_message.Message,), {
  'DESCRIPTOR' : _C2S,
  '__module__' : 'Qot_GetOrderBook_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetOrderBook.C2S)
  })
_sym_db.RegisterMessage(C2S)

S2C = _reflection.GeneratedProtocolMessageType('S2C', (_message.Message,), {
  'DESCRIPTOR' : _S2C,
  '__module__' : 'Qot_GetOrderBook_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetOrderBook.S2C)
  })
_sym_db.RegisterMessage(S2C)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'Qot_GetOrderBook_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetOrderBook.Request)
  })
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'Qot_GetOrderBook_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetOrderBook.Response)
  })
_sym_db.RegisterMessage(Response)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
