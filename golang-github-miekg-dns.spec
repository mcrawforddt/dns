# Define backup go macros
%if %{rhel} == 8
%global gopkg %package devel \
Summary:	%{summary} \
BuildArch:  noarch \
%description devel \
%{common_description}
%global goprep(A) %setup -q
%global gopkgfiles %files devel -f devel.file-list
%global gocheck echo "skipping gocheck on rhel8"
%endif

%global debug_package %{nil}
# https://github.com/miekg/dns
%global goipath         github.com/miekg/dns
%global common_description %{expand:
Complete and usable DNS library. All Resource Records are supported, including
the DNSSEC types. It follows a lean and mean philosophy. If there is stuff you
should know as a DNS programmer there isn't a convenience function for it.
Server side and client side programming is supported, i.e. you can build servers
and resolvers with it.}
%global golicenses      COPYRIGHT LICENSE
%global godocs          AUTHORS CONTRIBUTORS README.md

Version:        1.1.62
Release:        1%{?dist}
Summary:        DNS library in Go
%gometa
Name:           %{goname}
License:        BSD-3-Clause
URL:            %{gourl}
Source:         %{gosource}

%description
%{common_description}

%package -n %{goname}-devel
%gopkg

%prep
%goprep -A
%autopatch -p1

%install
for file in $(find . -iname "*.go" \! -iname "*_test.go" \! -iname "main.go" ) ; do
    echo "%%dir %%{gopath}/src/%%{goipath}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{goipath}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{goipath}/$file
    echo "%%{gopath}/src/%%{goipath}/$file" >> devel.file-list
done
sort -u -o devel.file-list devel.file-list

%if %{with check}
%check
%gocheck
%endif

%gopkgfiles

%changelog
