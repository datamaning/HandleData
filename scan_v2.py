#!c:\Python27\python.exe
# filename : scandir.py
# author : liuxiang
# update : 2016/06/21
import os
import re
import collections
import re
import time
#patt=re.compile("\w+")
#counter=collections.Counter(patt.findall(open('apdcore.cpp').read()))

#for word,times in counter.most_common(1000):
    #print word,times
starttime=time.clock()
if os.path.exists(os.path.abspath('.')+"//..//Aqueryes")==False:
    os.mkdir("..//Aqueryes")
dirList=[]
def scandir(startdir):
    n=0
    os.chdir(startdir)
    for obj in os.listdir(os.curdir):
        res=r"\w+\.cpp$|\w+\.h$"
        reobj=re.compile(res)
        
        result=reobj.search(obj.strip())
        if result!=None:
            curpath=os.path.abspath('.')+"\\"+result.group()
            dirList.append(curpath)
            #print curpath
        #if obj == target:
            #print os.getcwd()+os.sep+obj
        if os.path.isdir(obj):
            scandir(obj)
            os.chdir(os.pardir)
        
startdir=raw_input("Please input startdir:")

#target=raw_input("Please input target:")
scandir(startdir)
tableList=[]
tableDic={}
dirNum=0
ffile=open(os.path.abspath('.')+"//..//Aqueryes"+"//"+startdir.lower()+"file.txt","w+")
for dirName in dirList:
    ffile.write(dirName+"\n")
    dirNum=dirNum+1
    patt=re.compile("(SELECT\\s+.*FROM\\s+.*\\s)|(INSERT\\s+.*INTO\\s.*\")|(DELETE\\s+.*FROM\\s+.*)")
    #print "(SELECT.*\\s+.*FROM\\s.*\\s)|(INSERT\\s.*INTO\\s.*\")|(SELECT\\s.*FROM\\s.*\\s)"
    counter=collections.Counter(patt.findall(open(dirName).read()))
    for word,times in counter.most_common(100):
        #print word,times,dirName
        if len(word[0])!=0:
            tmp=word[0].split(" ")
            for i in range(len(tmp)):
                tmp[i]=tmp[i].replace("\"","").upper()        
            num=tmp.count("FROM")
            start=0
            i=0
            while i<num:                
                if "FROM" in tmp:                 
                    tableIndex=tmp.index("FROM",start)                  
                    start=tableIndex+1

                    #print start
                if "%" not in tmp[tableIndex+1]:
                    if len(tmp[tableIndex+1].strip())>=2:
                        #print len(tmp[tableIndex+1]),tmp[tableIndex+1]
                        tableList.append(tmp[tableIndex+1])
                i=i+1
        if len(word[1])!=0:
            tmp=word[1].split(" ")
            for i in range(len(tmp)):
                tmp[i]=tmp[i].replace("\"","").upper()        
            num=tmp.count("FROM")
            start=0
            i=0
            while i<num:
                if "INTO" in tmp:
                    tableIndex=tmp.index("INTO")  
                if "%" not in tmp[tableIndex+1]:
                    if len(tmp[tableIndex+1].strip())>=2:
                        tableList.append(tmp[tableIndex+1])         
        if len(word[2])!=0:
            tmp=word[2].split(" ")
            tmp=word[1].split(" ")
            for i in range(len(tmp)):
                tmp[i]=tmp[i].replace("\"","").upper()        
            num=tmp.count("FROM")
            start=0
            i=0
            while i<num:
                if "FROM" in tmp:
                    tableIndex=tmp.index("FROM")
                if "%" not in tmp[tableIndex+1]:
                    if len(tmp[tableIndex+1].strip())>=2:               
                        tableList.append(tmp[tableIndex+1])
ffile.close()                    
print "���ҵ�"+str(dirNum)+"����׺��Ϊ.cpp��.h���ļ�"            
for name in tableList:
    name=name.replace("\"","")
    name=name.replace(")","")
    name=name.strip()
    name=name.upper()
    name=name.replace("\\","")
    name=name.replace("+","")
    name=name.replace("(","")
    name=name.split(";")[0]
    #print name,len(name)
    
    if tableDic.has_key(name):
         tableDic[name]=tableDic[name]+1
    else:
        tableDic[name]=1
ftable=open(os.path.abspath('.')+"//..//Aqueryes"+"//"+startdir.lower()+"table.txt","w+")
tableNum=0
for key,value in tableDic.items():
    tableNum=tableNum+1
    li="����:"+key.lower()+"          "+"���ִ���:"+str(value)+"\n"
    ftable.write(li)
    #print li
print "���ҵ�"+str(tableNum)+"�����ݱ�"
ftable.close()
f=open(os.path.abspath('.')+"//..//Aqueryes"+"//"+startdir.lower()+".txt","w+")
useNum=0
if len(tableDic)>0:
    for dirName in dirList:
        #print dirName
        fp=open(dirName,'rb').readlines()
        lineNum=0
        for line in fp:
            lineNum=lineNum+1
            res=''
            tablenum=0
            for key,value in tableDic.items():
                tablenum=tablenum+1
                if '$' in key:
                   keylist=key.split('$')
                   key=keylist[0]+"\$"+keylist[1]
                #print key
                #if key.strip()!='\.':
                #print tablenum
                if tablenum<=49:
                    res=res+'|'+'('+'.*'+key.strip()+'.*'+')'
            
            if len(res)==0:
                res=res+"|"         
            pos=res.index("|")
            res=res[pos+1:]
            
            res=str(res+'|'+res.lower())
            res.replace("//","")
            #print res
            reobj=re.compile(res)
            result1=reobj.search(line.strip())
            if result1!=None:
                #print result1.group(),dirName,lineNum
                li="ʹ��:"+result1.group().lower()+"\n"+"�ļ���:"+dirName+"       "+"�к�:"+str(lineNum)+"\n"
                useNum=useNum+1
                f.write(li)
                f.write("\n")
    f.close()    
else:
    print "û���ҵ����ݱ�"
endtime=time.clock()
print "һ����"+str(useNum)+"��ʹ�ù����ݱ�"
print "������%f s" % (endtime -starttime)
print "����ļ�����·��"+os.path.abspath('.')+"\..\Aqueryes"+"\\   "+"�鿴�ļ���"+startdir+".txt,"+startdir+"table.txt,"+startdir+"file.txt,"
