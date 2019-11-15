# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "rosaria: 1 messages, 0 services")

set(MSG_I_FLAGS "-Irosaria:/home/heinrich/catkin_ws/src/rosaria/msg;-Igeometry_msgs:/opt/ros/kinetic/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(rosaria_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg" NAME_WE)
add_custom_target(_rosaria_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rosaria" "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg" "std_msgs/Header"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(rosaria
  "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rosaria
)

### Generating Services

### Generating Module File
_generate_module_cpp(rosaria
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rosaria
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(rosaria_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(rosaria_generate_messages rosaria_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg" NAME_WE)
add_dependencies(rosaria_generate_messages_cpp _rosaria_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosaria_gencpp)
add_dependencies(rosaria_gencpp rosaria_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosaria_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(rosaria
  "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rosaria
)

### Generating Services

### Generating Module File
_generate_module_eus(rosaria
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rosaria
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(rosaria_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(rosaria_generate_messages rosaria_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg" NAME_WE)
add_dependencies(rosaria_generate_messages_eus _rosaria_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosaria_geneus)
add_dependencies(rosaria_geneus rosaria_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosaria_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(rosaria
  "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rosaria
)

### Generating Services

### Generating Module File
_generate_module_lisp(rosaria
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rosaria
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(rosaria_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(rosaria_generate_messages rosaria_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg" NAME_WE)
add_dependencies(rosaria_generate_messages_lisp _rosaria_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosaria_genlisp)
add_dependencies(rosaria_genlisp rosaria_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosaria_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(rosaria
  "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rosaria
)

### Generating Services

### Generating Module File
_generate_module_nodejs(rosaria
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rosaria
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(rosaria_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(rosaria_generate_messages rosaria_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg" NAME_WE)
add_dependencies(rosaria_generate_messages_nodejs _rosaria_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosaria_gennodejs)
add_dependencies(rosaria_gennodejs rosaria_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosaria_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(rosaria
  "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosaria
)

### Generating Services

### Generating Module File
_generate_module_py(rosaria
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosaria
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(rosaria_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(rosaria_generate_messages rosaria_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/heinrich/catkin_ws/src/rosaria/msg/BumperState.msg" NAME_WE)
add_dependencies(rosaria_generate_messages_py _rosaria_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rosaria_genpy)
add_dependencies(rosaria_genpy rosaria_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rosaria_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rosaria)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rosaria
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(rosaria_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(rosaria_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rosaria)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rosaria
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(rosaria_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(rosaria_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rosaria)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rosaria
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(rosaria_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(rosaria_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rosaria)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rosaria
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(rosaria_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(rosaria_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosaria)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosaria\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rosaria
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(rosaria_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(rosaria_generate_messages_py std_msgs_generate_messages_py)
endif()
