Summary:	Implementation of the draft Desktop Menu Specification
Name:		gnome-menus
Version:	3.10.1
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-menus/3.10/%{name}-%{version}.tar.xz
# Source0-md5:	6db025e79e2b69f39fc7aa0753f43081
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	python-devel
Requires:	%{name}-libs = %{version}-%{release}
Provides:	xdg-menus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec

%package libs
Summary:	gnome-menu library
Group:		Libraries

%description libs
gnome-menu library.

%package devel
Summary:	Header files of gnome-menus library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Headers for gnome-menus library.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e '/GNOME_COMPILE_WARNINGS.*/d' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# unsupported locale
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,dv,en@shaw,gn,ha,ig,io,kg,ps,szl}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_datadir}/desktop-directories/*
%{_sysconfdir}/xdg/menus/gnome-applications.menu

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgnome-menu-3.so.?
%attr(755,root,root) %{_libdir}/libgnome-menu-3.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_pkgconfigdir}/*.pc
%{_includedir}/gnome-menus-3.0
%{_datadir}/gir-1.0/GMenu-3.0.gir

