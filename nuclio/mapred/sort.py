import os
import pika
import json

# command to run this using config file 'function.yaml' (metadata.namespace in config file seems to be broken?!?)
"""
 nuctl deploy sort -p sort.py -f mapper.yaml \
	 	--namespace nuclio \
 		--registry $(minikube ip):5000 --run-registry localhost:5000 
"""


def entry_point(context, event):
    context.logger.info_with('Got invoked', trigger_kind=event.trigger.kind, event_body=event.body)
	# use the logger, outputting the event body
    if event.trigger.kind == "rabbitMq":
        # channel = context.user_data.channel
        # channel.basic_publish(exchange='',
        #             routing_key='goodbye',
        #             body=event.body)
        # debug log
        f = open("/tmp/messages.txt","a+")
        f.write("fields: " + json.dumps(event.fields) + "\n")
        f.write("id: " + str(event.id) + "\n")
        f.write("method: " + event.method + "\n")
        f.write("path: " + event.path + "\n")
        f.write("body: " + event.body + "\n")
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
    pass
    # credentials = pika.PlainCredentials('nuclio', 'nuclio')
    # parameters = pika.ConnectionParameters(host='10.32.128.199', port=5672, credentials=credentials)
    # connection = pika.BlockingConnection(parameters)
    # channel = connection.channel()
    # channel.queue_declare(queue='goodbye')
    
    # setattr(context.user_data, 'channel', channel)
    # setattr(context.user_data, 'exchange_name', exchange_name)
    # setattr(context.user_data, 'routing_key', routing_key)