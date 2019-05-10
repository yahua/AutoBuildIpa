#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import subprocess
import json
import uploadIpa
from datetime import datetime

outputPath = None
archivePath = None
exportOptionsPlistFilePath = None
workspace = None
project = None
scheme = None
configuration = None

def getIpaPath(exportPath):
	#获取ipa文件
	cmd = "ls %s" %(exportPath)
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(stdoutdata, stderrdata) = process.communicate()
	str1 = str(stdoutdata, 'utf-8')
	fileList = str1.split('\n')
	ipaName = ''
	for fileName in fileList:
		if re.search('.ipa$', fileName):
			ipaName = fileName
			break
	if ipaName == '':
		raise('无法获取ipa')
	ipaPath = exportPath + "/" + ipaName
	return ipaPath

def exportArchive():
	exportCmd = "xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s" %(archivePath, outputPath, exportOptionsPlistFilePath)
	process = subprocess.Popen(exportCmd, shell=True)
	process.wait()
	signReturnCode = process.returncode
	if signReturnCode != 0:
		print ('export Archive failed')
		return ''
	else:
		return outputPath

def buildProject():
	archiveCmd = 'xcodebuild -project %s -scheme %s -configuration %s archive -archivePath %s -destination generic/platform=iOS' %(project, scheme, configuration, archivePath)
	process = subprocess.Popen(archiveCmd, shell=True)
	process.wait()

	archiveReturnCode = process.returncode
	if archiveReturnCode != 0:
		print ("archive project %s failed" %(project))
	else:
		exportDirectory = exportArchive()
		if exportDirectory != "":
			pass
			ipaPath= getIpaPath(exportDirectory)
			uploadIpa.uploadIpa(ipaPath)

def buildWorkspace():
	print('clean project')
	cleanCmd = 'xcodebuild clean -workspace %s -scheme %s -configuration %s' %(workspace, scheme, configuration)
	process = subprocess.Popen(cleanCmd, shell=True)
	process.wait()

	print('pod install --verbose --no-repo-update')
	podCmd = 'pod install --verbose --no-repo-update'
	process = subprocess.Popen(podCmd, shell=True)
	process.wait()

	#生成archive文件
	print ("archivePath: " + archivePath)
	archiveCmd = 'xcodebuild -workspace %s -scheme %s -configuration %s archive -archivePath %s -destination generic/platform=iOS' %(workspace, scheme, configuration, archivePath)
	process = subprocess.Popen(archiveCmd, shell=True)
	process.wait()

	archiveReturnCode = process.returncode
	if archiveReturnCode != 0:
		print ("archive workspace %s failed" %(workspace))
	else:
		exportDirectory = exportArchive()
		if exportDirectory != "":
			pass
			ipaPath= getIpaPath(exportDirectory)
			uploadIpa.uploadIpa(ipaPath)

#打开项目路径, 修改工作目录
def openProjectPath(filePath):
	if filePath == '' or filePath == None:
		return;
	os.chdir(filePath)

#代码调用打包
def startBag(filePath, output, log):

	#上传初始化
	uploadIpa.initConfig(filePath, log)

	global exportOptionsPlistFilePath
	exportOptionsPlistFilePath = filePath + '/exportOptions.plist'

	jsonFilePath = filePath + '/ipa.json'
	with open(jsonFilePath, 'r') as load_f:
		ipaConfig = json.load(load_f)
	global scheme
	scheme = ipaConfig.get('scheme')

	global outputPath
	outputPath = output + scheme + '/' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

	global archivePath
	archivePath = outputPath + '/' + '%s.xcarchive'%(scheme)

	global workspace
	workspace = ipaConfig.get('workspace')

	global project
	project = ipaConfig.get('project')

	global configuration
	configuration = ipaConfig.get('configuration')

	if project is None and workspace is None:
		pass
	elif workspace is not None:
		openProjectPath(ipaConfig.get('projectPath'))
		buildWorkspace()
	elif project is not None:
		openProjectPath(ipaConfig.get('projectPath'))
		buildProject()


