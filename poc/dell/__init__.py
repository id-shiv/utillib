import requests
from bs4 import BeautifulSoup

SERVICE_TAG = "FK00BP2"

URL = "https://www.dell.com/support/home/in/en/indhs1/product-support/servicetag/<SERVICE TAG>/configuration"
URL = URL.replace("<SERVICE TAG>", SERVICE_TAG)

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

content = soup.find("div", {"class": "col-lg-12 col-md-12 col-sm-12 hidden-xs"})
components = content.findChildren("div", recursive=False)

for component in components:
    component_name = component.find("span", {"class": "show-collapsed"}).text
    print("\n{}".format(component_name))
    parts_table = component.find("table", {"class": "table table-striped"})
    for row in parts_table.find_all("tr"):
        cells = row.find_all("div")
        for cell in cells:
            print('{} | '.format(cell.text.replace("\n", "")), end='')
        print("")