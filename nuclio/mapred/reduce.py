import os
import json
import time

# command to deploy this function (metadata.namespace in config file seems to be broken?!?)
"""
 nuctl deploy reduce -p reduce.py -f ./config/reduce_config.yaml --namespace nuclio --registry $(minikube ip):5000 --run-registry localhost:5000 
"""


def entry_point(context, event):
    context.logger.info_with('Got invoked', trigger_kind=event.trigger.kind, event_body=event.body)
	# use the logger, outputting the event body
    if event.trigger.kind == "rabbitMq":    
        # debug log
        f = open("/tmp/messages.txt","a+")
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
