Name:       wireplumber
Version:    0.4.5
Release:    2%{?dist}
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
%{?systemd_ordering}

# Make sure that we have -libs package in the same version
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

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
%autosetup -p1

%build
%meson -Dsystem-lua=true \
       -Ddoc=disabled \
       -Dsystemd=enabled \
       -Dsystemd-user-service=true \
       -Dintrospection=enabled \
       -Delogind=disabled
%meson_build

%install
%meson_install

# Create local config skeleton
mkdir -p %{buildroot}%{_sysconfdir}/wireplumber/{bluetooth.lua.d,common,main.lua.d,policy.lua.d}

%posttrans
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%triggerun -- fedora-release < 35
# When upgrading to Fedora Linux 35, transition to WirePlumber by default
if [ -x "/bin/systemctl" ]; then
    /bin/systemctl --no-reload preset --global %{name}.service || :
fi

%files
%license LICENSE
%{_bindir}/wireplumber
%{_bindir}/wpctl
%{_bindir}/wpexec
%dir %{_sysconfdir}/wireplumber
%dir %{_sysconfdir}/wireplumber/bluetooth.lua.d
%dir %{_sysconfdir}/wireplumber/common
%dir %{_sysconfdir}/wireplumber/main.lua.d
%dir %{_sysconfdir}/wireplumber/policy.lua.d
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
* Wed Nov 17 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.5-2
- Move the systemd scriptlet to posttrans so we can dnf swap with
  media-session (#2022584)

* Thu Nov 11 2021 Wim Taymans <wim.taymans@redhat.com> - 0.4.5-1
- wireplumber 0.4.5

* Tue Nov 02 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.4.4-3
- Try again for WirePlumber preset upgrades to F35+ (#2016253)

* Sun Oct 24 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.4.4-2
- Ensure WirePlumber activates on upgrade to F35+ (#2016253)

* Fri Oct 15 2021 Wim Taymans <wim.taymans@redhat.com> - 0.4.4-1
- wireplumber 0.4.4

* Wed Oct 13 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.4.3-3
- Fix config setup in file list (#2013861)

* Mon Oct 11 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.3-2
- Fix segfault due to a typo (#2012606)

* Fri Oct 08 2021 Wim Taymans <wim.taymans@redhat.com> - 0.4.3-1
- wireplumber 0.4.3

* Wed Sep 01 2021 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.2-1
- wireplumber 0.4.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 06 2021 Peter Hutterer <peter.hutterer@redhat.com> 0.4.1-1
- Initial package (#1976012)
