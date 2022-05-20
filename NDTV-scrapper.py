from cgitb import text
from bs4 import BeautifulSoup
import requests
import pprint

import json

def getNDTVstories():
    main_data=[]

    for r in range(1,6):

        url="https://www.ndtv.com/india/page-"+str(r)
        data= requests.get(url)
        soup=BeautifulSoup(data.text,'html.parser')
        main= soup.find("div",class_="lisingNews")
        news=main.find("div",class_="news_Itm-cont")

        image=[]
        for img in main.findAll("div",class_="news_Itm-img"):
            image.append(img.find("a").img["src"])

        
            

        hading=[]    
        for hdng in main.findAll("h2", class_="newsHdng"):
            if hdng != None:
                hading.append(hdng.text.strip())
            


        ownr=[]
        # non=main.fNone:
        for owner in main.findAll("span",class_="posted-by"):
        # if non !=  owner in non: 
            if owner != None:   
                ownr.append(owner.a.text.strip())
            

        dt=[]
        non1= main.findAll("span",class_="posted-by")
        for date in non1:
            if date != None:
                dt.append(date.text.strip())
            


        dtl=[]
        for detail in main.findAll("p",class_="newsCont"):
            dtl.append(detail.text)
            

        for i in range(len(dtl)):
            data1={}
            data1["imageurl"]=image[i]
            data1["heading"]=hading[i]
            data1["ownername"]=ownr[i]
            data1["date"]=dt[i]
            data1["details"]=dtl[i]

            main_data.append(data1)


    return main_data

        
# x=getNDTVstories()

# with open("NDTV-news.json",'w') as file:
#     json.dump(x,file,indent=2)


def LoadHistory():
    with open("NDTV-news.json",'r') as f:
        old_data=json.load(f)

    new_data=getNDTVstories()

    j=1
    while j<=len(new_data):
        if new_data[-j] not in old_data:
            old_data.insert(0,new_data[-j])
        else:
            break
        j+=1
        
    return old_data

y= LoadHistory() 



with open("NDTV-news.json","a") as file:
    json.dump(y,file,indent=2)







