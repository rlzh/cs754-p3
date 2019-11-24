import os
import pika
import json
import time

# command to deploy this function (metadata.namespace in config file seems to be broken?!?)
"""
 nuctl deploy map -p map.py -f ./config/function.yaml --namespace nuclio --registry $(minikube ip):5000 --run-registry localhost:5000 
"""


def entry_point(context, event):
    context.logger.info_with('Got invoked', trigger_kind=event.trigger.kind, event_body=event.body)
	# use the logger, outputting the event body
    if event.trigger.kind == "rabbitMq":
        # channel = context.user_data.channel
        # message = event.body
        # channel.basic_publish(exchange='',
        #             routing_key='goodbye',
        #             body=event.body)

        # debug log
        f = open("/tmp/messages.txt","a+")
        f.write("body: " + event.body + "\n")
        f.write("-"*10 + "\n")
        f.close()
        return ""
    else:
        # time.sleep(100)
        # # debug http GET check
        # messages = []
        # f = open("/tmp/messages.txt","r+")
        # lines = f.readlines()
        # for l in lines:
        #     messages.append(l)
        # return "".join(messages)
        return str(fib(40))


def init_context(context):
    pass
    # user_name = os.environ.get('RMQ_USER')
    # password = os.environ.get('RMQ_PASS')
    # rmq_host = os.environ.get('RMQ_HOST')
    # rmq_port = os.environ.get('RMQ_PORT')
    # credentials = pika.PlainCredentials(user_name, password)
    # parameters = pika.ConnectionParameters(host=rmq_host, port=rmq_port, credentials=credentials)
    # connection = pika.BlockingConnection(parameters)
    # channel = connection.channel()
    
    # setattr(context.user_data, 'channel', channel)
    # setattr(context.user_data, 'exchange_name', exchange_name)
    # setattr(context.user_data, 'routing_key', routing_key)


def fib(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	
	return fib(n-1) + fib(n-2)