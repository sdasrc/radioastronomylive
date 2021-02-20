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
