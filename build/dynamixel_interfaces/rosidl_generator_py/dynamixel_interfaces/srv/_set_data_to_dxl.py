# generated from rosidl_generator_py/resource/_idl.py.em
# with input from dynamixel_interfaces:srv/SetDataToDxl.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_SetDataToDxl_Request(type):
    """Metaclass of message 'SetDataToDxl_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('dynamixel_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'dynamixel_interfaces.srv.SetDataToDxl_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_data_to_dxl__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_data_to_dxl__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_data_to_dxl__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_data_to_dxl__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_data_to_dxl__request

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetDataToDxl_Request(metaclass=Metaclass_SetDataToDxl_Request):
    """Message class 'SetDataToDxl_Request'."""

    __slots__ = [
        '_header',
        '_id',
        '_item_name',
        '_item_data',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'id': 'uint8',
        'item_name': 'string',
        'item_data': 'uint32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.id = kwargs.get('id', int())
        self.item_name = kwargs.get('item_name', str())
        self.item_data = kwargs.get('item_data', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.id != other.id:
            return False
        if self.item_name != other.item_name:
            return False
        if self.item_data != other.item_data:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property  # noqa: A003
    def id(self):  # noqa: A003
        """Message field 'id'."""
        return self._id

    @id.setter  # noqa: A003
    def id(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'id' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'id' field must be an unsigned integer in [0, 255]"
        self._id = value

    @builtins.property
    def item_name(self):
        """Message field 'item_name'."""
        return self._item_name

    @item_name.setter
    def item_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'item_name' field must be of type 'str'"
        self._item_name = value

    @builtins.property
    def item_data(self):
        """Message field 'item_data'."""
        return self._item_data

    @item_data.setter
    def item_data(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'item_data' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'item_data' field must be an unsigned integer in [0, 4294967295]"
        self._item_data = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_SetDataToDxl_Response(type):
    """Metaclass of message 'SetDataToDxl_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('dynamixel_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'dynamixel_interfaces.srv.SetDataToDxl_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_data_to_dxl__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_data_to_dxl__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_data_to_dxl__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_data_to_dxl__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_data_to_dxl__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetDataToDxl_Response(metaclass=Metaclass_SetDataToDxl_Response):
    """Message class 'SetDataToDxl_Response'."""

    __slots__ = [
        '_result',
    ]

    _fields_and_field_types = {
        'result': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.result = kwargs.get('result', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'result' field must be of type 'bool'"
        self._result = value


class Metaclass_SetDataToDxl(type):
    """Metaclass of service 'SetDataToDxl'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('dynamixel_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'dynamixel_interfaces.srv.SetDataToDxl')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__set_data_to_dxl

            from dynamixel_interfaces.srv import _set_data_to_dxl
            if _set_data_to_dxl.Metaclass_SetDataToDxl_Request._TYPE_SUPPORT is None:
                _set_data_to_dxl.Metaclass_SetDataToDxl_Request.__import_type_support__()
            if _set_data_to_dxl.Metaclass_SetDataToDxl_Response._TYPE_SUPPORT is None:
                _set_data_to_dxl.Metaclass_SetDataToDxl_Response.__import_type_support__()


class SetDataToDxl(metaclass=Metaclass_SetDataToDxl):
    from dynamixel_interfaces.srv._set_data_to_dxl import SetDataToDxl_Request as Request
    from dynamixel_interfaces.srv._set_data_to_dxl import SetDataToDxl_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
