#    Copyright 2015, Ericsson AB
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

from oslo_config import cfg

API_SERVICE_OPTS = [
    cfg.IntOpt('port',
               default=2705,
               help='The port for the proton API server'),
    cfg.StrOpt('host',
               default='127.0.0.1',
               help='The listen IP for the proton API server'),
    cfg.StrOpt('service_name',
               default='net-l3vpn',
               help='Name of the proton service'),
    cfg.StrOpt('service_type',
               default='L3VPN',
               help='Network service type provided by the proton API server'),
    cfg.StrOpt('etcd_host',
               default='127.0.0.1',
               help='etcd host'),
    cfg.IntOpt('etcd_port',
               default=2379,
               help='etcd port'),
    cfg.StrOpt('gluon_host',
               default='127.0.0.1',
               help='etcd host'),
    cfg.IntOpt('gluon_port',
               default=2704,
               help='etcd port'),
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='api',
                         title='Options for the proton-api service')
CONF.register_group(opt_group)
CONF.register_opts(API_SERVICE_OPTS, opt_group)
