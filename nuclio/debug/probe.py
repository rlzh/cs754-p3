import pika
import sys
import settings

credentials = pika.PlainCredentials('nuclio', 'nuclio')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RMQ_HOST_VALUE, port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange=settings.EXCHANGE_NAME_VALUE, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

routing_key = ' '.join(sys.argv[1:]) or '#'
channel.queue_bind(exchange=settings.EXCHANGE_NAME_VALUE, queue=queue_name, routing_key=routing_key)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()