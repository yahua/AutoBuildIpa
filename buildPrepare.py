import subprocess
import os
import sys
import argparse
import json
import buildStart

commonConfig = None
projectConfig = None

def excuteCmd(cmd):
    print('cmd: %s', cmd)
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.wait()
    return process.returncode

def logGit():
    cmd = 'git log -5'
    print('cmd: %s', cmd)
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.wait()
    stdout, stderr = process.communicate()  # 记录错误日志文件
    log = str(stdout, encoding="utf-8")
    logList = log.split('\n\n')
    uploadLogList = []
    for desc in logList:
        space = ' '
        if desc.startswith(space):
            #去除空格
            uploadLogList.append(desc.replace(' ', ''))
    commit_content = '\n'.join(uploadLogList)
    print('本次更新内容:\n', commit_content)
    return commit_content

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
                log = logGit()
                #开始打包
                buildStart.startBag(projectConfig.get('ipaConfigFilePath'), commonConfig.get('outputPath'), log)
                pass
            else:
                print('git pull failure')
        else:
            print('git clone failure')
    else:
        if pullGit():
            log = logGit()
            # 开始打包
            buildStart.startBag(projectConfig.get('ipaConfigFilePath'), commonConfig.get('outputPath'), log)
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

def initConifg(rootPath):

    commonConfigFilePath = rootPath + '/CommonConfig.json'
    with open(commonConfigFilePath, 'r') as load_f:
        global commonConfig
        commonConfig = json.load(load_f)

    jsonFilePath = rootPath + commonConfig['project']
    if os.path.exists(jsonFilePath) == False:
        print('there is no project config')
        return False
    with open(jsonFilePath, 'r') as load_f:
        global projectConfig
        projectConfig = json.load(load_f)

    return True

if __name__ == '__main__':
    # 命令行输入
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Build the project config json file.", metavar="project config json file")
    options = parser.parse_args()
    #options.file = 'Project/Fischerhaus.json'
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    if dirname is None:
        print('请输入要打包的项目配置json路径')
    else:
         if initConifg(dirname):
             intoProjectWorkspace()