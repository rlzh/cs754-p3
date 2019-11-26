import pika
import sys

credentials = pika.PlainCredentials('nuclio', 'nuclio')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='pc799.emulab.net', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='mapred_exchange', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

routing_key = ' '.join(sys.argv[1:]) or '#'
channel.queue_bind(exchange='mapred_exchange', queue=queue_name, routing_key=routing_key)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()