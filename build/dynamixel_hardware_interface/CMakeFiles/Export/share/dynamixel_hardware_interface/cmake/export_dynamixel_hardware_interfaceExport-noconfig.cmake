#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "dynamixel_hardware_interface::dynamixel_hardware_interface" for configuration ""
set_property(TARGET dynamixel_hardware_interface::dynamixel_hardware_interface APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(dynamixel_hardware_interface::dynamixel_hardware_interface PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libdynamixel_hardware_interface.so"
  IMPORTED_SONAME_NOCONFIG "libdynamixel_hardware_interface.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS dynamixel_hardware_interface::dynamixel_hardware_interface )
list(APPEND _IMPORT_CHECK_FILES_FOR_dynamixel_hardware_interface::dynamixel_hardware_interface "${_IMPORT_PREFIX}/lib/libdynamixel_hardware_interface.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
