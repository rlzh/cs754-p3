import os
import json
import time
from collections import defaultdict
from pprint import pprint
from hdfs import InsecureClient

# command to deploy this function (metadata.namespace in config file seems to be broken?!?)
"""
 nuctl deploy reduce -p reduce.py -f ./config/reduce_config.yaml --namespace nuclio --registry $(minikube ip):5000 --run-registry localhost:5000 
"""

def is_key_value(x):
    return len(x) != 0

def write_output():
    pass

def entry_point(context, event):
    context.logger.info_with('Got invoked', trigger_kind=event.trigger.kind, event_body=event.body)
	# use the logger, outputting the event body
    if event.trigger.kind == "rabbitMq": 
        k_v = json.loads(event.body)
        print(k_v)
        if is_key_value(k_v):   
            context.user_data.key_count[k_v["key"]] += 1 
        else:
            context.user_data.finished_mapper_counts += 1

        if context.user_data.finished_mapper_counts == 1:
            print("Writing to HDFS")
            print()
            context.user_data.web_hdfs_client.write(
                os.environ.get('REDUCER_OUTPUT_FILE_NAME'), 
                data=json.dumps(context.user_data.key_count),
                encoding='utf-8'
            )
    else:
        pprint(context.user_data.key_count)

def init_context(context):
    pprint(os.environ)
    web_hdfs_client = InsecureClient('http://10.38.163.87:9870', user='harsh')
    key_count = defaultdict(int)
    finished_mapper_counts = 0
    setattr(context.user_data, 'web_hdfs_client', web_hdfs_client)
    setattr(context.user_data, 'key_count', key_count)
    setattr(context.user_data, 'finished_mapper_counts', finished_mapper_counts)