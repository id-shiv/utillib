# Service to notify and remind users and tasks, to dos and critical information

from time import sleep
from datetime import datetime, timedelta
import json
# import os
import re


ROOT_FOLDER = '/Users/shiv/Desktop/utillib/poc/notification_service/'
BREAK_TIME_HRS = 24


class General_Modules:
    def validate_date(input_date):
        date_format_expression = "(?<!\d)((1[0-2])|(0?[0-9]))/(((1[0-9])|(2[0-9])|(3[0-1])|(0?[0-9])))(?!\d)"
        date_format_check = re.search(date_format_expression, input_date)
        return True
        if date_format_check:
            return True
        else:
            return False

    def validate_string(input_string):
        return input_string.strip()[0].isalpha()

    def validate_project_model(input_model):
        return (input_model.lower() in ["agile", "waterfall", "hybrid"])

    def get_project_model(task_profile):
        for task in task_profile["PROFILE"]:
            if task["PARAMETER"] == "PROJECT MODEL":
                return task["RESPONSE"]

    def pad_date_with_zero(input_date, delimiter='-'):
        output_date = []
        for date_paramter in input_date.split(delimiter):
            if len(date_paramter) < 2:
                output_date.append('0' + date_paramter)
            else:
                output_date.append(date_paramter)
        return delimiter.join(output_date)


def get_tasks():
    with open(ROOT_FOLDER + 'tasks.json', 'r') as task_file:
        tasks = json.load(task_file)
    return tasks["TASKS"]


def check_notifications():
    current_date = datetime.now().date()
    print('Current date is {}'.format(current_date))
    return False


def notify():
    pass


# Collect task profile
with open(ROOT_FOLDER + 'task_profile.json', 'r') as task_profile_file:
    tasks = json.load(task_profile_file)

tasks_updated_profile_list = []
# Collect the task parameters
for task in tasks["PROFILE"]:
    # Is this task dependent of any other parameter?
    skip_task = False  # skip the question does not match dependency
    if task["DEPENDENCIES"] != "":
        for dependency in task["DEPENDENCIES"]:
            if dependency["TYPE"] == "PROJECT MODEL":
                if dependency["VALUE"].lower() != General_Modules.get_project_model(tasks).lower():
                    skip_task = True

    if skip_task:
        continue

    print(task["QUESTION"])
    response = input('Enter: ')

    # Validate if mandatory
    while task["MANDATORY"] == "True" and response.strip() == "":
        print('This is a Mandatory Attribute')
        response = input('Enter: ')

    # Validate date format
    if task["TYPE"] == "DATE":
        while not General_Modules.validate_date(response):
            print('Enter Date in YYYY-MM-DD format')
            response = input('Enter: ')

    # Validate if string
    if task["TYPE"] == "STRING":
        while not General_Modules.validate_string(response):
            print('Enter String')
            response = input('Enter: ')

    # Validate if project model
    if task["TYPE"] == "PROJECT MODEL":
        while not General_Modules.validate_project_model(response):
            print('Enter Project Model as Agile/Waterfall/Hybrid')
            response = input('Enter: ')
    
    task["RESPONSE"] = response
    tasks_updated_profile_list.append(task)
    print("-"*50 + "\n")

# Build task list
task_list = []
tasks = get_tasks()

for task in tasks:
    task_details = {}
    task_details["NAME"] = task["NAME"]
    task_details["TYPE"] = "TRIGGER"
    for tasks_updated_profile in tasks_updated_profile_list:
        if tasks_updated_profile["PARAMETER"] == task["PROFILE PARAMTER"]:
            task_details["TASK DATE"] = General_Modules.pad_date_with_zero(tasks_updated_profile["RESPONSE"])
    if task["NOTIFY"] == "2_WEEKS_BEFORE":
        date_2_weeks_before = datetime.strptime(task_details["TASK DATE"], '%Y-%m-%d') - timedelta(days=14)
        task_details["TRIGGER DATE"] = General_Modules.pad_date_with_zero(str(date_2_weeks_before).split(" ")[0])
    if task["REMINDER"]:
        if task["REMINDER"] == 'EVERY_WEEK':
            reminder_date = datetime.strptime(task_details["TRIGGER DATE"], '%Y-%m-%d')
            task_date = datetime.strptime(task_details["TASK DATE"], '%Y-%m-%d')
            while reminder_date < task_date:
                reminder_date = reminder_date + timedelta(days=7)
                sub_task_details = {}
                sub_task_details["NAME"] = task["NAME"]
                sub_task_details["TYPE"] = "REMINDER"
                sub_task_details["TASK DATE"] = task_details["TASK DATE"]
                sub_task_details["TRIGGER DATE"] = str(reminder_date).split(" ")[0]
                task_list.append(sub_task_details)

    task_list.append(task_details)
    
task_list = [i for n, i in enumerate(task_list) if i not in task_list[n + 1:]]
for task in sorted(task_list, key=lambda i: i['TRIGGER DATE']):
    print('{}|{}|{}|{}'.format(task["NAME"], task["TYPE"], task["TASK DATE"], task["TRIGGER DATE"]))


# Run the notification service
while False:
    # Check if there is anything to notify
    print('Checking for any notifications')
    if check_notifications():
        print('Notfying user')
    else:
        print('Nothing to notify at this time, taking a break of {} hours'.format(BREAK_TIME_HRS))

    sleep(BREAK_TIME_HRS * 60 * 60)
