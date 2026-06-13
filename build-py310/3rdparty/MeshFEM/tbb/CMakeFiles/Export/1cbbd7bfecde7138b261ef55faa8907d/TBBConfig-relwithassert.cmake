#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithAssert".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "TBB::tbb" for configuration "RelWithAssert"
set_property(TARGET TBB::tbb APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHASSERT)
set_target_properties(TBB::tbb PROPERTIES
  IMPORTED_LOCATION_RELWITHASSERT "${_IMPORT_PREFIX}/lib/libtbb.dylib"
  IMPORTED_SONAME_RELWITHASSERT "@rpath/libtbb.dylib"
  )

list(APPEND _cmake_import_check_targets TBB::tbb )
list(APPEND _cmake_import_check_files_for_TBB::tbb "${_IMPORT_PREFIX}/lib/libtbb.dylib" )

# Import target "TBB::tbbmalloc" for configuration "RelWithAssert"
set_property(TARGET TBB::tbbmalloc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHASSERT)
set_target_properties(TBB::tbbmalloc PROPERTIES
  IMPORTED_LOCATION_RELWITHASSERT "${_IMPORT_PREFIX}/lib/libtbbmalloc.dylib"
  IMPORTED_SONAME_RELWITHASSERT "@rpath/libtbbmalloc.dylib"
  )

list(APPEND _cmake_import_check_targets TBB::tbbmalloc )
list(APPEND _cmake_import_check_files_for_TBB::tbbmalloc "${_IMPORT_PREFIX}/lib/libtbbmalloc.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
