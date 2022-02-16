import os
import time
import logging
import daemon
from daemon import pidfile
import signal
import sys

def do_something():
    logger = logging.getLogger('daemon_test')
    logger.setLevel(logging.INFO)
    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)
    fh = logging.FileHandler('/tmp/eg_daemon.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    while True:
        logger.debug('this is a DEBUG message')
        logger.info('this is a INFO message')
        logger.error('this is a ERROR message')
        time.sleep(5)

def start_daemon():
    with daemon.DaemonContext(
            working_directory='/tmp/lib/eg_daemon',
            umask=0o002,
            pidfile=pidfile.TimeoutPIDLockFile('daemon_test.pid')
    ) as context:
        do_something()

def stop_daemon():
    pidfile_path = '/tmp/lib/eg_daemon/daemon_test.pid'
    pidfile_daemon =  pidfile.TimeoutPIDLockFile(pidfile_path)

    if not pidfile_daemon.is_locked():
        raise Exception("{} is not locked".format(pidfile_path))

    pid = pidfile_daemon.read_pid()
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError as exc:
        raise exc

def restart_daemon(daemon):
    stop_daemon()
    start_daemon()

if __name__ == '__main__':
  if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("start daemon")
            start_daemon()
        elif 'stop' == sys.argv[1]:
            stop_daemon()
        elif 'restart' == sys.argv[1]:
            restart_daemon()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
  else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)


