def main():
    """
    runner.py
    Contains sample invokations of utility libraries
    """
    # from general import print_dictionary
    # from environment import get
    # print_dictionary(get(), width=80, cell_outer_border= '==', cell_inner_border=':')

    from general import logger
    log_handler = logger('sample.log')
    log_handler.error("test error")

    print('{} execution complete'.format(__file__))

if __name__ == '__main__':
    main()