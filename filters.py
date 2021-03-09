ignoretagarr = []
for line in urllib.request.urlopen(IGNORETAGFILE):
    currline = line.decode('utf-8') #utf-8 or iso8859-1 or whatever the page encoding scheme is
    currline = currline.replace('\n','')
    ignoretagarr.append(currline.replace('%20%',' '))

blockedaccs = []
for line in urllib.request.urlopen(BLOCKUSERFILE):
    currline = line.decode('utf-8') #utf-8 or iso8859-1 or whatever the page encoding scheme is
    currline = currline.replace('\n','')
    blockedaccs.append(currline.replace('%20%',' '))

filteredkeys = []
for line in urllib.request.urlopen(BLOCKWORDFILE):
    currline = line.decode('utf-8') #utf-8 or iso8859-1 or whatever the page encoding scheme is
    currline = currline.replace('\n','')
    filteredkeys.append(currline.replace('%20%',' '))        
