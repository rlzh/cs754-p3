import pika

credentials = pika.PlainCredentials('nuclio', 'nuclio')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.32.128.199', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='map_exchange', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='map_exchange', queue=queue_name, routing_key='tasks.map')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()