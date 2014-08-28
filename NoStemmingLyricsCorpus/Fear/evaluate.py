usrbinenv python

evaluate rhyme schemes against gold standard
also contains some utilities to parse data
jan 2011

import sys pickle
import numpy math string
from collections import defaultdict
import codecs

def removepuncts
    remove nonletter chars
    return joinfilterlambda c c not in stringpunctuation and c not in stringdigits s

def getwordsetpoems
    get all words
    words=sortedlistsetreducelambda x y x+y poems
    return words

def getrhymelistspoem scheme
    transform poem into lists of rhymesets as given by rhyme scheme
    rhymelists=defaultdictlist
    for poemword schemeword in zippoem scheme
        rhymelistsschemeword]appendpoemword
    return mapsorted rhymelistsvalues

patstr=liststringlowercase+stringuppercase+mapstr range50

def genpatternseed n
    generate scheme from seed
    seed=mapint seed
    if n%lenseed0
        return error
    pattern=seed]
    increment=maxseed
    while lenpatternn
        pattern+=maplambda seedunit seedunit+increment seed
        increment=maxpattern
    return mapstr pattern

def parsefilename
    read rhyme schemes and poemsstanzas
    f=maplambda xxsplit codecsopenfilename encoding=utf8readlines
    f=filterlambda line lenline==0 or line0] not in date author] f
    
    curscheme=]
    curpoemscheme=]
    stanzaschemes=]
    poemschemes=]
    curstanza=]
    poems=]
    stanzas=]
    for i line in enumeratef
        if lenline==0
            if curstanza=]
                
                if curscheme==]
                    print error no scheme read curstanza
                
                stanzasappendcurstanza
                stanzasize=lencurstanza
                
                if curscheme1]==
                    generate pattern
                    genscheme=genpatterncurscheme1] stanzasize
                    if genscheme==error
                        print error seed doesn not match i curstanza curscheme1]
                    stanzaschemesappendgenscheme
                elif lencurscheme=stanzasize
                        print error stanza size and scheme size do not match curstanza curscheme
                else
                    stanzaschemesappendcurscheme

                if curpoemscheme1]==
                    generate pattern
                    genscheme=genpatterncurpoemscheme1] stanzasize
                    poemschemesappendgenscheme
                elif lencurpoemscheme=stanzasize
                        print error stanza size and scheme size do not match curstanza curpoemscheme
                else
                    poemschemesappendcurpoemscheme
                
                curstanza=]
        
        elif line0]==rhyme
            curscheme=maplambda x strpatstrindexx+1 line11]
            if line1]==
                curschemeappend
            else
                curschemeappendstrpatstrindexline1]+1

            curpoemscheme=curscheme]  in case rhymepoem isn not specified

        elif line0]==rhymepoem
            curpoemscheme=maplambda x strpatstrindexx+1 line1]
        
        elif line0]==title
            if stanzas=]
                poemsappendstanzas
                stanzas=]
        else
            line=filterlambda xx= mapremovepunct line
            curstanzaappendline1]lower

    if curstanza=]
        stanzasappendcurstanza
        stanzaschemesappendcurscheme
        poemschemesappendcurpoemscheme
    
    poemsappendstanzas
    
    return stanzaschemes poemschemes poems]

def distschemesrhymeschemes storefile store=false
    all rhyme schemes of a given length with frequencies
    dist=defaultdictlambda  defaultdictint
    for r in rhymeschemes
        distlenr] joinr]+=1

    if not store
        return dist

    newdist={  convert to normal dict with tuple keys in order to pickle
    for l in dist
        newdistl]=]
        for r in distl]
            newdistl]appendr distl]r]
    allschemes=openstorefile wb
    pickledumpnewdist allschemes
    allschemesclose

    return dist

def savegoldstdstanzaschemes poemschemes poems filename
    write gold standard
    o=codecsopenfilename w utf8
    schemectr=0
    for pi poem in enumeratepoems
        for stanza in poem
            stanzascheme=stanzaschemesschemectr]
            poemscheme=poemschemesschemectr]
            owritepoem+strpi+ +unicode joinstanza+n
            owrite joinstanzascheme+n
            owrite joinpoemscheme+nn
            schemectr+=1
    oclose

def loadgoldfilename
    f=openfilenamereadlines
    stanzas=]
    stanzaschemes=]
    poemschemes=]
    for i line in enumeratef
        line=linesplit
        if i%4==0
            stanzasappendline1]
        elif i%4==1
            if line==]
                print error in gold i fi1] fi2]
            stanzaschemesappendline
        elif i%4==2
            poemschemesappendline            
    return stanzaschemes poemschemes stanzas]

def rhymingentropystanzaschemes stanzas
    compute entropy of rhyming pairs
    pairs=defaultdictint
    totalpairs=00
    for scheme stanza in zipstanzaschemes stanzas
        for i schemei wordi in enumeratezipscheme stanza
            for schemej wordj in zipschemei+1] stanzai+1]
                totalpairs+=1
                if schemei==schemej
                    if wordi=wordj
                        pairswordi wordj]+=1
                    else
                        pairswordj wordi]+=1
    normalize
    for pair in pairs
        pairspair]=pairspair]totalpairs
    compute entropy
    return summaplambda paircount paircountmathlogpaircount 2 pairsvalues

def schemeentropystanzaschemes stanzas
    compute entropy of rhyme schemes
    schemes=defaultdictfloat
    for scheme stanza in zipstanzaschemes stanzas
        schemestuplescheme]+=10
    normalize
    total=lenstanzaschemes
    for scheme in schemes
        schemesscheme]=schemesscheme]total
    compute entropy
    return summaplambda schemecount schemecountmathlogschemecount 2 schemesvalues

def loadresultfilename
    f=openfilenamereadlines
    stanzas=]
    schemes=]
    for i line in enumeratef
        line=linesplit
        if i%3==0
            stanzasappendline1]
        elif i%3==1
            if line==]
                print error in result i fi1] fi2]
            schemesappendline
    return schemes stanzas]

def statsrhymeschemes
    show distribution of schemes of different lengths
    dist=defaultdictlambda  defaultdictint
    for r in rhymeschemes
        distlenr] joinr]+=1
    for l in dist
        print l 
        distl=sorteddistl]items key=lambda xx1] reverse=true
        for r v in distl
            print v
        print

def comparestanzas goldschemes foundschemes
    get accuracy and precisionrecall
    total=floatlengoldschemes
    correct=00
    for g f in zipgoldschemes foundschemes
        if g==f
            correct+=1
    print accuracy correct total 100correcttotal

    for each word let rhymesetword] = set of words in rest of stanza rhyming with the word
    precision =  correct words in rhymesetword] words in proposed rhymesetword]
    recall =  correct words in rhymesetword] words in reference words in rhymesetword]
    total precision and recall = avg over all words over all stanzas
    
    totp=00
    totr=00
    totwords=00
    
    for s g f in zipstanzas goldschemes foundschemes
        stanzasize=lens
        for wi word in enumerates
            grhymesetword = setmaplambda xx0] filterlambda xx1]==gwi] ziprangewi+1 stanzasize gwi+1]
            frhymesetword = setmaplambda xx0] filterlambda xx1]==fwi] ziprangewi+1 stanzasize fwi+1]

            if lengrhymesetword==0
                continue

            totwords+=1

            if lenfrhymesetword==0
                continue
            
            find intersection
            correct=floatlengrhymesetwordintersectionfrhymesetword
            precision=correctlenfrhymesetword
            recall=correctlengrhymesetword
            totp+=precision
            totr+=recall

    precision=totptotwords
    recall=totrtotwords
    print precision precision
    print recall recall
    print fscore 2precisionrecallprecision+recall
    
def naivegoldschemes
    find naive baseline most common scheme of a given length
    dist = pickleloadopenallschemespickle
    bestschemes={
    for i in dist
        if disti]==]
            continue
        bestschemesi]=maxdisti] key=lambda xx1]0]split

    naiveschemes=]
    for g in goldschemes
        naiveschemesappendbestschemesleng]
    return naiveschemes

def lessnaivegoldschemes
    find less naive baseline most common scheme of a given length in subcorpus
    bestschemes=defaultdictlambda  defaultdictint
    for g in goldschemes
        bestschemesleng]tupleg]+=1

    m=summaplen bestschemesvalues
    
    for i in bestschemes
        bestschemesi]=listmaxbestschemesi]items key=lambda xx1]0]

    naiveschemes=]
    for g in goldschemes
        naiveschemesappendbestschemesleng]
    return naiveschemes

def mainargs
    if lenargs1 or lenargs2
        print usage evaluatepy goldfile hypothesisoutputfilename]
        return 
    
    gold=args0]    
    gstanzaschemes gpoemschemes gstanzas]=loadgoldgold

    words=getwordsetgstanzas
    n=lenwords
    
    for stanzas 
    print num of stanzas  lengstanzas
    print num of lines  summaplen gstanzas
    print num of end word types  lenwords
    print
    
    naiveschemes=naivegstanzaschemes
    print naive baseline
    comparegstanzas gstanzaschemes naiveschemes
    print

    lessnaiveschemes=lessnaivegstanzaschemes
    print less naive baseline
    comparegstanzas gstanzaschemes lessnaiveschemes
    print

    if lenargs1
        hyp=args1]
        hstanzaschemes hstanzas]=loadresulthyp
        print hyp
        comparegstanzas gstanzaschemes hstanzaschemes
        print

if name==main
    mainsysargv1]