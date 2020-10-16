import asyncio
import os, time
from datetime import datetime
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler


'''
Global variable to store the details of the last time the file was updated.
'''
cached_stamp = 0


'''
An Asynchronous function to display the current time using the datetime module.

Input - NA
Output - prints the current time on the terminal
'''
async def time():
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


'''
An Synchronous function that prints the content of the file on the terminal.
The function only prints if the contents of the file have been changed.
The value stored in cached_stamp represents the time when the file was last changed.
The values of cached_stamp and os.stat(filename).st_mtime are compared to see if the file has been updated again or not.

Input - NA
Output - print the file content only if it is changed else no output
'''
async def file_data():
    global cached_stamp
    filename= './data.txt'
    stamp = os.stat(filename).st_mtime
    if stamp != cached_stamp:
        cached_stamp = stamp
        with open(filename, 'r') as reader:
            print(reader.read())


'''
Execution of the two above functions in an Asynchronous way.
We create an object of AsyncIOScheduler class ie an async scheduler and add the two methods as jobs which will run in intervals of 10 seconds.
We then create an asyncio reference which gets the event loop from the scheduler and runs the task forever until Cntl + C is pressed.
'''
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
