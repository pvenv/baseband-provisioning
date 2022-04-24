from bs4 import BeautifulSoup
import re
import sys

def parse_xml(bts_number):
    '''Парсим xls файл'''
    
    result = {}
    base_ip_file_name = 'БС_IP.xls'
    base_ip_file = open(base_ip_file_name, "r")
    base_ip_file_text = base_ip_file.readlines()
    bs = BeautifulSoup (str(base_ip_file_text), 'html.parser')
    
    bs_bts = bs.find('th')
    while True:
        print('bs_bts', bs_bts)
        if re.search(bts_number, str(bs_bts)) is None:
            bs_bts = bs_bts.find_next()
            continue
        else:
            print('bs_bts', bs_bts)
            break
        
    
    # print(bs_name)
    
    
    return result