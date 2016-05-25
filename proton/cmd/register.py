import threading
import Queue
import json
from oslo_log import log as logging
from oslo_log._i18n import _LE
from oslo_log._i18n import _LW
from oslo_log._i18n import _LI
from oslo_config import cfg
from requests import get, put, post, delete

LOG = logging.getLogger(__name__)

class MyData:
    pass

RegData = MyData()
RegData.registered = False
RegData.thread_running = False
RegData.service_name = "proton"
RegData.service_type = "unknown"
RegData.port = 2705
RegData.host = '127.0.0.1'
RegData.gluon_port = 2704
RegData.gluon_host = '127.0.0.1'


class RegThread(threading.Thread):
    """
    A worker thread that will periodically try to register with
    the gluon service until it is successful.
    """
    def __init__(self, service_name, service_type, host, port, gluon_host, gluon_port):
        super(RegThread, self).__init__()
        self.input_q = Queue.Queue()
        self.base_url = "http://%s:%d/v1/" % (gluon_host, gluon_port)
        self.my_url = "http://%s:%d" % (host, port)
        self.service_name = service_name
        self.service_type = service_type
        LOG.info("RegThread starting")

    def _make_url(self, x):
        return '%s%s' % (self.base_url, x)

    def proc_reg_msg(self, msg):
        pass

    def proc_timeout(self):
        payload = {'name': self.service_name,
                   'service_type': self.service_type,
                   'url': self.my_url}
        try:
            resp = post(self._make_url('backends'), json=payload)
            if resp.status_code == 201:
                LOG.info(_LI("RegThread: registered with gluon"))
                RegData.registered = True
            if resp.status_code == 409:
                LOG.info(_LI("RegThread: already registered with gluon"))
                RegData.registered = True
        except:
            pass

    def run(self):
        while not RegData.registered:
            try:
                msg = self.input_q.get(True, 3.0)
                LOG.info(_LI("RegThread: received message %s ") % msg)
                self.proc_reg_msg(msg)
            except Queue.Empty:
                LOG.debug("RegThread: Queue timeout")
                self.proc_timeout()
            except ValueError:
                LOG.error(_LE("Error processing reg message"))
                break
        LOG.info(_LI("RegThread exiting"))
        RegData.thread_running = False

def register_with_gluon(**kwargs):
    """
    Kick of thread to register this proton with the gluon service.
    :param kwargs:
    :return:
    """
    if not RegData.registered:
        start_reg_thread(**kwargs)

def start_reg_thread(**kwargs):
    """
    Start the RegThread.  
    """
    for key, value in kwargs.iteritems():
        if key == "service_name":
            RegData.service_name = value
        elif key == "service_type":
            RegData.service_type = value
        elif key == "port":
            RegData.port = value
        elif key == "host":
            RegData.host = value
        elif key == "gluon_port":
            RegData.gluon_port = value
        elif key == "gluon_host":
            RegData.gluon_host = value
    if not RegData.thread_running:
        RegData.reg_thread = RegThread(RegData.service_name,
                                       RegData.service_type,
                                       RegData.host,
                                       RegData.port,
                                       RegData.gluon_host,
                                       RegData.gluon_port)
        RegData.reg_thread.start()
        RegData.thread_running = True