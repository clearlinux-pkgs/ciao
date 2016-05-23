Name     : ciao
Version  : 5f40deb74b895be01c7d6e4daa0f12f0850ac82e
Release  : 9
URL      : https://github.com/01org/ciao
Source0  : https://github.com/01org/ciao/archive/5f40deb74b895be01c7d6e4daa0f12f0850ac82e.tar.gz
Source1  : ciao.tmpfiles
Summary  : Cloud Integrated Advanced Orchestrator
Group    : Development/Tools
License  : Apache-2.0

Requires : ciao-bin
Requires : ciao-config

BuildRequires : go

%description
Ciao is the "Cloud Integrated Advanced Orchestrator".
Its goal is to provide an easy to deploy, secure, scalable
cloud orchestration system which handles virtual machines,
containers, and bare metal apps agnostically as generic workloads.
Implemented in the Go language, it separates logic into
"controller", "scheduler" and "launcher" components which communicate
over the "Simple and Secure Node Transfer Protocol (SSNTP)".

%package bin
Summary: bin components for the ciao package.
Group: Binaries

%description bin
bin components for the ciao package.

%package config
Summary: config components for the ciao package.
Group: Default

%description config
config components for the ciao package.

%package cnci-agent
Summary: Compute Node Concentrators
Group: Default

%description cnci-agent
The CNCI Agent is the service running within a CNCI VM
that communicates with the ciao-scheduler to create new
bridges and tunnels in response to remote bridge and
tunnel creation on a compute node.

%prep
%setup -q

%build
export GOROOT="/usr/lib/golang"
export GOPATH="%{buildroot}/usr/lib/golang:$(pwd)"
mv vendor src
mkdir -p src/github.com/01org
ln -s ../../../ src/github.com/01org/ciao
for dir in ciao-cli ciao-controller ciao-launcher ciao-scheduler networking/ciao-cnci-agent payloads ciao-cert;
do
    pushd $dir
    go build -v -x
    popd
done

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE1} %{buildroot}/usr/lib/tmpfiles.d/ciao.conf
install -D ./ciao-cli/ciao-cli               %{buildroot}%{_bindir}
install -D ./ciao-controller/ciao-controller %{buildroot}%{_bindir}
install -D ./ciao-launcher/ciao-launcher     %{buildroot}%{_bindir}
install -D ./ciao-scheduler/ciao-scheduler   %{buildroot}%{_bindir}
install -D ./networking/ciao-cnci-agent/ciao-cnci-agent %{buildroot}%{_bindir}
install -D ./ciao-cert/ciao-cert %{buildroot}%{_bindir}
install -D ./networking/ciao-cnci-agent/scripts/ciao-cnci-agent.service %{buildroot}%{_prefix}/lib/systemd/system/


%check
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost
export GOROOT="/usr/lib/golang"
export GOPATH="%{buildroot}/usr/lib/golang:$(pwd)"
for dir in ciao-cli ciao-controller ciao-launcher ciao-scheduler networking/ciao-cnci-agent payloads ciao-cert;
do
    pushd $dir
    go test ./ || :
    popd
done

%files
%defattr(-,root,root,-)

%files bin
/usr/bin/ciao-cli
/usr/bin/ciao-cert
/usr/bin/ciao-controller
/usr/bin/ciao-launcher
/usr/bin/ciao-scheduler

%files config
/usr/lib/tmpfiles.d/ciao.conf

%files cnci-agent
/usr/bin/ciao-cnci-agent
/usr/lib/systemd/system/ciao-cnci-agent.service
