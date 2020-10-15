import asyncio
import os, time
from datetime import datetime
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

cached_stamp = 0

async def time():
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

async def file_data():
    global cached_stamp
    filename= './data.txt'
    stamp = os.stat(filename).st_mtime
    if stamp != cached_stamp:
        cached_stamp = stamp
        with open(filename, 'r') as reader:
            print(reader.read())


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(time, 'interval', seconds=10)
    scheduler.add_job(file_data, 'interval', seconds=10)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

# Reference links

# https://stackoverflow.com/a/63157020/11792496

# https://apscheduler.readthedocs.io/en/stable/userguide.html

# https://stackoverflow.com/a/182259/11792496
