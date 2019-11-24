import os
from dotenv import load_dotenv
load_dotenv()

current_dir = os.getcwd()

# Rabbit MQ settings
RMQ_HOST = os.getenv('RMQ_HOST', '10.32.128.199')
RMQ_PORT = os.getenv('RMW_PORT', '5672')
RMQ_USER = os.getenv('RMQ_USER', 'nuclio')
RMQ_PASS = os.getenv('RMQ_PASS', 'nuclio')
RMQ_URL = os.getenv('RMQ_URL', 'amqp://{}:{}@{}:{}'.format(RMQ_USER, RMQ_PASS, RMQ_HOST, RMQ_PORT))
EXCHANGE_NAME = os.getenv('EXCHANGE_NAME', 'mapred_exchange')
MAP_TOPIC_PREFIX = os.getenv('MAP_TOPIC_PREFIX', 'tasks.map.')
REDUCE_TOPIC_PREFIX = os.getenv('REDUCE_TOPIC_PREFIX','tasks.reduce.')
SORT_TOPIC_PREFIX = os.getenv('SORT_TOPIC_PREFIX', 'tasks.sort.')

# File path settings
CONFIG_TEMPLATE = '{}/config/template.yaml'.format(current_dir)
MAP_PATH = '{}/map.py'.format(current_dir)
REDUCE_PATH = '{}/reduce.py'.format(current_dir)
SORT_PATH = '{}/sort.py'.format(current_dir)

# Env settings
MAP_ENV = {
    'RMQ_HOST': RMQ_HOST,
    'RMQ_PORT': RMQ_PORT,
    ''
}
REDUCE_ENV = {

}
SORT_ENV = {

}
DEBUG = True
