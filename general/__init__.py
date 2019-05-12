import logging
import random
import string
import datetime

def print_dictionary(dictionary, width=80, cell_outer_border = '--', cell_inner_border = '|'):
    """
    Print dictionary as table 
    """
    try:
        print('\n')
        print(cell_outer_border*width)
        print("{}{}{}{}{}{}{}{}{}".format(cell_inner_border,
                                       ' '*(int(width/2) - len('KEY')), 
                                       'KEY',
                                       ' '*(int(width/2) - len('KEY') + 1),
                                       cell_inner_border,
                                       ' '*(int(width/2)- len('VALUE')), 
                                       'VALUE',
                                       ' '*(int(width/2) - len('VALUE') + 4),
                                       cell_inner_border
                                       ))
        print(cell_outer_border*width)
        for key, value in dictionary.items():
            print('{} {}{} {} {}{} {}'.format(cell_inner_border,
                                           key, 
                                           ' '*(width - 4 - len(key)), 
                                           cell_inner_border,
                                           value, 
                                           ' '*(width - 4 - len(value) + 1),
                                           cell_inner_border
                                           ))
            print(cell_outer_border*width)
        print('\n')
    except BaseException as exception:
        print('Cannot print dictionary')
        print(exception)

def logger(log_file, log_level='DEBUG'):
    """
    Returns logging handler to specified log file with specified log level
    log message example entry : 
    [ERROR, 2019-05-12 18:27:04,867, runner.py, runner, main, line#12] test error
    """
    level = logging.DEBUG
    logging.basicConfig(filename=log_file,
                        format='[%(levelname)s, %(asctime)s, %(filename)s, '
                            '%(module)s, %(funcName)s, line#%(lineno)s] %(message)s',
                        level=level)
    return logging

def generate_random_string(length=5):
    """
    Returns a random string of fixed length 
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_timestamp_as_string():
    """
    Gets the current time and returns it as string
    """
    current_time = datetime.datetime.now().isoformat()
    chars_to_replace = ['.', '-', ':', ' ']
    for character in chars_to_replace:
        current_time = current_time.replace(character, '')
    return current_time