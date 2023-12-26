#
# Conditional build:
%bcond_without	python2		# Python 2 bindings

Summary:	A SIXEL encoder/decoder implementation
Name:		libsixel
Version:	1.10.3
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/libsixel/libsixel/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c104233ee1a4c18fb2e76a478d9bb60c
Patch0:		git-fixes.patch
URL:		https://github.com/libsixel/libsixel
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	pkgconfig
%if %{with python2}
BuildRequires:	python >= 1:2.3
BuildRequires:	python-modules >= 1:2.3
BuildRequires:	python-setuptools
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SIXEL is one of image formats for printer and terminal imaging
introduced by Digital Equipment Corp. (DEC). Its data scheme is
represented as a terminal-friendly escape sequence. So if you want to
view a SIXEL image file, all you have to do is "cat" it to your
terminal.

This package provides encoder/decoder implementation for DEC SIXEL
graphics.

%package devel
Summary:	Header files for libsixel library
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for libsixel library.

%package static
Summary:	Static libsixel library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libsixel library.

%package utils
Summary:	Converter utilities to/from SIXEL format
Group:		Applications/Graphics
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description utils
Converter utilities to/from SIXEL format.

%package -n python-libsixel
Summary:	Python 2 bindings for libsixel
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules >= 1:2.3
BuildArch:	noarch

%description -n python-libsixel
Python 2 bindings for libsixel.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	-Dbashcompletiondir="%{bash_compdir}" \
	-Dzshcompletiondir="%{zsh_compdir}"

%ninja_build -C build

%if %{with python2}
cd  python
%py_build
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with python2}
cd  python
%py_install

%py_postclean
cd ..
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README.md
%attr(755,root,root) %{_libdir}/libsixel.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsixel.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libsixel-config
%attr(755,root,root) %{_libdir}/libsixel.so
%{_includedir}/sixel.h
%{_pkgconfigdir}/libsixel.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsixel.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/img2sixel
%attr(755,root,root) %{_bindir}/sixel2png
%{_mandir}/man1/img2sixel.1*
%{_mandir}/man1/sixel2png.1*
%{bash_compdir}/img2sixel
%{zsh_compdir}/_img2sixel

%if %{with python2}
%files -n python-libsixel
%defattr(644,root,root,755)
%doc python/README.rst
%{py_sitescriptdir}/libsixel/*.py[co]
%{py_sitescriptdir}/libsixel_python-*-py*.egg-info
%endif
