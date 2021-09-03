#from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import io


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
    print(url_list)
    pattern = r"(?<!Default\/)(?<=\/)\d{4}[-|\%20]*?[^\d]*?(?:General|Primar|Gen|Pri)"
    election_list = list(map(lambda url: re.findall(pattern,url)[0],url_list))
    pattern2 = r"\d{4}|[A-Za-z]+"
    election_name  = list(map(lambda s: " ".join(re.findall(pattern2,s)),election_list))
    election_name = list(map(lambda s: s[:5]+type[s[5:]]+" Election",election_name))
    # url_list = extract_url()
    # #pattern = r"\d{4}[A-Za-z ]+?(?:General|Primary)"
    # pattern = r"(?<!Default\/)(?<=\/)\d{4}[-|\%20]*?[^\d]*?(?:General|Primar|Gen|Pri)"
    # election_list = list(map(lambda url: re.findall(pattern,url)[0],url_list))
    # pattern2 = r"\d{4}|[A-Za-z]+"
    # election_name  = list(map(lambda s: " ".join(re.findall(pattern2,s)),election_list))
    # election_name = list(map(lambda s: s[:5]+type[s[5:]]+" Election",election_name))
    
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