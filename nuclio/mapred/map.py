import os
import pika
import json
import time
import string
from hdfs import InsecureClient

# command to deploy this function  (metadata.namespace in config file seems to be broken?!?)
"""
for minikube:
nuctl deploy map -p map.py -f ./config/map_config.yaml --namespace nuclio --registry $(minikube ip):5000 --run-registry localhost:5000 

for k8s:
nuctl deploy map -p map.py -f ./config/map_config.yaml --namespace nuclio --registry docker.io/<docker_username>
"""

def to_reducer(channel, message):
    # publish to appropriate reducer queue
    num_reducers = int(os.environ.get('NUM_REDUCERS'))
    reducer_id = hash(message) % num_reducers
    reduce_topic = "{}{}".format(os.environ.get('REDUCE_TOPIC_PREFIX'), reducer_id)
    channel.basic_publish(
        exchange=os.environ.get('EXCHANGE_NAME'),
        routing_key=reduce_topic,
        body=message
    )

def send_completion(channel):
    # publish completion message to all reduce queues
    num_reducers = int(os.environ.get('NUM_REDUCERS'))
    for i in range(num_reducers):
        reduce_topic = "{}{}".format(os.environ.get('REDUCE_TOPIC_PREFIX'), i)
        channel.basic_publish(
            exchange=os.environ.get('EXCHANGE_NAME'),
            routing_key=reduce_topic,
            body=json.dumps({})
        )

def clean(word):
    return word.strip().lower().translate(str.maketrans('', '', string.punctuation))

def entry_point(context, event):
    context.logger.info_with('Got invoked', trigger_kind=event.trigger.kind)
	# use the logger, outputting the event body
    if event.trigger.kind == "rabbitMq":
        # get rabbitmq channel
        channel = context.user_data.channel

        # get hdfs client
        hdfs_client = context.user_data.hdfs_client

        # load data
        data = json.loads(event.body.decode("utf-8"))

        # get path
        hdfs_path = data["hdfs_path"]
        
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
                        to_reducer(channel, json.dumps({"key": cleaned, "value": 1}))
        
        # write completion message to all reduce queues
        send_completion(channel)

        # # debug log
        # f = open("/tmp/messages.txt","a+")
        # f.write(hdfs_path)
        # f.write("*"*10)
        # f.close()
        # return ""
    # else:
        # debug http GET check
        # messages = []
        # f = open("/tmp/messages.txt","r+")
        # lines = f.readlines()
        # for l in lines:
        #     messages.append(l)
        # return "".join(messages)


def init_context(context):
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
    channel.exchange_declare(exchange=exchange_name,
                         exchange_type='topic')   
    setattr(context.user_data, 'channel', channel)

    # init HDFS
    hdfs_host = os.environ.get('HDFS_HOST')
    hdfs_client = InsecureClient('http://{}:9870'.format(hdfs_host))
    setattr(context.user_data, 'hdfs_client', hdfs_client)


# def fib(n):
# 	if n == 0:
# 		return 0
# 	elif n == 1:
# 		return 1
	
# 	return fib(n-1) + fib(n-2)