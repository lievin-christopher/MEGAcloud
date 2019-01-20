#!/bin/python3
import compte as c
import config
from Crypto.Hash import SHA256
import mega as m
from getpass import getpass
from logger import Logger
import argparse
from compte import Compte
import readline
import os

class Main:

    def __init__(self,conf_file,daemon=False,log_file="mega_activity.log"):
        print("Begin Initialisation ...")
        self.logger = Logger(log_file)
        self.conf_file = conf_file
        self.conf = config.read_conf(conf_file)
        self.mega = m.Mega(self.conf["mega"],self.logger)
        self.comptes = []
        for compte in self.conf["comptes"]:
            self.comptes.append(c.Compte(compte))
        passwd = SHA256.new(getpass("Enter MasterPassword : ").encode('utf-8')).hexdigest()[:32].encode('utf-8')
        if daemon:
            print("Initialisation Success")
            for compte in self.comptes:
                self.mega._do_default_(compte,compte.decrypt_passwd(passwd,True))
            return
        for compte in self.comptes:
            self.mega.login(compte,compte.decrypt_passwd(passwd,True))
            self.mega.logout()
        print("Initialisation Success")
        
    def _save_conf(self):
        self.conf["mega"] = config.json.loads(self.mega.__repr__())
        self.conf["comptes"] = config.json.loads(self.comptes.__repr__())
        config.write_conf(self.conf,self.conf_file)
        self.mega.logout()

    def _get_account_by_name(self,name):
        for compte in self.comptes:
            if compte.name == name:
                return compte
        print("Error account not found")
        self.logger.info("Error account not found")
        return None

    def add_account(self,name=None,email=None,passwd=None):
        if email == None:
            email = input("Account email : ")
        if passwd == None:
            passwd = getpass("Account password : ")
        if name == None:
            name = input("Give a name to this account : ")
        while self._get_account_by_name(name) != None:
            name = input('Error account name already exist, give another name : ')
        acc_tmp = Compte({"name":name,"email":email,"passwd":passwd})
        acc_tmp.encrypt_passwd()
        self.comptes.append(acc_tmp)
        print("Success to add an account")
        self.logger.info("Success to add an account")

    def del_account(self,account_name):
        try:
            self.comptes.remove(self._get_account_by_name(account_name))
            print("Success to delete an account")
            self.logger.info("Success to delete an account")
        except Exception as ex:
            print("Error account not found")
            self.logger.info("Error account not found")

parser = argparse.ArgumentParser(prog='MEGAcloud')
parser.add_argument('-a/--add_account', nargs=3, metavar=("name","email","password"), help='Add account in configuration file')
parser.add_argument('-c/--config_file', metavar="config.json", default=os.environ['HOME']+"/.config/megacloud/sync.conf.json", help='A json configuration file')
parser.add_argument('-d/--daemon', action='store_true', help='Run sync and mount on all accounts')
parser.add_argument('-e/--exec', nargs='+', metavar=("name","command"), help='Exec a command on an account')
parser.add_argument('-l/--log_file', metavar="logfile.log", default="mega_activity.log", help='A log file')
parser.add_argument('-r/--remove_account', metavar="name", help='Remove account in configuration file')
parser.add_argument('--version', action='version', version='%(prog)s 0.2')

args = vars(parser.parse_args())
m = Main(args['c/__config_file'],args['d/__daemon'],args['l/__log_file'])
import atexit
atexit.register(m._save_conf)
if args['a/__add_account']:
    print(args['a/__add_account'])
    m.add_account(args['a/__add_account'][0],args['a/__add_account'][1],args['a/__add_account'][2])
if args['e/__exec']:
    m.mega.commands(m._get_account_by_name(args['e/__exec'][0]),args['e/__exec'][1:])
if args['r/__remove_account']:
    m.del_account(args['r/__remove_account'])
if not args['a/__add_account'] and not args['e/__exec'] and not args['r/__remove_account']:
    last_account = ""
    while True:
        try:
            args = input("$ ").split()
            if m._get_account_by_name(args[0]) != last_account:
                m.mega.logout()
                last_account = m._get_account_by_name(args[0])
                m.mega.login(last_account)
            m.mega.commands(last_account,args[1:],False)
        except EOFError:
            print("quit")
            break
        except KeyboardInterrupt:
        	break