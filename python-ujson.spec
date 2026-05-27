%define module ujson
%bcond tests 1

Name:		python-ujson
Version:	5.12.1
Release:	1
Summary:	Ultra fast JSON encoder and decoder for Python
License:	BSD-3-Clause AND TCL
Group:		Development/Python
URL:		https://github.com/ultrajson/ultrajson
Source0:	https://github.com/ultrajson/ultrajson/archive/%{version}/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildRequires:	double-conversion-devel
BuildRequires:	pkgconfig(python)
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

%prep -a
# Remove bundled double-conversion
rm -vrf src/ujson/deps/

%build -p
export CFLAGS="%{optflags} -fno-strict-aliasing"
export LDFLAGS="%{ldflags} -lpython%{pyver}"
export UJSON_BUILD_DC_INCLUDES="%{_includedir}/double-conversion"
export UJSON_BUILD_DC_LIBS="-ldouble-conversion"
export UJSON_BUILD_NO_STRIP=1
export SETUPTOOLS_SCM_PRETEND_VERSION="%{version}"

%install -a
rm -rvf %{buildroot}%{python_sitearch}/src

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitearch}"
pytest
%endif

%files
%doc README.md
%{python_sitearch}/%{module}.cpython-*.so
%{python_sitearch}/%{module}-%{version}.dist-info
%{python_sitearch}/%{module}-stubs
