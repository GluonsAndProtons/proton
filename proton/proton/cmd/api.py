#    Copyright 2015, Ericsson AB
#    Copyright 2013 - Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys
import os
from wsgiref import simple_server
from oslo_log._i18n import _LI

from oslo_log import log as logging
from oslo_config import cfg

from gluon.common import service
from gluon.api import app as api_app
from gluon.sync_etcd.thread import start_sync_thread
import proton.cmd.config
from proton.cmd.register import register_with_gluon

from gluon.common.particleGenerator.generator import set_package

LOG = logging.getLogger(__name__)
#
# Set the package name before class generation.
# The generator will look in the models directory of the package for the yaml files.
#
set_package("proton")
#
# Register API Manager for this service.
# Loading these modules will trigger the generation of the API and DB classes
#
from gluon.core.manager import register_api_manager
from proton.cmd.manager import ProtonManager
register_api_manager(ProtonManager())

def main():
    service.prepare_service(sys.argv)

    app = api_app.setup_app()

    # Create the WSGI server and start it
    host, port = cfg.CONF.api.host, cfg.CONF.api.port
    srv = simple_server.make_server(host, port, app)

    LOG.info(_LI('Starting server in PID %s') % os.getpid())
    LOG.debug("Configuration:")
    cfg.CONF.log_opt_values(LOG, logging.DEBUG)

    if host == '0.0.0.0':
        LOG.info(_LI('serving on 0.0.0.0:%(port)s, '
                     'view at http://127.0.0.1:%(port)s') %
                 dict(port=port))
    else:
        LOG.info(_LI('serving on http://%(host)s:%(port)s') %
                 dict(host=host, port=port))
    register_with_gluon(service_name=cfg.CONF.api.service_name,
                        service_type=cfg.CONF.api.service_type,
                        host=cfg.CONF.api.host,
                        port=cfg.CONF.api.port,
                        gluon_host=cfg.CONF.api.gluon_host,
                        gluon_port=cfg.CONF.api.gluon_port)
    start_sync_thread(service_name=cfg.CONF.api.service_name,
                      etcd_host=cfg.CONF.api.etcd_host,
                      etcd_port=cfg.CONF.api.etcd_port)
    srv.serve_forever()
