# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZF

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RBMQ_HOST = '192.168.8.8'
QUEUE = 'rpc-que3'
EXCHANGE = 'rpc-ex3'
Q_TYPE = 'direct'
AGENT_HOST = '192.168.8.9'
CLIENT_LOG = 'logs/client.log'
AGENT_LOG = 'logs/agent.log'

