Summary:	Foreign Function Interface library (cross MinGW32 version)
Summary(pl.UTF-8):	Biblioteka Foreign Function Interface (wersja skrośna MinGW32)
Name:		crossmingw32-libffi
Version:	3.2.1
Release:	1
License:	MIT-like
Group:		Libraries
Source0:	ftp://sourceware.org/pub/libffi/libffi-%{version}.tar.gz
# Source0-md5:	83b89587607e3eb65c70d361f13bab43
URL:		http://sources.redhat.com/libffi/
BuildRequires:	texinfo
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
The libffi library provides a portable, high level programming
interface to various calling conventions. This allows a programmer to
call any function specified by a call interface description at
run-time.

Ffi stands for Foreign Function Interface. A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language. The
libffi library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface. A layer must
exist above libffi that handles type conversions for values passed
between the two languages.

This package contains the cross version for MinGW32.

%description -l pl.UTF-8
Biblioteka libffi dostarcza przenośny, wysokopoziomowy interfejs do
różnych konwencji wywołań funkcji. Pozwala to programiście wywołać
dowolną funkcję podaną przez opis interfejsu wywołania w czasie
działania programu.

FFI to skrót od Foreign Function Interface, czyli interfejsu do obcych
funkcji. Jest to potoczna nazwa interfejsu pozwalającego programowi
napisanemu w jednym języku wywoływać kod napisany w innym języku.
Biblioteka libffi daje tylko najniższą, zależną od maszyny warstwę
pełnego interfejsu. Potrzebne są wyższe warstwy do obsługi konwersji
typów dla wartości przekazywanych pomiędzy różnymi językami.

Ten pakiet zawiera wersję skrośną dla MinGW32.

%package static
Summary:	Static libffi library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libffi (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libffi library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libffi (wersja skrośna MinGW32).

%package dll
Summary:	Foreign Function Interface DLL library for Windows
Summary(pl.UTF-8):	Biblioteka DLL Foreign Function Interface dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
Foreign Function Interface DLL library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL Foreign Function Interface dla Windows.

%prep
%setup -q -n libffi-%{version}

%build
%configure \
	--target=%{target} \
	--host=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT{%{_mandir},%{_infodir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog* LICENSE README
%{_libdir}/libffi.dll.a
%{_libdir}/libffi.la
%{_libdir}/libffi-%{version}
%{_pkgconfigdir}/libffi.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libffi.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libffi-6.dll
