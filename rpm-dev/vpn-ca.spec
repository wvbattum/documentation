%global git 74e0a2c9d89490f8aa78123da58bc4f88aecd3fe

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**}; 
%endif

Name:           vpn-ca
Version:        0.0.6
Release:        1%{?dist}
Summary:        Simple CA intended for use with Let's Connect! VPN

License:        MIT
URL:            https://software.tuxed.net/vpn-ca

%if %{defined git}
Source0:        https://git.tuxed.net/fkooman/vpn-ca/snapshot/vpn-ca-%{git}.tar.xz
%else
Source0:        https://software.tuxed.net/vpn-ca/files/vpn-ca-%{version}.tar.xz
Source1:        https://software.tuxed.net/vpn-ca/files/vpn-ca-%{version}.tar.xz.minisig
Source2:        minisign-8466FFE127BCDC82.pub
%endif 

BuildRequires:  minisign
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
Simple CA intended for use with Let's Connect! & eduVPN.

%prep
%if %{defined git}
%setup -qn vpn-ca-%{git}
%else
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -p %{SOURCE2}
%setup -qn vpn-ca-%{version}
%endif

%build
for cmd in vpn-ca; do
  %gobuild -o _bin/$(basename $cmd) $cmd/main.go
done

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp _bin/*              %{buildroot}%{_bindir}/

%files
%{_bindir}/*

%doc README.md AUTHORS.md
%license LICENSE.txt

%changelog
* Thu Oct 10 2019 François Kooman <fkooman@tuxed.net> - 0.0.6-1
- update to 0.0.6

* Thu Oct 10 2019 François Kooman <fkooman@tuxed.net> - 0.0.5-1
- update to 0.0.5

* Wed Oct 09 2019 François Kooman <fkooman@tuxed.net> - 0.0.4-1
- update to 0.0.4

* Sat Sep 28 2019 François Kooman <fkooman@tuxed.net> - 0.0.3-1
- update to 0.0.3

* Thu Sep 19 2019 François Kooman <fkooman@tuxed.net> - 0.0.2-1
- initial package
