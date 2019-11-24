#!/usr/bin/env python
import pika
import sys
import argparse

credentials = pika.PlainCredentials('nuclio', 'nuclio')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.32.128.199', port=5672, credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='mapred_exchange',
                         exchange_type='topic')
message = ' '.join(sys.argv[1:]) or 'Hello World!'

channel.basic_publish(exchange='mapred_exchange',
                      routing_key='tasks.map',
                      body=message)

print(" [x] Sent %r" % (message))
connection.close()