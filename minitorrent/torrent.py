import bencoder 
import hashlib
from collections import OrderedDict, namedtuple
import urllib.parse
from pprint import pprint


TorrentFile = namedtuple('TorrentFile', ['name','length'])
class Torrent:
    def __init__(self, filename):
        self.filename=filename
        self.files=[]
        
        with open("../tests/file3.torrent","rb") as f:
            self.data=bencoder.decode(f.read())
            info_dict=data[b'info']
            info_bencoded=bencoder.encode(info_dict)
            self.info_hash=hashlib.sha1(info_bencoded).digest()
            self._identify_files() 
            #info_hash = ''.join(f'%{b:02X}' for b in info_hash_b)
    def _identify_files(self):

        if self.multi_file:
            raise RuntimeError('Multi-file torrents is not supported')
        self.files.append(Torrentfile(self.data[b'info'][b'name'].decode('utf-8'),self.data[b'info'][b'length']))

    @property 
    def announce(self) -> str:
        return self.data[b'announce'].decode('utf-8')

    @property
    def multi_file(self) -> bool:
        return b'files' in self.data[b'info']

    @property
    def piece_length(self) -> int:
        return self.data[b'info'][b'piece length']
    
    @property
    def total_size(self) -> int:
        pass
    @property
    def pieces(self):
        pass
    @property
    def output_file(self):
        pass

    def __str__(self):
    return f'Filename: {self.data[b'info'][b'info']}\n'\'File length: {self.data[b'info'][b'length']}\n'\'Announce URL: {self.data[b'announce']}'\'Hash: {self.info_hash}'





































