#!/usr/bin/python
# Based in Wanderlei Huttel shell script

import sys
import urllib2
import urllib
import pymysql
import socket
import socks # you need to install pysocks (see above)

# Configuration
SOCKS5_PROXY_HOST = 'socks hostname or IP'
SOCKS5_PROXY_PORT = 8080
SOCKS5_PROXY_USER = 'put your proxy username here'
SOCKS5_PROXY_PW = 'put your proxy password here'

# Remove this if you don't plan to "deactivate" the proxy later
default_socket = socket.socket

# Set up a proxy
socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT, True,  SOCKS5_PROXY_USER,SOCKS5_PROXY_PW)
socket.socket = socks.socksocket

try:
    connection = pymysql.connect(host='localhost',
                                 user='bacula',
                                 password='',
                                 db='bacula',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
except:
    sys.exit(1)

#Fill with your data
BOT_ID = ""
CHAT_ID = ""

B_OK= u'\U00002705'
B_F = u'\U0000274C'
B_A = u'\U000026D4'


def human_readable(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixindex = 0
    while size > 1024 and suffixindex < 4:
        suffixindex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision, size, suffixes[suffixindex])

cursor = connection.cursor()

#result = urllib2.urlopen("https://api.telegram.org/bot" + BOT_ID + "/getUpdates").read()
#print result
#sys.exit(0)

try:
    jobid = int(sys.argv[1])
except:
    sys.exit(0)

sql = ("SELECT "
       "j.name as jobname, c.name as client, "
       "j.jobbytes as jobbytes, j.jobfiles as jobfiles, "
       "j.jobstatus as jobstatus, "
       "case when j.level = 'F' then 'Full' when j.level = 'I' "
       "then 'Incremental' when j.level = 'D' then 'Differential' end as level, "
       "p.name as pool, "
       "j.starttime as starttime, j.endtime as endtime, "
       "SEC_TO_TIME(TIMESTAMPDIFF(SECOND, starttime, endtime)) as duration, "
       "m.mediatype as mediatype, s.name as storage, "
       "st.jobstatuslong as status "
       "FROM Job as j "
       "INNER JOIN Pool as p on p.poolid = j.poolid "
       "INNER JOIN Client as c on c.clientid = j.clientid "
       "INNER JOIN JobMedia as jm on jm.jobid = j.jobid "
       "INNER JOIN Media as m on jm.mediaid = m.mediaid "
       "INNER JOIN Storage as s on m.storageid = s.storageid "
       "INNER JOIN Status as st on st.jobstatus = j.jobstatus "
       "where j.jobid = %d") % jobid

cursor.execute(sql)
message = ""

data = cursor.fetchone()

if not data:
    print "no data"
    sys.exit(0)

if data["JobStatus"] == "T":
    message += B_OK + " %s backup of %s %s in %s \n" % (data["Level"],data["Client"],data["JobStatusLong"],data["Duration"])

    
elif data["JobStatus"] == "A":
    message += B_A +" %s backup of %s %s \n" % (data["Level"],data["Client"],data["JobStatusLong"])
    message += "Duration  = %s\n" % data["Duration"]
    
else:
    message += B_F + " %s backup of %s %s \n" % (data["Level"],data["Client"],data["JobStatusLong"])
    message += "Duration  = %s\n" % data["Duration"]
    

messageLong += "JobName = %s\n" % data["Name"]
messageLong += "JobId = %s\n" % jobid
#message += "Client = %s\n" % data["Client"]
messageLong += "JobBytes = %s\n" % human_readable(data["JobBytes"])
messageLong += "JobFiles = %d\n" % data["JobFiles"]
messageLong += "Level = %s\n" % data["Level"]
messageLong += "JobFiles = %d\n" % data["JobFiles"]
#message += "Level = %s\n" % data["Level"]
messageLong += "Pool = %s\n" % data["Pool"]
messageLong += "Storage = %s\n" % data["Storage"]
messageLong += "StartTime = %s\n" % data["StartTime"]
messageLong += "EndTime = %s\n" % data["EndTime"]
#message += "Duration  = %s\n" % data["Duration"]
messageLong += "JobStatus = %s\n" % data["JobStatus"]
#message += "Status = %s\n" % data["JobStatusLong"]

connection.close()

#use for short messages
"""
try:
    TLMESSAGE = urllib.urlencode({"chat_id": CHAT_ID, "text": message.encode('utf-8', 'strict')})
    urllib2.urlopen("https://api.telegram.org/bot" + BOT_ID + "/sendMessage", TLMESSAGE).read()
except:
    print "could not connect to telegram"
    sys.exit(0)

message+=messageLong
"""
#for long messages
try:
    TLMESSAGE = urllib.urlencode({"chat_id": CHAT_ID, "text": message.encode('utf-8', 'strict')})
    urllib2.urlopen("https://api.telegram.org/bot" + BOT_ID + "/sendMessage", TLMESSAGE).read()
except:
    print "could not connect to telegram"
    sys.exit(0)
