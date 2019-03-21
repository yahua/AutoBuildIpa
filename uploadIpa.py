
import requests
import os
import json
import firUpload as fir

uploadLog = None

def initConfig(folder, log):

    global uploadLog
    uploadLog = log

    jsonFilePath = folder  + 'upload.json'
    if os.path.exists(jsonFilePath) == False:
        print('there is not upload config, so don\'t upload ipa')
        return
    with open(jsonFilePath, 'r') as load_f:
        emailDict = json.load(load_f)
    if emailDict is None:
        print('there is not upload config, so don\'t upload ipa')
        return

    global uploadPlatform
    uploadPlatform = emailDict.get('uploadPlatform')
    global allUploadPlatform
    allUploadPlatform = emailDict.get('uploadPlatformInfo')


def parserPgyerUploadResult(jsonResult):
    resultCode = jsonResult['code']
    if resultCode == 0:
        downUrl = 'https://www.pgyer.com/' + jsonResult['data']['buildShortcutUrl']
        print("Upload Success")
        print("DownUrl is:" + downUrl)
        return downUrl
    else:
        print("Upload Fail!")
        print("Reason:"+jsonResult['message'])
        return ''

def uploadIpaToPgyer(ipaPath, platformDict):

    print ("ipaPath:%s" % ipaPath)
    files = {'file': open(ipaPath, 'rb')}
    headers = {'enctype':'multipart/form-data'}
    payload = {'_api_key':platformDict.get('_api_key'),
             'buildInstallType':platformDict.get('buildInstallType'),
             'buildPassword':platformDict.get('buildPassword'),
             'buildUpdateDescription':uploadLog,
             'buildName':platformDict.get('buildName')}
    print(str(payload))
    print('uploading....')
    r = requests.post(platformDict.get('uploadUrl'), data=payload, files=files, headers=headers)
    print(str(r))
    if r.status_code == requests.codes.ok:
        result = r.json()
        print('result:%s' % result)
    else:
        print('HTTPError,Code:'+r.status_code)

def uploadIpa(ipaPath):
    if ipaPath is None:
        print('error ipaPath')
        return
    if uploadPlatform is None or uploadPlatform == '':
        print('not config uploadPlatform')
        return
    platformDict = allUploadPlatform.get(uploadPlatform)
    if platformDict is None or platformDict == '':
        print('can not find %s platform' % uploadPlatform)
        return
    if uploadPlatform == 'payer':
        uploadIpaToPgyer(ipaPath, platformDict)
        return

    if uploadPlatform == 'fir':
        fir.uploadIpaToFir(ipaPath, platformDict)
        return

