__author__ = 'vladimirpiskunov'

from xml.etree import ElementTree
from urllib.request import urlopen
from newsmaker_stocks import newsmaker_stocks

with open("stock_thld.txt", "r", encoding = "utf-8") as infile:
    value = infile.read()
treshold = float(value)
apiURL = 'http://www.micex.ru/iss/engines/stock/markets/index/boards/SNDX/securities/{}.xml'
name = 'MICEXINDEXCF'
share_iterations = {'MICEXINDEXCF':0}

def main_micex():
    """
    formates URL for the API and gets the xmltree
    genreates news for MICEX
    """
    good_url = apiURL.format(name)
    tree = ElementTree.parse(urlopen(good_url))
    get_info(tree)

def get_info(tree):
    """
    xml tree is parsed. The relevant information is extracted
    If the news generating condition is met, the text generating
    module is run
    """
    market_price = 0.0
    open_value = 0.0
    last_value = 0.0
    last_change_prc = 0.0
    for word in tree.findall('.//data[@id="marketdata"]//rows//row'):
        open_value = word.get('OPENVALUE')
        current_value = word.get('CURRENTVALUE')
        last_change_prc = word.get('LASTCHANGEPRC')
        if float(last_change_prc) >= treshold and share_iterations[name] == 0:
            newsmaker_stocks(name, open_value, current_value, last_change_prc)
            share_iterations[name] = current_value
        elif share_iterations[name] > 0:
            last_price = share_iterations[name]
            pc = float(last_price)/100.0
            if float(last_price) < float(current_value):
                val = float(current_value) - float(last_price)
                val_pc = val/pc
                if val_pc >= treshold:
                    newsmaker_stocks(name, open_value, current_value, last_change_prc)
                    share_iterations[name] = current_value
            if float(last_price) > float(current_value):
                val = float(last_price) - float(current_value)
                val_pc = val/pc
                if val_pc >= treshold:
                    newsmaker_stocks(name, open_value, current_value, last_change_prc)
                    share_iterations[name] = current_value

if __name__ == '__main__':
    main_micex()
