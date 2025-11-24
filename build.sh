#!/usr/bin/env bash
set -e
mkdir -p ~/rpkg/
spectool -gS opencl-amd.spec
rpkg local --outdir ~/rpkg/
