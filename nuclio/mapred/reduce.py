import os
import json
import time
import pika
import pprint as pp
import ujson
from collections import defaultdict
from hdfs import InsecureClient

# command to deploy this function (metadata.namespace in config file seems to be broken?!?)
"""
 nuctl deploy reduce -p reduce.py -f ./config/reduce_config.yaml --namespace nuclio --registry $(minikube ip):5000 --run-registry localhost:5000 
"""

def is_key_value(x):
    return len(x) != 0

def get_rabbitmq_channel():
     # init RabbitMQ
    user_name = os.environ.get('RMQ_USER')
    password = os.environ.get('RMQ_PASS')
    rmq_host = os.environ.get('RMQ_HOST')
    rmq_port = os.environ.get('RMQ_PORT')
    exchange_name = os.environ.get('EXCHANGE_NAME')
    credentials = pika.PlainCredentials(user_name, password)
    parameters = pika.ConnectionParameters(host=rmq_host, port=rmq_port, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')   
    return channel

def entry_point(context, event):
    # context.logger.info_with("Got invoked", trigger_kind=event.trigger.kind)
	# use the logger, outputting the event body
    key_count = {}
    if event.trigger.kind == "rabbitMq": 
        hdfs_client = context.user_data.hdfs_client
        num_mappers = int(os.environ.get("NUM_MAPPERS"))
        for i in range(num_mappers):
            # load data from hdfs
            file_path = "/tmp/map-{}/reduce-{}.json".format(i, os.environ.get("ID"))
            print("Reading from {}".format(file_path))
            with hdfs_client.read(file_path, encoding='utf-8', delimiter=";") as reader:
                for kv_pair in reader:
                    if len(kv_pair) == 0:
                        continue
                    d = ujson.loads(kv_pair)
                    key_count[d[0]] = 1 + (0 if d[0] not in key_count else key_count[d[0]]) 

        print("Done Reading")
        # write output file to hdfs
        output_path = os.environ.get("REDUCER_OUTPUT_FILENAME")
        with open(output_path, "w+") as f:
            f.write(pp.pformat(key_count))
        remote_path = hdfs_client.upload(
            hdfs_path=output_path, 
            local_path=output_path, 
            n_threads=-1, 
            overwrite=True
        )
        print("Done Writing")
        channel = get_rabbitmq_channel()
        # publish to done topic
        channel.basic_publish(
            exchange=os.environ.get('EXCHANGE_NAME'),
            routing_key=os.environ.get('DONE_TOPIC'),
            body="Reduce task done! output={}".format(output_path)
        )

def init_context(context):
    key_count = defaultdict(int)
    setattr(context.user_data, "key_count", key_count)
    
     # init HDFS
    hdfs_host = os.environ.get("HDFS_HOST")
    hdfs_user = os.environ.get("HDFS_USER")
    output_path =os.environ.get("REDUCER_OUTPUT_FILENAME")
    hdfs_client = InsecureClient("http://{}:9870".format(hdfs_host), user=hdfs_user)

    # delete existing output file
    if hdfs_client.content(output_path, strict=False) != None:
        hdfs_client.delete(output_path)

    setattr(context.user_data, "hdfs_client", hdfs_client)
    
    