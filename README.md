AMDGPU-PRO OpenCL driver for Fedora
===================================

This package is completely based on the AUR package.
https://aur.archlinux.org/packages/opencl-amd/


Installation
------------

Since we are not allowed to distribute the binary releases, you
will need to build the RPM package yourself.

```
$ sudo dnf -y groupinstall 'RPM Development Tools'
$ ./build.sh
```

You can find rpm in ~/rpkg/


Usage
-----

Do whatever you want

```
$ clinfo
$ clpeak
$ blender
$ darktable-cltest
$ darktable
```
