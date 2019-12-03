

import deploy
import upload
import settings
import argparse
import asyncio
import pika
import json
import time
import pydoop.hdfs as hdfs
from urllib.parse import urlparse

def invoke_mappers(input_dir, mappers):
    # fetch hdfs file paths
    hdfs_file_paths = []
    rfs = hdfs.hdfs(host=settings.HDFS_HOST_VALUE, port=9000)
    contents = rfs.list_directory(input_dir)
    for content in contents:
        if content['kind'] == 'file':
            hdfs_file_paths.append(urlparse(content["path"]).path)
    
    credentials = pika.PlainCredentials(settings.RMQ_USER_VALUE, settings.RMQ_PASS_VALUE)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RMQ_HOST_VALUE, 
            port=settings.RMQ_PORT_VALUE, 
            credentials=credentials
            )
        )
    channel = connection.channel()
    channel.exchange_declare(exchange=settings.EXCHANGE_NAME_VALUE,
                            exchange_type='topic')

    map_index = 0 
    num_mappers = len(mappers)

    # invoke a mapper for each file
    for hdfs_file in hdfs_file_paths:
        print("Pushing to queue: " + hdfs_file)
        i = map_index % num_mappers
        channel.basic_publish(exchange=settings.EXCHANGE_NAME_VALUE,
                    routing_key='tasks.map.{}'.format(i),
                    body=json.dumps({'hdfs_path': hdfs_file}))
        map_index += 1
    connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # shared args
    parser.add_argument('--mode', '-m', type=str, default=None, help="available modes: upload, run")
    parser.add_argument('--input_dir', '-i', type=str, default=None)
    parser.add_argument('--output_dir', '-o', type=str, default="/")
    # upload args
    parser.add_argument('--chunk_size', '-cs', type=int, default=127)
    # run args
    parser.add_argument('--mappers', '-map', type=int, default=1)
    parser.add_argument('--reducers', '-red', type=int, default=1)
    parser.add_argument('--registry', '-reg', type=str, default="$(minikube ip):5000")
    parser.add_argument('--run-registry', '-runreg', type=str, default=None)

    args = parser.parse_args()
    print(str(args) + "\n\n")

    if args.mode == None:
        pass
    elif args.mode == "upload":
        # chunk & upload input files to hdfs
        upload.upload_to_hdfs(args.input_dir, args.output_dir, args.chunk_size)
    elif args.mode == "run":
         # update settings values from args
        settings.NUM_REDUCERS_VALUE = args.reducers
        settings.HDFS_OUT_DIR_VALUE = args.output_dir

        # deploy map and reduce workers
        mappers = [None] * args.mappers
        for i in range(args.mappers):
            mappers[i] = deploy.create_map_function(
                function_id=i, 
                registry=args.registry, 
                run_registry=args.run_registry
            )
        reducers = [None] * args.reducers
        for i in range(args.reducers):
            reducers[i] = deploy.create_reduce_function(
                function_id=i, 
                registry=args.registry, 
                run_registry=args.run_registry
            )
        # deploy
        for mapper in mappers:
            mapper.deploy()
        for reducer in reducers:
            reducer.deploy()
        # cleanup
        for mapper in mappers:
            mapper.cleanup()
        for reducer in reducers:
            reducer.cleanup()

        # invoke mappers
        invoke_mappers(args.input_dir, mappers)

        # invoke reducers
        # invoke_reducers(reducers)
