#################################
##### Name: Michael Payne
##### Uniqname:mpaynei
##### Final Project
#################################

from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests
import json
import sqlite3

#database with Underground Railroad Data
DB_Name = 'underground_railroad_db.sqlite'

CACHE_FILENAME = "cache.json"
CACHE_DICT = {}
BASE_URL = "https://www.nps.gov/nr/travel/underground/states.htm"


#provides the site manager contact information if they need to reach me.
headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Scraping',
    'From': 'mpaynei@umich.edu',
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


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


def build_state_site_lst():
    ''' Make a list of tuples that maps state name to site page url from
    "https://www.nps.gov/nr/travel/underground/states.htm". Each tuple is made
    up of one site. It has the state the site is located, the site name
    and the url of the site.

    Parameters
    ----------
    None

    Returns
    -------
    list
        A list of tuples with each tuple being (state name, site name, site url)
        e.g. ('colorado','Barney L. Ford Building','https://www.nps.gov/nr/travel/underground/co1.htm')
    '''
    state_site_lst = []

    site_text = make_url_request_using_cache(BASE_URL, CACHE_DICT)
    soup = BeautifulSoup(site_text, "html.parser")
    # print(soup)

    #get list of states
    searching_td = soup.find_all("td", width="287")


    for td in searching_td:

        if td.find("font",size="+2") is None:
            continue
        else:
            state_name = td.find("font",size="+2").text.lower()

            searching_a = td.find_all("a")
            # print(searching_a)

            site_lst = []
            for a in searching_a:

                name = a.text.lower().split()
                site_name = " ".join(name)
                link = a["href"]

                site_url = "https://www.nps.gov/nr/travel/underground/" + link
                site_lst.append((state_name,site_name,site_url))

            state_site_lst.append(site_lst)
    return state_site_lst


def get_site_info(site_url):
    '''Retrieves the information of a site from it's webpage.

    Parameters
    ----------
    site_url: string
        The URL for a site page e.g. ('https://www.nps.gov/nr/travel/underground/co1.htm')

    Returns
    -------
    Tuple
        a site's (name,location,description,image)
    '''
    site_text = make_url_request_using_cache(site_url, CACHE_DICT)
    soup = BeautifulSoup(site_text, "html.parser")
    # print(soup)

    #get image and Name
    name = "See States_Sites Table for Name"
    if soup.find("table", width="260") is None:
        image = "No Image Available"

    else:
        searching_page = soup.find("table", width="260")
        image = searching_page.find("img")["src"]

        # print(image)

        if "alt" not in searching_page.find("img"):
            name = "See States_Sites Table for Name"
        else:
            name = searching_page.find("img")["alt"]
            # print(name)


    location = "Location Data unavailable"
    #get Location
    if soup.find_all("i") is None:
        location = "Location Data Available"

    else:
        p_tags = soup.find_all("i")
        for item in p_tags:
            if "located" in item.text:
                txt = item.text.split()
                location = " ".join(txt)

    # print(location)


    #get Description
    replace_newline = soup.text.replace("\n","")
    txt = replace_newline.split()
    description = " ".join(txt).strip()


    return (name,location,description,image)


def create_db():
    '''Creates a database with two tables for my Underground Railroad Site data.

    Creates two tables: One called State Sites that has four columns (ID, State,
    Site_Name, and Site_URl. The other table is called Site_Info and has five columns
    (ID, Site_Name, Location, Description and Image_URL).

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    conn = sqlite3.connect(DB_Name)
    cur = conn.cursor()

    drop_states_sql = 'DROP TABLE IF EXISTS "States_Sites"'
    drop_sites_sql = 'DROP TABLE IF EXISTS "Site_Info"'

    create_states_sql = '''
        CREATE TABLE IF NOT EXISTS "States_Sites" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "State" TEXT NOT NULL,
            "Site_Name" TEXT NOT NULL,
            "Site_URL" TEXT NOT NULL
        )
    '''
    create_sites_sql = '''
        CREATE TABLE IF NOT EXISTS 'Site_Info'(
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Site_name" TEXT NOT NULL,
            "Location" TEXT NOT NULL,
            "Description" TEXT NOT NULL,
            "Image_URL" TEXT NOT NULL
        )
    '''
    cur.execute(drop_states_sql)
    cur.execute(create_states_sql)
    cur.execute(drop_sites_sql)
    cur.execute(create_sites_sql)
    conn.commit()
    conn.close()


def load_states_db(lst):
    '''Loads data from my master list of States and their associated sites.


    Parameters
    ----------
    lst
        A list of states, the names of Underground Railroad sites in that state,
        and the site's url.

    Returns
    -------
    None
    '''

    insert_states_sql = '''
        INSERT INTO States_Sites
        VALUES (NULL, ?, ?, ?)

    '''

    conn = sqlite3.connect(DB_Name)
    cur = conn.cursor()

    for item in lst:
        for elem in item:
            cur.execute(insert_states_sql,
            [
            elem[0],
            elem[1],
            elem[2]
            ]
        )
    conn.commit()
    conn.close()


def load_sites_db(lst):
    '''Loads data from my list of Underground Railroad Sites and their associated information.

    For each site, it's name, location, description and an image is loaded into
    the database.

    Parameters
    ----------
    lst
        A list of sites with their names, locations, descriptions and images.

    Returns
    -------
    None
    '''

    insert_sites_sql = '''

        INSERT INTO Site_Info
        VALUES (NULL, ?, ?, ?, ?)
    '''
    conn = sqlite3.connect(DB_Name)
    cur = conn.cursor()


    for site in lst:
        cur.execute(insert_sites_sql,
        [
        site[0],
        site[1],
        site[2],
        site[3]
        ]
    )
    conn.commit()
    conn.close()

app = Flask(__name__)

def get_results(sort_by, sort_order, source_state):
    conn = sqlite3.connect(DB_Name)
    cur = conn.cursor()

    if sort_by == 'State':
        sort_column = 'SS.State'
    else:
        sort_column = 'SS.Site_Name'

    where_clause = ''
    if (source_state != 'All'):
        where_clause = f'WHERE SS.State = "{source_state}"'

    q = f'''
        SELECT {sort_column}, SS.State, SS.Site_name,SS.Site_URL, SI.Location, SI.Description,SI.Image_URL
        FROM States_Sites as ss
            JOIN Site_Info as si
                ON SS.Id = SI.Id
        {where_clause}
        ORDER BY {sort_column} {sort_order}
    '''

    # print(q)
    results = cur.execute(q).fetchall()
    conn.close()
    # print(results)
    return results

@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/results', methods=['POST'])
def sites():
    sort_by = request.form['sort']
    sort_order = request.form['dir']
    source_state = request.form['place']
    results = get_results(sort_by, sort_order, source_state)
    # print(results)

    return render_template('results.html',
        sort=sort_by, results=results,
        source=source_state)


if __name__ == "__main__":

    master_lst = build_state_site_lst()

    site_lst = []

    for elem in master_lst:
        for site in elem:
            inst = get_site_info(site[2])
            # print(inst)
            # print("\n")
            site_name = inst[0]
            site_location = inst[1]
            site_description = inst[2]
            site_image = inst[3]
            site_lst.append([
                site_name,
                site_location,
                site_description,
                site_image,
            ])

    create_db()
    load_states_db(master_lst)
    load_sites_db(site_lst)

    app.run(debug=True)
