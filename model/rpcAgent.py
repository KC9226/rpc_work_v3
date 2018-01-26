# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZF

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pika
from conf import settings
from libs import loglib


class RpcAgent(object):
    def __init__(self):
        """
        构造方法
        :return: 无
        """
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RBMQ_HOST))  # 创建连接
        self._log = loglib.mylog(settings.AGENT_LOG)
        self._channel = self._connection.channel()  # 创建channel
        self._channel.exchange_declare(exchange=settings.EXCHANGE,
                                       type=settings.Q_TYPE)
        res = self._channel.queue_declare(durable=True)  # 队列持久化
        self._queue_name = res.method.queue

    def run_commend(self, commend):
        """
        运行命令方法
        :param commend: 要执行的命令
        :return: 返回命令执行的结果
        """
        import subprocess
        try:
            p = subprocess.Popen(commend, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            error = p.stderr.read()
            if not error:
                res = p.stdout.read()  # 读取命令执行的结果
            else:
                res = error
            res = str(res, 'utf-8')
        except Exception as e:
            res = e
        return '-----[%s]-----\n%s' % (settings.AGENT_HOST, res)

    def on_request(self, ch, method, props, body):
        """
        回调方法，当收到消息的时候将自动调用这个方法
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        commend = body.decode()
        self._log.info('run commend %s' % body.decode())
        response = self.run_commend(commend)
        print(response)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))  # 发送消息
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 通知消息消费完了

    def run(self):
        """
        agent入口方法
        :return:
        """
        self._channel.queue_bind(exchange=settings.EXCHANGE,
                                 queue=self._queue_name,
                                 routing_key=settings.AGENT_HOST)  # 绑定queue和exchange
        self._channel.basic_consume(self.on_request, queue=self._queue_name)  # 接收消息

        print(" [x] Awaiting RPC requests")
        self._channel.start_consuming()  # 等待接收消息
