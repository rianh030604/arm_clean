// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dynamixel_interfaces:srv/GetDataFromDxl.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dynamixel_interfaces/srv/detail/get_data_from_dxl__rosidl_typesupport_introspection_c.h"
#include "dynamixel_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dynamixel_interfaces/srv/detail/get_data_from_dxl__functions.h"
#include "dynamixel_interfaces/srv/detail/get_data_from_dxl__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `item_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dynamixel_interfaces__srv__GetDataFromDxl_Request__init(message_memory);
}

void dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_fini_function(void * message_memory)
{
  dynamixel_interfaces__srv__GetDataFromDxl_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_member_array[4] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamixel_interfaces__srv__GetDataFromDxl_Request, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamixel_interfaces__srv__GetDataFromDxl_Request, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "item_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamixel_interfaces__srv__GetDataFromDxl_Request, item_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "timeout_sec",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamixel_interfaces__srv__GetDataFromDxl_Request, timeout_sec),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_members = {
  "dynamixel_interfaces__srv",  // message namespace
  "GetDataFromDxl_Request",  // message name
  4,  // number of fields
  sizeof(dynamixel_interfaces__srv__GetDataFromDxl_Request),
  dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_member_array,  // message members
  dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_type_support_handle = {
  0,
  &dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dynamixel_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamixel_interfaces, srv, GetDataFromDxl_Request)() {
  dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_type_support_handle.typesupport_identifier) {
    dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dynamixel_interfaces__srv__GetDataFromDxl_Request__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "dynamixel_interfaces/srv/detail/get_data_from_dxl__rosidl_typesupport_introspection_c.h"
// already included above
// #include "dynamixel_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "dynamixel_interfaces/srv/detail/get_data_from_dxl__functions.h"
// already included above
// #include "dynamixel_interfaces/srv/detail/get_data_from_dxl__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dynamixel_interfaces__srv__GetDataFromDxl_Response__init(message_memory);
}

void dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_fini_function(void * message_memory)
{
  dynamixel_interfaces__srv__GetDataFromDxl_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_member_array[2] = {
  {
    "item_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamixel_interfaces__srv__GetDataFromDxl_Response, item_data),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamixel_interfaces__srv__GetDataFromDxl_Response, result),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_members = {
  "dynamixel_interfaces__srv",  // message namespace
  "GetDataFromDxl_Response",  // message name
  2,  // number of fields
  sizeof(dynamixel_interfaces__srv__GetDataFromDxl_Response),
  dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_member_array,  // message members
  dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_type_support_handle = {
  0,
  &dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dynamixel_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamixel_interfaces, srv, GetDataFromDxl_Response)() {
  if (!dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_type_support_handle.typesupport_identifier) {
    dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dynamixel_interfaces__srv__GetDataFromDxl_Response__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "dynamixel_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "dynamixel_interfaces/srv/detail/get_data_from_dxl__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_service_members = {
  "dynamixel_interfaces__srv",  // service namespace
  "GetDataFromDxl",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_Request_message_type_support_handle,
  NULL  // response message
  // dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_Response_message_type_support_handle
};

static rosidl_service_type_support_t dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_service_type_support_handle = {
  0,
  &dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamixel_interfaces, srv, GetDataFromDxl_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamixel_interfaces, srv, GetDataFromDxl_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dynamixel_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamixel_interfaces, srv, GetDataFromDxl)() {
  if (!dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_service_type_support_handle.typesupport_identifier) {
    dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamixel_interfaces, srv, GetDataFromDxl_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamixel_interfaces, srv, GetDataFromDxl_Response)()->data;
  }

  return &dynamixel_interfaces__srv__detail__get_data_from_dxl__rosidl_typesupport_introspection_c__GetDataFromDxl_service_type_support_handle;
}
