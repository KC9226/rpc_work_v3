# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZF

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import rpcClient


if __name__ == '__main__':
    client = rpcClient.RpcClient()
    while True:
        cmd = input(">>>:")
        if len(cmd) == 0:
            continue
        action = cmd.split()[0]
        if hasattr(client, "cmd_%s" % action):
            func = getattr(client, "cmd_%s" % action)
            func(cmd)
        else:
            client.help()
    pass