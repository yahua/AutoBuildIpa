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
    iconDict = None
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
    uploadInfo.iconDict = resultDict['cert']['icon']

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

def uploadIconToFir(iconPath, config):
    files = {'file': open(iconPath, 'rb')}
    payload = {'key': config['key'],
               'token': config['token']}
    r = requests.post(config['upload_url'], data=payload, files=files)
    if r.status_code == 200:
        return True
    return False

def notifyToDingDing(info):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=c49c02cd22c715588795616c2a8bd884aeeacfc835bd86d522c89061b49038fc'
    content = '版本：' + info.ipaVersion + '\n更新内容：' + info.log
    data = {'msgtype': 'link',
            'link': {
                'title': 'Habibi ios包新鲜出炉了！！！',
                'text': content,
                'messageUrl': info.downloadUrl,
                'picUrl': 'https://oivkbuqoc.qnssl.com/2e57c297e946d80f2baeb1945088ae639ef9bb27?attname=Icon-1024.png&tmp=1553226455.537458'
                }
            }

    header = {'Content-Type': 'application/json'}
    data = json.dumps(data)
    res = requests.post(url, data=data, headers=header)
    print('钉钉通知')
    print(res.text)

def uploadIpaToFir(ipaPath, iconPath, config):

    uploadInfo = FirUploadInfo(config)
    if getUploadUrl(uploadInfo):
        print('获取fir upload url成功：%@', uploadInfo.uploadUrl)
    else:
        print('获取fir token失败，无法上传')
        return
    #上传图标
    print('上传icon，请稍候。。。')
    result = uploadIconToFir(iconPath, uploadInfo.iconDict)
    if result == False:
        print('上传icon，失败')
    print('上传icon，成功')

    files = {'file': open(ipaPath, 'rb')}
    payload = {'key': uploadInfo.uploadKey,
               'token': uploadInfo.uploadToken,
                'x:name': uploadInfo.ipaName,
                'x:version': uploadInfo.ipaVersion,
                'x:build': uploadInfo.ipaBuild,
                'x:release_type': uploadInfo.ipaRelease_type,
                'x:changelog': uploadInfo.log}
    print('上传fir的参数：' + str(payload))
    print('上传ipa中，请稍候。。。')
    r = requests.post(uploadInfo.uploadUrl, data=payload, files=files)
    if r.status_code == 200:
        print('上传fir成功\n' + uploadInfo.desc())
        notifyToDingDing(uploadInfo)
        return True
    else:
        print('上传fir失败：')
        return False