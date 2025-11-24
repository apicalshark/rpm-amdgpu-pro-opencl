# This package is inspired by the AUR package for opencl-amd by George Sofianos.
# It has been updated to use the modern ROCm stack from AMD's official repositories.
# https://aur.archlinux.org/packages/opencl-amd

# Important:
# The AMD EULA may forbid redistribution of the resulting binary RPM files.
# Build and use this package for personal use only.
%global __requires_exclude ^(libncursesw\\.so\\.6\\(NCURSESW6_.*\\)\\(64bit\\)|libtinfo\\.so\\.6\\(NCURSES6_TINFO.*\\)\\(64bit\\))$
%global rocm_version 7.1.0
%global rocm_release 1

# RPM flags
%global debug_package %{nil}
%undefine __brp_check_rpaths

Name:           opencl-amd
Version:        %{rocm_version}
Release:        %{rocm_release}%{?dist}
Summary:        ROCm OpenCL and HIP runtime for AMD GPUs

License:        custom:AMD
URL:            https://rocm.docs.amd.com/en/latest/
ExclusiveArch:  x86_64

# Source .deb files from the official AMD ROCm repository
Source0:        https://repo.radeon.com/rocm/apt/7.1/pool/main/a/amd-smi-lib/amd-smi-lib_26.1.0.70100-20~24.04_amd64.deb
Source1:        https://repo.radeon.com/rocm/apt/7.1/pool/main/c/comgr/comgr_3.0.0.70100-20~24.04_amd64.deb
Source2:        https://repo.radeon.com/rocm/apt/7.1/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.70100-20~24.04_amd64.deb
Source3:        https://repo.radeon.com/rocm/apt/7.1/pool/main/h/hsa-rocr/hsa-rocr_1.18.0.70100-20~24.04_amd64.deb
Source4:        https://repo.radeon.com/rocm/apt/7.1/pool/main/h/hsa-rocr-dev/hsa-rocr-dev_1.18.0.70100-20~24.04_amd64.deb
Source5:        https://repo.radeon.com/rocm/apt/7.1/pool/main/h/hip-runtime-amd/hip-runtime-amd_7.1.25424.70100-20~24.04_amd64.deb
Source6:        https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocm-core/rocm-core_7.1.0.70100-20~24.04_amd64.deb
Source7:        https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocminfo/rocminfo_1.0.0.70100-20~24.04_amd64.deb
Source8:        https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocm-opencl/rocm-opencl_2.0.0.70100-20~24.04_amd64.deb
Source9:        https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocm-opencl-dev/rocm-opencl-dev_2.0.0.70100-20~24.04_amd64.deb
Source10:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocm-smi-lib/rocm-smi-lib_7.8.0.70100-20~24.04_amd64.deb
Source11:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocm-device-libs/rocm-device-libs_1.0.0.70100-20~24.04_amd64.deb
Source12:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocprofiler/rocprofiler_2.0.70100.70100-20~24.04_amd64.deb
Source13:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocprofiler-dev/rocprofiler-dev_2.0.70100.70100-20~24.04_amd64.deb
Source14:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocprofiler-plugins/rocprofiler-plugins_2.0.70100.70100-20~24.04_amd64.deb
Source15:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocprofiler-register/rocprofiler-register_0.6.0.70100-20~24.04_amd64.deb
Source16:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocm-dbgapi/rocm-dbgapi_0.77.4.70100-20~24.04_amd64.deb
Source17:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocm-debug-agent/rocm-debug-agent_2.1.0.70100-20~24.04_amd64.deb
Source18:       https://repo.radeon.com/rocm/apt/7.1/pool/main/r/rocm-gdb/rocm-gdb_16.3.70100-20~24.04_amd64.deb

BuildRequires:  binutils
BuildRequires:  patchelf
BuildRequires:  tar
BuildRequires:  xz
Requires:       ncurses-compat-libs
Requires:       ocl-icd
Requires:       libdrm
Requires:       libgcc
Requires:       numactl-libs

%description
ROCm components repackaged from AMD's Ubuntu releases.
This package includes the ROCr runtime, OpenCL runtime, and HIP runtime.
It is intended to work along with the free amdgpu kernel driver stack.

%prep
# Create the build directory but do not unpack any sources automatically
%setup -c -T

# Unpack all the source .deb files
for deb_file in %{sources}; do
    ar x "${deb_file}"
    tar xf data.tar.gz
    rm -f data.tar.gz control.tar.gz debian-binary
done

%build
# No build steps needed as we are repackaging pre-compiled binaries

%install
# Move the extracted 'opt' directory into the buildroot
mv opt %{buildroot}/

# Rename the versioned rocm directory to a generic one
mv %{buildroot}/opt/rocm-%{rocm_version} %{buildroot}/opt/rocm

# Configure OpenCL ICD loader
mkdir -p %{buildroot}%{_sysconfdir}/OpenCL/vendors
echo "libamdocl64.so" > %{buildroot}%{_sysconfdir}/OpenCL/vendors/amdocl64.icd

# Remove invalid RUNPATHs from binaries that cause check-rpaths to fail.
# The linker will find the correct libraries via the ld.so.conf.d file.
patchelf --remove-rpath %{buildroot}/opt/rocm/bin/roccoremerge
patchelf --remove-rpath %{buildroot}/opt/rocm/bin/rocgdb-py_3.12
patchelf --remove-rpath %{buildroot}/opt/rocm/bin/rocgdb-py_3.13

# Configure dynamic linker
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "/opt/rocm/lib" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/opencl-amd.conf
echo "/opt/rocm/hip/lib" >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/opencl-amd.conf

# Add ROCm binaries to the system-wide PATH
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
echo 'export PATH="${PATH}:/opt/rocm/bin:/opt/rocm/hip/bin"' > %{buildroot}%{_sysconfdir}/profile.d/opencl-amd.sh

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
# System configuration files
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/opencl-amd.conf
%config(noreplace) %{_sysconfdir}/OpenCL/vendors/amdocl64.icd
%config(noreplace) %{_sysconfdir}/profile.d/opencl-amd.sh

# Main ROCm installation directories
/opt/rocm/.info/version
/opt/rocm/amdgcn
/opt/rocm/bin/
/opt/rocm/include/
/opt/rocm/lib/
/opt/rocm/libexec/
/opt/rocm/share/

%changelog
* Sun Nov 23 2025 apicalshark - 7.1.0-1
- Updated spec to match opencl-amd AUR package version 7.1.0 with the power of vibe coding
- Switched from single amdgpu-pro tarball to multiple ROCm .deb packages
- Replaced amdgporun script with system-wide ld.so.conf and profile.d files

* Sat Feb 20 2021 optimize-fast - a20.45.1188099-1
- Update to 20.45

* Wed Jun 17 2020 secureworkstation - a20.20.1089974-1
- Update to 20.20

* Tue Mar 10 2020 secureworkstation - a20.10.1048554-2
- Update to 20.10

* Tue Mar 10 2020 secureworkstation - a19.50.967956-1
- Initial release based on amdgpu-pro driver
