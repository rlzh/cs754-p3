import os
import pika
import json
import time

# command to deploy this function  (metadata.namespace in config file seems to be broken?!?)
"""
for minikube:
nuctl deploy map -p map.py -f ./config/map_config.yaml --namespace nuclio --registry $(minikube ip):5000 --run-registry localhost:5000 

for k8s:
nuctl deploy map -p map.py -f ./config/map_config.yaml --namespace nuclio --registry docker.io/<docker_username>
"""


def entry_point(context, event):
    context.logger.info_with('Got invoked', trigger_kind=event.trigger.kind, event_body=event.body)
	# use the logger, outputting the event body
    if event.trigger.kind == "rabbitMq":
        channel = context.user_data.channel
        message = str(event.body)

        # publish to appropriate reducer queue
        num_reducers = int(os.environ.get('NUM_REDUCERS'))
        reducer_id = hash(message) % num_reducers
        reduce_topic = "{}{}".format(os.environ.get('REDUCE_TOPIC_PREFIX'), reducer_id)
        channel.basic_publish(exchange=os.environ.get('EXCHANGE_NAME'),
                    routing_key=reduce_topic,
                    body=message)

        # debug log
        f = open("/tmp/messages.txt","a+")
        f.write("body: " + message + "\n")
        f.write("pushed to: " + "exchange="+ os.environ.get('EXCHANGE_NAME') + " topic="+ reduce_topic + "\n")
        f.write("-"*10 + "\n")
        f.close()
        return ""
    else:
        # debug http GET check
        messages = []
        f = open("/tmp/messages.txt","r+")
        lines = f.readlines()
        for l in lines:
            messages.append(l)
        return "".join(messages)


def init_context(context):
    user_name = os.environ.get('RMQ_USER')
    password = os.environ.get('RMQ_PASS')
    rmq_host = os.environ.get('RMQ_HOST')
    rmq_port = os.environ.get('RMQ_PORT')
    exchange_name = os.environ.get('EXCHANGE_NAME')
    credentials = pika.PlainCredentials(user_name, password)
    parameters = pika.ConnectionParameters(host=rmq_host, port=rmq_port, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name,
                         exchange_type='topic')
    setattr(context.user_data, 'channel', channel)


# def fib(n):
# 	if n == 0:
# 		return 0
# 	elif n == 1:
# 		return 1
	
# 	return fib(n-1) + fib(n-2)