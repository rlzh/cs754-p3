import argparse
import settings
from model import Function, DeployInfo


def create_map_function(function_id, registry, run_registry=None):
    function_name = "map-{}".format(function_id)
    deploy_info = create_deploy_info(
        settings.MAP_PATH, 
        settings.MAP_CONFIG_TEMPLATE_PATH, 
        registry,
        run_registry
    )
    # create function
    function = Function(function_name, deploy_info, debug=settings.DEBUG)

    # load config data
    config_data = function.get_config_data()
    spec = config_data['spec']

    # update env vars
    update_env_var(spec['env'], name=settings.RMQ_HOST_KEY, value=settings.RMQ_HOST_VALUE)
    update_env_var(spec['env'], name=settings.RMQ_PORT_KEY, value=settings.RMQ_PORT_VALUE)
    update_env_var(spec['env'], name=settings.RMQ_USER_KEY, value=settings.RMQ_USER_VALUE)
    update_env_var(spec['env'], name=settings.RMQ_PASS_KEY, value=settings.RMQ_PASS_VALUE)
    update_env_var(spec['env'], name=settings.NUM_REDUCERS_KEY, value=settings.NUM_REDUCERS_VALUE)
    update_env_var(spec['env'], name=settings.REDUCE_TOPIC_PREFIX_KEY, value=settings.REDUCE_TOPIC_PREFIX_VALUE)
    update_env_var(spec['env'], name=settings.EXCHANGE_NAME_KEY, value=settings.EXCHANGE_NAME_VALUE)

    # update rmq trigger info
    update_rmq_trigger(
        spec['triggers'], 
        settings.RMQ_URL_VALUE, 
        settings.EXCHANGE_NAME_VALUE, 
        ["{}{}".format(settings.MAP_TOPIC_PREFIX_VALUE, function_id)]
    )

    # update http trigger
    update_http_trigger(
        spec['triggers'],
        settings.MAP_PORT_START + function_id,
    )

    # apply config changes
    function.apply_config(config_data)
    return function

def create_reduce_function(function_id, registry, run_registry=None):
    function_name = "red-{}".format(function_id)
    deploy_info = create_deploy_info(
        settings.REDUCE_PATH, 
        settings.REDUCE_CONFIG_TEMPLATE_PATH, 
        registry,
        run_registry
    )
    # create function
    function = Function(function_name, deploy_info, debug=settings.DEBUG)

    # load config data
    config_data = function.get_config_data()
    spec = config_data['spec']

    # update rmq trigger info
    update_rmq_trigger(
        spec['triggers'], 
        settings.RMQ_URL_VALUE, 
        settings.EXCHANGE_NAME_VALUE, 
        ["{}{}".format(settings.REDUCE_TOPIC_PREFIX_VALUE, function_id)]
    )

    # update http trigger
    update_http_trigger(
        spec['triggers'],
        settings.REDUCE_PORT_START + function_id,
    )

    # apply config changes
    function.apply_config(config_data)
    return function

def create_deploy_info(function_path, config_template_path, registry, run_registry=None):
    return DeployInfo(
        function_path=function_path, 
        config_template_path=config_template_path, 
        registry=registry,
        run_registry=run_registry
    )
    
def update_http_trigger(triggers, port, target_name=None):
    if target_name == None:
        for trigger_name in triggers:
            trigger_data = triggers[trigger_name]
            if trigger_data['kind'] == 'http':
                update_http_trigger(triggers, port, target_name=trigger_name)
    else:
        if target_name not in triggers:
            # trigger not existing in config -> create new
            triggers[target_name] = {
                'kind': 'http',
                'maxWorkers': 100,
                'attributes': {},
            }
        # update trigger values
        trigger_data = triggers[target_name]
        trigger_data['attributes']['port'] = port

def update_rmq_trigger(triggers, url, exchange_name, topics, target_name=None):
    if target_name == None:
        for trigger_name in triggers:
            trigger_data = triggers[trigger_name]
            if trigger_data['kind'] == 'rabbit-mq':
                update_rmq_trigger(triggers, url, exchange_name, topics, target_name=trigger_name)
    else:
        if target_name not in triggers:
            # trigger not existing in config -> create new
            triggers[target_name] = {
                'kind': 'rabbit-mq',
                'maxWorkers': 100,
                'attributes': {},
            }
        # update trigger values
        trigger_data = triggers[target_name]
        trigger_data['url'] = url
        trigger_data['attributes']['topics'] = topics
        trigger_data['attributes']['exchangeName'] = exchange_name


def update_env_var(env_vars, name, value):
    for var in env_vars:
        if var['name'] == name:
            var['value'] = value
            return
    env_vars.append({'name': name, 'value': value})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mappers', '-m', type=int, default=1)
    parser.add_argument('--reducers', '-r', type=int, default=1)
    parser.add_argument('--registry', '-reg', type=str, default="$(minikube ip):5000")
    parser.add_argument('--run-registry', '-runreg', type=str, default=None)

    args = parser.parse_args()
    print(str(args) + "\n\n")

    # update settings
    settings.NUM_REDUCERS = args.reducers

    # setup
    mappers = [None] * args.mappers
    for i in range(args.mappers):
        mappers[i] = create_map_function(function_id=i, registry=args.registry, run_registry=args.run_registry)
    reducers = [None] * args.reducers
    for i in range(args.reducers):
        reducers[i] = create_reduce_function(function_id=i, registry=args.registry, run_registry=args.run_registry)

    # deploy
    for mapper in mappers:
        mapper.deploy()
    for reducer in reducers:
        reducer.deploy()

    # cleanup
    for mapper in mappers:
        mapper.cleanup()

