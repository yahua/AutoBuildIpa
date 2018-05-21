import subprocess
import os
import argparse
import json
import buildStart

commonConfig = None
projectConfig = None

def excuteCmd(cmd):
    print('cmd: %s', cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    return process.returncode



def cloneGit():
    cmd = 'git init'
    if excuteCmd(cmd) == 0:
        gitUrl = projectConfig['workSpaceGitUrl']
        cmd = 'git remote add origin %s'%(gitUrl)
        if excuteCmd(cmd) == 0:
            cmd = 'git fetch origin'
            if excuteCmd(cmd) == 0:
                branch = 'master'  #default master
                cmd = 'git checkout %s'%(branch)
                if excuteCmd(cmd) == 0:
                    return True

    return False

def pullGit():
    branch = projectConfig['branch'] #需要打包的branch
    cmd = 'git checkout %s' %(branch)
    if excuteCmd(cmd) == 0:
        cmd = 'git pull origin %s'%(branch)
        if excuteCmd(cmd) == 0:
            return True
        else:
            return False
    else:
        return False

def checkGit():
    cmd = 'git rev-parse --is-inside-work-tree'
    if excuteCmd(cmd) != 0:
        if cloneGit():
            if pullGit():
                #开始打包
                buildStart.startBag(projectConfig.get('ipaConfigFilePath'), commonConfig.get('outputPath'))
                pass
            else:
                print('git pull failure')
        else:
            print('git clone failure')
    else:
        if pullGit():
            # 开始打包
            buildStart.startBag(projectConfig.get('ipaConfigFilePath'), commonConfig.get('outputPath'))
            pass
        else:
            print('git pull failure')

def intoProjectWorkspace():
    desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
    rootWorkspace = desktop + commonConfig['workSpaceFilePath']
    folder = projectConfig['workSpaceFolder']
    projectFilePath = '%s%s' %(rootWorkspace, folder)
    if os.path.exists(projectFilePath) == False:
        #创建文件夹
        os.makedirs(projectFilePath)
    print('cd %s'%(projectFilePath))
    os.chdir(projectFilePath)
    commonConfig['outputPath'] = desktop + commonConfig.get('outputPath')
    checkGit()

def initConifg(filePath):
    jsonFilePath = filePath
    if os.path.exists(jsonFilePath) == False:
        print('there is no project config')
        return False
    with open(jsonFilePath, 'r') as load_f:
        global projectConfig
        projectConfig = json.load(load_f)
    with open('CommonConfig.json', 'r') as load_f:
        global commonConfig
        commonConfig = json.load(load_f)
    return True

if __name__ == '__main__':
    # 命令行输入
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Build the project config json file.", metavar="project config json file")
    options = parser.parse_args()
    if options.file is None:
        print('请输入要打包的项目配置json路径')
    else:
         if initConifg(options.file):
             intoProjectWorkspace()