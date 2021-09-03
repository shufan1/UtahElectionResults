import pytest
import pandas as pd
import requests
import re
import io
from scraper import build_election_list, extract_url,make_url_dict,get_juidicial,match

URL = "https://voteinfo.utah.gov/historical-election-results/"
page = requests.get(URL)
html = page.text

def test_build_election_list():
    assert build_election_list(html)[-1]== "2000 Primary Election"

def test_extract_url():
    s ='''<a href="https://voteinfo.utah.gov/wp-content/uploads/sites/42/2020/12/2020-General-Election-Canvass.pdf"data-type="URL" data-id="https://voteinfo.utah.gov/wp-content/uploads/sites/42/2020/12/2020-General-Election-Canvass.pdf">PDF</a>)  (<a href="https://voteinfo.utah.gov/wp-content/uploads/sites/42/2021/02/2020-General-Election-Statewide-Canvass.xlsx">'''
    url = extract_url(s)[0]
    assert url[-4:] =="xlsx"
    
def test_match():
    s = 'Mark McIff             Ephraim City Justice Court'
    s2 = 'Jeffrey J. Noland           2nd District -  Juvenile Court Judge '
    assert match(s) == ['Mark McIff','Ephraim City Justice Court']
    assert match(s2) == ['Jeffrey J. Noland','2nd District -  Juvenile Court Judge ']
    
