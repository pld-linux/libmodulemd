#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	python2		# CPython 2.x module
%bcond_without	tests		# unit tests
#
Summary:	Module metadata manipulation library
Name:		libmodulemd
Version:	2.12.0
Release:	2
License:	MIT
Group:		Libraries
Source0:	https://github.com/fedora-modularity/libmodulemd/releases/download/libmodulemd-%{version}/modulemd-%{version}.tar.xz
# Source0-md5:	e0b77248ee9d786d6d226492805d2cf2
Patch0:		no-docs-for-build.patch
URL:		https://github.com/fedora-modularity/libmodulemd
BuildRequires:	glib2-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	libmagic-devel
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-devel
BuildRequires:	rpmbuild(macros) >= 1.726
BuildRequires:	yaml-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C Library for manipulating module metadata files.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package apidocs
Summary:	API documentation for %{name} library
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%package -n python-%{name}
Summary:	Python 2 bindings for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python-pygobject3
Requires:	python-six

%description -n python-%{name}
Python 2 bindings for %{name}

%package -n python3-%{name}
Summary:	Python 3 bindings for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python3-pygobject3
Requires:	python3-six

%description -n python3-%{name}
Python 3 bindings for %{name}

%package validator
Summary:	Simple modulemd YAML validator
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description validator
Simple modulemd YAML validator.

%prep
%setup -q -n modulemd-%{version}
%patch0 -p1

%build
%meson build \
%if %{with doc}
	-Dwith_docs=true \
	-Dglib_docpath=%{_gtkdocdir} \
%endif
	%{?with_python2:-Dwith_py2=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/%{name}.so.*.*.*
%ghost %{_libdir}/%{name}.so.2
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/%{name}.so
%{_includedir}/modulemd-2.0
%{_pkgconfigdir}/modulemd-2.0.pc
%{_datadir}/gir-1.0/Modulemd-2.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc %{_gtkdocdir}/modulemd-2.0
%endif

%if %{with python2}
%files -n python-%{name}
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Modulemd.py
%endif

%files -n python3-%{name}
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/Modulemd.py

%files validator
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/modulemd-validator
%{_mandir}/man1/modulemd-validator.1*
