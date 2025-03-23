import bencoder 
import hashlib
from collections import OrderedDict, namedtuple


TorrentFile = namedtuple('TorrentFile', ['name','length'])
class Torrent:
    def __init__(self, filename):
        self.filename=filename
        self.files=[]
        
        with open("self.filename","rb") as f:
            self.meta_data=bencoder.decode(f.read())
            info_dict=self.meta_data[b'info']
            info_bencoded=bencoder.encode(info_dict)
            self.info_hash=hashlib.sha1(info_bencoded).digest()
            self._identify_files() 
            #info_hash = ''.join(f'%{b:02X}' for b in info_hash_b)
    def _identify_files(self):

        if self.multi_file:
            raise RuntimeError('Multi-file torrents is not supported')
        self.files.append(Torrentfile(self.meta_data[b'info'][b'name'].decode('utf-8'),self.meta_data[b'info'][b'length']))

    @property 
    def announce(self) -> str:
        return self.meta_data[b'announce'].decode('utf-8')

    @property
    def multi_file(self) -> bool:
        return b'files' in self.meta_data[b'info']

    @property
    def piece_length(self) -> int:
        return self.meta_data[b'info'][b'piece length']
    
    @property
    def total_size(self) -> int:
        if self.multi_file:
            raise RuntimeError('Multi-file torrents is not supported!')
        return self.files[0].length
    @property
    def pieces(self):
        # Represents all pieces SHA1 pieces hashes, each 20 bytes long.
        data = self.meta_data[b'info'][b'pieces']
        pieces=[]
        offset=0
        length=len(data)

        while offset<length:
            pieces.append(data[offset:offset+20])
            offset +=20
        return pieces

    @property
    def output_file(self):
        return self.meta_data[b'info'][b'name'].decode('utf-8')

    def __str__(self):
        return (
        f"Filename: {self.data[b'info'][b'name'].decode('utf-8')}\n"
        f"File length: {self.data[b'info'][b'length']}\n"
        f"Announce URL: {self.data[b'announce'].decode('utf-8')}\n"
        f"Hash: {self.info_hash.hex()}"
        )



































