Summary:	Unix port of Borland TurboVision library
Summary(pl):	Uniksowa wersja biblioteki TurboVision Borlanda
Name:		librhtv
Version:	2.0.3
Release:	2
License:	Borland, some modifications are BSD-like licensed (generally free)
Group:		Libraries
Source0:	http://dl.sourceforge.net/tvision/rhtvision-%{version}.src.tar.gz
# Source0-md5:	b6129f5c510ba9d28d21c9575b7e1c75
Patch0:		%{name}-nolowlevelgarbage.patch
Patch1:		%{name}-gcc4.patch
URL:		http://tvision.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	gpm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	perl-base
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
Requires:	%{name} = %{version}-%{release}

%description devel
rhtvision header files.

%description devel -l pl
Pliki nag³ówkowe rhtvision.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static rhtvision libraries.

%description static -l pl
Biblioteki statyczne rhtvision.

%prep
%setup -q -n tvision
%patch0 -p1
%patch1 -p1

%build
%{__perl} config.pl \
	--prefix=%{_prefix} \
	--cflags="%{rpmcflags} -I/usr/include/ncurses" \
	--cxxflags="%{rpmcflags} -fno-exceptions -I/usr/include/ncurses" \
	%{?debug:--with-debug}

%{__make} \
	RHIDE_GCC="%{__cc}" \
	RHIDE_GXX="%{__cxx}" \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# let's create new rhide.env
cat > examples/rhide.env  <<EOF
RHIDE_GCC=gcc
RHIDE_GXX=g++
RHIDE_LD=gcc
RHIDE_AR=ar
RHIDE_ARFLAGS=rcs
RHIDE_OS_CFLAGS=%{rpmcflags} -Wall
RHIDE_OS_CXXFLAGS=%{rpmcflags} -Wall
RHIDE_STDINC=/usr/include /usr/X11R6/include /usr/include/ncurses
TVSRC=%{_includedir}/rhtvision
RHIDE_OS_LIBS=stdc++
TVOBJ=
STDCPP_LIB=-lstdc++
SHARED_CODE_OPTION=-fPIC
EOF

cd examples
%{__perl} patchenv.pl
cd ..

cp -ar examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%find_lang tvision%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f tvision%{version}.lang
%defattr(644,root,root,755)
%doc readme.txt TODO borland.txt
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt doc/*.html
%attr(755,root,root) %{_bindir}/rhtv-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
