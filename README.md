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

By default this driver is disabled, because it's needed only by
the software that uses OpenCL and in theory you may want to use
other OpenCL drivers like ROCm or Clover. You will need to explicitly
run the `amdgporun` wrapper script. Eg.

```
$ amdgporun clinfo
$ amdgporun clpeak
$ amdgporun blender
$ amdgporun darktable-cltest
$ amdgporun darktable
```

If you want to enable it by default, you will need to execute two
additional commands:

```
$ echo /usr/lib64/amdgpu-pro-opencl | sudo tee /etc/ld.so.conf.d/amdgpu-pro-opencl-x86_64.conf
$ sudo ldconfig
```

Once this is done, you can execute your OpenCL-needing applications
normally.
