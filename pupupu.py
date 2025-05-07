# from datetime import datetime, timedelta

# time = timedelta(minutes=5)
# start = datetime(2025, 5, 6, 18, 21, 57, 321534)
# while datetime.now() - start > timedelta(seconds=30):
#     print(start)
#     start = datetime.now()


import aiohttp
import asyncio

import aiohttp
import asyncio

async def main():

    with open("screenshot.jpg", "rb") as f:
        file = f.read()
    
    form = aiohttp.FormData()
    form.add_field("file", file)
    async with aiohttp.ClientSession() as session:
       async with session.post(url="http://127.0.0.1:8000/faces/find", data=form) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.json()
            print("Body:", html)

asyncio.run(main())