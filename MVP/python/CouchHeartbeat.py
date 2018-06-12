"""
 CouchDB heartbeat
 Check database and if not running, restart
 Restarting CouchDB does not always go clear, reboot is better
"""

import os
import requests
from LogUtil import get_logger

class CouchHeartbeat(object):
    """Heartbeat object    """

    logger = None

    def __init__(self):
        """Standard constructor
        Get and hold a Python logger
        """
        self.logger = get_logger('CouchHeartbeat')

    def check(self, port):
        """Ping the database
        Should return the welcome message
        Throws an exception if cannot make a connection to the database

        Args:
            port: port the database is communicating on
        Returns:
            None
        Raises:
            None
        """
        try:
            request = requests.get('http://localhost:' + port)
            if request.json()["couchdb"] == 'Welcome':
                self.logger.info('Port: %s Couch Up' % (port))
        except requests.ConnectionError as error:
            self.logger.warning('Port: %s Couch Down %s' % (port, error))
            restart()

    def restart(self):
        """System restart (reboot)
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        cmd = 'sudo reboot'
        self.logger.warning('System restart: %s' % (cmd))
        os.system(cmd)

def test():
    """Standard test function

    Args:
        None
    Returns:
        None
    Raises:
        None
    """
    heartbeat = CouchHeartbeat()
    heartbeat.check('5984')

if __name__ == "__main__":
    test()

