%define major 6
%define libname %mklibname KPim6Mime
%define devname %mklibname KPim6Mime -d

#define git 20240217
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e 's,/,-,g')

Name: plasma6-kmime
Version:	24.08.2
%define is_beta %(if test `echo %{version} |cut -d. -f3` -ge 70; then echo -n 1; else echo -n 0; fi)
%if %{is_beta}
%define ftpdir unstable
%else
%define ftpdir stable
%endif
Release:	%{?git:0.%{git}.}1
%if 0%{?git:1}
Source0: https://invent.kde.org/pim/kmime/-/archive/%{gitbranch}/kmime-%{gitbranchd}.tar.bz2
%else
Source0: http://download.kde.org/%{ftpdir}/release-service/%{version}/src/kmime-%{version}.tar.xz
%endif
Summary: KDE library for handling MIME types
URL: https://kde.org/
License: GPL
Group: System/Libraries
Requires: %{libname} = %{EVRD}
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF6Codecs)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: boost-devel
# For QCH format docs
BuildRequires: doxygen
BuildRequires: qt6-qttools-assistant

%description
KDE library for handling MIME types

%package -n %{libname}
Summary: KDE library for handling MIME types
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
KDE library for handling MIME types

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%autosetup -p1 -n kmime-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja -C build

%install
%ninja_install -C build

%find_lang libkmime6 --with-qt

%files -f libkmime6.lang
%{_datadir}/qlogging-categories6/kmime.categories

%files -n %{libname}
%{_libdir}/*.so*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/cmake/*
