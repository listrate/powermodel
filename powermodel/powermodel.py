import os
import pandas as pd
import datetime
import csv
import re
import calendar
import numpy as np
import json

H5_FOLDER = os.path.join(os.getcwd(),'data/h5')

def parse(csv_file, session_id,file_type):
    #VEC validation
    #only powercor files are supported
    
    #if session/hash exists - skip
    if os.path.exists(H5_FOLDER + '/' + session_id + '.h5'):
        return

    #validate csv
    if (validate(csv_file,'powercor')):
        csv_data = pd.read_csv(csv_file, usecols=[1, 2, 4, 7], header=None,
        names=['date', 'time', 'meter', 'usage'])
        csv_data['date'] = pd.to_datetime(csv_data['date'], format='%d/%m/%Y')
        csv_data['date'] = pd.DatetimeIndex(csv_data['date'])
        csv_data['dayofweek'] = csv_data['date'].map(lambda x: x.weekday())
        csv_data['time'] = csv_data['time'].map(
            lambda x: datetime.timedelta(hours=datetime.datetime.strptime(x, '%H:%M').hour,
                                         minutes=datetime.datetime.strptime(x, '%H:%M').minute))
        csv_data['date'] = csv_data['date'] + csv_data['time']
        csv_data['weekno'] = csv_data['date'].map(lambda x: x.date().isocalendar()[1])
        del csv_data['time']
        csv_grouped_data = csv_data.groupby(csv_data['date'].dt.date).sum().reset_index()
        csv_grouped_data['date'] = pd.DatetimeIndex(csv_grouped_data['date'])
        csv_grouped_data['dayofweek'] = csv_grouped_data['date'].map(lambda x: x.weekday())
        csv_grouped_data['weekno'] = csv_grouped_data['date'].map(lambda x: x.date().isocalendar()[1])
        hdf_store = pd.HDFStore(H5_FOLDER + '/' + session_id + '.h5')
        hdf_store.put('master', csv_data, format='table', append=False)
        hdf_store.put('grouped', csv_grouped_data, format='table', append=False)
        hdf_store.close()


def validate(csv_file, file_type):
    # get the first row
    firstrow = []
    with open(csv_file,'r') as csvfile:
        csv_file_reader = csv.reader(csvfile,delimiter=',')
        firstrow = next(csv_file_reader)
    
    if file_type == 'powercor':
        #check column 1,2,4,7

        #first check for 12 columns
        if len(firstrow) != 12:
            return False
        
        #check date format for column 1
        if not bool(re.match(r'\d\d\/\d\d\/\d\d\d\d',firstrow[1])):
            return False
        
        #check time format for column 2
        if not bool(re.match(r'\d\d:\d\d',firstrow[2])):
            return False
        
        #check meter/consumption column
        #skipped due to not currently used

        #check usage column
        isfloat = None
        try:
            float(firstrow[7])
            isfloat = True
        except:
            isfloat = False
        
        if isfloat is False:
            return False
        
        return True
    
def generateHeatmapData(session_id):
    path = os.path.join(H5_FOLDER,session_id+'.h5')

    grouped = pd.read_hdf(path,key='grouped')
    uniqueyears = list(grouped['date'].dt.year.unique())
    monthyearbreakdowns = []
    yvalues = []
    xval = [x for x in range(1,32)]

    for year in uniqueyears:
        for month in range(1,13):
            value = []
            yvalue = str(calendar.month_name[month]) + "/" + str(year)
            for day in calendar.Calendar().itermonthdays(year,month):
                if day == 0: 
                    continue
                dayval = grouped[(grouped['date'].dt.date == datetime.date(year,month,day))]['usage'].sum()
                value.append(dayval)
            if (len(value) > 0 and not all (item == np.float64(0) for item in value)):
                monthyearbreakdowns.append(list(value))
                yvalues.append(yvalue)
    monthyearbreakdowns.reverse()
    yvalues.reverse()
    data = {'x': xval,'y': yvalues, 'z': monthyearbreakdowns, 'type':'heatmap'}
    return data

def generateweekdayweekendData(session_id):
    path = os.path.join(H5_FOLDER,session_id+'.h5')

    grouped = pd.read_hdf(path,key='grouped')
    yvalues = [grouped[(grouped['dayofweek']>= 0) & (grouped['dayofweek'] <= 4)].mean()['usage'],grouped[(grouped['dayofweek'] >= 5) & (grouped['dayofweek'] <=6)].mean()['usage']]
    xvalues = ['Weekdays','Weekend']

    data = {'x': xvalues, 'y': yvalues, 'type': 'bar'}
    return data

def generatedaybreakdown(session_id):
    path = os.path.join(H5_FOLDER,session_id+'.h5')

    grouped = pd.read_hdf(path,key='grouped')
    dayvalues = []
    for day in range(0,7):
        dayvalue = grouped[(grouped['dayofweek'] == day)]
        dayvalues.append(dayvalue['usage'].mean())
    data = {'x': list(calendar.day_name), 'y': dayvalues, 'type': 'bar'}
    return data

def generatetimeofdaybreakdown(session_id):
    path = os.path.join(H5_FOLDER,session_id+'.h5')
    master = pd.read_hdf(path,key='master')
    uniqueyears = list(master['date'].dt.year.unique())
    #scatter with morning (00:00 to 12:00)/afternoon (12:30 to 18:00)/night (18:30 to 23:30) over months
    morningvalues = []
    afternoonvalues = []
    nightvalues = []
    xvalues=[]
    for year in uniqueyears:
        uniquemonths = list(master[(master['date'].dt.year == year)]['date'].dt.month.unique())
        for month in uniquemonths:
            monthvalues = master[(master['date'].dt.year == year) & (master['date'].dt.month == month)]
            morning = monthvalues[(monthvalues['date'].dt.time >= datetime.time(0,0)) & (monthvalues['date'].dt.time <= datetime.time(12,0))]['usage'].mean()
            afternoon = monthvalues[(monthvalues['date'].dt.time >= datetime.time(12,30)) & (monthvalues['date'].dt.time <= datetime.time(18,0))]['usage'].mean()
            night = monthvalues[(master['date'].dt.time >= datetime.time(18,30)) & (monthvalues['date'].dt.time <= datetime.time(23,30))]['usage'].mean()
            xvalue = str(calendar.month_name[month]) + "/" + str(year)
            
            monthdays = calendar.monthrange(year,month)[1]
            if not (len(monthvalues['date'].dt.date.unique()) != monthdays):
                morningvalues.append(morning)
                afternoonvalues.append(afternoon)
                nightvalues.append(night)
                xvalues.append(xvalue)
    
    datalist = []
    morninggraphdata = {'x': xvalues, 'y': morningvalues, 'mode': 'lines+markers', 'name':'morning' }
    afternoongraphdata = {'x': xvalues, 'y': afternoonvalues, 'mode': 'lines+markers', 'name':'afternoon' }
    nightgraphdata = {'x': xvalues, 'y': nightvalues, 'mode': 'lines+markers', 'name':'night' }
    datalist.append(morninggraphdata)
    datalist.append(afternoongraphdata)
    datalist.append(nightgraphdata)
    return datalist

def generatesummarydata(session_id):
    path = os.path.join(H5_FOLDER,session_id+'.h5')
    grouped = pd.read_hdf(path,key='grouped')
    summarydata = {}
    usagestats = dict(grouped['usage'].describe())
    sortedusage = grouped.sort_values(by='usage', ascending=False)
    highestusage = flattenusagedict(sortedusage.head(1).to_dict(orient='list'))
    lowestusage = flattenusagedict(sortedusage.tail(1).to_dict(orient='list'))
    usagesum = grouped['usage'].sum()
    summarydata['session_id'] = session_id
    summarydata['usagesum'] = round(float(usagesum),3)
    summarydata['collectiondays'] = usagestats['count']
    summarydata['usageaverage'] = round(float(usagestats['mean']),3)
    summarydata['highestusage'] = highestusage
    summarydata['lowestusage'] = lowestusage
    summarydata['startdate'] = list(grouped.head(1)['date'].to_dict().values())[0]
    summarydata['enddate'] = list(grouped.tail(1)['date'].to_dict().values())[0]
    return summarydata

def flattenusagedict(usagedict):
    usagedict['date'] = usagedict['date'][0]
    usagedict['dayofweek'] = usagedict['dayofweek'][0]
    usagedict['usage'] = round(float(usagedict['usage'][0]),3)
    usagedict['weekno'] = usagedict['weekno'][0]
    return usagedict