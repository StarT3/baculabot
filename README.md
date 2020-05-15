# baculabot
Simple Bacula bot to notify when backup ends
Based in Wanderlei Huttel bash script, socks proxy added.


```
pip install pymysql
```

configure socks proxy hostname, port, username, password.

You need create a bot, to do this:

Add BotFather to your telegram :
https://telegram.me/BotFather

send /newbot

Choose a name

at end it will return the http API token.

put it in telegram.py variable BOT_ID

To get chat id

Add you new bot to your telegram and start message something with him.

Uncomment these lines in telegram.py:

```
#result = urllib2.urlopen("https://api.telegram.org/bot" + BOT_ID + "/getUpdates").read()
#print result
#sys.exit(0)
```

Run the telegram.py it will return CHAT_ID put it in your telegram.py.
delete or comment lines you have uncommented.

### Option number one - change your bacula-dir.conf Default Job to like this:

```
JobDefs {
  Name = "DefaultJob"
  Type = Backup
  Level = Differential
  Client = tralha-fd
  FileSet = "Full Set"
  Schedule = "WeeklySchedule"
  Storage = LTO6-Library
  Messages = Standard
  Pool = Daily
  SpoolAttributes = yes
  Priority = 10
  Write Bootstrap = "/var/lib/bacula/%c.bsr"
  RunScript {
     Command = "/etc/bacula/scripts/telegram.py %i"
     FailJobOnError = no
     RunsWhen = After
     RunsOnFailure = yes
     RunsOnClient = no
     RunsOnSuccess = yes
  }
}
```

### Option number two - add telegram.conf to folder bareos\bareos-dir.d\messages\:

```
Messages {
  Name = telegram
  Description = "Reasonable message delivery -- send most everything to email address and to the console."
  operatorcommand = "/usr/bin/bsmtp -h localhost -f \"\(Bareos\) \<%r\>\" -s \"Bareos: Intervention needed for %j\" %r"
  mailcommand = "python /etc/bareos/scripts/telegram.py %i"
  operator = root@localhost = mount                                 # (#03)
  mail = root@localhost = all, !skipped, !saved, !audit             # (#02)
  console = all, !skipped, !saved, !audit
  append = "/var/log/bareos/bareos.log" = all, !skipped, !saved, !audit
  catalog = all, !skipped, !saved, !audit
}
```
and change your jobs configs to use new messages type. Replace  
```
  # the message reporting
  Messages = Standart
```
with
```
  # the message reporting
  Messages = telegram
```
