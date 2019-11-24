import os
import subprocess
import yaml
import configparser

# current_dir = os.getcwd()
# args = ["cp", current_dir + "/test.py", current_dir+"/copy_test.py"]#, ">", current_dir+"/copy_test.py"]

# print(" ".join(args))
# proc = subprocess.Popen(args)
# proc.wait()

# args = ["rm", current_dir+"/copy_test.py"]#, ">", current_dir+"/copy_test.py"]
# print(" ".join(args))
# proc = subprocess.Popen(args)
# proc.wait()

# env_vars = [{"VAR_1": 1}, {"VAR_2": 2}]

# current_dir = os.getcwd()
# config_copy_path = '{}/{}_config.yaml'.format(current_dir, 'test')
# cp_args = [
#     'cp', 
#     '{}/{}'.format(current_dir, 'mapper_config.yaml'), 
#     config_copy_path
# ]
# # create copy of template
# proc = subprocess.Popen(cp_args)
# proc.wait()

# # set config values
# with open(config_copy_path) as file:
#     config_file = yaml.load(file, Loader=yaml.FullLoader)

# spec = config_file['spec']
# env = spec['env']
# if env == None:
#     env = []
#     spec['env'] = env
# for var in env_vars:
#     new_var = {}
#     name = next(iter(var))
#     new_var['name'] = name
#     new_var['value'] = var[name]
#     env.append(new_var)


# with open(config_copy_path, "w") as file:
#     yaml.dump(config_file, file)

