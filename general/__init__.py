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
