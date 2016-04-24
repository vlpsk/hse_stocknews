__author__ = 'vladimirpiskunov'

import re, time
from xml.etree import ElementTree
from urllib.request import urlopen
from newsmaker import newsmaker
from MICEX import main_micex
from RTSI import main_rtsi

with open("share_thld.txt", "r", encoding = "utf-8") as infile:
    value = infile.read()
treshold = float(value)
last_change_prc = 0
apiURL = "http://www.micex.ru/iss/engines/stock/markets/shares/securities.xml"

##These are security identifications
share_names = ["GAZP","LKOH","SBER","SBERP","MGNT","SNGS","SNGSP","GMKN","NVTK","ROSN","MTSS","VTBR","TATN","TATNP","TRNFP","URKA","POLY","YNDX","MFON","RTKM","RTKMP","ALRS","CHMF","HYDR","MOEX","RUALR","NLMK","AFKS","PHOR","PIKK","BANE","BANEP","EONR","MAGN","LSRG","DIXY","PHST","GCHE","TRMK","IRAO","MVID","AFLT","FEES","RSTI","AKRN","VSMO","MSTT","BSPB","NMTP"]
share_iterations = {"GAZP":0,"LKOH":0,"SBER":0,"SBERP":0,"MGNT":0,"SNGS":0,"SNGSP":0,"GMKN":0,"NVTK":0,"ROSN":0,"MTSS":0,"VTBR":0,"TATN":0,"TATNP":0,"TRNFP":0,"URKA":0,"POLY":0,"YNDX":0,"MFON":0,"RTKM":0,"RTKMP":0,"ALRS":0,"CHMF":0,"HYDR":0,"MOEX":0,"RUALR":0,"NLMK":0,"AFKS":0,"PHOR":0,"PIKK":0,"BANE":0,"BANEP":0,"EONR":0,"MAGN":0,"LSRG":0,"DIXY":0,"PHST":0,"GCHE":0,"TRMK":0,"IRAO":0,"MVID":0,"AFLT":0,"FEES":0,"RSTI":0,"AKRN":0,"VSMO":0,"MSTT":0,"BSPB":0,"NMTP":0}

def getmethedata(share_name):
    """
    Function gets the data by formating the correct url for the security
    The returned xmltree is parsed and the relevant information is extracted
    If the condition of generating news is met, the function for generating
    text is called
    """
    market_price = 0.0
    open_value = 0.0
    last_value = 0.0
    last_change_prc = 0.0
    pattern = './/data[@id="marketdata"]//rows//row[@SECID="{}"][@BOARDID="TQBR"]'
    pattern_name = './/data[@id="securities"]//rows//row[@SECID="{}"][@BOARDID="SMAL"]'
    if share_name == "YNDX":
        pattern = re.sub('SMAL', 'TQBR', pattern)
    pattern = pattern.format(share_name)
    pattern_name = pattern_name.format(share_name)

    tree = ElementTree.parse(urlopen(apiURL))
    for word in tree.findall(pattern_name):
        name = word.get('SECNAME')
    for word in tree.findall(pattern):
        try:
            market_price = word.get('MARKETPRICE')
            open_value = word.get('OPEN')
            last_value = word.get('LAST')
            last_change_prc = word.get('LASTCHANGEPRCNT')
            date_and_time = word.get('SYSTIME')
        except:
            print("oops!")
    time, = re.findall(" (\d\d)", date_and_time)
    if time == "09":
        share_iterations[share_name] = 0
    if float(last_change_prc) >= treshold and share_iterations[share_name] == 0:
        newsmaker(name, open_value, market_price, last_change_prc)
        share_iterations[share_name] = market_price
    elif share_iterations[share_name] > 0:
        last_price = share_iterations[share_name]
        pc = float(last_price)/100.0
        if float(last_price) < float(market_price):
            val = float(market_price) - float(last_price)
            val_pc = val/pc
            if val_pc >= treshold:
                newsmaker(name, open_value, market_price, last_change_prc)
                share_iterations[share_name] = market_price
        if float(last_price) > float(market_price):
            val = float(last_price) - float(market_price)
            val_pc = val/pc
            if val_pc >= treshold:
                newsmaker(name, open_value, market_price, last_change_prc)
                share_iterations[share_name] = market_price


def writer():
    """
    This module generates news for securities
    It also runs modules that generate news for indices
    """
    for share_name in share_names:
        getmethedata(share_name)
    main_micex()
    main_rtsi()
        
while True:
    writer()
    time.sleep(59)