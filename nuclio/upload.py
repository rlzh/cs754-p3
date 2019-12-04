#!/usr/bin/env python
import sys
import argparse
import os
import shutil
import settings
from hdfs import InsecureClient
from fsplit.filesplit import FileSplit
from os import listdir
from os.path import isfile, join


split_files = []
hdfs_file_paths = []

def split_callback(f, s, c):
    split_files.append(os.path.abspath(f))
    print("file: {0}, size: {1}, count: {2}".format(f, s, c))

def upload_to_hdfs(input_dir, output_dir, chunk_size):
    # locate files in directory
    files = [os.path.abspath("{}/{}".format(input_dir, f)) for f in listdir(input_dir) if isfile(join(input_dir, f))]
    tmp_dir = "{}/tmp".format(input_dir)

    # setup temp dir
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    # split files into 128mb chunks
    for f in files:
        fs = FileSplit(file=f, splitsize=(chunk_size)*1e6, output_dir=tmp_dir)
        fs.split(callback=split_callback)

    # upload to hdfs
    hdfs_client = InsecureClient("http://{}:9870".format(settings.HDFS_HOST_VALUE), user=settings.HDFS_USER_VALUE)

    # delete existing output dir
    if hdfs_client.content(output_dir, strict=False) != None:
        hdfs_client.delete(output_dir, recursive=True)

    # upload files to tmp dir
    remote_path = hdfs_client.upload(hdfs_path="/tmp", local_path=tmp_dir, n_threads=-1, overwrite=True)
    
    # rename to output_dir
    hdfs_client.rename("/tmp", output_dir)

    print("{} files uploaded to hdfs host '{}{}'  ({} file chunks total)".format(
        len(files),
        settings.HDFS_HOST_VALUE,
        output_dir,
        len(split_files),
    ))
    # delete temp files
    shutil.rmtree(tmp_dir)

    return hdfs_file_paths

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '-i', type=str, default=None)
    parser.add_argument('--output_dir', '-o', type=str, default="/")
    parser.add_argument('--chunk_size', '-cs', type=int, default=127)
    args = parser.parse_args()
    print(str(args) + "\n\n")

    if args.input_dir == None:
        print("Error: missing input dir arg")
    # chunk files in input dir and upload to hdfs
    upload_to_hdfs(args.input_dir, args.output_dir, args.chunk_size)



    

