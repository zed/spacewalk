# Smartpm rpm spec file for Solaris

%define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')
%define python_version %(%{__python} -c 'import sys; print sys.version.split(" ")[0]')

%define _prefix /opt/redhat/rhn/solaris/usr
%define _localstatedir /opt/redhat/rhn/solaris/var

Summary: Next generation package handling tool
Name: smartpm
Source0: smartpm-%{version}.tar.gz
Version: 0.1
Release: 0
License: GPLv2
Group: Applications/System
URL: http://www.smartpm.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

##BuildRequires: popt, rpm-devel >= 4.2.1, python-devel
##BuildRequires: autoconf, automake

Requires: python = %{python_version}

%description
Smart Package Manager is a next generation package handling tool.

%prep
%setup

%build
env %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install --root="%{buildroot}" --install-scripts="%{_bindir}"

%{__install} -d -m 0755 %{buildroot}%{_localstatedir}/lib/smart/
%{__cp} -p contrib/solaris/distro-solaris.py %{buildroot}%{_localstatedir}/lib/smart/distro.py
%{__cp} -p contrib/solaris/adminfile %{buildroot}%{_localstatedir}/lib/smart/adminfile
%{__install} -d -m 0755 %{buildroot}%{python_sitearch}/rhn/actions/
%{__mv} %{buildroot}%{python_sitearch}/smart/interfaces/up2date/solarispkgs.py* %{buildroot}%{python_sitearch}/rhn/actions/

# For now, remove unused language files
%{__rm} -r %{buildroot}/opt/redhat/rhn/solaris/share/locale

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc HACKING IDEAS LICENSE README TODO doc/*
%{_bindir}/smart
%{_bindir}/up2date
%{python_sitearch}/smart/
%exclude %{python_sitearch}/smart/interfaces/gtk/
%{_localstatedir}/lib/smart/
%{python_sitearch}/rhn/actions/solarispkgs.py*

%changelog
* Mon Mar 23 2009 Devan Goodwin <dgoodwin@redhat.com> 0.1-0
- Rebuild from Spacewalk git.

* Mon Jun 23 2005 Joel Martin <jmartin@redhat.com> - 4.0.0-6
- Fix Solaris patch db bug

* Mon Jun 15 2005 Joel Martin <jmartin@redhat.com> - 4.0.0-5
- Change to use version file, change spec and package name to smartpm

* Mon May 31 2005 Joel Martin <jmartin@redhat.com> - 4.0.0-2
- Make solarispkgs.py byte compiled 

* Mon May 24 2005 Joel Martin <jmartin@redhat.com> - 4.0.0-1
- Initial package creation for RHN 400 release
