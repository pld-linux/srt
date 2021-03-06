#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Secure Reliable Transport library
Summary(pl.UTF-8):	Biblioteka Secure Reliable Transport
Name:		srt
Version:	1.4.2
Release:	1
License:	MPL v2.0
Group:		Libraries
#Source0Download: https://github.com/Haivision/srt/releases
Source0:	https://github.com/Haivision/srt/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6e4604f5638d222191a5eb7444d23701
URL:		https://www.srtalliance.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Secure Reliable Transport (SRT) is an open source transport technology
that optimizes streaming performance across unpredictable networks,
such as the Internet.

%description -l pl.UTF-8
Secure Reliable Transport (SRT) to oparta na otwartych źródłach
technika transportu optymalizująca wydajność przesyłania strumieni po
nieprzewidywalnych sieciach, takich jak Internet.

%package devel
Summary:	Header files for SRT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SRT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for SRT library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SRT.

%package static
Summary:	Static SRT library
Summary(pl.UTF-8):	Statyczna biblioteka SRT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SRT library.

%description static -l pl.UTF-8
Statyczna biblioteka SRT.

%prep
%setup -q

%build
install -d build
cd build
# .pc file generation expects relative CMAKE_INSTALL_{INCLUDE,LIB}DIR
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DENABLE_CXX_DEPS=OFF \
	%{!?with_static_libs:-DENABLE_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md docs/{*.md,images}
%attr(755,root,root) %{_bindir}/srt-ffplay
%attr(755,root,root) %{_bindir}/srt-file-transmit
%attr(755,root,root) %{_bindir}/srt-live-transmit
%attr(755,root,root) %{_bindir}/srt-tunnel
%attr(755,root,root) %{_libdir}/libsrt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsrt.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsrt.so
%{_includedir}/srt
%{_pkgconfigdir}/haisrt.pc
%{_pkgconfigdir}/srt.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsrt.a
%endif
