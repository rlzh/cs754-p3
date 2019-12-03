#!/usr/bin/env python
import pika
import sys
import argparse
import settings

credentials = pika.PlainCredentials(settings.RMQ_USER_VALUE, settings.RMQ_PASS_VALUE)
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RMQ_HOST_VALUE, 
        port=settings.RMQ_PORT_VALUE, 
        credentials=credentials
        )
    )
channel = connection.channel()
channel.exchange_declare(exchange=settings.EXCHANGE_NAME_VALUE,
                         exchange_type='topic')
message = ' '.join(sys.argv[1:]) or 'Hello World!'

channel.basic_publish(exchange=settings.EXCHANGE_NAME_VALUE,
                      routing_key='tasks.reduce.0',
                      body=message)

print(" [x] Sent %r" % (message))
connection.close()