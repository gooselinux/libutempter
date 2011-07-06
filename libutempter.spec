%define utempter_compat_ver 0.5.2

Summary: A privileged helper for utmp/wtmp updates
Name: libutempter
Version: 1.1.5
Release: 4.1%{?dist}
License: LGPLv2
Group: System Environment/Libraries
URL: ftp://ftp.altlinux.org/pub/people/ldv/utempter
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.bz2

Requires(pre): shadow-utils
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Provides: utempter = %{utempter_compat_ver}
Obsoletes: utempter

%description
This library provides interface for terminal emulators such as
screen and xterm to record user sessions to utmp and wtmp files.

%package devel
Summary: Development environment for utempter
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development files required to build
utempter-based software.

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR="$RPM_BUILD_ROOT" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

# FIXME: We might need to enable this part for backward compat with the
# Red Hat / Fedora 'utempter' package:
#
# mkdir -p %{_sbindir}
# ln -sf %{helperdir}/utempter %{_sbindir}/utempter


# NOTE: Static lib intentionally disabled.
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%pre
{
    %{_sbindir}/groupadd -g 22 -r -f utmp || :
    %{_sbindir}/groupadd -g 35 -r -f utempter || :
}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libutempter.so.0
%{_libdir}/libutempter.so.1.1.5
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter
# FIXME: If a symlink is needed for compat here, uncomment the code in the
# install section and this as well:
#%{_sbindir}/utempter

%files devel
%defattr(-,root,root,-)
%{_includedir}/utempter.h
%{_libdir}/libutempter.so

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.1.5-4.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.5-2
- Autorebuild for GCC 4.3

* Wed Nov 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.5-1
- version upgrade
- fix #246063

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.1.4-4
- Rebuild for build id

* Thu Jul 27 2006 Mike A. Harris <mharris@redhat.com> 1.1.4-3.fc6
- Create 'utempter' group with official allocated GID==35 (from setup package).

* Tue Jul 25 2006 Mike A. Harris <mharris@redhat.com> 1.1.4-2.fc6
- Removed usage of rpm macros inside the spec changelog (#200051)
- Removed non-UTF-8 chars from changelog.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.1.4-1.fc6
- Initial build of Dimitry's libutempter replacement for Fedora Core.
- Reworked the upstream spec file for Fedora packaging compliance.
- Removed static lib subpackage as we dont ship those.

* Fri Dec 09 2005 Dmitry V. Levin <ldv@altlinux.org> 1.1.4-alt1
- Enabled almost all diagnostics supported by gcc and fixed all
  issues found by gcc-3.4.4-alt3.
- Added FreeBSD support, based on patches from Gentoo/FreeBSD.
- Makefile:
  + Fixed few portability issues reported by Gentoo developers.
- libutempter: Linked with -Wl,-z,defs.
- utempter:
  + Fixed struct utmp initialization on 64-bit architectures
    with 32-bit backwards compatibility enabled (like x86_64).
  + Linked with -Wl,-z,now, i.e., marked it to tell the dynamic
    linker to resolve all symbols when the program is started.
    Suggested by Gentoo developers.

* Thu Aug 18 2005 Dmitry V. Levin <ldv@altlinux.org> 1.1.3-alt1
- Restricted list of global symbols exported by the library.
- Updated FSF postal address.

* Sun Sep 05 2004 Dmitry V. Levin <ldv@altlinux.org> 1.1.2-alt1
- Added multilib support.

* Fri Feb 14 2003 Dmitry V. Levin <ldv@altlinux.org> 1.1.1-alt1
- iface.c: don't block SIGCHLD; redefine signal handler instead.

* Mon Dec 23 2002 Dmitry V. Levin <ldv@altlinux.org> 1.1.0-alt1
- Changed soname back to libutempter.so.0, introduced versioning.

* Tue Sep 24 2002 Dmitry V. Levin <ldv@altlinux.org> 1.0.7-alt1
- If helper execution fails, try saved group ID.

* Tue May 21 2002 Dmitry V. Levin <ldv@altlinux.org> 1.0.6-alt1
- New function: utempter_set_helper.

* Mon Dec 10 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.5-alt1
- iface.c: block SIGCHLD instead of redefine signal handler.

* Wed Nov 21 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.4-alt1
- utempter.h: do not use "__attribute ((unused))".

* Tue Nov 13 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.3-alt1
- Added compatibility declarations to ease upgrade of old applications.
- Added small README file.
- Corrected provides.

* Thu Nov 08 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.2-alt1
- Added compatibility library to ease upgrade of old applications.

* Mon Nov 05 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.1-alt1
- Indented code a bit (Solar request).

* Mon Oct 15 2001 Dmitry V. Levin <ldv@alt-linux.org> 1.0.0-alt1
- Rewritten the code completely.
- Renamed to libutempter.
- Corrected the package description.
- FHSificated (yes, there are no more {_sbindir}/utempter).
- Libificated.

* Fri Oct 12 2001 Dmitry V. Levin <ldv@altlinux.ru> 0.5.2-alt4
- {_libdir}/utempter sounds better so use it as helper directory.

* Thu Oct 11 2001 Dmitry V. Levin <ldv@altlinux.ru> 0.5.2-alt3
- Specfile cleanup.
- Owl-compatible changes:
  + added utempter group;
  + utempter binary moved to {_libdir}/utempter.d,
    owned by group utempter with 710 permissions.

* Thu Jun 28 2001 Sergie Pugachev <fd_rag@altlinux.ru> 0.5.2-alt1
- new version

* Tue Dec 05 2000 AEN <aen@logic.ru>
- build for RE

* Tue Jul 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.1-4mdk
- BM

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 0.5.1-3mdk
- add -devel
- add soname
- spec helper cleanup

* Sat Apr 08 2000 Christopher Molnar <molnarc@mandrakesoft.com> 0.5.1-2mdk
- changed group

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.5.1
- fix utmp as group 22.
- strip utempter.
- defattr to root.

* Thu Jun 10 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Jun  4 1999 Jeff Johnson <jbj@redhat.com>
- ignore SIGCHLD while processing utmp.
