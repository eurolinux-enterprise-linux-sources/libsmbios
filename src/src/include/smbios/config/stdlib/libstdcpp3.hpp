//  (C) Copyright John Maddock 2001. 
//  (C) Copyright Jens Maurer 2001. 
//  Use, modification and distribution are subject to the 
//  Boost Software License, Version 1.0. (See accompanying file 
//  LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

//  See http://www.boost.org for most recent version.

//  config for libstdc++ v3
//  not much to go in here:

#define LIBSMBIOS_STDLIB "GNU libstdc++ version " LIBSMBIOS_STRINGIZE(__GLIBCPP__)

#ifndef _GLIBCPP_USE_WCHAR_T
#  define LIBSMBIOS_NO_CWCHAR
#  define LIBSMBIOS_NO_CWCTYPE
#  define LIBSMBIOS_NO_STD_WSTRING
#  define LIBSMBIOS_NO_STD_WSTREAMBUF
#endif
 
#ifndef _GLIBCPP_USE_LONG_LONG
// May have been set by compiler/*.hpp, but "long long" without library
// support is useless.
#  undef LIBSMBIOS_HAS_LONG_LONG
#endif


