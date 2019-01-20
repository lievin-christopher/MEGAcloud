from subprocess import Popen, PIPE
import json
import os

class Mega:
    def __init__(self,mega_json,logger):
        for k, v in mega_json.items():
            setattr(self, k, v)
        self.l = logger
        self.logout(False)
        args = [self.cmd_https,"on"]
        self.__run__(args)

    def __repr__(self):
        logger_tmp = self.l
        del self.l
        json.dumps(self, default=lambda x: x.__dict__, indent=4)
        tmp_repr = json.dumps(self.__dict__)
        self.l = logger_tmp
        return tmp_repr

    def __run__(self,args):
        self.l.logger.debug(args)
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()
        if stdout != "":
            self.l.logger.info(stdout)
        if stderr != "":
            self.l.logger.error(stderr)
            return stdout,stderr
        return stdout

    def _do_default_(self,account,passwd):
        for tmp_dir in account.dirs:
            if tmp_dir["action"] == "sync":
                self.sync(account,tmp_dir["local"],tmp_dir["remote"],passwd,False,True)
            if tmp_dir["action"] == "mount":
                self.mount(account,tmp_dir["local"],tmp_dir["remote"],passwd)

    def login(self,account,passwd=None):
        args = [self.cmd_login,account._session]
        if account._session == None:
            if passwd == None:
                passwd = account.decrypt_passwd(account.passwd)
            args = [self.cmd_login,account.email,passwd]
        self.__run__(args)
        args = [self.cmd_session]
        stdout = self.__run__(args)
        account._session = stdout.split(': ')[1]

    def logout(self,keep_session=True):
        args = [self.cmd_transfers]
        if self.__run__(args) != "":
            self.l.logger.warning("Logout when transfers in progress ...")
            print("Warning : Logout when transfers in progress ...")
        args = [self.cmd_logout,"--keep-session"]
        if not keep_session:
            args = [self.cmd_logout]
        self.__run__(args)

    def sync(self,account,local,remote,passwd=None,persistent=False,daemon=False):
        if not os.path.isdir(local):
            os.makedirs(local)
        if persistent:
            app_dir = { "remote": remote, "local": local, "action": "sync" }
            already_exist_dir = False
            for tmp_dir in account.dirs:
                if tmp_dir == app_dir:
                    already_exist_dir = True
            if not already_exist_dir:
                account.dirs.append(app_dir)
        my_env = os.environ.copy()
        args = [self.cmd_sync,local,remote]
        if daemon or persistent:
            if persistent and not passwd:
                 passwd = account.decrypt_passwd(account.passwd)
            my_env["MEGA_EMAIL"] = account.email
            my_env["MEGA_PWD"] = passwd
            args = [self.cmd_sync_daemon,local,remote]
        if not daemon and not persistent:
            self.login(account,passwd)
        self.__run__(args,env=my_env)

    def mount(self,account,local,remote,passwd=None):
            if not os.path.isdir(local):
                os.makedirs(local)
            app_dir = { "remote": remote, "local": local, "action": "sync" }
            already_exist_dir = False
            for tmp_dir in account.dirs:
                if tmp_dir == app_dir:
                    already_exist_dir = True
            if not already_exist_dir:
                account.dirs.append(app_dir)
            my_env = os.environ.copy()
            args = [self.cmd_mount,local,remote]
            if not passwd:
                passwd = account.decrypt_passwd(account.passwd)
            my_env["MEGA_EMAIL"] = account.email
            my_env["MEGA_PWD"] = passwd
            self.__run__(args,env=my_env)

    def commands(self,account,args=None,one_time=True):
        if one_time:
            self.login(account)
        if not args:
            args = input().split()
        if args[0] == "sync":
            if args[3] == True:
                self.sync(account,args[1],args[2],persistent=True)
                return
            self.sync(account,args[1],args[2])
            return
        args[0] = "mega-"+args[0]
        print(self.__run__(args))
        if one_time:
            self.logout()
        