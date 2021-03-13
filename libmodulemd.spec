#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	python2		# CPython 2.x module
%bcond_without	tests		# unit tests
#
Summary:	Module metadata manipulation library
Name:		libmodulemd
Version:	2.12.0
Release:	0.1
License:	MIT
Group:		Libraries
Source0:	https://github.com/fedora-modularity/libmodulemd/releases/download/%{name}-%{version}/modulemd-%{version}.tar.xz
# Source0-md5:	e0b77248ee9d786d6d226492805d2cf2
Patch0:		no-docs-for-build.patch
URL:		https://github.com/fedora-modularity/libmodulemd
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	rpm-devel
BuildRequires:	pkgconfig
BuildRequires:	glib2-devel
BuildRequires:	yaml-devel
BuildRequires:	libmagic-devel
%{?with_apidocs:BuildRequires:	gtk-doc}
#Requires:	
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

%files devel
%defattr(644,root,root,755)
%{_libdir}/%{name}.so
%{_includedir}/modulemd-2.0
%{_pkgconfigdir}/modulemd-2.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc %{_gtkdocdir}/modulemd-2.0
%endif
