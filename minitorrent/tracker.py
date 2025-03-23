import aiohttp
import asyncio


class Tracker: 
    def __init__(self, torrent):
        self.torrent=torrent # Torrent object
        self.peer_id=calculate_id()
        self.http_client=aiohttp.ClientSession()
    async def connect(self, first: bool=None, uploaded:int=0, downloaded int=0):
        params={'info_hash':self.torrent.info_hash, 'peer_id':self.peer_id, 'uploaded'=uploaded, 'downloaded':downloaded, 'left': self.torrent.total_size - downloaded, 'compact':1}
        
        if first:
            params['event']='started'

        url = self.torrent.announce + '?' + urlencode(params)
        logging.info('Connecting to tracker at: '+url)

    def calculate_id():
        id='-PC0001-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])
        return id
    


