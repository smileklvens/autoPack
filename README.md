# autoPack 
一步解决360加固后[Walle](https://github.com/Meituan-Dianping/walle)渠道和签名信息丢失的问题。

官方给出的方案是:==先加固没签名的包，然后用buildtool中的apksigner签名（有同学反馈24不可以，25.0.0就可以了），然后用walle注入渠道==

```
在此就是用python实现了这些步骤： 
1、利用android sdk的build-tools下面的zipalign和apksigner进行对其并签名
2、利用CheckAndroidSignature检查签名、walle-cli-all写入渠道信息
```

----------

# 用法：

- 修改 config.py 文件，主要填写 keystore 信息和sdk安装路径配置和 app 名字
- 在channel文件中定义渠道信息
- 将已经加固好的包放到该脚本工具根目录下，注意不能使用加固工具签名（否则会报SignatureNotFoundException: No APK Signing Block before ZIP Central Directory）
- 运行命令 `python pack.py`,即可自动生成所有渠道包

# 注意事项

如果报错，可查看输出日志，整体分为4步

```
zipalign 4 " + protectedSourceApkPath + " " + zipalignedApkPath
apksigner sign --ks
java -jar CheckAndroidSignature.jar
java -jar walle-cli-all.jar batch -f
```
可按照日志一个个修改
 

# 感谢
[walle](https://github.com/Meituan-Dianping/walle)

[ProtectedApkResignerForWalle](https://github.com/Jay-Goo/ProtectedApkResignerForWalle)



