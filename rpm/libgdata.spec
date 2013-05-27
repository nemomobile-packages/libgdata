Name:           libgdata
Version:        0.10.1
Release:        1
Summary:        Library for the GData protocol
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://live.gnome.org/libgdata
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.10/%{name}-%{version}.tar.xz
Patch0:         disable-gtkdoc.patch
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(oauth)
BuildRequires:  intltool
BuildRequires:  gnome-common

%description
libgdata is a GLib-based library for accessing online service APIs using the
GData protocol --- most notably, Google's services. It provides APIs to access
the common Google services, and has full asynchronous support.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}/%{name}

# disable-gtkdoc.patch
%patch0 -p1

%build
echo "EXTRA_DIST = missing-gtk-doc" > gtk-doc.make
PKG_NAME=libgdata REQUIRED_PKG_CONFIG_VERSION=0.17.1 REQUIRED_AUTOMAKE_VERSION=1.9 USE_GNOME2_MACROS=1 NOCONFIGURE=1 . gnome-autogen.sh

%configure --disable-static --disable-gnome --disable-goa
#make %{?jobs:-j%jobs}
make -j1 V=1

%install
rm -rf %{buildroot}
%make_install
rm -rf %{buildroot}/%{_datadir}/gtk-doc/html/gdata/
%find_lang gdata


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gdata.lang
%doc COPYING NEWS README AUTHORS
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
