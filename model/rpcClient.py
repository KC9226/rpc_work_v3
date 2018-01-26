# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZF

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pika
import re
import uuid
import random
import time
from conf import settings
from libs import loglib


class RpcClient(object):
    """
    定义一个RpcClient类
    """

    def __init__(self):
        """
        构造方法
        :return:
        """
        self._corr_id = None
        self._log = loglib.mylog(settings.CLIENT_LOG)
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RBMQ_HOST))  # 创建连接
        self._channel = self._connection.channel()  # 创建channel
        self._channel.exchange_declare(exchange=settings.EXCHANGE,
                                       type=settings.Q_TYPE)  # 定义exchange
        self._channel.queue_declare(queue=settings.QUEUE, exclusive=True)  # exclusive=True会在使用此queue的消费者断开后,自动将queue删除
        # result = self._channel.queue_declare(exclusive=True)
        self._callback_queue = None  # 定义接收返回的队列

        # self._channel.basic_consume(self.on_response, no_ack=True,
                                    # queue=self._callback_queue)  # 调用消费方法，接收消息

    def on_response(self, ch, method, props, body):
        """
        回调函数，收到数据后将会自动调用该方法，处理接收到的请求
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        if self._corr_id == props.correlation_id:  # 判断收到的相应是否是我刚才发送请求的响应
            print(str(body, 'utf-8'))

    def cmd_check_task(self, cmd):

        tmp = cmd.split()
        q_name = tmp[1]
        self._channel.basic_consume(self.on_response, no_ack=True, queue=q_name)
        self._connection.process_data_events(0.5)


    def cmd_run(self, cmd):
        """
        模块主入口
        :param cmd: 要远端服务器执行的命令
        :return:
        """
        tmp = cmd.split('"')
        print(tmp)
        cmd_str = tmp[1]
        reip = re.compile(r'(?<![.\d])(?:\d{1,3}\.){3}\d{1,3}(?![.\d])')
        t_list = reip.findall(cmd)  # 匹配命令中的主机IP，若有多个IP都进行匹配，匹配成功生成一个列表
        x = time.time() / 100 * 3
        y = random.uniform(100, 20000)
        z = x // y
        q_queue = str(int(z))
        result1 = self._channel.queue_declare(queue=q_queue, exclusive=True)
        self._callback_queue = result1.method.queue
        self._corr_id = str(uuid.uuid4())  # 生成一个随机字符串
        self._log.info('excute commend %s' % cmd)
        for q in t_list:  # 循环列表中的主机，发送消息
            self._channel.basic_publish(exchange=settings.EXCHANGE,
                                        routing_key=q,
                                        properties=pika.BasicProperties(
                                             delivery_mode=2,
                                             reply_to=self._callback_queue,  # 定义回调队列
                                             correlation_id=self._corr_id,
                                             # 当此队列接收到一个响应的时候它无法辨别出这个响应是属于哪个请求的。correlation_id 就是为了解决这个问题而来的
                                         ),
                                        body=cmd_str)  # 相对队列发送请求
            # self._connection.process_data_events(0.5)  # 接收相应的而数据
        print("task id:%s" % q_queue)

    def help(self):
        msg = '''
        run "df -h" --hosts 192.168.3.55
        '''
        print("命令格式如下：")
        print(msg)
