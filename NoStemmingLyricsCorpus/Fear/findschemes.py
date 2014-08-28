usrbinenv python

em algorithm for learning rhyming words and rhyme schemes with independent stanzas
sravana reddy sravanacsuchicagoedu 2011


import sys string random pickle os re
import numpy math
from collections import defaultdict
import codecs

def loadstanzasfilename
    load raw stanzas from gold standard file
    f=codecsopenfilename r utf8readlines
    stanzas=]
    for i line in enumeratef
        line=linesplit
        if i%4==0
            stanzasappendline1]
    return stanzas

def loadschemesschemefile
    load rhyme schemes from pickled file
    schemes=pickleloadopenschemefile
    for i in schemes
        schemesi]=maplambda xmapint x0]split schemesi]  remove freq and convert to list of integers
    return schemes

def getwordsetstanzas
    get all words
    words=sortedlistsetreducelambda x y x+y stanzas
    return words

def getrhymelistsstanza scheme
    transform stanza into ordered lists of rhymesets as given by rhyme scheme
    rhymelists=defaultdictlist
    for stanzaword schemeword in zipstanza scheme
        rhymelistsschemeword]appendstanzaword
    return rhymelistsvalues

def inituniformttablewords
    initialize normalized theta uniformly
    n=lenwords
    ttable=numpyzerosn n+1  
    uniprob=1floatn
    for c in rangen+1
        for r in rangen
            ttabler c]=uniprob   
    return ttable
    
def basicwordsimword1 word2
    simple measure of similarity num of letters in commonmax length
    common=00
    if word1==word2
        return 10
    for c in word1
        if c in word2
            common+=1
    return commonmaxlenword1 lenword2

def initbasicorthottablewords
    initialize probs according to simple measure of orthographic similarity
    n=lenwords
    ttable=numpyzerosn n+1 

    initialize pcr accordingly
    for r w in enumeratewords
        for c v in enumeratewords
            if cr
                ttabler c]=ttablec r]  similarity is symmetric
            else
                ttabler c]=basicwordsimw v+0001  for backoff
        ttabler n]=randomrandom  no estimate for prno history

    normalize
    for c in rangen+1
        tot=floatsumttable c]
        for r in rangen
            ttabler c]=ttabler c]tot

    return ttable

vowels=recompileiyeaou$3iyea{&qovucq0~^klm123456789wbx]
celexdir=datacelexcelexv2  change to the location of your celex directory
epwfile=celexdir+englishepwepwcd

def readcelex
    spam=maplambda xxstripsplit openepwfilereadlines
    spam=maplambda xx1] x6]replace replace  spam
    d=defaultdictlist
    for word pron in spam
        if  in pron   can only test words with at least on stressed syllable
            dword]appendpron
    return d

def isrhymed w1 w2
    check if words rhyme
    for p1 in dw1]
        extract only rhyming portion
        p1=p1split1]
        m=vowelssearchp1
        if not m
            print p1
        p1=p1mstart]
        for p2 in dw2]
            p2=p2split1]
            m=vowelssearchp2
            if not m
                print w2 p2
            p2=p2mstart]
            if p1==p2
                return true
    return false

def initperfectttablewords
    initialize normalized theta according to whether words rhyme
    d=readcelex
    
    notindict=0
    
    n=lenwords
    ttable=numpyzerosn n+1  
    
    initialize pcr accordingly
    for r w in enumeratewords
        if w not in d
            notindict+=1
        for c v in enumeratewords
            if cr
                ttabler c]=ttablec r]
            elif w in d and v in d
                ttabler c]=intisrhymed w v+0001  for backoff
            else
                ttabler c]=randomrandom
        ttabler n]=randomrandom  no estimate for prno history

    print notindict of n  words are not in celex
    
    normalize
    for c in rangen+1
        tot=floatsumttable c]
        for r in rangen
            ttabler c]=ttabler c]tot

    return ttable

def postprobschemettable words stanza myscheme
    posterior prob of a scheme for a stanza with prob of every word in rhymelist rhyming with all one before it
    myprob=10
    n=lenwords
    rhymelists=getrhymelistsstanza myscheme
    plen=lenstanza
    for rhymelist in rhymelists
        for i w in enumeraterhymelist            
            r=wordsindexw
            if i==0  first word use pwx
                myprob=myprobttabler n]
            else
                for v in rhymelisti]  history
                    c=wordsindexv
                    myprob=ttabler c]
    if myprob==0 and lenstanza30 probably underflow
        myprob=1e300
    return myprob

def eunnormpostttable words stanzas schemes rprobs
    compute posterior prob of rhymescheme for each stanza expectation step
    probs=]
    numstanzas=lenstanzas
    for i stanza in enumeratestanzas
        if i==numstanzas2
           print i
        elif i%10==0
            sysstdoutwrite
        stanzaprobs=]
        myschemes=schemeslenstanza]
        for myscheme in myschemes
            stanzaprobsappendrprobstuplemyscheme]postprobschemettable words stanza myscheme 
        probsappendstanzaprobs
    print
    return probs

def enormpostprobs
    normalize posterior probs
    normprobs=]
    for stanzaprobs in probs
        tot=sumstanzaprobs
        if tot0
            normstanzaprobs=maplambda myprob myprobtot stanzaprobs
        else
            normstanzaprobs=stanzaprobs]
        normprobsappendnormstanzaprobs
    return normprobs

def mfraccountswords stanzas schemes normprobs
    find fractional pseudocounts maximization step
    n=lenwords
    tctable=numpyzerosn n+1
    rprobs=defaultdictfloat
    for stanza stanzaprobs in zipstanzas normprobs
        myschemes=schemeslenstanza]
        for myscheme myprob in zipmyschemes stanzaprobs

            rprobstuplemyscheme]+=myprob  

            rhymelists=getrhymelistsstanza myscheme
            for rhymelist in rhymelists
                for i w in enumeraterhymelist
                    r=wordsindexw
                    tctabler n]+=myprob
                    for v in rhymelisti]+rhymelisti+1]
                        c=wordsindexv
                        tctabler c]+=myprob


    return tctable rprobs]

def mnormfractctable n rprobs
    normalize counts to get conditional probs
    ttable=numpyzerosn n+1

    for c in rangen+1
        tot=sumtctable c]
        if tot==0
            continue
        for r in rangen
            ttabler c]=tctabler c]tot

    
    totrprob=sumrprobsvalues
    for scheme in rprobs
        rprobsscheme]=rprobsscheme]totrprob
    
    
    return ttable rprobs]

def iteratettable words stanzas schemes rprobs maxsteps
    iterate steps 25 until convergence return final ttable
    numstanzas=floatlenstanzas
    dataprob = 1010
    epsilon=1
    for ctr in rangemaxsteps
        olddataprob=dataprob
        
        estep
        probs=eunnormpostttable words stanzas schemes rprobs
        
        estimate total probability
        allschemeprobs=mapsum probs

        if 00 in allschemeprobs   this may happen for very large data on large stanzas small hack to prevent
            underflows=filterlambda xx2]==00 ziprangelenstanzas stanzas allschemeprobs
            for underflow in underflows
                if lenprobsunderflow0]]==1
                    probsunderflow0]]0]=1e300
                    allschemeprobsunderflow0]]=1e300
                    print fixed underflow error on underflow1]
                else
                    print problem underflow probsunderflow0]]
        

        allschemeprobs=maplambda xmathlogx 2 allschemeprobs 
        dataprob=sumallschemeprobs

        probs=enormpostprobs  normalize

        mstep
        ttable rprobs]=mfraccountswords stanzas schemes probs
        
        check convergence
        if ctr0 and dataprobolddataprobepsilon
            break
        
        print iteration ctr  log likelihood of data dataprob

        ttable rprobs]=mnormfracttable lenwords rprobs

    error if it didn not converge
    if ctr==maxsteps1 and dataprobolddataprob=epsilon
        print warning em did not converge
    
    return ttable probs dataprob]

def showrhymesprobs stanzas schemes outfile
    write rhyme schemes at convergence
    o=codecsopenoutfile w utf8
    for stanza stanzaprobs in zipstanzas probs
        scheme with highest probability
        bestscheme=schemeslenstanza]numpyargmaxnumpyarraystanzaprobs]
        owrite joinstanza+n
        owrite joinmapstr bestscheme+nn
    oclose

def inituniformrschemes
    assign equal prob to every scheme
    rprobs={
    numschemes=floatsummaplen schemesvalues
    uniprob=1numschemes
    
    for i in schemes
        for scheme in schemesi]
            rprobstuplescheme]=uniprob

    return rprobs

def mainargs
    if lenargs=3
        print usage findschemespy golddata inittype outputfilename
        print where inittype may be u for uniform o for orthographic
        return
    
    sysstdout = osfdopensysstdoutfileno w 0  to flush buffer
    
    load stanzas and schemes
    infile=args0]
    stanzas=loadstanzasinfile 
    schemes=loadschemesallschemespickle
    print loaded files
    
    get list of words
    words=getwordsetstanzas

    initialize pr
    rprobs=inituniformrschemes

    if args1]0]==u  uniform init
        ttable=inituniformttablewords
        
        print initialized lenwords words
        finalttable finalprobs dataprob]=iteratettable words stanzas schemes rprobs 100
    
    elif args1]0]==o  init based on orthographic word sim
        ttable=initbasicorthottablewords
        print initialized lenwords words
        finalttable finalprobs dataprob]=iteratettable words stanzas schemes rprobs 100

    elif args1]0]==p  init based on rhyming definition
        ttable=initperfectttablewords
        print initialized lenwords words
        finalttable finalprobs dataprob]=iteratettable words stanzas schemes rprobs 100
        
    write rhyme schemes
    showrhymesfinalprobs stanzas schemes args2]
    print wrote result

if name==main
    mainsysargv1]