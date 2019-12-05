import os
from dotenv import load_dotenv
load_dotenv()

current_dir = os.path.dirname(os.path.realpath(__file__))

# Host 
HOST = os.getenv("HOST", None)

if HOST == None:
    print("Error: HOST set to 'localhost'. Please create .env file in nuclio/ directory and set proper HOST value! " + ("*" * 10))
    

# Rabbit MQ settings
RMQ_HOST_KEY = "RMQ_HOST"
RMQ_HOST_VALUE = os.getenv(RMQ_HOST_KEY, HOST)
RMQ_PORT_KEY = "RMQ_PORT"
RMQ_PORT_VALUE = os.getenv(RMQ_PORT_KEY, "5672")
RMQ_USER_KEY = "RMQ_USER"
RMQ_USER_VALUE = os.getenv(RMQ_USER_KEY, "nuclio")
RMQ_PASS_KEY = "RMQ_PASS"
RMQ_PASS_VALUE = os.getenv(RMQ_PASS_KEY, "nuclio")
RMQ_URL_KEY = "RMQ_URL"
RMQ_URL_VALUE = os.getenv(RMQ_URL_KEY, "amqp://{}:{}@{}:{}".format(RMQ_USER_VALUE, RMQ_PASS_VALUE, RMQ_HOST_VALUE, RMQ_PORT_VALUE))
EXCHANGE_NAME_KEY = "EXCHANGE_NAME"
EXCHANGE_NAME_VALUE = os.getenv(EXCHANGE_NAME_KEY, "mapred_exchange")
MAP_TOPIC_PREFIX_KEY = "MAP_TOPIC_PREFIX"
MAP_TOPIC_PREFIX_VALUE = os.getenv(MAP_TOPIC_PREFIX_KEY, "tasks.map.")
REDUCE_TOPIC_PREFIX_KEY = "REDUCE_TOPIC_PREFIX"
REDUCE_TOPIC_PREFIX_VALUE = os.getenv(REDUCE_TOPIC_PREFIX_KEY,"tasks.reduce.")
DONE_TOPIC_KEY = "DONE_TOPIC"
DONE_TOPIC_VALUE = os.getenv(DONE_TOPIC_KEY,"tasks.done")
# SORT_TOPIC_PREFIX_VALUE = os.getenv("SORT_TOPIC_PREFIX", "tasks.sort.")

# HDFS
HDFS_HOST_KEY = "HDFS_HOST"
HDFS_HOST_VALUE = os.getenv(HDFS_HOST_KEY, HOST)
HDFS_OUTPUT_DIR_KEY = "HDFS_OUT_DIR"
HDFS_OUTPUT_DIR_VALUE = os.getenv(HDFS_OUTPUT_DIR_KEY, "/")
HDFS_USER_KEY = "HDFS_USER"
HDFS_USER_VALUE = os.getenv(HDFS_USER_KEY, "ubuntu")
HDFS_CHUNK_COUNT_KEY = "HDFS_CHUNK_COUNT"
HDFS_CHUNK_COUNT_VALUE = 0

# File path settings
MAP_CONFIG_TEMPLATE_PATH = "{}/config/map_config.yaml".format(current_dir)
REDUCE_CONFIG_TEMPLATE_PATH = "{}/config/reduce_config.yaml".format(current_dir)
MAP_PATH = "{}/mapred/map.py".format(current_dir)
REDUCE_PATH = "{}/mapred/reduce.py".format(current_dir)
# SORT_PATH = "{}/sort.py".format(current_dir)

DEBUG = True

# Mapreduce settings
NUM_REDUCERS_KEY = "NUM_REDUCERS"
NUM_REDUCERS_VALUE = 1
NUM_MAPPERS_KEY = "NUM_MAPPERS"
NUM_MAPPERS_VALUE = 1

# Nuclio settings
MAP_PORT_START = 30100
REDUCE_PORT_START = 31000
