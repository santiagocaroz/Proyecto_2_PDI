cmake_minimum_required(VERSION 3.13.4)

project(PDI_2)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/PDI_2")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Carlos Munoz (UdeA), Santiago Caro (UdeA)")
set(EXTENSION_DESCRIPTION "This is an example of a simple extension")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/PDI_2.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/PDI_2/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(PDI_2)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
