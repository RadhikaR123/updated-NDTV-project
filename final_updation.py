from cgitb import text
from bs4 import BeautifulSoup
import requests
import pprint
import json
import os
                                    # code will start execution from the last "appendData" function
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
            
        dt1=[]
        non1= main.findAll("span",class_="posted-by")
        for date in non1:
            if date != None:
                dt1.append(date.text.strip())
        main_dt=[]
        st=""
        for dt in dt1:
            for i in dt:
                if i=="|":
                    st=""
                else:
                    st+=i
            c=0
            str1=""
            for i in st:
                if i==",":
                    c+=1
                    if c==2:
                        break
                else:
                    str1+=i
            main_dt.append(str1)   


        dtl=[]
        for detail in main.findAll("p",class_="newsCont"):
            dtl.append(detail.text)
            

        for i in range(0,len(dtl)):
            data1={}
            data1["imageurl"]=image[i]
            data1["heading"]=hading[i]
            data1["ownername"]=ownr[i]
            data1["date"]=main_dt[i]
            data1["details"]=dtl[i]
            
            
            main_data.append(data1)                 
   
    return main_data               #this will return all 5 page's data


def getNewStories():

    rdata = LoadHistory()           #will take thw returns of loadHistory function into "rdata" variable
    mainData = []
    r=1
    while r<=5:
                                                                    
        url="https://www.ndtv.com/india/page-"+str(r)
        data= requests.get(url)
        soup=BeautifulSoup(data.text,'html.parser')
        main= soup.find("div",class_="lisingNews")
        news=main.findAll("div",class_="news_Itm")
        index=0
        for j in main:                  #each "j" includes every stories all type of information.
            
            check_heading= (j.find("h2", class_="newsHdng"))           #''' it will check each page's each story' heading, untill it doen't exist in rdata(history)'''
            if check_heading != None:                                   
                chckHdng=check_heading.text.strip()
            
            if rdata[index]["heading"]== chckHdng:                      # if any story's data exists in rdata then it will break the crowling there.
                break
            else:
                data1={}                                                 #else will crowl for the next story
                
                hdng=j.find("h2", class_="newsHdng")
                if hdng != None:
                    data1["heading"]=(hdng.text.strip())
                                
                img=j.find("div",class_="news_Itm-img")
                if img != None:        
                    data1["imageurl"]=(img.find("a")["href"])
                    
                owner = j.find("span",class_="posted-by")
                if owner != None:   
                    data1["ownername"] = owner.find("a").text.strip()
                else:
                    continue    

                date= j.find("span",class_="posted-by")
                if date != None:
                    dt1 = date.text.strip()
                    main_dt=""
                    st=""
                    for dt in dt1:
                        for i in dt:
                            if i=="|":
                                st=""
                            else:
                                st+=i
                        c=0
                        str1=""
                        for i in st:
                            if i==",":
                                c+=1
                                if c==2:
                                    break
                            else:
                                str1+=i
                    data1["date"]= str1 

                detail = j.find("p",class_="newsCont")
                if detail != None:
                    data1["details"] = detail.text
                    
                mainData.append(data1)            
            index+=1
        r+=1
    return mainData   
            
             

def LoadHistory():
    file = os.path.exists("ndtv_news.json")            #for the first execution when the json file is not exists,it will return false
    if file== False:
        oldData= getNDTVstories()                      #if file doesn't exists, it will call "getNDTVstories" ,which will return all 5 page's data
                                                         #and take data from there in oldData variable
    else:
        with open("ndtv_news.json",'r') as f:       #if file exists then it will load that into same oldData variable.
            oldData = json.load(f)

    return oldData                             #finally will return old stories




def appendData():
    
    old_data=LoadHistory()

    new_data= getNewStories()                  

    j=1
    while j<=len(new_data):
        if new_data[-j] not in old_data:
            old_data.insert(0,new_data[-j])
        else:
            break
        j+=1
    
    with open("ndtv_news.json","w") as file:
        json.dump(old_data,file,indent=2)


appendData()

