# This is a dummy CMakeLists.txt file to test the Scaffold class.

cmake_minimum_required(VERSION 3.9)

# Some unicode to test correct handling of multibyte characters:
# Voilà un petit projet à moi
project(DumDum)

option(BUILD_EXECUTABLE "Build the executable for this project")

if (BUILD_EXECUTABLE):

  #$[main-target

  add_executable(${PROJECT_NAME} 
    src/dummy.cpp
  )

    #$]

endif()