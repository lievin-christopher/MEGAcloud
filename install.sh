#!/bin/bash
if [[ -d MEGAcloud && -d /usr/local/src/megacloud/sdk && -f /usr/local/src/megacloud/sdk/Makefile ]]
then
    cd /usr/local/src/megacloud/sdk
    make examples/megasimplesync CPPFLAGS=-Wno-deprecated-declarations
    make examples/linux/megafuse 
    sudo ln -s examples/megasimplesync /usr/bin/
    sudo ln -s examples/linux/megafuse /usr/bin/
    exit 0
fi
git clone https://github.com/lievin-christopher/MEGAcloud
cd MEGAcloud
echo "install MEGAcloud"
sudo mkdir /usr/local/src/megacloud
sudo chmod 775 /usr/local/src/megacloud
sudo cp *.py LICENSE /usr/local/src/megacloud
sudo chown -R root:users /usr/local/src/megacloud
sudo ln -s /usr/local/src/megacloud/main.py /usr/local/bin/megacloud
echo "install MEGAcloud config"
mkdir ~/.config/megacloud
cp sync.conf.json ~/.config/megacloud/
cd /usr/local/src/megacloud
git clone https://github.com/meganz/sdk
cd -
cp megafuse/megafuse.cpp /usr/local/src/megacloud/sdk/examples/linux/
cd /usr/local/src/megacloud/sdk
echo "configure MegaSDK"
sh autogen.sh && ./configure --with-fuse --without-freeimage --without-sodium --without-sqlite
if [[ ! -f Makefile ]]
then
    
    sh autogen.sh && ./configure --with-fuse --without-freeimage --without-sodium --without-sqlite
    if [[ ! -f Makefile ]]
    then
        echo """
        Fail to configure MegaSDK
        Please fix there issues and run me again:
        cd /usr/local/src/megacloud/sdk
        sh autogen.sh
        ./configure --with-fuse --without-freeimage --without-sodium --without-sqlite
        """
        exit 1
    fi
fi
make examples/megasimplesync CPPFLAGS=-Wno-deprecated-declarations
make examples/linux/megafuse 
sudo ln -s /usr/local/src/megacloud/sdk/examples/megasimplesync /usr/local/bin/
sudo ln -s /usr/local/src/megacloud/sdk/examples/linux/megafuse /usr/local/bin/