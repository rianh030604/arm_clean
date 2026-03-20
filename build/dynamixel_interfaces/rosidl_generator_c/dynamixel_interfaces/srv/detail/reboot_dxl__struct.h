// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dynamixel_interfaces:srv/RebootDxl.idl
// generated code does not contain a copyright notice

#ifndef DYNAMIXEL_INTERFACES__SRV__DETAIL__REBOOT_DXL__STRUCT_H_
#define DYNAMIXEL_INTERFACES__SRV__DETAIL__REBOOT_DXL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in srv/RebootDxl in the package dynamixel_interfaces.
typedef struct dynamixel_interfaces__srv__RebootDxl_Request
{
  std_msgs__msg__Header header;
} dynamixel_interfaces__srv__RebootDxl_Request;

// Struct for a sequence of dynamixel_interfaces__srv__RebootDxl_Request.
typedef struct dynamixel_interfaces__srv__RebootDxl_Request__Sequence
{
  dynamixel_interfaces__srv__RebootDxl_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dynamixel_interfaces__srv__RebootDxl_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/RebootDxl in the package dynamixel_interfaces.
typedef struct dynamixel_interfaces__srv__RebootDxl_Response
{
  bool result;
} dynamixel_interfaces__srv__RebootDxl_Response;

// Struct for a sequence of dynamixel_interfaces__srv__RebootDxl_Response.
typedef struct dynamixel_interfaces__srv__RebootDxl_Response__Sequence
{
  dynamixel_interfaces__srv__RebootDxl_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dynamixel_interfaces__srv__RebootDxl_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DYNAMIXEL_INTERFACES__SRV__DETAIL__REBOOT_DXL__STRUCT_H_
