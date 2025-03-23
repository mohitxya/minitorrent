import aiohttp
import asyncio


class Tracker: 
    def __init__(self, torrent):
        self.torrent=torrent
        self.peer_id=calculate_id()
    def _peerid(torrent):
        id='-PC0001-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])
        return id



