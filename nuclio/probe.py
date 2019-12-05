import pika
import sys
import settings

credentials = pika.PlainCredentials(settings.RMQ_USER_VALUE, settings.RMQ_PASS_VALUE)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RMQ_HOST_VALUE, port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange=settings.EXCHANGE_NAME_VALUE, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

routing_key = ' '.join(sys.argv[1:]) or '#'
channel.queue_bind(exchange=settings.EXCHANGE_NAME_VALUE, queue=queue_name, routing_key=routing_key)

count = 0

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    global count 
    count += 1
    print("count={}".format(count))
    if count == 100:
        ch.stop_consuming()

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
print(" [*] Done!")