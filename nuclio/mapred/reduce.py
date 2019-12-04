import os
import json
import time
import pprint as pp
from collections import defaultdict
from hdfs import InsecureClient

# command to deploy this function (metadata.namespace in config file seems to be broken?!?)
"""
 nuctl deploy reduce -p reduce.py -f ./config/reduce_config.yaml --namespace nuclio --registry $(minikube ip):5000 --run-registry localhost:5000 
"""

def is_key_value(x):
    return len(x) != 0

def entry_point(context, event):
    context.logger.info_with("Got invoked", trigger_kind=event.trigger.kind)
	# use the logger, outputting the event body
    key_count = context.user_data.key_count
    if event.trigger.kind == "rabbitMq": 
        k_v = json.loads(event.body.decode("utf-8"))
        # check for mapper complete message "{}"
        if is_key_value(k_v):   
            key_count[k_v["key"]] += 1 
        else:
            print("mapper completed!")
            hdfs_client = context.user_data.hdfs_client
            context.user_data.finished_mapper_counts += 1
            num_mappers = int(os.environ.get("NUM_MAPPERS"))
            print("num mappers="+str(num_mappers))
            if context.user_data.finished_mapper_counts == num_mappers:
                output_path =os.environ.get("REDUCER_OUTPUT_FILENAME")
                print("write to hdfs! {}".format(output_path))
                # write to output file on hdfs
                hdfs_client.write(
                    output_path, 
                    data=pp.pformat(dict(key_count)),
                    encoding="utf-8"
                )
    else:
        return "key_count len: {}, finished mappers: {}".format(
            len(key_count),
            context.user_data.finished_mapper_counts
        )

def init_context(context):
    key_count = defaultdict(int)
    finished_mapper_counts = 0
    setattr(context.user_data, "key_count", key_count)
    setattr(context.user_data, "finished_mapper_counts", finished_mapper_counts)
    
     # init HDFS
    hdfs_host = os.environ.get("HDFS_HOST")
    hdfs_user = os.environ.get("HDFS_USER")
    output_path =os.environ.get("REDUCER_OUTPUT_FILENAME")

    hdfs_client = InsecureClient("http://{}:9870".format(hdfs_host), user=hdfs_user)

    # delete existing output file
    if hdfs_client.content(output_path, strict=False) != None:
        hdfs_client.delete(output_path)

    setattr(context.user_data, "hdfs_client", hdfs_client)
    
    