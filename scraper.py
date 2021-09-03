#from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import io
import numpy as np

URL = "https://voteinfo.utah.gov/historical-election-results/"
page = requests.get(URL)
html = page.text

type = {"Gen": "General",
        "General": "General",
        "Pri": "Primary",
        "Primar": "Primary",
        "Primary": "Primary",
        "Presidential Primar": "Presidential Primary"}

def extract_url(html):
    pattern = r'''https:\/\/(?:elections|voteinfo).utah.gov\/.(?:(?!.pdf).)+?xlsx?'''
    pdf_url = re.findall(pattern,html)
    return pdf_url

def build_election_list(html):
    url_list = extract_url(html)
    pattern = r"(?<!Default\/)(?<=\/)\d{4}[-|\%20]*?[^\d]*?(?:General|Primar|Gen|Pri)"
    election_list = list(map(lambda url: re.findall(pattern,url)[0],url_list))
    pattern2 = r"\d{4}|[A-Za-z]+"
    election_name  = list(map(lambda s: " ".join(re.findall(pattern2,s)),election_list))
    election_name = list(map(lambda s: s[:5]+type[s[5:]]+" Election",election_name))
    return election_name

def make_url_dict(html):
    election_name = build_election_list(html)
    xlsx_url = extract_url(html)
    df = pd.DataFrame({'election': election_name,'url': xlsx_url})
    return df


# df = build_election_list()
# print(df)
# url= 'https://voteinfo.utah.gov/wp-content/uploads/sites/42/2020/04/2020-Presidential-Primary-Election-State-Canvass.pdf'
# r = requests.get(url)
# f = io.BytesIO(r.content)
# reader = PyPDF2.pdf.PdfFileReader(f)

url = "https://voteinfo.utah.gov/wp-content/uploads/sites/42/2021/02/2020-General-Election-Statewide-Canvass.xlsx"
url2= "https://voteinfo.utah.gov/wp-content/uploads/sites/42/2021/02/2020-Primary-Election-State-Canvass.xlsx"


def get_juidicial(url):
    try:
        df = pd.read_excel(url,sheet_name="Judicial") 
        pattern = r"^(?!\d{4})(?:(?!Unnamed).)+?.+$"
        candidate_position = list( map(lambda x: re.match(pattern,x),df))
        candidate_position =  [i[0] for i in candidate_position if i is not None]
        df = list(map(lambda s:match(s),candidate_position))
        df = np.array(df)
        name = df[:,0]
        position = df[:,1]
        return (pd.DataFrame({'Candidate':name,'Office':position}))
        
    except:
         return ("No judicial offices were elected in this election")
        
def match(name_position):
    match = re.split(r'\s{5,}|,', name_position)
    return match
    
    
#url3 = "https://elections.utah.gov/Media/Default/2018%20Election/2018%20General%20Election%20Canvass.xlsx"


url = "https://elections.utah.gov/Media/Default/2016%20Election/2016%20Primary%20Election%20State%20Canvass.xlsx"