// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dynamixel_interfaces:srv/SetDataToDxl.idl
// generated code does not contain a copyright notice

#ifndef DYNAMIXEL_INTERFACES__SRV__DETAIL__SET_DATA_TO_DXL__TRAITS_HPP_
#define DYNAMIXEL_INTERFACES__SRV__DETAIL__SET_DATA_TO_DXL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dynamixel_interfaces/srv/detail/set_data_to_dxl__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace dynamixel_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetDataToDxl_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: item_name
  {
    out << "item_name: ";
    rosidl_generator_traits::value_to_yaml(msg.item_name, out);
    out << ", ";
  }

  // member: item_data
  {
    out << "item_data: ";
    rosidl_generator_traits::value_to_yaml(msg.item_data, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetDataToDxl_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: item_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "item_name: ";
    rosidl_generator_traits::value_to_yaml(msg.item_name, out);
    out << "\n";
  }

  // member: item_data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "item_data: ";
    rosidl_generator_traits::value_to_yaml(msg.item_data, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetDataToDxl_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace dynamixel_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use dynamixel_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dynamixel_interfaces::srv::SetDataToDxl_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  dynamixel_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dynamixel_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const dynamixel_interfaces::srv::SetDataToDxl_Request & msg)
{
  return dynamixel_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dynamixel_interfaces::srv::SetDataToDxl_Request>()
{
  return "dynamixel_interfaces::srv::SetDataToDxl_Request";
}

template<>
inline const char * name<dynamixel_interfaces::srv::SetDataToDxl_Request>()
{
  return "dynamixel_interfaces/srv/SetDataToDxl_Request";
}

template<>
struct has_fixed_size<dynamixel_interfaces::srv::SetDataToDxl_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<dynamixel_interfaces::srv::SetDataToDxl_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<dynamixel_interfaces::srv::SetDataToDxl_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace dynamixel_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetDataToDxl_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: result
  {
    out << "result: ";
    rosidl_generator_traits::value_to_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetDataToDxl_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result: ";
    rosidl_generator_traits::value_to_yaml(msg.result, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetDataToDxl_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace dynamixel_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use dynamixel_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dynamixel_interfaces::srv::SetDataToDxl_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  dynamixel_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dynamixel_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const dynamixel_interfaces::srv::SetDataToDxl_Response & msg)
{
  return dynamixel_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dynamixel_interfaces::srv::SetDataToDxl_Response>()
{
  return "dynamixel_interfaces::srv::SetDataToDxl_Response";
}

template<>
inline const char * name<dynamixel_interfaces::srv::SetDataToDxl_Response>()
{
  return "dynamixel_interfaces/srv/SetDataToDxl_Response";
}

template<>
struct has_fixed_size<dynamixel_interfaces::srv::SetDataToDxl_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dynamixel_interfaces::srv::SetDataToDxl_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dynamixel_interfaces::srv::SetDataToDxl_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<dynamixel_interfaces::srv::SetDataToDxl>()
{
  return "dynamixel_interfaces::srv::SetDataToDxl";
}

template<>
inline const char * name<dynamixel_interfaces::srv::SetDataToDxl>()
{
  return "dynamixel_interfaces/srv/SetDataToDxl";
}

template<>
struct has_fixed_size<dynamixel_interfaces::srv::SetDataToDxl>
  : std::integral_constant<
    bool,
    has_fixed_size<dynamixel_interfaces::srv::SetDataToDxl_Request>::value &&
    has_fixed_size<dynamixel_interfaces::srv::SetDataToDxl_Response>::value
  >
{
};

template<>
struct has_bounded_size<dynamixel_interfaces::srv::SetDataToDxl>
  : std::integral_constant<
    bool,
    has_bounded_size<dynamixel_interfaces::srv::SetDataToDxl_Request>::value &&
    has_bounded_size<dynamixel_interfaces::srv::SetDataToDxl_Response>::value
  >
{
};

template<>
struct is_service<dynamixel_interfaces::srv::SetDataToDxl>
  : std::true_type
{
};

template<>
struct is_service_request<dynamixel_interfaces::srv::SetDataToDxl_Request>
  : std::true_type
{
};

template<>
struct is_service_response<dynamixel_interfaces::srv::SetDataToDxl_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DYNAMIXEL_INTERFACES__SRV__DETAIL__SET_DATA_TO_DXL__TRAITS_HPP_
