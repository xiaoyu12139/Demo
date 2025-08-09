#!/bin/bash
build="./build"
if [[ -d ${build} ]]; then
    rm -rf ${build}
fi
mkdir build
cmake -B build -S .
make -C build
# ${build}/${execute}