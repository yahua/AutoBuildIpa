import subprocess
import os
import sys
import buildStart

commonConfig = None


def initConifg(rootPath):

    global commonConfig
    commonConfig = {'outputPath': rootPath+'/output-ipa/'}

    # 开始打包
    buildStart.startBag(rootPath, commonConfig.get('outputPath'))

    return True

if __name__ == '__main__':

    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    if dirname is None:
        print('请输入要打包的项目配置json路径')
    else:
         initConifg(dirname)