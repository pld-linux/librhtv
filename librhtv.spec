Summary:	Unix port of Borland TurboVision library
Summary(pl):	Uniksowa wersja biblioteki TurboVision Borlanda
Name:		librhtv
Version:	1.1.4
Release:	2
License:	Borland, some modifications are BSD-like licensed (generally free)
Group:		Libraries
Source0:	http://prdownloads.sourceforge.net/setedit/rhtvision-%{version}.src.tar.gz
Patch0:		%{name}-nostrip.patch
Patch1:		%{name}-nolowlevelgarbage.patch
Patch2:		%{name}-gcc32.patch
BuildRequires:	XFree86-devel
BuildRequires:	gpm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Turbo Vision (or TV, for short) is a library that provides an
application framework. With TV you can write a beautiful
object-oriented character-mode user interface in a short time.

TV is available in C++ and Pascal and is a product of Borland
International. It was developed to run on MS-DOS systems, but today it
is available for many other platforms (ported by independent
programmers).

This port is based on the Borland 2.0 version with fixes.

%description -l pl
Uniksowa wersja biblioteki TurboVision 2.0 Borlanda. TurboVision jest
obiektow± bibliotek± do okienkowych interfejsów u¿ytkownika w trybie
tekstowym.

%package devel
Summary:	%{name} header files
Summary(pl):	Pliki nag³ówkowe %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
rhtvision header files.

%description devel -l pl
Pliki nag³ówkowe rhtvision.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static rhtvision libraries.

%description static -l pl
Biblioteki statyczne rhtvision.

%prep
%setup -q -n tvision
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
./configure --prefix=%{_prefix} \
	--cflags="-I/usr/include/ncurses"

sed 's|<sys/time.h>|<time.h>|' examples/demo/puzzle.cc > examples/demo/puzzle.cc.tmp
mv -f examples/demo/puzzle.cc.tmp examples/demo/puzzle.cc

%{__make} \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcflags} -fno-exceptions -fno-implicit-templates"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix}

# let's create new rhide.env
cat > examples/rhide.env  <<EOF
RHIDE_GCC=gcc
RHIDE_GXX=g++
RHIDE_LD=gcc
RHIDE_AR=ar
RHIDE_OS_CFLAGS=-I%{_includedir}/ncurses
RHIDE_OS_CXXFLAGS=-I%{_includedir}/ncurses

TVSRC=%{_includedir}/rhtvision
RHIDE_OS_LIBS=
TVOBJ=
EOF

cd examples
perl patchenv.pl
cd ..

cp -ar examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc readme.txt TODO borland.txt
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%dir %{_examplesdir}/%{name}
%{_examplesdir}/%{name}/*

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
