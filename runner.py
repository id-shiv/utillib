def main():
    """
    runner.py
    Contains sample invokations of utility libraries
    """
    # from general import print_dictionary
    # from environment import get
    # print_dictionary(get(), width=80, cell_outer_border= '==', cell_inner_border=':')

    # from general import logger
    # log_handler = logger('sample.log')
    # log_handler.error("test error")

    print('{} execution complete'.format(__file__))

if __name__ == '__main__':
    main()

    import browser

    url = 'https://pythonspot.com'
    links = browser.get_hyper_links(url)
    for link_text, link in links.items():
        print(link)
        driver = browser.start(link, wait_seconds_after_launch=5)
        browser.screen_shot(driver, 'sample.png')
        browser.stop(driver)
        break