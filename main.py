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

RemoteFiles = {}#远程文件数据
LocalFiles = {}#本地文件数据
IgnoreFiles = ["/Taoni/settings.py",]#忽略更新文件名列表


RemoteFolders = []#远程文件夹数据
LocalFolders = []#本地文件夹数据
IgnoreFolders = ["/.git","/.idea"]#忽略更新文件夹名列表

dir=os.getcwd()

for root,dirs,files in os.walk(dir):
    for file in files:
        AbsolutePath = os.path.join(root,file)#绝对路径
        RelativePath = AbsolutePath.replace(dir,"").replace('\\', '/')#相对路径
        if RelativePath in IgnoreFiles or CheckFolderIgnore(RelativePath,IgnoreFolders)==False:
            continue
            
        FileMD5 = GetFileMd5(AbsolutePath)
        
        LocalFiles[RelativePath] = FileMD5
    
    for folder in dirs:
        AbsolutePath = os.path.join(root,folder)#绝对路径
        RelativePath = AbsolutePath.replace(dir,"").replace('\\', '/')#相对路径
        if RelativePath in IgnoreFolders:
            continue
        
        if CheckFolderIgnore(RelativePath,IgnoreFolders):
            #print(AbsolutePath,RelativePath)
            LocalFolders.append(RelativePath)

else:
    print(LocalFolders)
    print("当前获取到本地有{FilesCount}个文件,{FolderCount}个文件夹.".format(FolderCount=len(LocalFolders),FilesCount=len(LocalFiles.keys())))
        
        