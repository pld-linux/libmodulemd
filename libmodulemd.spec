#
# Conditional build:
%bcond_without	apidocs	# API documentation
%bcond_with	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	tests	# unit tests
#
Summary:	Module metadata manipulation library
Summary(pl.UTF-8):	Biblioteka operowania na metadanych modułów
Name:		libmodulemd
Version:	2.15.0
Release:	2
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/fedora-modularity/libmodulemd/releases
Source0:	https://github.com/fedora-modularity/libmodulemd/releases/download/%{version}/modulemd-%{version}.tar.xz
# Source0-md5:	3d231596fad04b1a16ff67257b3145da
Patch0:		no-docs-for-build.patch
URL:		https://github.com/fedora-modularity/libmodulemd
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gobject-introspection-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	meson >= 0.55.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
%if %{with python2}
BuildRequires:	python >= 1:2.5
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-pygobject3
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-pygobject3
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-devel
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yaml-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C Library for manipulating module metadata files.

%description -l pl.UTF-8
Biblioteka C do operowania na metadanych modułów.

%package devel
Summary:	Header files for modulemd library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki modulemd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	rpm-devel
Requires:	yaml-devel

%description devel
Header files for modulemd library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki modulemd.

%package static
Summary:	Static modulemd library
Summary(pl.UTF-8):	Statyczna biblioteka modulemd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static modulemd library.

%description static -l pl.UTF-8
Statyczna biblioteka modulemd.

%package apidocs
Summary:	API documentation for modulemd library
Summary(pl.UTF-8):	Dokumentacja API biblioteki modulemd
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for modulemd library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki modulemd.

%package -n python-%{name}
Summary:	Python 2 bindings for modulemd library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki modulemd
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python-pygobject3
Requires:	python-six

%description -n python-%{name}
Python 2 bindings for modulemd library.

%description -n python-%{name} -l pl.UTF-8
Wiązania Pythona 2 do biblioteki modulemd.

%package -n python3-%{name}
Summary:	Python 3 bindings for module md library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki modulemd
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-pygobject3
Requires:	python3-six

%description -n python3-%{name}
Python 3 bindings for module md library.

%description -n python3-%{name} -l pl.UTF-8
Wiązania Pythona 3 do biblioteki modulemd.

%package validator
Summary:	Simple modulemd YAML validator
Summary(pl.UTF-8):	Prosty walidator YAML-a modulemd
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description validator
Simple modulemd YAML validator.

%description validator -l pl.UTF-8
Prosty walidator YAML-a modulemd.

%prep
%setup -q -n modulemd-%{version}
%patch -P 0 -p1

%build
%meson \
	-Dwith_docs=%{__true_false apidocs} \
	-Dglib_docpath=%{_gtkdocdir} \
	%{?with_python2:-Dwith_py2=true} \
	%{!?with_python3:-Dwith_py2=false}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README.md
%attr(755,root,root) %{_libdir}/libmodulemd.so.*.*.*
%ghost %{_libdir}/libmodulemd.so.2
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmodulemd.so
%{_includedir}/modulemd-2.0
%{_pkgconfigdir}/modulemd-2.0.pc
%{_datadir}/gir-1.0/Modulemd-2.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libmodulemd.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/modulemd-2.0
%endif

%if %{with python2}
%files -n python-%{name}
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Modulemd.py[co]
%endif

%if %{with python3}
%files -n python3-%{name}
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/Modulemd.py
%{py3_sitedir}/gi/overrides/__pycache__/Modulemd.cpython-*.py[co]
%endif

%files validator
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/modulemd-validator
%{_mandir}/man1/modulemd-validator.1*
