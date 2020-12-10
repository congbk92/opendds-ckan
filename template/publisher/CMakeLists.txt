project(OpenDDS_DevGuide_Messenger CXX)
cmake_minimum_required(VERSION 3.8.2)

find_package(OpenDDS REQUIRED)
find_package(RapidJSON REQUIRED)

set(CMAKE_CXX_COMPILER ${OPENDDS_COMPILER})


set(opendds_libs
  OpenDDS::Dcps # Core OpenDDS Library
  OpenDDS::InfoRepoDiscovery OpenDDS::Tcp # For run_test.pl
  OpenDDS::Rtps OpenDDS::Rtps_Udp # For run_test.pl --rtps
)

# Publisher
add_executable(publisher
  Publisher.cpp
)
OPENDDS_TARGET_SOURCES(publisher
  Messenger.idl
  OPENDDS_IDL_OPTIONS -Grapidjson)
target_link_libraries(publisher ${opendds_libs})