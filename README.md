# AutoBuildIpa
利用python自动打包

## 打包命名
python3 buildPrepare.py -f Project/TestProject.json

TestProject.json为打包的项目配置，需要手动配置
"workSpaceFolder":"TestProject",    --拉取下来的项目文件夹名称
"workSpaceGitUrl":"https://github.com/yahua/TestAutoBuildIpa.git",   --仓库地址
"branch":"master",    --打包的分支
"ipaConfigFilePath":"ipaConfig/debug/"   --打包的配置路径

## buildPrepare.py
拉去git仓库，更新最新代码

## buildStart.py
使用xcodebuild开始打包

## uploadIpa.py
上传ipa到蒲公英，暂时只支持蒲公英的上传
