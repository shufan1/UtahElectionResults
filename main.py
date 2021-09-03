from fastapi import FastAPI
import pandas as pd
import requests
from scraper import build_election_list, extract_url,make_url_dict

import uvicorn

app = FastAPI()


URL = "https://voteinfo.utah.gov/historical-election-results/"
page = requests.get(URL)
html = page.text



@app.get("/")
async def root():
    return {"message": [{
        "What this does":"Retrive available Utah state election results in xlsx form from https://voteinfo.utah.gov/historical-election-results/",
        "List": "root_url/list will list all the available election data on the offcial webste", 
        "How": "after root url type '/get/election_name',e.g. '/2020 General'. Find acceptable election_name on root_url/list"}]
    }
    
@app.get("/list")
async def list():
    list = build_election_list(html)
    return {"Election Results List": list}
        
@app.get("/get/{election_name}")
async def get(election_name) :
    url_df = make_url_dict(html)
    url = url_df.loc[url_df['election']==election_name]['url'] 
    return {"result":[{
        "election": election_name,
        "url": url}]
    }
    

    
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
