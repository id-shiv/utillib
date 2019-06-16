# Service to notify and remind users and tasks, to dos and critical information

from time import sleep
from datetime import datetime
import json
# import os


ROOT_FOLDER = '/Users/shiv/Desktop/utillib/poc/notification_service/'

PROJECT_NAME = 'Test Project'
PROJECT_MODEL = 'Agile'
CURRENT_TASK_ID = 0
BREAK_TIME_HRS = 24


def get_tasks():
    with open(ROOT_FOLDER + 'tasks.json', 'r') as task_file:
        tasks = json.load(task_file)
    for task in tasks["TASKS"]:
        print(task["NAME"])


def check_notifications():
    current_date = datetime.now().date()
    print('Current date is {}'.format(current_date))
    get_tasks()
    return False


def notify():
    pass


# Run the notification service
while True:
    # Check if there is anything to notify
    print('Checking for any notifications')
    if check_notifications():
        print('Notfying user')
    else:
        print('Nothing to notify at this time, taking a break of {} hours'.format(BREAK_TIME_HRS))

    sleep(BREAK_TIME_HRS * 60 * 60)
