import requests
import json

class FirUploadInfo:
    downloadUrl = ''
    log = ''
    ipaName = ''
    ipaBuild = ''
    ipaVersion = ''
    bundle_id = ''
    ipaRelease_type = 'Adhoc' #打包类型，只针对 iOS (Adhoc, Inhouse)（上传 ICON 时不需要）
    appsUrl = ''
    type = ''
    api_token = ''
    def __init__(self, config):
        self.ipaName = config['ipaName']
        self.ipaVersion = config['ipa_version']
        self.ipaBuild = config['ipa_build']
        self.bundle_id = config['bundle_id']
        self.log = config['log']
        self.type = config['type']
        self.appsUrl = config['appsUrl']
        self.api_token = config['api_token']

    def parseData(self, params):
        self.uploadKey = params['key']
        self.uploadToken = params['token']
        self.uploadUrl = params['upload_url']

    def desc(self):
        return '本次更新内容：'+self.log + '\n下载地址：'+self.downloadUrl


def parseFirTokenResult(content, uploadInfo):
    resultDict = json.loads(content)
    uploadInfo.downloadUrl = 'https://fir.im/' + resultDict['short']
    uploadInfo.parseData(resultDict['cert']['binary'])

def getUploadUrl(uploadInfo):

    #headers = {'enctype': 'multipart/form-data'}
    payload = {'type': uploadInfo.type,
               'bundle_id': uploadInfo.bundle_id,
               'api_token': uploadInfo.api_token}
    print('请求fir上传url的参数：' + str(payload))
    r = requests.post(uploadInfo.appsUrl, data=payload)
    if r.status_code == 201:
        parseFirTokenResult(r.content, uploadInfo)
        return True
    else:
        return False

def uploadIpaToFir(ipaPath, config):

    uploadInfo = FirUploadInfo(config)
    if getUploadUrl(uploadInfo):
        print('获取fir upload url成功：%@', uploadInfo.uploadUrl)
    else:
        print('获取fir token失败，无法上传')
        return

    files = {'file': open(ipaPath, 'rb')}
    payload = {'key': uploadInfo.uploadKey,
               'token': uploadInfo.uploadToken,
                'x:name': uploadInfo.ipaName,
                'x:version': uploadInfo.ipaVersion,
                'x:build': uploadInfo.ipaBuild,
                'x:release_type': uploadInfo.ipaRelease_type,
                'x:changelog': uploadInfo.log}
    print('上传fir的参数：' + str(payload))
    print('上传中，请稍候。。。')
    r = requests.post(uploadInfo.uploadUrl, data=payload, files=files)
    if r.status_code == 200:
        print('上传fir成功\n' + uploadInfo.desc())
        return True
    else:
        print('上传fir失败：')
        return False