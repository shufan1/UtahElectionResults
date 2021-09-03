from fastapi import FastAPI
import requests
from scraper import build_election_list,make_url_dict,get_juidicial

import uvicorn

app = FastAPI()


URL = "https://voteinfo.utah.gov/historical-election-results/"
page = requests.get(URL)
html = page.text



@app.get("/")
async def root():
    return {"message": [{
        "Greeting": "Welcome",
        "What this does":"Retrive first 10 available Utah state election results in xlsx form from https://voteinfo.utah.gov/historical-election-results/",
        "List": "root_url/list_election will list all the available election data on the offcial webste", 
        "How": "after root url type '/get/election_name',e.g. '/2020 General Election'. Find acceptable election_name on root_url/list_election"}]
    }
    
@app.get("/list_election")
async def list_election():
    election_list = build_election_list(html)
    return {"Election Results List": election_list}
        
@app.get("/get/{election_name}")
async def get(election_name) :
    url_df = make_url_dict(html)
    url_df = url_df.iloc[:10]
    url = url_df.loc[url_df['election']==election_name]['url'].values[0] 
    candidate_position_df = get_juidicial(url)
    
    return {"result":[{
        "Election Name": election_name,
        "Url": url,
        "Judicial Election Results": candidate_position_df
    }]
    }
    

    
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
