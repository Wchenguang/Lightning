#-*- coding: UTF-8 -*-


import os
import re
import pickle
import pprint


datafilename = 'data.pkl'
recordfilename = 'record.pkl'
srcfilepac = 'data'

EXT_CPP = '.cpp'
EXT_C = '.c'
EXT_H = '.h'

def is_cext(filename):
    res = filename.rfind('.')
    if(-1 == res):
        return 0
    ans = filename[res:len(filename)]
    if(EXT_C == ans):
        return 1
    elif(EXT_CPP == ans):
        return 1
    elif(EXT_H == ans):
        return 1
    else:
        return 0

def GetSrcpacPath():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/' + srcfilepac

def GetSrcFilePath(filename):
    return GetSrcpacPath() + '/' + filename

def GetdataFliePath(filename):
    return os.path.abspath(os.path.dirname(__file__)) + '/' + filename

def GetRecordFilePath(filename):
    return os.path.abspath(os.path.dirname(__file__)) + '/' + filename

def GetAllSrcFilename():
    a = []
    for i in os.listdir(GetSrcpacPath()):
        if(is_cext(i)):
            a.append(i)
    return a


def GetRecord():
    recordfile = open(GetRecordFilePath(recordfilename), 'r')
    record = pickle.load(recordfile)
    pprint.pprint(record)
    recordfile.close()
    return record


def WriteRecord(newrecord):
    recordfile = open(GetRecordFilePath(recordfilename), 'w')
    pickle.dump(newrecord, recordfile)
    recordfile.close()


def GetData():
    input = open(GetdataFliePath(datafilename), 'r')
    indic = pickle.load(input)
    pprint.pprint(indic)
    input.close()
    return indic

def WriteData(oudic):
    output = open(GetdataFliePath(datafilename), 'w')
    pickle.dump(oudic, output)
    output.close()


def GetKeys(filename):
    filepath = GetSrcFilePath(filename)
    f = open(filepath,'r')
    cont = f.read()
    new_cont = cont.decode('UTF-8')
    cr = re.compile(ur'[\u4e00-\u9fa5]+')
    ctxt = cr.findall(new_cont)
    efr = re.compile(ur'\b\D\w*\b.*\([[a-zA-Z]\w*\s+\**[a-zA-Z]\w*.*]?\).*(?=\n)')
    eftxt = efr.findall(new_cont)
    eefr = re.compile(ur'\b\D\w*\b.*\(\).*(?=\n)')
    eeftxt = eefr.findall(new_cont)
    esr = re.compile(ur'\bstruct.*(?=\n)')
    estxt = esr.findall(new_cont)
    ecr = re.compile(ur'\bclass.*(?=\n)')
    ectxt = ecr.findall(new_cont)
    return list(set(ctxt + eftxt + ectxt + estxt + eeftxt))

def update(addlist, filename):
    indic = GetData()
    for i in addlist:
        if(0 == indic.has_key(i)):
            indic[i] = [filename]
        else:
            indic[i] += [filename]
            indic[i] = list(set(indic[i]))
    WriteData(indic)


def _UpdateAll():
    newrecord = GetAllSrcFilename()
    WriteRecord(newrecord)
    data = {}
    for i in newrecord:
        for j in GetKeys(i):
            if(0 == data.has_key(j)):
                data[j] = [i]
            else:
                data[j] += [i]
    WriteData(data)

def _DefaultUpdate():
    newrecord = GetAllSrcFilename()
    oldrecord = GetRecord()
    for i in newrecord:
        if(i not in oldrecord):
            update(GetKeys(i),i)
    WriteRecord(newrecord)


def GetREchar(relist,ch):
    if('*' == ch):
        relist.append('\\')
        relist.append('*')
    elif('.' == ch):
        relist.append('\\')
        relist.append('.')
    else:
        relist.append(ch)


def GetSearchReStr(key):
    rlist = []
    rlist.append('.')
    rlist.append('*')
    for i in key:
        GetREchar(rlist,i)
        rlist.append('.')
        rlist.append('*')
    return ''.join(rlist)

def _Search(key):
    data = GetData()
    if(data.has_key(key)):
        return {key:data[key]}
    r = re.compile(GetSearchReStr(key))
    ans = {}
    for i in data:
        if(re.search(r,i)):
            ans[i] = data[i]
    return ans



def init():
    if (0 == os.path.exists(GetdataFliePath(datafilename))):
        initdata = {'NULL':['NULL']}
        WriteData((initdata))
    if(0 == os.path.exists(GetSrcpacPath())):
        os.mkdir(GetSrcpacPath())
    if(0 == os.path.exists(GetRecordFilePath(recordfilename))):
        initdata = ['NULL']
        WriteRecord((initdata))





