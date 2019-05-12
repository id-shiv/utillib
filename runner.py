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
    from general import get_timestamp_as_string

    url = 'https://pythonspot.com'
    links = browser.get_hyper_links(url)

    for link_text, link in links.items():
        if url in link and (len(link) - len(url) <= 1):
            # Skip the base url 
            continue
        
        try:
            # launch the url
            driver = browser.launch(url=link, wait_seconds_after_launch=5)

            # Save the screen shot
            screen_shot_file = 'temp/' + get_timestamp_as_string() + '.png'
            browser.screen_shot(driver, screen_shot_file)

            # Close the browser
            browser.quit(driver)

        # break
        except BaseException as exception:
            print('Exception {}'.format(exception))