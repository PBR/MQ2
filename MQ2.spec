Name:           MQ2
Version:        0.1.0
Release:        1%{?dist}
Summary:        Process MapQTL output to find QTLs hotspot

License:        GPLv3+
URL:            https://github.com/PBR/pymq2
Source0:        MQ2-0.1.0.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
A python library to process output files from MapQTL.

%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check
%{__python} setup.py test
 
%files
%doc COPYING README.rst
# For noarch packages: sitelib
%{python_sitelib}/*
%{_bindir}/MQ2

%changelog
* Tue Jun 26 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1.0-1
- Initial spec file
