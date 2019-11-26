import pydoop.hdfs as hdfs
import os
import requests

# h = hdfs.hdfs(host="pc816.emulab.net", port=9000, user="ubuntu")
# print(h.list_directory("/"))
# with h.open_file('/test/ssh_key_gen.txt') as f:
#     for line in f:
#         print(line)
# lfs = hdfs.hdfs("", 0)
# # print(lfs.list_directory(os.getcwd()))
# lfs.copy("{}/logs.txt".format(os.getcwd()), h, "/logs.txt")
# print(h.list_directory("/test"))
# h.close()
# lfs.close()

r = requests.get(url="http://pc816.emulab.net:9870/webhdfs/v1/test/ssh_key_gen.txt?op=OPEN")
print(r.text)


# import pyarrow as pa
# fs = pa.hdfs.connect('pc786.emulab.net', 9000)#, user=user, kerb_ticket=ticket_cache_path)
# with fs.open(path, 'rb') as f:
    # Do something with f


# from snakebite.client import Client
# client = Client("pc816.emulab.net", 8020, use_trash=False)
# for x in client.ls(['/']):
#     print(x)

# from hdfs import InsecureClient
# client = InsecureClient('http://pc816.emulab.net:9000', user='ubuntu')
# with client.read('/test/ssh_key_gen.txt') as f:
#     pass