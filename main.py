from dotenv import load_dotenv
import argparse
import requests
import os

load_dotenv()


BITLY_TOKEN = os.getenv("BITLY_TOKEN")
HEADERS = {"Authorization":"Bearer {}".format(BITLY_TOKEN)}

def shorten_link(link_to_short):
  url = "https://api-ssl.bitly.com/v4/bitlinks"
  shorten_link_payload = {"long_url": str(link_to_short)}
  response = requests.post(url, json=shorten_link_payload, headers=HEADERS)
  response.raise_for_status()
  response_dict = response.json()
  short_link = response_dict['id']
  return short_link

def count_link_clicks(link_to_short):
  url = "https://api-ssl.bitly.com/v4/bitlinks/{0}/clicks/summary".format(link_to_short)
  count_link_payload = {
    "unit": "day",
    "units": -1
  }
  response = requests.get(url, params=count_link_payload,headers=HEADERS)
  response.raise_for_status()
  response_dict = response.json()
  total_clicks = response_dict['total_clicks']
  return total_clicks 

def get_bitlink_id(link_to_short):
  url = "https://api-ssl.bitly.com/v4/bitlinks/{0}".format(link_to_short)
  response = requests.get(url, headers=HEADERS)
  response.raise_for_status()
  response_dict = response.json()
  bitlink_id = response_dict['id']
  return bitlink_id

def get_parser():
  parser = argparse.ArgumentParser(
	description='Скрипт выполняет сокращение ссылки (битлинк) либо показывает количество переходов по битлинку')
  parser.add_argument('parser_link', help='Ссылка для сокращения')
  return parser
  args = parser.parse_args()
  parser_link = args.parser_link
  return parser_link

if __name__ == "__main__":
  args = get_parser().parse_args()
  link = args.parser_link
  if link.startswith("http://") or link.startswith("https://"):
    short_link = shorten_link(link)
    print("Сокращенная ссылка:", short_link)
  elif link == get_bitlink_id(link):
    total_clicks = count_link_clicks(link)
    print("Количество переходов по ссылке:", total_clicks)
  else:
    print("Некорректная ссылка")

