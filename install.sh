#!/bin/bash
git clone https://github.com/lievin-christopher/MEGAcloud
cd MEGAcloud
sudo mkdir /usr/src/megacloud
sudo cp *.py LICENSE /usr/src/megacloud/
sudo ln -s /usr/src/megacloud/main.py /usr/bin/megacloud
mkdir ~/.config/megacloud
cp sync.conf.json ~/.config/megacloud/
git clone https://github.com/meganz/sdk
cp megafuse/megafuse.cpp sdk/examples/linux/
cd sdk
sh autogen.sh
./configure --with-fuse --without-freeimage --without-sodium --without-sqlite
make examples/megasimplesync CPPFLAGS=-Wno-deprecated-declarations
make examples/linux/megafuse 
sudo cp examples/megasimplesync /usr/bin/
sudo cp examples/linux/megafuse /usr/bin/
cd .. && rm -rf sdk
cd .. && rm -rf MEGAcloud