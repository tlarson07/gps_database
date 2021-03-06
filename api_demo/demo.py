from bewhere import *
from time import * 

## parse a string in the following format: `year month day hour minute time_zone` 
 #   year ------ '2018' include century
 #   month ----- '01' [01,12] 
 #   day ------- '01' [01,31]
 #   hour ------ '00' [00,23]
 #   minute ---- '00' [00,59] 
 #   time_zone - 'PST'           FIXME: where is this comprehensive list? who is in control of this madness
 #   EX: '2018 04 15 13 10 PST'
 #
 # returns struct_time in local time
def parseTime(timeString):
  return strptime(timeString, "%Y %m %d %H %M %Z")

def parseResponse(r):
  data = r.json()
  module = {}
  module["points"] = []
  for i in data:
    temp = {}
    temp["id"] = i["id"]
    temp["longitude"] = i["longitude"]
    temp["latitude"] = i["latitude"]
    temp["timestamp"] = i["timestamp"]
    temp["timestampLong"] = asctime(epochToLocaltime(i["timestamp"]))
    module["points"].append(temp)
  print "Number of points:", len(data) 
  return json.dumps(module, sort_keys=True, indent=4, separators=(',', ': '))

## converts struct_time in local time to milliseconds since epoch
def localtimeToEpoch(timeStruct):
  return mktime(timeStruct) * 1000

## converts milliseconds since epoch to struct_time in local time
def epochToLocaltime(epoch):
  return localtime(epoch/1000)

def dateRange(user, module, start, end): 
  stE = localtimeToEpoch(start) 
  etE = localtimeToEpoch(end)   
  st = epochToLocaltime(stE) 
  et = epochToLocaltime(etE)
  r = user.stream(module, stE, etE)
  
  print r.status_code
  print "Human Start Time (PST): ", st 
  print "Epoch Start Time (milliseconds): ", 
  print "%d" % (stE)
  print "Human End Time (PST): ", et
  print "Epoch End Time (milliseconds): ",
  print "%d" % (etE)
  print parseResponse(r)
