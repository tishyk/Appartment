# -*- coding: utf-8 -*-
import requests
import re
import datetime

data = {'2013':{'inf_i':'100,3 98,4 102,2 102,5 103,1 97,3 97,1 101,2 100,2 100,2 98,7 100,7'.split()},
        '2014':{'inf_i':'100,5 99,7 102,7 106,1 104,3 103,6 102,7 102,6 102,4 99,3 104,2 100,0'.split()},
        '2015':{'page':'http://ukrstat.gov.ua/operativ/operativ2015/ct/icv/icv_u/icv_pm15_u.html',
                'inf_i':'102,3 104,8 110,5'.split()} }

text_2013 = '100,3 98,4 102,2 102,5 103,1 97,3 97,1 101,2 100,2 100,2 98,7 100,7'
text_2014 = '100,5 99,7 102,7 106,1 104,3 103,6 102,7 102,6 102,4 99,3 104,2 100,0'


def data_collection(year,page):
    print 'parce ukrstat website'
    month_count = 12
    if datetime.datetime.now().year==int(year):
        month_count = datetime.datetime.now().month - 1
    r = requests.get(page)
    answer = r.content.split('body>')[1]
    templ = '<font size="2">(\d{2,3},\d)</font>'
    #print re.findall(templ,answer,re.M|re.S)[datetime.datetime.now().month - 1::month_count]
    for inf_index in re.findall(templ,answer,re.M|re.S)[len(data['2015']['inf_i']):month_count]:
        print inf_index 
        data[year].setdefault('inf_i', []).append(inf_index)


# Create dict with page to ukrstat.gov.ua
for year in [str(x) for x in range(2015,2030)]:
    data.setdefault(year, {})
    page = 'http://ukrstat.gov.ua/operativ/operativ'+year+'/ct/icv/icv_u/icv_pm'+year[2:]+'_u.html'
    data[year].setdefault('page', page)
    
#Get data from ukrstat pages if need it
for year in sorted(data.keys())[2:]:
    if (datetime.datetime.now().year<=int(year) and 
        datetime.datetime.now().month - 1 <= len(data['2015']['inf_i']) ):
        break
    else:
        data_collection(year,data[year]['page'])
        
print data['2013']
print data['2014']
print data['2015']