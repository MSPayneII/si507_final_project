#################################
##### Name: Michael Payne
##### Uniqname:mpaynei
##### Final Project
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key

"Work in progress"

CACHE_FILENAME = "cache.json"
CACHE_DICT = {}
BASE_URL = "https://www.nps.gov/nr/travel/underground/states.htm"

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()



def make_url_request_using_cache(url, cache):
    '''Check the cache for a saved result for a Site. If the result
    is found, return it. Otherwise send a new request, save it, then return it.

    Parameters
    ----------
    url: string
        The BASE_URL "https://www.nps.gov/nr/travel/underground/states.htm"
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''

    if (url in cache.keys()): # the url is our unique key
        print("Using Cache")
        return cache[url]     # we already have it, so return it
    else:
        print("Fetching")
        response = requests.get(url, headers=headers) # gotta go get it
        cache[url] = response.text # add the TEXT of the web page to the cache
        save_cache(cache)          # write the cache to disk
        return cache[url]

#provides the site manager contact information if they need to reach me.
headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Scraping',
    'From': 'mpaynei@umich.edu',
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}


state_url_dict = {}

resp = make_url_request_using_cache(BASE_URL, CACHE_DICT)
soup = BeautifulSoup(resp, "html.parser")
print(soup)
