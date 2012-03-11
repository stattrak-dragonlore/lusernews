import os
import sys
import logging

from scgiwsgi import WSGIServer
from app import application

import config

pid = None

def write_pid_file():
    global pid
    pid = os.getpid()
    f = open(config.PidFile, 'w')
    f.write(str(pid) + '\n')
    f.close()

def remove_pid_file():
    if os.getpid() != pid:
        return
    try:
        os.unlink(config.PidFile)
    except OSError:
        pass

try:
    os.chdir(os.path.expanduser(config.HomePath))
    write_pid_file()
    logging.basicConfig(filename=config.LogFile,
                        level=getattr(logging, config.LogLevel),
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()

    WSGIServer(application, logger).run(port=7778)
except KeyboardInterrupt:
    pass

finally:
    remove_pid_file()
