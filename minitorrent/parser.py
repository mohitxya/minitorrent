import bencoder 
from pprint import pprint
import hashlib
from collections import OrderedDict
import urllib.parse
import random



with open("../tests/file3.torrent","rb") as f:
    data=bencoder.decode(f.read())
    od=OrderedDict(data)
    info_dict=od[b'info']
    h=hashlib.sha1



    info_bencoded=bencoder.encode(info_dict)
    info_hash_b=hashlib.sha1(info_bencoded).digest()

    info_hash = ''.join(f'%{b:02X}' for b in info_hash_b)
    print(info_hash)



peer_id='-PC0001-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])

print(peer_id)
pprint(od)
