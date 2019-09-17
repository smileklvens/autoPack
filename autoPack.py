#coding=utf-8

# /**
#  * ================================================
#  *  update by zlk
#  * ================================================
#  */

import os
import sys
import config
import platform



#判断当前系统
def isWindows():
  sysstr = platform.system()
  if("Windows" in sysstr):
    return 1
  else:
    return 0

#兼容不同系统的路径分隔符
def getBackslash():
	if(isWindows() == 1):
		return "\\"
	else:
		return "/"


# 清空临时资源
def cleanTempResource():
  try:
    os.remove(zipalignedApkPath)
    os.remove(signedApkPath)
    pass
  except Exception:
    pass
 
  # 清空渠道信息
def cleanChannelsFiles():
  try:
    os.makedirs(channelsOutputFilePath)
    pass
  except Exception:
    pass

# 创建Channels输出文件夹
def createChannelsDir():
  try:
    os.makedirs(channelsOutputFilePath)
    pass
  except Exception:
    pass

 #当前脚本文件所在目录
parentPath = path = os.path.dirname(os.path.realpath(__file__)) + getBackslash()

#config
libPath = parentPath + "lib" + getBackslash()
buildToolsPath =  config.sdkBuildToolPath + getBackslash()
keystorePath = config.keystorePath
keyAlias = config.keyAlias
keystorePassword = config.keystorePassword
keyPassword = config.keyPassword
channelsOutputFilePath = parentPath + "channels"
channelFilePath = parentPath +"channel"
protectedSourceApkPath = parentPath + config.protectedSourceApkName


zipalignedApkPath = protectedSourceApkPath[0 : -4] + "_aligned.apk"
signedApkPath = zipalignedApkPath[0 : -4] + "_signed.apk"

# 创建Channels输出文件夹
createChannelsDir()
#清空Channels输出文件夹
cleanChannelsFiles()
#清空临时文件
cleanTempResource()
# 以下重点 
os.chdir(buildToolsPath)
#对齐
zipResult = os.system("zipalign 4 " + protectedSourceApkPath + " " + zipalignedApkPath)
if zipResult == 0:
    print("zipalign success")
else:
    print("zipalign failed")
    exit(1)
#签名
signShell = "apksigner sign --ks "+ keystorePath + " --ks-key-alias " + keyAlias + " --ks-pass pass:" + keystorePassword + " --key-pass pass:" + keyPassword + " --out " + signedApkPath + " " + zipalignedApkPath
print(signShell)
signResult = os.system(signShell)
if signResult == 0:
    print("sign success")
else:
    print("sign failed")
    exit(1)

os.chdir(libPath)
#检查V2签名是否正确
checkResult = os.system("java -jar CheckAndroidSignature.jar "  + signedApkPath)
if checkResult == 0:
    print("check sign success")
else:
    print("check sign failed")
    exit(1)
#写入渠道
writeChannelShell = "java -jar walle-cli-all.jar batch -f " + channelFilePath + " " + signedApkPath + " " + channelsOutputFilePath
print(writeChannelShell)
channelResult = os.system(writeChannelShell)
if channelResult == 0:
    print("build channel success，Please check channels dir")
else:
    print("build channel failed")
    exit(1)




