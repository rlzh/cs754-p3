import os
from dotenv import load_dotenv
load_dotenv()

current_dir = os.getcwd()

# Rabbit MQ settings
RMQ_HOST_KEY = 'RMQ_HOST'
RMQ_HOST_VALUE = os.getenv(RMQ_HOST_KEY, '10.38.194.7')
RMQ_PORT_KEY = 'RMQ_PORT'
RMQ_PORT_VALUE = os.getenv(RMQ_PORT_KEY, '5672')
RMQ_USER_KEY = 'RMQ_USER'
RMQ_USER_VALUE = os.getenv(RMQ_USER_KEY, 'nuclio')
RMQ_PASS_KEY = 'RMQ_PASS'
RMQ_PASS_VALUE = os.getenv(RMQ_PASS_KEY, 'nuclio')
RMQ_URL_KEY = 'RMQ_URL'
RMQ_URL_VALUE = os.getenv(RMQ_URL_KEY, 'amqp://{}:{}@{}:{}'.format(RMQ_USER_VALUE, RMQ_PASS_VALUE, RMQ_HOST_VALUE, RMQ_PORT_VALUE))
EXCHANGE_NAME_KEY = 'EXCHANGE_NAME'
EXCHANGE_NAME_VALUE = os.getenv(EXCHANGE_NAME_KEY, 'mapred_exchange')
MAP_TOPIC_PREFIX_KEY = 'MAP_TOPIC_PREFIX'
MAP_TOPIC_PREFIX_VALUE = os.getenv(MAP_TOPIC_PREFIX_KEY, 'tasks.map.')
REDUCE_TOPIC_PREFIX_KEY = 'REDUCE_TOPIC_PREFIX'
REDUCE_TOPIC_PREFIX_VALUE = os.getenv(REDUCE_TOPIC_PREFIX_KEY,'tasks.reduce.')
# SORT_TOPIC_PREFIX_VALUE = os.getenv('SORT_TOPIC_PREFIX', 'tasks.sort.')

# File path settings
MAP_CONFIG_TEMPLATE_PATH = '{}/config/map_config.yaml'.format(current_dir)
REDUCE_CONFIG_TEMPLATE_PATH = '{}/config/reduce_config.yaml'.format(current_dir)
MAP_PATH = '{}/map.py'.format(current_dir)
REDUCE_PATH = '{}/reduce.py'.format(current_dir)
SORT_PATH = '{}/sort.py'.format(current_dir)

DEBUG = True

# Mapreduce settings
NUM_REDUCERS_KEY = 'NUM_REDUCERS'
NUM_REDUCERS_VALUE = 3

# Nuclio settings
MAP_PORT_START = 30000
REDUCE_PORT_START = 31000


# # spec
# MAP_SPEC = {
#     'env': [
#         {'name': 'RMQ_HOST', 'value': RMQ_HOST}, 
#         {'name': 'RMQ_PORT', 'value': RMQ_PORT},
#         {'name': 'RMQ_USER', 'value': RMQ_USER},
#         {'name': 'RMQ_PASS', 'value': RMQ_PASS},
#         {'name': 'NUM_REDUCERS', 'value': NUM_REDUCERS}
#     ], 
#     'replicas': 1, 
#     'minReplicas': 1, 
#     'maxReplicas': 5,
#     'targetCPU': 10, 
#     'triggers': {
#         'rmqTrigger': {
#             'kind': 'rabbit-mq',
#             'url': 'amqp://nuclio:nuclio@10.32.128.199:5672', 
#             'attributes': {
#                 'topics': ['tasks.#'], 
#                 'exchangeName': EXCHANGE_NAME
#             }
#         }, 
#         'debugTrigger': {
#             'maxWorkers': 4, 
#             'kind': 'http', 
#             'attributes': {
#                 'port': 32001
#             }
#         }
#     }, 
#     'handler': 'map:entry_point', 
#     'build': {
#         'commands': [
#             'apk update', 
#             'apk add py-pip', 
#             'pip install pika'
#         ]
#     }, 
#     'runtime': 'python:2.7'
# }
