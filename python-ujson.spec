%define module ujson
%define oname ultrajson
%bcond_without tests

# NOTE Next release > 5.10.0 should have internal typing stubs available
# NOTE Which means no need to package them separately.

Name:		python-ujson
Version:	5.11.0
Release:	1
Summary:	Ultra fast JSON encoder and decoder for Python
URL:		https://github.com/ultrajson/ultrajson
License:	BSD-3-Clause AND TCL
Group:		Development/Python
Source0:	https://github.com/ultrajson/ultrajson/archive/%{version}/%{module}-%{version}.tar.gz
BuildSystem:	python

BuildRequires:	double-conversion-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	python
BuildRequires:	python%{pyver}dist(black)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif

%description
Ultra fast JSON encoder and decoder for Python

%prep
%autosetup -n %{oname}-%{version} -p1

# remove bundled double-conversion
rm -vrf deps

# remove pip and git badges from readme
sed -i '3,10d;14,17d;' README.md

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export UJSON_BUILD_DC_INCLUDES="%{_includedir}/double-conversion"
export UJSON_BUILD_DC_LIBS="-ldouble-conversion"
export UJSON_BUILD_NO_STRIP=1
export SETUPTOOLS_SCM_PRETEND_VERSION="%{version}"
%py_build

%install
%py_install

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}"
%{__python} -m pytest -v
%endif


%files
%{python_sitearch}/ujson.cpython-*.so
%{python_sitearch}/ujson-%{version}.dist-info
%doc README.md
%license LICENSE.txt
