import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

SERVICE_TAG = "FK00BP2"
EXPORT_TO_FOLDER = "poc/dell/exported/"
EXPORT_FILE_NAME = '{}.csv'.format(SERVICE_TAG)
EXPORT_PATH = EXPORT_TO_FOLDER + EXPORT_FILE_NAME
URL = "https://www.dell.com/support/home/in/en/indhs1/product-support/servicetag/<SERVICE TAG>/configuration"
URL = URL.replace("<SERVICE TAG>", SERVICE_TAG)
    

def __soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"}
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, "html.parser")


def __insert(df, row):
    insert_loc = df.index.max()

    if np.isnan(insert_loc):
        df.loc[0] = row
    else:
        df.loc[insert_loc + 1] = row

    return df


def __original_configuration(service_tag, url):
    columns = ["COMPONENT NAME", "PART NUMBER", "QUANTITY", "DESCRIPTION"]
    config_details = pd.DataFrame(columns=columns)

    locators = {
        "content": "col-lg-12 col-md-12 col-sm-12 hidden-xs",
        "component_name": "show-collapsed",
        "table": "table table-striped"
    }

    try:
        soup = __soup(url)
    except BaseException as e:
        print(e)
        return
    content = soup.find("div", {"class": locators["content"]})
    components = content.findChildren("div", recursive=False)

    for component in components:
        config_info = []
        component_name = component.find("span", {"class": locators["component_name"]}).text
        parts_table = component.find("table", {"class": "table"})
        for row in parts_table.find_all("tr"):
            cells = row.find_all("div")
            for cell in cells:
                cell_value = cell.text.replace("\n", "").replace(" ", "")
                if cell_value not in ["PartNumber", "Quantity", "Description"]:
                    config_info.append(cell_value)

            if len(config_info) > 1:
                config_info = [component_name] + config_info
                config_details = __insert(config_details, config_info)
                config_info = []

    return config_details


def original_configuration(service_tag):
    config_details = __original_configuration(SERVICE_TAG, URL)
    if config_details is not None:
        config_details.to_csv(EXPORT_PATH)
    else:
        print('Original configuration of the device {} could not be retrived'.format(SERVICE_TAG))
        print('Check internet connectivity to www.dell.com')


original_configuration(SERVICE_TAG)
