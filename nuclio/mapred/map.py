import os
import pika
import time
import string
import sys
import shutil
from hdfs import InsecureClient
import collections 
import pickle
import ujson

# command to deploy this function  (metadata.namespace in config file seems to be broken?!?)
"""
for minikube:
nuctl deploy map -p map.py -f ./config/map_config.yaml --namespace nuclio --registry $(minikube ip):5000 --run-registry localhost:5000 

for k8s:
nuctl deploy map -p map.py -f ./config/map_config.yaml --namespace nuclio --registry docker.io/<docker_username>
"""

def get_rabbitmq_channel():
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
    return channel

def clean(word):
    return word.strip().lower().translate(str.maketrans('', '', string.punctuation))

def entry_point(context, event):
    context.logger.info_with('Got invoked', trigger_kind=event.trigger.kind)
	# use the logger, outputting the event body
    if event.trigger.kind == "rabbitMq":
        # get context data
        hdfs_client = context.user_data.hdfs_client
        red_to_data = context.user_data.red_to_data
        num_reducers = int(os.environ.get('NUM_REDUCERS'))

        # load data
        data = ujson.loads(event.body.decode("utf-8"))
        # get path
        hdfs_path = data["hdfs_path"]
        files = [None] * len(red_to_data)
        is_first = [True] * len(red_to_data)
        for i in range(len(red_to_data)):
            file_path = "{}/reduce-{}.json".format(context.user_data.local_output_path, i)
            files[i] = open(file_path, "w+")
            # files[i].write("[")
        
        # stream file from hdfs
        with hdfs_client.read(hdfs_path, encoding='utf-8', delimiter='\n') as reader:
            for line in reader:
                # split into words
                words = line.split()
                for word in words:
                    # clean word
                    cleaned = clean(word)
                    # if alpha send to queue
                    if cleaned.isalpha():
                        data = (cleaned, 1)
                        reducer_id = hash(cleaned) % num_reducers
                        # red_to_data[reducer_id].append(data)
                        if is_first[reducer_id]:
                            # don't add comma ["word", 1]
                            is_first[reducer_id] = False
                            files[reducer_id].write(ujson.dumps(data))
                        else:
                            # add comma ,["word", 1]
                            files[reducer_id].write(";"+ujson.dumps(data))
        
        print("Done reading!")
        # dump data to appropriate files on hdfs
        for i in range(len(red_to_data)):
            # files[i].write("]")
            files[i].close()
        print("Done writing")
        
        remote_path = hdfs_client.upload(
            hdfs_path=context.user_data.hdfs_output_path, 
            local_path=context.user_data.local_output_path, 
            n_threads=-1, 
        )
        print("Done uploading")
        # publish completion message to done topic
        channel = get_rabbitmq_channel()
        channel.basic_publish(
            exchange=os.environ.get('EXCHANGE_NAME'),
            routing_key=os.environ.get('DONE_TOPIC'),
            body="Map task done! input={}".format(hdfs_path)
        )  
        channel.close()      
    return ""

def init_context(context):
    # init HDFS
    hdfs_host = os.environ.get('HDFS_HOST')
    hdfs_user = os.environ.get("HDFS_USER")
    hdfs_client = InsecureClient('http://{}:9870'.format(hdfs_host), user=hdfs_user)
    # setup hdfs dir for intermediate output
    hdfs_output_path = "/tmp"
    setattr(context.user_data, 'hdfs_client', hdfs_client)
    setattr(context.user_data, 'hdfs_output_path', hdfs_output_path)
     # setup local output dir
    local_output_path = "/map-{}".format(os.environ.get("ID"))
    if os.path.isdir(local_output_path) == False:
        os.mkdir(local_output_path)
    setattr(context.user_data, 'local_output_path', local_output_path)

    # init reducer to file map
    red_to_data = [None] * int(os.environ.get('NUM_REDUCERS'))
    for i in range(len(red_to_data)):
        red_to_data[i] = []
    setattr(context.user_data, 'red_to_data', red_to_data)