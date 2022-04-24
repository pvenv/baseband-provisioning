from itertools import count
import sqlite3
import os
from numpy import count_nonzero

if os.path.exists('bts.db'):
   if os.path.exists('bts.db_old'):
      os.remove('bts.db_old')
   os.rename('bts.db', 'bts.db_old')

conn = sqlite3.connect('bts.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS BTS(
   bts_name TEXT PRIMARY KEY,
   bts_oam TEXT,
   bts_ip_bts TEXT,
   bts_ip_mbh TEXT);
""")
conn.commit()

from bs4 import BeautifulSoup
import re
import sys

def parse_xml():
   '''Парсим xls файл'''
   
   result = {}
   try:
      base_ip_file_name = 'БС_IP.xls'
      base_ip_file = open(base_ip_file_name, "r")
   except Exception:
      while True:
         base_ip_file_name = input('Файл БС_IP.xls не найден! Укажите путь до файла:')
         if os.path.isfile(f'{base_ip_file_name}'):
            break
      base_ip_file = open(base_ip_file_name, "r")
   contents = base_ip_file.read()
   soup = BeautifulSoup(contents, 'lxml')


   current_bts_number = ''
   current_bts_attributes = {}

   count_tr = 0
   # i = 20 # для тестов 20
   for tag in soup.find_all("tr"):
      count_tr += 1

      # i -= 1
      # if i == 0:
      #    break
      # print("{0}: {1}".format(tag.name, tag))

      if count_tr == 1:
         current_bts_number = re.search(r'BTS_56_\s?(\w+)[ \<\(]', str(tag)).group(1)
         current_bts_attributes['name'] = current_bts_number

         oam = re.search(r'OAM\.(\d+)\<', str(tag))
         if oam is not None:
            oam = oam.group(1)
            result[f'{current_bts_number}_OAM'] = oam
            current_bts_attributes['oam'] = oam
         else:
            count_tr -= 1
         continue

      if count_tr == 2:
         bts_ip = re.search(r'(\d+\.\d+\.\d+\.\d+).+BTS', str(tag))
         if bts_ip is None:
            count_tr -= 1
         else:
            result[f'{current_bts_number}_IP_BTS'] = bts_ip.group(1)
            current_bts_attributes['ip_bts'] = bts_ip.group(1)

      if count_tr == 3:
         mbh_ip = re.search(r'(\d+\.\d+\.\d+\.\d+).+MBH', str(tag))
         if mbh_ip is None:
            count_tr -= 1
         else:
            result[f'{current_bts_number}_IP_MBH'] = mbh_ip.group(1)
            current_bts_attributes['ip_mbh'] = mbh_ip.group(1)
         continue

      if tag.text == '':
         count_tr = 0
         # print('continue')
         print(f"'{current_bts_attributes['name']}', '{current_bts_attributes['oam']}', '{current_bts_attributes['ip_bts']}', '{current_bts_attributes['ip_mbh']}'")
         cur.execute(f"INSERT OR REPLACE INTO BTS(bts_name, bts_oam, bts_ip_bts, bts_ip_mbh) \
            VALUES ('{current_bts_attributes['name']}', '{current_bts_attributes['oam']}', '{current_bts_attributes['ip_bts']}', '{current_bts_attributes['ip_mbh']}')")
         conn.commit()
         continue
   # print('result', result, len(result))
   



input('Конвертирование файла .xls в базу данных! Нажмите Enter, чтобы продолжить!')
parse_xml()
input('Конвертирование .xls в базу данных завершено! Нажмите Enter, чтобы закрыть программу!')
