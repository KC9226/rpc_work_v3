# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZF


import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import rpcAgent

if __name__ == '__main__':
    agent = rpcAgent.RpcAgent()
    agent.run()
