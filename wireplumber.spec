Name:       wireplumber
Version:    0.4.3
Release:    1%{?dist}
Summary:    A modular session/policy manager for PipeWire

License:    MIT
URL:        https://pipewire.pages.freedesktop.org/wireplumber/
Source0:    https://gitlab.freedesktop.org/pipewire/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  meson gcc pkgconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libspa-0.2) >= 0.2
BuildRequires:  pkgconfig(libpipewire-0.3) >= 0.3.26
BuildRequires:  pkgconfig(systemd)
BuildRequires:  systemd-devel >= 184
BuildRequires:  pkgconfig(lua)
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-lxml doxygen
BuildRequires:  systemd-rpm-macros

Provides:       pipewire-session-manager
Conflicts:      pipewire-session-manager

%package        libs
Summary:        Libraries for WirePlumber clients
Recommends:     %{name}%{?_isa} = %{version}-%{release}

%description libs
This package contains the runtime libraries for any application that wishes
to interface with WirePlumber.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description
WirePlumber is a modular session/policy manager for PipeWire and a
GObject-based high-level library that wraps PipeWire's API, providing
convenience for writing the daemon's modules as well as external tools for
managing PipeWire.

%prep
%autosetup

%build
%meson -Dsystem-lua=true \
       -Ddoc=disabled \
       -Dsystemd=enabled \
       -Dsystemd-user-service=true \
       -Dintrospection=enabled
%meson_build

%install
%meson_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%{_bindir}/wireplumber
%{_bindir}/wpctl
%{_bindir}/wpexec
%dir %{_datadir}/wireplumber
%config(noreplace) %{_datadir}/wireplumber/bluetooth.conf
%dir %{_datadir}/wireplumber/bluetooth.lua.d
%config(noreplace) %{_datadir}/wireplumber/bluetooth.lua.d/00-functions.lua
%config(noreplace) %{_datadir}/wireplumber/bluetooth.lua.d/30-bluez-monitor.lua
%config(noreplace) %{_datadir}/wireplumber/bluetooth.lua.d/50-bluez-config.lua
%config(noreplace) %{_datadir}/wireplumber/bluetooth.lua.d/90-enable-all.lua
%dir %{_datadir}/wireplumber/common
%config(noreplace) %{_datadir}/wireplumber/common/00-functions.lua
%config(noreplace) %{_datadir}/wireplumber/main.conf
%dir %{_datadir}/wireplumber/main.lua.d
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/00-functions.lua
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/20-default-access.lua
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/30-alsa-monitor.lua
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/30-v4l2-monitor.lua
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/40-device-defaults.lua
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/50-alsa-config.lua
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/50-default-access-config.lua
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/50-v4l2-config.lua
%config(noreplace) %{_datadir}/wireplumber/main.lua.d/90-enable-all.lua
%config(noreplace) %{_datadir}/wireplumber/policy.conf
%dir %{_datadir}/wireplumber/policy.lua.d
%config(noreplace) %{_datadir}/wireplumber/policy.lua.d/00-functions.lua
%config(noreplace) %{_datadir}/wireplumber/policy.lua.d/10-default-policy.lua
%config(noreplace) %{_datadir}/wireplumber/policy.lua.d/50-endpoints-config.lua
%config(noreplace) %{_datadir}/wireplumber/policy.lua.d/90-enable-all.lua
%config(noreplace) %{_datadir}/wireplumber/wireplumber.conf
%{_datadir}/wireplumber/
%{_userunitdir}/wireplumber.service
%{_userunitdir}/wireplumber@.service

%files libs
%license LICENSE
%dir %{_libdir}/wireplumber-0.4/
%{_libdir}/wireplumber-0.4/libwireplumber-*.so
%{_libdir}/libwireplumber-0.4.so.*
%{_libdir}/girepository-1.0/Wp-0.4.typelib

%files devel
%{_includedir}/wireplumber-0.4/
%{_libdir}/libwireplumber-0.4.so
%{_libdir}/pkgconfig/wireplumber-0.4.pc
%{_datadir}/gir-1.0/Wp-0.4.gir

%changelog
* Fri Oct 07 2021 Wim Taymans <wim.taymans@redhat.com> - 0.4.3-1
- wireplumber 0.4.3

* Wed Sep 01 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.2-1
- wireplumber 0.4.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 06 2021 Peter Hutterer <peter.hutterer@redhat.com> 0.4.1-1
- Initial package (#1976012)
