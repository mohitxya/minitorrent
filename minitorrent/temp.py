import bencoder 
from pprint import pprint


with open('./response.txt','rb') as f:
    data=bencoder.decode(f.read())

pprint(data)
