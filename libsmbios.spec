# these are all substituted by autoconf
%define pot_file  libsmbios
%define lang_dom  libsmbios-2.3

# pure python stuff goes here
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

# arch-dep python stuff goes here
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name: libsmbios
Version: 2.3.3
Release: 8%{?dist}
License: GPLv2+ or OSL 2.1
Summary: Libsmbios C shared libraries
Group: System Environment/Libraries
URL: https://github.com/dell/libsmbios
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: strace libxml2-devel gettext git doxygen
BuildRequires: valgrind cppunit hardlink pkgconfig python-devel
BuildRequires: autoconf gettext-devel automake libtool help2man

# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch: x86_64 %{ix86}

Source0: https://github.com/dell/libsmbios/archive/v%{version}.tar.gz
Patch0001: 0001-Don-t-build-the-yum-plugin.patch
Patch0002: 0002-smbios-utils-bin-make-version-output-parsable-by-hel.patch
Patch0003: 0003-smbios-utils-python-make-version-output-parsable-by-.patch
Patch0004: 0004-Force-python-to-install-to-site-arch-not-site-packag.patch
Patch0005: 0005-Add-stuff-generated-during-the-build-to-.gitignore.patch
Patch0006: 0006-Enable-Wextra-with-some-minor-caveats.patch
Patch0007: 0007-Don-t-compare-signed-and-unsigned-values-in-loop-ite.patch
Patch0008: 0008-Fix-some-missing-error-checks-that-covscan-found.patch
Patch0009: 0009-Check-for-fseek-errors-everywhere.patch
Patch0010: 0010-Fix-a-data-leak-on-the-failure-path.patch
Patch0011: 0011-Fix-an-incorrect-error-check.patch
Patch0012: 0012-Simplify-smbios_table_free-token_table_free-and-cmos.patch
Patch0013: 0013-Fix-a-wrong-conditional.patch
Patch0014: 0014-Fix-a-leaked-file-handle.patch
Patch0015: 0015-Fix-some-plausible-buffer-overruns.patch
Patch0016: 0016-Don-t-leak-smbios_strerror-memory.patch
Patch0017: 0017-Fix-some-impossible-logic.patch
Patch0018: 0018-sysinfo_get_asset_tag-get-rid-of-a-strncpy-off-by-on.patch
Patch0019: 0019-sysinfo_get_dell_oem_system_id-don-t-look-at-the-wro.patch
Patch0020: 0020-dell_encode_service_tag-remove-conditionals-that-can.patch
Patch0021: 0021-token.c-don-t-leak-allocated-token-tables.patch
Patch0022: 0022-Fix-two-pointer-arithmetic-errors.patch
Patch0023: 0023-memory_linux.c-remap-fix-some-types-to-avoid-compari.patch
Patch0024: 0024-Get-rid-of-a-bad-debug-print-coverity-found.patch
Patch0025: 0025-smbios_strerror-always-return-a-new-allocation.patch
Patch0026: 0026-._get_id-don-t-promote-u16-int-u16.patch
Patch0027: 0027-slightly-better-token-debugging-information.patch
Patch0028: 0028-libsmbios_c-use-token_table_free-at-more-places.patch

%description
Libsmbios is a library and utilities that can be used by client programs to get
information from standard BIOS tables, such as the SMBIOS table.

This package provides the C-based libsmbios library, with a C interface.

%package -n python-smbios
Summary: Python interface to Libsmbios C library
Group: System Environment/Libraries
Requires: libsmbios = %{version}-%{release}
Requires: python python-ctypes

%description -n python-smbios
This package provides a Python interface to libsmbios

%package -n smbios-utils
Summary: Meta-package that pulls in all smbios binaries and python scripts
Group: Applications/System
Requires: smbios-utils-bin
Requires: smbios-utils-python

%description -n smbios-utils
This is a meta-package that pulls in the binary libsmbios executables as well
as the python executables.

%package -n smbios-utils-bin
Summary: Binary utilities that use libsmbios
Group: Applications/System
Requires: libsmbios = %{version}-%{release}

%description -n smbios-utils-bin
Get BIOS information, such as System product name, product id, service tag and
asset tag.

%package -n smbios-utils-python
Summary: Python executables that use libsmbios
Group: Applications/System
Requires: python-smbios = %{version}-%{release}

%description -n smbios-utils-python
Get BIOS information, such as System product name, product id, service tag and
asset tag. Set service and asset tags on Dell machines. Manipulate wireless
cards/bluetooth on Dell laptops. Set BIOS password on select Dell systems.
Update BIOS on select Dell systems. Set LCD brightness on select Dell laptops.

# name the devel package libsmbios-devel regardless of package name, per suse/fedora convention
%package -n libsmbios-devel
Summary: Development headers and archives
Group: Development/Libraries
Requires: libsmbios = %{version}-%{release}

%description -n libsmbios-devel
Libsmbios is a library and utilities that can be used by client programs to get
information from standard BIOS tables, such as the SMBIOS table.

This package contains the headers and .a files necessary to compile new client
programs against libsmbios.

%prep
%setup -q -n libsmbios-%{version}
find . -type d -exec chmod -f 755 {} \;
find doc src -type f -exec chmod -f 644 {} \;
chmod 755 src/cppunit/*.sh
git init
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git config gc.auto 0
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
# this line lets us build an RPM directly from a git tarball
# and retains any customized version information we might have
[ -e ./configure ] || PACKAGE_VERSION=%{version} ./autogen.sh --no-configure

mkdir _build
cd _build
echo '../configure "$@"' > configure
chmod +x ./configure

%configure

mkdir -p out/libsmbios_c
make CFLAGS="-Werror" %{?_smp_mflags} 2>&1 | tee build-%{_arch}.log

echo \%doc _build/build-%{_arch}.log > buildlogs.txt

TOPDIR=$(pwd)/../
pushd ../src/bin
for x in smbios-battery-ctl smbios-keyboard-ctl smbios-lcd-brightness \
	smbios-passwd smbios-sys-info smbios-thermal-ctl smbios-token-ctl \
	smbios-wakeup-ctl smbios-wireless-ctl ;
do
	chmod +x ${x}
	LD_LIBRARY_PATH=$TOPDIR/_build/out/.libs/ help2man -o ${x}.8 -s 8 -n ${x} -N -l ./${x}
done
popd
pushd out
for x in smbios-get-ut-data smbios-state-byte-ctl smbios-sys-info-lite \
	smbios-upflag-ctl ;
do
	LD_LIBRARY_PATH=$TOPDIR/_build/out/.libs/ help2man -o ${x}.8 -s 8 -n ${x} -N -l ./${x}
done
popd


%check
runtest() {
    mkdir _$1$2
    pushd _$1$2
    ../%configure
    make -e $1 CFLAGS="$CFLAGS -DDEBUG_OUTPUT_ALL" 2>&1 | tee $1$2.log
    touch -r ../configure.ac $1$2-%{_arch}.log
    make -e $1 2>&1 | tee $1$2.log
    popd
    echo \%doc _$1$2/$1$2-%{_arch}.log >> _build/buildlogs.txt
}

if [ -d /usr/include/cppunit ]; then
   # run this first since it is slightly faster than valgrind
    VALGRIND="strace -f" runtest check strace > /dev/null || echo FAILED strace check
fi

if [ -e /usr/bin/valgrind -a -d /usr/include/cppunit ]; then
    runtest valgrind > /dev/null || echo FAILED valgrind check
fi

if [ -d /usr/include/cppunit ]; then
    runtest check > /dev/null || echo FAILED check
fi

if [ ! -d /usr/include/cppunit ]; then
    echo "Unit tests skipped due to missing cppunit."
fi

%install
rm -rf %{buildroot}
mkdir %{buildroot}

cd _build
TOPDIR=..
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man8/
cp -v $TOPDIR/src/bin/*.8 %{buildroot}/%{_mandir}/man8/
cp -v $TOPDIR/_build/out/*.8 %{buildroot}/%{_mandir}/man8/
cp -a $TOPDIR/src/include/*  %{buildroot}/%{_includedir}/
cp -a out/public-include/*  %{buildroot}/%{_includedir}/
rm -f %{buildroot}/%{_libdir}/lib*.{la,a}
find %{buildroot}/%{_includedir} out/libsmbios_c -exec touch -r $TOPDIR/configure.ac {} \;

mv out/libsmbios_c    out/libsmbios_c-%{_arch}

rename %{pot_file}.mo %{lang_dom}.mo $(find %{buildroot}/%{_datadir} -name %{pot_file}.mo)
%find_lang %{lang_dom}

# hardlink files to save some space.
/usr/sbin/hardlink -c -v $RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f _build/%{lang_dom}.lang
%defattr(-,root,root,-)
%{_libdir}/libsmbios_c.so.*

%files -n libsmbios-devel -f _build/buildlogs.txt
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README.md src/bin/getopts_LICENSE.txt src/include/smbios/config/boost_LICENSE_1_0_txt
%{_includedir}/smbios_c
%{_libdir}/libsmbios_c.so
%{_libdir}/pkgconfig/libsmbios_c.pc
%doc _build/out/libsmbios_c-%{_arch}
%exclude %{_includedir}/smbios/
%exclude %{_libdir}/pkgconfig/libsmbios_c++.pc

%files -n smbios-utils
# opensuse 11.1 enforces non-empty file list :(
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README.md
# no other files.

%files -n smbios-utils-bin
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README.md
%doc src/bin/getopts_LICENSE.txt
%{_sbindir}/smbios-state-byte-ctl
%{_mandir}/man8/smbios-state-byte-ctl.*
%{_sbindir}/smbios-get-ut-data
%{_mandir}/man8/smbios-get-ut-data.*
%{_sbindir}/smbios-upflag-ctl
%{_mandir}/man8/smbios-upflag-ctl.*
%{_sbindir}/smbios-sys-info-lite
%{_mandir}/man8/smbios-sys-info-lite.*

%files -n python-smbios
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README.md
%{python_sitearch}/*

%files -n smbios-utils-python
%defattr(-,root,root,-)
%doc COPYING-GPL COPYING-OSL README.md
%doc src/bin/getopts_LICENSE.txt
%dir %{_sysconfdir}/libsmbios
%config(noreplace) %{_sysconfdir}/libsmbios/*

# python utilities
%{_sbindir}/smbios-battery-ctl
%{_mandir}/man8/smbios-battery-ctl.*
%{_sbindir}/smbios-sys-info
%{_mandir}/man8/smbios-sys-info.*
%{_sbindir}/smbios-token-ctl
%{_mandir}/man8/smbios-token-ctl.*
%{_sbindir}/smbios-passwd
%{_mandir}/man8/smbios-passwd.*
%{_sbindir}/smbios-wakeup-ctl
%{_mandir}/man8/smbios-wakeup-ctl.*
%{_sbindir}/smbios-wireless-ctl
%{_mandir}/man8/smbios-wireless-ctl.*
%{_sbindir}/smbios-lcd-brightness
%{_mandir}/man8/smbios-lcd-brightness.*
%{_sbindir}/smbios-keyboard-ctl
%{_mandir}/man8/smbios-keyboard-ctl.*
%{_sbindir}/smbios-thermal-ctl
%{_mandir}/man8/smbios-thermal-ctl.*

# data files
%{_datadir}/smbios-utils

%changelog
* Wed May 16 2018 Peter Jones <pjones@redhat.com> - 2.3.3-8
- Fix smbios-sys-info-lite crashes when an asset tag is not set
  Resolves: rhbz#1562440
- Fix vestigial c++ artifacts included in the package
  Resolves: rhbz#1562440

* Wed Feb 14 2018 Peter Jones <pjones@redhat.com> - 2.3.3-6
- Pull in all the coverity fixes we sent upstream.  I had thought these
  made it in to this release; they did not, but the 2.4.0 release they are
  in is also the python 3 switchover, so we need these as patches.
  Related: rhbz#1463329

* Tue Feb 13 2018 Peter Jones <pjones@redhat.com> - 2.3.3-5
- Try once more to fix the multilib issue...
  Related: rhbz#1463329

* Fri Feb 09 2018 Peter Jones <pjones@redhat.com> - 2.3.3-4
- Fix a multilib error rpmdiff caught
  Related: rhbz#1463329

* Thu Oct 05 2017 Peter Jones <pjones@redhat.com> - 2.3.3-3
- Fix some more rpmdiff complaints
  Related: rhbz#1463329

* Thu Oct 05 2017 Peter Jones <pjones@redhat.com> - 2.3.3-2
- Fix some rpmdiff complaints
  Related: rhbz#1463329

* Mon Oct 02 2017 Peter Jones <pjones@redhat.com> - 2.3.3-1
- Package 2.3.3
  Related: rhbz#1463329
