#!/usr/bin/env python
import pika
import sys
import argparse
import configparser

# credentials = pika.PlainCredentials('nuclio', 'nuclio')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.32.128.199', port=5672, credentials=credentials))
# channel = connection.channel()
# channel.exchange_declare(exchange='map_exchange',
#                          exchange_type='topic')
# message = ' '.join(sys.argv[1:]) or 'Hello World!'

# channel.basic_publish(exchange='map_exchange',
#                       routing_key='tasks.map',
#                       body=message)

# print(" [x] Sent %r" % (message))
# connection.close()


if __name__ == '__main__':
    print(sys.argv)

