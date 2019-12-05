

import deploy
import upload
import settings
import argparse
import asyncio
import pika
import json
import time
from hdfs import InsecureClient
from urllib.parse import urlparse


# global vars
reducer_finish_count = 0

def get_hdfs_paths(input_dir):
    hdfs_file_paths = []
    hdfs_client = InsecureClient("http://{}:9870".format(settings.HDFS_HOST_VALUE))
    contents = hdfs_client.list(input_dir, status=True)
    input_dir = "" if input_dir == "/" else input_dir
    for content in contents:
        if content[1]['type'] == 'FILE':
            hdfs_file_paths.append("{}/{}".format(input_dir, content[0]))
    return hdfs_file_paths

def create_out_dir(output_dir):
    if output_dir == "/":
        return
    hdfs_client = InsecureClient("http://{}:9870".format(settings.HDFS_HOST_VALUE))
    if hdfs_client.content(output_dir, strict=False) != None:
        hdfs_client.delete(output_dir, recursive=True)
    hdfs_client.makedirs(output_dir)

def invoke_mappers(channel, input_dir, hdfs_file_paths, mappers):
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

def wait_for_reducers(channel):
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=settings.EXCHANGE_NAME_VALUE, queue=queue_name, routing_key=settings.DONE_TOPIC_VALUE)   
    channel.basic_consume(queue=queue_name, on_message_callback=probe_callback, auto_ack=True)
    print(' [*] Waiting for messages...')
    channel.start_consuming()
    print(" [*] Done! ")

def probe_callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        global reducer_finish_count 
        reducer_finish_count += 1
        print(" [X] Count {}".format(reducer_finish_count))
        if reducer_finish_count == settings.NUM_REDUCERS_VALUE:
            ch.stop_consuming()


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
        print("Error: mode arg not set! '-m upload' or '-m run'")
    elif args.mode == "upload":
        # chunk & upload input files to hdfs
        upload.upload_to_hdfs(args.input_dir, args.output_dir, args.chunk_size)
    elif args.mode == "run":
        # get hdfs file paths
        hdfs_file_paths = get_hdfs_paths(args.input_dir)
        
        # create output dir
        create_out_dir(args.output_dir)

        # setup rabbitMQ connection
        credentials = pika.PlainCredentials(settings.RMQ_USER_VALUE, settings.RMQ_PASS_VALUE)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RMQ_HOST_VALUE, 
            port=settings.RMQ_PORT_VALUE, 
            credentials=credentials
            )
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange=settings.EXCHANGE_NAME_VALUE,
            exchange_type='topic'
        )

        # update settings values from args
        settings.HDFS_OUT_DIR_VALUE = args.output_dir
        settings.HDFS_CHUNK_COUNT_VALUE = len(hdfs_file_paths)
        settings.NUM_REDUCERS_VALUE = args.reducers
        args.mapper = min(len(hdfs_file_paths), args.mappers)
        settings.NUM_MAPPERS_VALUE = args.mappers

        # create map and reduce workers
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
        mapper_deploy_procs = [mapper.deploy() for mapper in mappers]
        for p in mapper_deploy_procs:
            p.wait()
        reducer_deploy_procs = [reducer.deploy() for reducer in reducers]
        for r in reducer_deploy_procs:
            r.wait()

            
        # invoke mappers
        invoke_mappers(channel, args.input_dir, hdfs_file_paths, mappers)

        # wait for completion
        wait_for_reducers(channel)


        # cleanup
        for mapper in mappers:
            mapper.cleanup()
        for reducer in reducers:
            reducer.cleanup()

        connection.close()

