# MEGAcloud

## Prerequisites

- python3
- pycrypto
- crypto++
- megacmd

## Installing

    wget https://raw.githubusercontent.com/lievin-christopher/MEGAcloud/master/install.sh
    chmod +x install.sh
    ./install.sh

## Usage

### Prerequisites

> choose a master password to encrypt each MEGA password

### add a MEGA account

    megacloud -a "default" "default@gmail.com" "default_password"
    (master password)
    (master password)

### delete a MEGA account

    megacloud -r "default"
    (master password)

### launch a megacmd command on a MEGA account

    # don't write prefix "mega-" before megacmd command
    megacloud -e "default" (mega-) command_args
    (master password)

### run multiple megacmd commands on multiple MEGA accounts

    megacloud
    (master password)
    default ls
    default du

### sync a MEGA account (with megasimplesync)

    megacloud
    (master password)
    sync Documents/MEGA / True

> add a startup task "megacloud -d" (you must enter your master password)
    
## Authors

* **Christopher Lievin** - *Initial work* - [lievin-christopher](https://github.com/lievin-christopher)

See also the list of [contributors](https://github.com/lievin-christopher/MEGAcloud/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details