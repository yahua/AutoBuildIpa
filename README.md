# AutoBuildIpa
利用python自动打包 

生成可执行文件 pyinstaller -F buildPrepare.py

#使用方式
拷贝Project/Car文件到任意目录

##配置
参考Project/Car文件夹


project.json为打包的项目配置，需要手动配置
"workSpaceFolder":"TestProject",    --拉取下来的项目文件夹名称
"workSpaceGitUrl":"https://github.com/yahua/TestAutoBuildIpa.git",   --仓库地址
"branch":"master",    --打包的分支
"ipaConfigFilePath":"ipaConfig/debug/"   --打包的配置路径


