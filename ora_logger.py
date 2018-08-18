#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'
import logging.config
import os
import yaml
'''
setup logging configuration
'''
log_conf = './CONF/ora_log.cfg'
if not os.path.exists("LOG"):
    os.mkdir('LOG')

if os.path.exists(log_conf):
    with open(log_conf, 'rt') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
else:
    logging.basicConfig(level=logging.INFO)
    print('The logging config file [./CONF/ora_log.cfg] not exist!')

logger = logging.getLogger()