from scrape import scrape_data
from reformat import reformat_data
from automation import automate

def main():
    scrape_data()

    reformat_data()

    automate()
if __name__ == '__main__':
    main()

