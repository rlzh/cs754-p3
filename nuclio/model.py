import os
import subprocess
import yaml
from subprocess import DEVNULL, STDOUT


class Function():
    def __init__(self, function_name, deploy_info, debug=True):
        self.function_name = function_name
        self.deploy_info = deploy_info
        self.debug = debug

        current_dir = os.path.dirname(os.path.realpath(__file__))
        # set config path in deploy info here!
        self.deploy_info.config_path = '{}/config/{}_config.yaml'.format(current_dir, self.function_name)
        # create copy of template
        cp_args = [
            'cp', 
            self.deploy_info.config_template_path, 
            self.deploy_info.config_path
        ]
        proc = subprocess.Popen(cp_args)
        proc.wait()
        self.is_deployed = False

    def get_config_data(self):
        # load config data
        with open(self.deploy_info.config_path) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def apply_config(self, config_data):
        # update config file
        with open(self.deploy_info.config_path, "w") as file:
            # print(config_data)
            yaml.safe_dump(config_data, file)
    
    def deploy(self):
        self.is_deployed = True
        args = [
            'nuctl', 'deploy', self.function_name, 
            '-p', self.deploy_info.function_path, 
            '-f', self.deploy_info.config_path,
            '--namespace', self.deploy_info.namespace,
            '--registry', self.deploy_info.registry,
        ]
        if self.deploy_info.run_registry != None:
            args.append('--run-registry')
            args.append(self.deploy_info.run_registry)
        self.deploy_proc = subprocess.Popen(args)#, stdout=DEVNULL, stderr=STDOUT)
        # self.deploy_proc.wait()
        return self.deploy_proc

    def cleanup(self):
        # delete copied config file
        os.remove(self.deploy_info.config_path)

        if self.is_deployed == False:
            return

        args = [
            'nuctl', 'delete', 'function', 
            self.function_name, 
            '--namespace', self.deploy_info.namespace,
        ]
        self.deploy_proc = subprocess.Popen(args)#, stdout=DEVNULL, stderr=STDOUT)
        self.deploy_proc.wait()
        self.is_deployed = False
        return self.deploy_proc
        

class DeployInfo():
    def __init__(self, function_path, config_template_path, registry, namespace='nuclio', run_registry=None):
        self.function_path = function_path
        self.config_template_path = config_template_path
        self.config_path = None
        self.namespace = namespace
        self.registry = registry
        self.run_registry = run_registry


