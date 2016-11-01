Name     : ciao
Version  : 58
Release  : 40
URL      : https://github.com/01org/ciao
Source0  : https://github.com/01org/ciao/archive/58.tar.gz
Summary  : Cloud Integrated Advanced Orchestrator
Group    : Development/Tools
License  : Apache-2.0

Requires : ciao-bin
Requires : ciao-config

BuildRequires : go

patch01: 0001-Add-Makefile.patch

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
%patch01 -p1


%build
make %{?_smp_mflags}

%install
%make_install


%check
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost
export GOROOT="/usr/lib/golang"
export GOPATH="%{buildroot}/usr/lib/golang:$(pwd)"
for dir in ciao-cli ciao-controller ciao-launcher ciao-scheduler networking/ciao-cnci-agent payloads ciao-cert;
do
    go test -v github.com/01org/ciao/${dir} || :
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
