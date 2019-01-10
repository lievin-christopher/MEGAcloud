import json

def read_conf(conf_file):
    fd = open(conf_file,"r")
    conf = json.loads(fd.read())
    fd.close()
    return conf

def write_conf(conf,conf_file):
    fd = open(conf_file,"w")
    fd.write(json.dumps(conf))
    fd.close()
