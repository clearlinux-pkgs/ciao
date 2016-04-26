Name     : ciao
Version  : ea6a2d4c4d419e6d9d0e8e228abc2b16ad29196e
Release  : 1
URL      : https://github.com/01org/ciao
Source0  : https://github.com/01org/ciao/archive/ea6a2d4c4d419e6d9d0e8e228abc2b16ad29196e.tar.gz
Summary  : Cloud Integrated Advanced Orchestrator
Group    : Development/Tools
License  : Apache-2.0

Requires : %{name}-bin
Requires : %{name}-config

BuildRequires : go
BuildRequires : golang-github-Sirupsen-logrus
BuildRequires : golang-github-boltdb-bolt
BuildRequires : golang-github-coreos-go-iptables
BuildRequires : golang-github-davecgh-go-spew
BuildRequires : golang-github-docker-distribution
BuildRequires : golang-github-docker-docker
BuildRequires : golang-github-docker-engine-api
BuildRequires : golang-github-docker-go-connections
BuildRequires : golang-github-docker-go-units
BuildRequires : golang-github-docker-libnetwork
BuildRequires : golang-github-go-yaml-yaml
BuildRequires : golang-github-golang-glog
BuildRequires : golang-github-gorilla-context
BuildRequires : golang-github-gorilla-mux
BuildRequires : golang-github-mattn-go-sqlite3
BuildRequires : golang-github-mitchellh-mapstructure
BuildRequires : golang-github-opencontainers-runc
BuildRequires : golang-github-rackspace-gophercloud
BuildRequires : golang-github-tylerb-graceful
BuildRequires : golang-github-vishvananda-netlink
BuildRequires : golang-googlecode-go-net

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
Requires: %{name}-config

%description bin
bin components for the ciao package.

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
mkdir -p src/github.com/01org
ln -s ../../../ src/github.com/01org/ciao
for dir in ciao-cli ciao-controller ciao-launcher ciao-scheduler networking/cnci_agent payloads ssntp;
do
    pushd $dir
    go build -v -x
    popd
done

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/
install -D ./ciao-cli/ciao-cli               %{buildroot}%{_bindir}
install -D ./ciao-controller/ciao-controller %{buildroot}%{_bindir}
install -D ./ciao-launcher/ciao-launcher     %{buildroot}%{_bindir}
install -D ./ciao-scheduler/ciao-scheduler   %{buildroot}%{_bindir}
install -D ./networking/cnci_agent/cnci_agent %{buildroot}%{_bindir}
install -D ./networking/cnci_agent/scripts/cnci-agent.service %{buildroot}%{_prefix}/lib/systemd/system/


%check
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost
export GOROOT="/usr/lib/golang"
export GOPATH="%{buildroot}/usr/lib/golang:$(pwd)"
go test -v ./... ||:

%files
%defattr(-,root,root,-)

%files bin
%{_bindir}/ciao-cli
%{_bindir}/ciao-controller
%{_bindir}/ciao-launcher
%{_bindir}/ciao-scheduler

%files cnci-agent
%{_bindir}/cnci_agent
%{_prefix}/lib/systemd/system/cnci-agent.service
