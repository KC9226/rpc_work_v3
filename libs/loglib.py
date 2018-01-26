# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZF

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging


def mylog(log_file_name, s_flag=True):
    logger = logging.getLogger()
    fh = logging.FileHandler(log_file_name, "a", encoding="UTF-8")
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", '%Y-%m-%d %H:%M:%S')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # root_logger = logging.getLogger()
    logger.addHandler(fh)
    if s_flag:
        logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    return logger


