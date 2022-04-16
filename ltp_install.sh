#!/bin/bash

core_num=$(cat /proc/cpuinfo | grep -c processor)-5
core_num=`expr "$core_num" - 5`

cd /home/ltp-master

# step one
make autotools

# step two
chmod +x configure
./configure

# step three
make -j $core_num
make install
