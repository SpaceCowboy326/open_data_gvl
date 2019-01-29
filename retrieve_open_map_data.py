#Retrieve map layer data from data.openupstate.org
#
#TODOS:
#   ~If implemented in browser, cache data for each layer retrieved.
#       ?Give the option to update via a button eventually?
#   
#

import requests
import time
import json
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

BASE_URL = "https://data.openupstate.org"
MAP_URL_DIRECTORY = "/map/"
geo_json_collection = {}

#Retrieve a single map category url
def retrieve_map_category_url(url):
    map_category_url = BASE_URL + url
    map_category_page = requests.get(map_category_url)
    #Don't spam the server
    plain = map_category_page.text
    s = BeautifulSoup(plain, "html.parser")
    geojson_link_anchor_list = s.select(".field--name-field-geojson-link a")
    geojson_link_anchor = ""
    if (geojson_link_anchor_list):
        geojson_link_anchor = geojson_link_anchor_list[0]
    return geojson_link_anchor.text

#Retrieve a single map category url
def retrieve_map_category_geojson_data(url):
    full_url = BASE_URL + url
    geojson_page = requests.get(full_url)
    geojson_data = ""
    if (geojson_page.status_code == 200 and geojson_page.text is not None):
        geojson_data = json.loads(geojson_page.text)
    return geojson_data


def web(page,WebUrl):
    href_list = []
    if(page>0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        #only_a_tags = SoupStrainer(".field-content a")
        count_entries = 0
        for link in s.select(".field-content a"):
        #for link in only_a_tags:
        #for link in only_a_tags.a:
            href = link.get('href')
            
            if MAP_URL_DIRECTORY in href:
                category = href.split(MAP_URL_DIRECTORY)[1]
                map_entry = {
                    'href': href,
                    'geojson_url': "/map/geojson/" + category,
                    'name': link.get_text(),
                    'category': category,
                }
                map_entry["geojson_data"] = retrieve_map_category_geojson_data(map_entry["geojson_url"])
                #skip for now
                print(map_entry)
                #map_entry['map_spreadsheet_url'] = retrieve_map_category_url(href)
                #print(map_entry)
                #href_list.append(map_entry)
                count_entries += 1
                if (count_entries > 3):
                    break
        return href_list

map_layer_url = BASE_URL + '/map-layers'
map_categories = web(1, map_layer_url)

#Retrieve map category URL
def retrieve_map_category_urls(url):
    map_layer_url = BASE_URL + 'map-layers'
    map_categories = web(1, map_layer_url)
    for map_category in map_categories:
        map_category_url = map_category
        #Don't want to spam the server too quickly
        time.sleep(5)
        map_category_page = requests.get(map_category_url)
        geojson_link_anchor = s.select(".field--name-field-geojson-link a")
        geojson_link_anchor.text



