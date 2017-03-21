# -*- coding: utf-8 -*-
import os
import hashlib
import base64


def GetFileMd5(fineName, block_size=64 * 1024):#获取文件md5 支持大文件,分块读取
  with open(fineName, 'rb') as f:
    myhash = hashlib.md5()
    while True:
      data = f.read(block_size)
      if not data:
        break
      myhash.update(data)
    return myhash.hexdigest()

def CheckFolderIgnore(FolderPath,IgnoreFolders):#检测文件目录是否被忽略
    FolderSplit = FolderPath.split(r"/")
    
    for folder in IgnoreFolders:
        #print (folder,FolderPath)
        if folder in FolderPath:
            #print("目录%s被排除"%FolderPath)
            return False
    
    return True
    
    
Version = "0.01"#版本号
VersionCode = 1#版本代数

RemoteFiles = {"1.txt":"c8ca3f2054e66acf6151b678a2db39d3",'/main.py': 'c8ca3f2054e66acf6151b678a2db39d3', '/old/1.txt': 'd41d8cd98f00b204e9800998ecf8427e', '/old/2.txt': 'd41d8cd98f00b204e9800998ecf8427e'}#远程文件数据
RemoteFolders = ['/old1']#远程文件夹数据


LocalFiles = {}#本地文件数据
IgnoreFiles = ["/Taoni/settings.py",]#忽略更新文件名列表

LocalFolders = []#本地文件夹数据
IgnoreFolders = ["/.git","/.idea"]#忽略更新文件夹名列表


DiffFiles = []#有差异的文件
#DiffFolders = []#有差异的文件夹

DelFiles = []#要删除的文件 本地多出的
DelFolders = []#要删除的文件夹 本地多出的

NewFiles = []#新的文件
NewFolders = []#新的文件夹

dir=os.getcwd()

for root,dirs,files in os.walk(dir):
    for file in files:
        AbsolutePath = os.path.join(root,file)#绝对路径
        RelativePath = AbsolutePath.replace(dir,"").replace('\\', '/')#相对路径
        if RelativePath in IgnoreFiles or CheckFolderIgnore(RelativePath,IgnoreFolders)==False:
            continue
        elif RelativePath not in RemoteFiles.keys():#远程文件没有这个文件 也就是本地多出的文件
            DelFiles.append(RelativePath)
            continue
            
        LocalFileMD5 = GetFileMd5(AbsolutePath)
        
        RemoteFileMD5 = RemoteFiles[RelativePath]
        
        if LocalFileMD5 != RemoteFileMD5:#与远程文件标识不同的本地文件
            DiffFiles.append(RelativePath)
            
        LocalFiles[RelativePath] = LocalFileMD5
    
    for folder in dirs:
        AbsolutePath = os.path.join(root,folder)#绝对路径
        RelativePath = AbsolutePath.replace(dir,"").replace('\\', '/')#相对路径
        if RelativePath in IgnoreFolders:
            continue
        
        elif CheckFolderIgnore(RelativePath,IgnoreFolders):
            #print(AbsolutePath,RelativePath)
            if RelativePath not in RemoteFolders:#远程文件没有这个文件夹 也就是本地多出的文件夹
                DelFolders.append(RelativePath)
                
            LocalFolders.append(RelativePath)

else:
    NewFiles = list(set(RemoteFiles.keys()).difference(set(LocalFiles.keys())))#新的文件
    NewFolders = list(set(RemoteFolders).difference(LocalFolders))#新的文件夹
    
    #print(LocalFolders)
    print("当前获取到本地有{FilesCount}个文件,{FolderCount}个文件夹.".format(FolderCount=len(LocalFolders),FilesCount=len(LocalFiles.keys())))
    print("=与远程对比结果=")
    print("{DiffFilesCount}个改动的文件,{DelFilesCount}个文件需要移除,{DelFilesFolders}个文件夹需要移除".format(DiffFilesCount=len(DiffFiles),DelFilesCount=len(DelFiles),DelFilesFolders=len(DelFolders)))
    
    print("{NewFilesCount}个要新增的文件,{NewFoldersCount}个要新增的文件夹".format(NewFilesCount=len(NewFiles),NewFoldersCount=len(NewFolders)))
        
        
