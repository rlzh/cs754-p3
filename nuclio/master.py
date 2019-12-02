#!/usr/bin/env python
import pika
import sys
import argparse
import os
import shutil
import settings
import pydoop.hdfs as hdfs

from fsplit.filesplit import FileSplit
from os import listdir
from os.path import isfile, join


# credentials = pika.PlainCredentials('nuclio', 'nuclio')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.32.128.199', port=5672, credentials=credentials))
# channel = connection.channel()
# channel.exchange_declare(exchange='map_exchange',
#                          exchange_type='topic')
# message = ' '.join(sys.argv[1:]) or 'Hello World!'

# channel.basic_publish(exchange='map_exchange',
#                       routing_key='tasks.map',
#                       body=message)

# print(" [x] Sent %r" % (message))
# connection.close()

split_files = []
hdfs_file_paths = []

def split_callback(f, s, c):
    split_files.append(os.path.abspath(f))
    print("file: {0}, size: {1}, count: {2}".format(f, s, c))

def upload_to_hdfs(input_dir):
    # locate files in directory
    files = [os.path.abspath("{}/{}".format(input_dir, f)) for f in listdir(input_dir) if isfile(join(input_dir, f))]
    tmp_dir = "{}/tmp".format(input_dir)

    # set temp dir
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    # split files into 128mb chunks
    for f in files:
        fs = FileSplit(file=f, splitsize=128e6, output_dir=tmp_dir)
        fs.split(callback=split_callback)

    # upload to hdfs
    host = settings.RMQ_HOST_VALUE
    rfs = hdfs.hdfs(host='localhost', port=9000)
    lfs = hdfs.hdfs("", 0)
    for f in split_files:
        print("uploading: " + f)
        hdfs_path = "/{}".format(os.path.basename(f))
        hdfs_file_paths.append(hdfs_path)
        lfs.copy(from_path=f, to_hdfs=rfs, to_path=hdfs_path)
    rfs.close()
    lfs.close()

    print("{} files uploaded to hdfs host '{}'  ({} file chunks total)".format(
        len(files),
        host,
        len(split_files),
    ))

    # delete temp files
    shutil.rmtree(tmp_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '-i', type=str, default=None)
    parser.add_argument('--output_dir', '-o', type=str, default=None)

    args = parser.parse_args()
    print(str(args) + "\n\n")

    # chunk files in input dir and upload to hdfs
    upload_to_hdfs(args.input_dir)



    

