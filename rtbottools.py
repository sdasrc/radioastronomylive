from urllib.request import urlopen

def splitarr(inparr, nn):
    cc = 0 
    outarr = [] 
    while cc < len(inparr): 
        dd = cc+nn if (cc+nn)<len(inparr) else len(inparr)
        outarr.append(inparr[cc:dd]) 
        cc = dd 
        if cc == len(inparr): 
            break 
    return outarr

def getarrayfromgit(GITFILENAME):
    outputarr = []
    for line in urlopen(GITFILENAME):
        currline = line.decode('utf-8') #utf-8 or iso8859-1 or whatever the page encoding scheme is
        currline = currline.replace('\n','')
        currline = currline.lower()
        outputarr.append(currline.replace('%20%',' '))
    return outputarr
