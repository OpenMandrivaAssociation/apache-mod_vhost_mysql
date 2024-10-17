#Module-Specific definitions
%define mod_name mod_vhost_mysql
%define mod_conf A74_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.10
Release:	22
Group:		System/Servers
License:	GPL
URL:		https://fabienne.tc2.utelisys.net/~skinkie/mod_vhost_mysql2/
Source0:	http://fabienne.tc2.utelisys.net/~skinkie/mod_vhost_mysql2/mod_vhost_mysql2-0.10.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	mariadb-devel
BuildRequires:	openssl-devel

%description
This module provides dynamically configured virtual Hosting. using MySQL in
Apache2.

%prep

%setup -q -n %{mod_name}2-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%{_bindir}/apxs `mysql_config --include` -lmysqlclient -c %{mod_name}.c

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%clean

%files
%doc README vh.sql
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.10-20mdv2012.0
+ Revision: 773239
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10-19
+ Revision: 678438
- mass rebuild

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10-18
+ Revision: 645773
- relink against libmysqlclient.so.18
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10-16mdv2011.0
+ Revision: 626505
- rebuilt against mysql-5.5.8 libs

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10-14mdv2011.0
+ Revision: 588084
- rebuild

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 0.10-13mdv2010.1
+ Revision: 537584
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10-12mdv2010.1
+ Revision: 516239
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.10-11mdv2010.0
+ Revision: 406680
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 0.10-10mdv2009.1
+ Revision: 326509
- fix build
- rebuilt against mysql-5.1.30 libs

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10-8mdv2009.0
+ Revision: 235124
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10-7mdv2009.0
+ Revision: 215668
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10-6mdv2008.1
+ Revision: 181986
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 0.10-5mdv2008.1
+ Revision: 170759
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10-4mdv2008.0
+ Revision: 82697
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10-3mdv2007.1
+ Revision: 140773
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.10-2mdv2007.0
+ Revision: 79547
- Import apache-mod_vhost_mysql

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 0.10-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Sat Jul 22 2006 Oden Eriksson <oeriksson@mandriva.com> 0.10-1mdv2007.0
- initial Mandriva package

