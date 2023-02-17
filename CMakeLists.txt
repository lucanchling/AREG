cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(AREG)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/AREG")
set(EXTENSION_CATEGORY "Automated Dental Tools")
set(EXTENSION_CONTRIBUTORS "Nathan Hutin (University of Michigan), Luc Anchling (University of Michigan)")
set(EXTENSION_DESCRIPTION "This is an example of a simple extension")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/AREG.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/AREG/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies


#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(AREG)
add_subdirectory(AREG_CBCT)
add_subdirectory(AREG_IOS)

## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
