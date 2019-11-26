#!/usr/bin/env python
import pika
import sys
import argparse

credentials = pika.PlainCredentials('nuclio', 'nuclio')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.38.194.7', port=5672, credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='mapred_exchange',
                         exchange_type='topic')
message = ' '.join(sys.argv[1:]) or 'Hello World!'

channel.basic_publish(exchange='mapred_exchange',
                      routing_key='tasks.map.0',
                      body=message)

print(" [x] Sent %r" % (message))
connection.close()