import sys
import time


tile = open('/tmp/123')


def tail():
    tile.seek(0, 2)
    while True:
        where = tile.tell()
        line = tile.readline()
        if not line:
            time.sleep(0.01)
            tile.seek(where)
        else:
            print(line.strip())
            yield line.strip()


# d = tail()

# for o in d:
#     print(o)