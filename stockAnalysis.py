from turtle import pd
import pandas as pd
from bs4 import BeautifulSoup 
import requests
import time

def set_jobs(soup,index):

    jobs = soup.find_all('li',class_ = 'flex flex-space-between')

    heads = ['ROCE','CurrentPrice','StockP/E','EPS','Earningsyield']

    for job in jobs:
        name = job.find('span', class_ = 'name').text.replace('\n','').replace(' ','')
        value = job.find('span', class_ = 'nowrap value').text.replace('\n','').replace(' ','').replace('%','').replace('₹','').replace(',','')

        if name in heads and value != '':
            dfs.at[index, name]  = value

def get_data(code,index,client):

    #URL 1
    url='https://www.screener.in/company/'+code+'/consolidated'
    response = client.get(url,cookies={'csrftoken' : client.cookies['csrftoken'] },headers=headers)
    if(response.status_code==429):
        time.sleep(7)
        response = client.get(url,cookies={'csrftoken' : client.cookies['csrftoken'] },headers=headers)
    if(response.status_code==404):
        print(index ,response.status_code)
        return 0
        

    print(index ,response.status_code)
    html_text = response.text
    soup = BeautifulSoup(html_text,'lxml')
    set_jobs(soup , index)
    #URL2
    dataid = soup.main.div['data-warehouse-id']
    url2 = 'https://www.screener.in/api/company/'+ dataid +'/quick_ratios/'
    response = client.get(url2,cookies={'csrftoken' : client.cookies['csrftoken'] })
    if(response.status_code==429):
        time.sleep(10)
        response = requests.get(url2)
    html_text = response.text
    soup = BeautifulSoup(html_text,'lxml')
    set_jobs(soup , index)

    dfs.to_csv("Final-Con.csv", index=False)


loginurl = 'https://www.screener.in/login/?'
payload = {
    'username' : '',
    'password' : ''
}
headers = {'Referer': 'https://www.screener.in/company/AVANTIFEED/consolidated/','Accept': 'text/html'}

client = requests.session()
client.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
client.headers['Accept'] = 'text/html'


# Retrieve the CSRF token first
client.get(loginurl)  # sets cookie
if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
else:
    # older versionss
    csrftoken = client.cookies['csrf']

login_data = dict(username='ganeshrao2676@gmail.com', password='Fire@1234', csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(loginurl, data=login_data, headers=dict(Referer=loginurl))
  
dfs = pd.read_csv('Final-Con.csv')

# 3694
index = 4239
for i in range(index,len(dfs['Security Code'])):
    get_data(str(dfs['Security Code'][i]),i,client)
