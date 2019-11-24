import pydoop.hdfs as hdfs


with hdfs.open('/data/alice.txt') as f:
    for line in f:
        