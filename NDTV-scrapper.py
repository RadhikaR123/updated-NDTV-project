
from bs4 import BeautifulSoup
import requests
import pprint
import json


def getNDTVstories():
    rdata=[]                             # all new stories will be stored in this list
    r=1
    while r<=5:
        main_data =[]                                                        # All story of one page will be stored in this list
        url="https://www.ndtv.com/india/page-"+str(r)
        data= requests.get(url)
        soup=BeautifulSoup(data.text,'html.parser')
        main= soup.find("div",class_="lisingNews")
        news=main.findAll("div",class_="news_Itm")

        for j in main: 
            data1={}                                                #the data of 1 story will be stored in this dictionary                                      
            img=j.find("div",class_="news_Itm-img")
            if img != None:        
                data1["image"]=(img.find("a")["href"])

         
            hdng=j.find("h2", class_="newsHdng")
            if hdng != None:
                data1["hading"]=(hdng.text.strip())
            
                
            owner = j.find("span",class_="posted-by")
            if owner != None:   
                data1["owner"] = owner.find("a").text.strip()
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
                
            main_data.append(data1)            

        if main_data[0] not in rdata:      #if first story of any page is not in rdata,then it will append that page's stories in rdata
            for i in main_data:
                rdata.append(i)
            r+=1                          #after appending, next page will be executed
        else:
            break                # otherwise if that story is already in radata then loop will be terminated
    return rdata  

        

def LoadHistory():    
    with open("NDTV-news.json",'r') as f:
        oldData=json.load(f)

    return oldData


def appendData():

    old_data= LoadHistory() 

    new_data= getNDTVstories()

    j=1
    while j<len(new_data):
        if new_data[-j] not in old_data:
            old_data.insert(0,new_data[-j])
        else:
            break
        j+=1
    
        with open("NDTV-news.json","a") as file:
            json.dump(old_data,file,indent=2)

appendData()                                          #execution of the code will be started from here..(appendData function)







