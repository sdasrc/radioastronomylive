'''
Set of functions to do essentials tasks needed for the retweetbot.
'''
from urllib.request import urlopen

# Split an array into several components
# Helpful since twitter only accepts a limited number of
# search arguments.
def splitarr(inparr, nn):
    cc, outarr = 0, [] 
    while cc < len(inparr): 
        dd = cc+nn if (cc+nn)<len(inparr) else len(inparr)
        outarr.append(inparr[cc:dd]) 
        cc = dd 
        if cc == len(inparr): 
            break 
    return outarr

# Retrieve arrays -- containing keywords to be ignored etc --
# from text files on a PUBLIC github repo.
# Can be generalized for any array stored only.
def getarrayfromgit(GITFILENAME):
    outputarr = []
    for line in urlopen(GITFILENAME):
        currline = line.decode('utf-8') #utf-8 or iso8859-1 or whatever the page encoding scheme is
        currline = currline.replace('\n','')
        currline = currline.lower()
        outputarr.append(currline.replace('%20%',' '))
    return outputarr
