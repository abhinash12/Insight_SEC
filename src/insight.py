
# coding: utf-8

# In[25]:


import csv
from collections import OrderedDict
import datetime


def get_duration(start, end):
    return (end-start).total_seconds()

def writeOutput(ip, line, session_duration):
    with open('output/sessionization.txt', 'a') as f:
        start_datetime = line[1].strftime("%Y-%m-%d %H:%M:%S")
        end_datetime = line[2].strftime("%Y-%m-%d %H:%M:%S")
        
        output = [ip, start_datetime, end_datetime, session_duration, str(line[-1])]
        print('output:', output)
        f.write(','.join(output)+'\n')
        
# for testing
try:
    with open('output/sessionization.txt', 'r+') as f:
        f.truncate()
except FileNotFoundError:
    pass

log = OrderedDict()
start_time = {}
first_time = True

with open('input/inactivity_period.txt', 'r') as f:
    inactivity_period = int(f.read().strip()) 

with open('input/log.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip header
    
    for line in reader:
        print('request:', line)
        ip = line[0]
        date_time = line[1] + ' ' + line[2]
        time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        max_time = time
        
        if first_time:
            min_time = time
            max_time = time
            first_time = False
        
        print('min time:', min_time)
        print('max time:', max_time)
        
        if ip not in log:
            log[ip] = [date_time, time, time, 1]
            
            if time not in start_time:
                start_time[time] = set()
            start_time[time].add(ip)
            
            duration = get_duration(min_time, max_time)
            
                
        else:
            log[ip][-2] = time
            duration = get_duration(min_time, max_time)
            print('duration:', duration)
            if duration>=inactivity_period:
                for exp_ip in start_time[min_time]:
                    if exp_ip in log and get_duration(log[exp_ip][-2], max_time)>=inactivity_period:
                        print('{}\'s session expired'.format(exp_ip))
                        session_duration = str(int(get_duration(log[exp_ip][-2], log[exp_ip][-3])+1))
                        writeOutput(exp_ip, log[exp_ip], session_duration)
                        del log[exp_ip]
                        
                        min_time += datetime.timedelta(0, 1)
                        while min_time not in start_time:
                            min_time += datetime.timedelta(0, 1)
            if ip in log:
                log[ip][-1] += 1
        
        for key in log:
            print(key, log[key])
        print()

for ip in log.keys():
    session_duration = str(int(get_duration(log[ip][-3], log[ip][-2])+1))
    writeOutput(ip, log[ip], session_duration)


# In[24]:





# In[18]:




