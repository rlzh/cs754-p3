import os
import subprocess
import yaml


class Function():
    def __init__(self, function_name, deploy_info, config_info, debug=True):
        self.function_name = function_name
        self.deploy_info = deploy_info
        self.config_info = config_info
        self.is_setup = False
        self.debug = debug

    def setup(self):
        if self.is_setup:
            self.cleanup()
        
        current_dir = os.getcwd()
        # set config path in deploy info here!
        self.deploy_info.config_path = '{}/{}_config.yaml'.format(current_dir, self.function_name)
        # create copy of template
        cp_args = [
            'cp', 
            '{}/{}'.format(current_dir, self.config_info.config_file_template), 
            self.deploy_info.config_path
        ]
        proc = subprocess.Popen(cp_args)
        proc.wait()

        # set config values
        with open(self.deploy_info.config_path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        spec = data['spec']
        
        # set env vars
        env = []
        spec['env'] = env
        for var in self.config_info.env_vars:
            new_var = {}
            name = next(iter(var))
            new_var['name'] = name
            new_var['value'] = var[name]
            env.append(new_var)
        env.append({'name': 'DEBUG', 'value': ('True' if self.debug else 'False')})

        # update handler name
        spec['handler'] = "{}:entry_point".format(self.config_info.module_name)

        # set rmq_url
        rmq_trigger = spec['triggers']['rmqTrigger']
        rmq_trigger['url'] = self.config_info.rmq_url
        
        # set exchange name
        rmq_trigger['attributes']['exchangeName'] = self.config_info.exchange_name
        
        # set topics
        rmq_trigger['attributes']['topics'] = self.config_info.topics

        # update config file
        with open(config_path, "w") as file:
            yaml.dump(data)

        self.is_setup = True
    
    def deploy(self):
        if self.is_setup == False:
            print("Error not setup for deployment!")
            return None
        args = [
            'nuctl', 'deploy', self.function_name, 
            '-p', self.deploy_info.function_path, 
            '-f', self.deploy_info.config_path,
            '--namespace', self.deploy_info.namespace,
            '--registry', self.deploy_info.registry,
        ]
        if self.run_registry != None:
            args.append('--run-registry').append(self.deploy_info.run_registry)
        self.deploy_proc = subprocess.Popen(args)
        return self.deploy_proc

    def cleanup(self):
        # todo: 
        # - delete config file 
        self.is_setup = False
        

class ConfigInfo():
    def __init__(self, module_name, env_vars, rmq_url, exchange_name, topics):
        self.module_name = module_name
        self.env_vars = env_vars
        self.rmq_url = rmq_url
        self.topics = topics
        self.exchange_name = exchange_name

class DeployInfo():
    def __init__(self, function_path, config_file_template, registry, namespace='nuclio', run_registry=None):
        self.function_path = function_path
        self.config_file_template = config_file_template
        self.config_path = None
        self.namespace = namespace
        self.registry = registry
        self.run_registry = run_registry


