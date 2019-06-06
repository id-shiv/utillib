def main():
    """
    runner.py
    Contains sample invokations of utility libraries
    """
    # from general import print_dictionary
    # from environment import get
    # print_dictionary(get(), width=80, cell_outer_border= '==',
    #                  cell_inner_border=':')

    # from general import logger
    # log_handler = logger('sample.log')
    # log_handler.error("test error")

    # from environment import install_packages, verify_installed_packages
    # install_packages('Requirements.txt')
    # verify_installed_packages('Requirements.txt')

    print('{} execution complete'.format(__file__))


def webcrawl_and_take_screen_shot():
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


def ml_with_scikit_learn():
    # import pylab as pl
    import numpy as np

    from sklearn.datasets import load_digits
    digits = load_digits()
    # print(digits.DESCR)

    X, y = digits.data, digits.target
    print('Shape of X : {} | Shape of y : {}'.format(X.shape, y.shape))
    print('Classes : {}'.format(list(np.unique(y))))
    n_samples, n_features = X.shape
    print('# of Samples : {} | # of Features : {}'.format(n_samples,
                                                          n_features))

    # Initial plot configuration
    # pl.rcParams['figure.figsize'] = 10, 7.5
    # pl.rcParams['axes.grid'] = True
    # pl.gray()

    # for i, j in enumerate(np.random.permutation(X.shape[0])[:5]):
    #     pl.subplot(1, 5, (i + 1))
    #     pl.imshow(X[j].reshape((8, 8)), interpolation='nearest')
    #     pl.title('true class {}'.format(y[j]))
    #     pl.xticks(()), pl.yticks(())
    #     pl.plot(pl.xticks(()), pl.yticks(()))


def web_crawl():
    from browser.crawler import Crawler

    base_url = 'https://en.wikipedia.org/wiki/Main_Page'
    Crawler('temp/', 'wiki', base_url)
    Crawler.create_workers()
    Crawler.crawl()


if __name__ == '__main__':
    # webcrawl_and_take_screen_shot()
    # ml_with_scikit_learn()
    web_crawl()
    main()
