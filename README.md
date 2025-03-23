### A simple BitTorrent Client written in python.

- Python's asyncio library is used to access multiple peers simultaneously.
- Bencoded .torrent file is parsed initially.
- We put the decoded data into an ordered Dictionary.
- announce: gives the tracker url. If 'announce_list' is present ignore 'announce' key.
- Send a request to the first tracker in 'announce_list', moving onto the next if that doesn't work.
- Extract meta data and store as variables.
