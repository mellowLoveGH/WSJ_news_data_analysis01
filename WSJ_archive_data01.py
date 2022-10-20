import requests
from bs4 import BeautifulSoup

# reference: https://stackoverflow.com/questions/63643538/web-scraping-wsj-archive-with-bs4
# get WSJ archive news by date-time (for example, 2022-10-19)
    # the archive news only include brief info for each news: topic, title, time
def get_archive_wsj(year, month, day, page=1):
    if month<10:
        month = "0"+str(month)
    if day<10:
        day = "0"+str(day)
    year = str(year)
    month = str(month)
    day = str(day)
    url = 'https://www.wsj.com/news/archive/'
    url = url + year + "/" + month + "/" + day
    if page>1:
        url = url + "?page="+str(page)
    #
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    #
    article_data = []
    counter_news = 0
    for article in soup.select('article'):
        topic = article.span.text
        title = article.h2.text
        time = article.p.text
        if False:
            print(topic)
            print(title)
            print(time)
            print('-' * 80)
        article_data.append( (topic, title, time) )
        counter_news += 1
    print(url, counter_news)
    return article_data

# pack every day WSJ news (topic, title, time) to be a list
    # every item is one piece of news
def get_data_by_date(year, month, day):
    data_by_date = {}
    page=1
    fg = False
    for page in range(1,10):
        if fg:
            break
        try:
            article_data = get_archive_wsj(year, month, day, page)
            if len(article_data) == 0:
                fg = True
                continue
            articles_to_string = ""
            for it in article_data:
                topic, title, time = it
                articles_to_string = articles_to_string + str(topic) + "\t" + str(title) + "\t" + str(time) + "\n"
            data_by_date[page] = articles_to_string
        except:
            print('no more page', page)
    return data_by_date

# number: year, month, day -> string
    # for example: 2022, 10, 19 -> '2022-10-19'
def date_to_str(year, month, day):
    if month<10:
        month = "0"+str(month)
    if day<10:
        day = "0"+str(day)
    year = str(year)
    month = str(month)
    day = str(day)
    return year + "-" + month + "-" + day

# write every day news to a file
def write_to_file(year, month, day):
    date_time = date_to_str(year, month, day)
    f = open('wsj_news/'+date_time, 'w', encoding="utf-8")
    f.write( date_time+"\n" )
    data_by_date = get_data_by_date(year, month, day)
    ks = data_by_date.keys()
    for k in sorted(ks):
        st = data_by_date[k]
        f.write(st)
    f.close()
    return 


import datetime
def get_dates_from_range(start_date, end_dates):
    start = datetime.datetime.strptime(start_date, "%d-%m-%Y") 
    end = datetime.datetime.strptime(end_dates, "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    date_list = []
    for date in date_generated:
        date_ymd = date
        y, m, d = date_ymd.year, date_ymd.month, date_ymd.day
        date_list.append( (y, m, d)  )
    return date_list



### ----------------------------------- run from here
y1 = 2017
start_date = "01-01-"+str(y1) # dd-mm-yyyy, included
end_dates = "01-01-"+str(y1+1) # dd-mm-yyyy, not included
date_list = get_dates_from_range( start_date, end_dates )
for it in date_list:
    y, m, d = it
    year, month, day = y, m, d
    write_to_file(year, month, day)



















