# updated-NDTV-project

I have created 3 functions for different tasks.they are as-
* getNDTVstories 
* loadHistory
* appendData

#### Execution of the code

Code execution will be started from the **appendData** function.I call this function at the end of the code.
inside this function firstly **loadHistory** function will be called,which will load the json file with the whole data,which is present into it, 
and store this data into __old_data__ variable.

after that **getNDTVstories** function will be called,it will take the list with new data,and sore this data into __new_data__ variable.

after that I have runed a loop on the **new_data** , and put a if condition,which states that
if any story of new_data is not in old_data,then it will insert that story inside old_data.

and inside the loop only this data will be dumped into **NDTV-news.json** file,,which is our main file , storing all the stories.



