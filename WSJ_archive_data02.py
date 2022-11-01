#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 
import os
import pandas as pd
import numpy as np
import datetime


import warnings
warnings.filterwarnings("ignore")


# In[ ]:


# read filenames under directory
def get_filenames(directory_path = "C:/Users/Admin/Desktop/wsj_news/2022/"):
    filenames_list = []
    filenames = os.listdir(directory_path)
    for it in filenames:
        #print()
        filenames_list.append( directory_path + it )
    return sorted(filenames_list)

# read a single file
def read_file(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    content = f.readlines()
    f.close()
    return content

# wsj news: date-time, news info (topic, title, time), counter (the number of news for that day)
# read files and process as dataframe
def wsj_news_as_df(filenames_list):
    wsj_news_data = pd.DataFrame(columns = ['news_date', 'news_counter', 'news_topic', 'news_title', 'news_time'])
    for filename in filenames_list[:]:
        content = read_file(filename)
        counter = 0
        for news in content:
            it = news.strip().split('\t')
            if len(it)==3:
                counter += 1
                news_topic, news_title, news_time = it
                news_date = filename.strip()[-10:]
                news_date = datetime.datetime.strptime(news_date, "%Y-%m-%d")#.strftime("%Y-%m-%d")
                each_row = {'news_date':news_date, 'news_counter':counter, 'news_topic':news_topic, 'news_title':news_title, 'news_time':news_time}
                wsj_news_data = wsj_news_data.append(each_row, ignore_index = True)
                #print( news_date, counter, news_topic, news_title, news_time )
    return wsj_news_data


# In[ ]:


which_year = 2012
filenames_list = get_filenames("C:/Users/Admin/Desktop/wsj_news/" + str(which_year) + "/")
filenames_list
wsj_news_data = wsj_news_as_df(filenames_list)
wsj_news_data.to_csv('C:/Users/Admin/Desktop/wsj_news' + str(which_year) + '.csv')
wsj_news_data["ymd_time"] = wsj_news_data['news_date'].astype(str)
wsj_news_data["year"] = wsj_news_data["ymd_time"].str.slice(0, 4)
wsj_news_data["month"] = wsj_news_data["ymd_time"].str.slice(5, 7)
wsj_news_data["day"] = wsj_news_data["ymd_time"].str.slice(8, 10)
wsj_news_data

