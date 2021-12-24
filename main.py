import re
import requests
from bs4 import BeautifulSoup
import time

usrItems = {}
formItems = {
"RADIO_799044" : "正常（37.3℃）",
"RADIO_384811" : "校内",
"RADIO_907280" : "健康",
"RADIO_716001" : "健康",
"RADIO_248990" : "否"
}
keyList = [ 'usrname','password',
    'XGH_566872','XM_140773',
    'SFZJH_402404','SZDW_439708',
    'ZY_878153','GDXW_926421',
    'DSNAME_606453','PYLB_253720',
    'SELECT_172548','TEXT_91454',
    'TEXT_24613','TEXT_826040'
]


loginParms = {'IDToken0':None,'IDToken1':'usrname','IDToken2':'password',\
            'IDButton':'Submit','goto':None,\
              'encoded':'false','inputCode':None,'gx_charset':'UTF-8'}
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
headers = {'Host':'form.hhu.edu.cn','Upgrade-Insecure-Requests':'1','User-Agent':user_agent}



loginUrl = 'http://ids.hhu.edu.cn/amserver/UI/Login'
redirectUrl = 'http://form.hhu.edu.cn/pdc/form/list'
entranceUrl = 'http://form.hhu.edu.cn/pdc/formDesignApi/S/xznuPIjG'
postWidUrl = 'http://form.hhu.edu.cn/pdc/formDesignApi/initFormAppInfo'
commitPostUrl = 'http://dailyreport.hhu.edu.cn/pdc/formDesignApi/dataFormSave?wid='
getRetUrl = 'http://dailyreport.hhu.edu.cn/pdc/formDesignApi/afterSubmitForm?submitRes=true&userId='
historyUrl = 'http://dailyreport.hhu.edu.cn/pdc/formDesign/showFormFilled?selfFormWid='

def readConfig(path='./config.txt'):
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f.readlines()):
            line = line.strip('\n')
            if i < 2:
                usrItems[keyList[i]] = line
            elif i < 14:
                formItems[keyList[i]] = line

def parseHTML(data) -> dict:
    def searchKey(item) -> str:
        soup = BeautifulSoup(data, "html.parser")
        pattern = re.compile(item, re.MULTILINE | re.DOTALL)
        script = soup.find('script', text=pattern)
        if script == None:
            raise Exception('网页解析错误,请确保信息填写完整')
            return None
        return pattern.search(script.text).group(1)

    dic = {}
    dic['wid'] = searchKey(r"var _selfFormWid = '(.*?)';")
    dic['userId'] = searchKey("var _userId = '(.*?)';")
    dic['cycleDate'] = searchKey(r"var cycleDate = '(.*?)';")
    return dic

if __name__ == '__main__':
    readConfig('./config.txt')
    if len(usrItems) == 0:
        print('信息配置文件错误')
        exit(-1)

    loginParms['IDToken1'] = usrItems['usrname']
    loginParms['IDToken2'] = usrItems['password']

    sess = requests.Session()               # hold the session
    sess.post(loginUrl,data=loginParms)     # login
    sess.get(redirectUrl)                   # redirect
    resp = sess.get(entranceUrl)            # enter


    tokenDic = parseHTML(resp.text)
    sess.post(postWidUrl,data={"selfFormWid":tokenDic['wid']})      # post selfFormWid

    commitPostUrl = commitPostUrl + tokenDic['wid'] + '&userId=' + tokenDic['userId']
    formItems['DATETIME_CYCLE'] = tokenDic['cycleDate']
    resp_post = sess.post(commitPostUrl,data=formItems)             # post FormInfo

    getRetUrl = getRetUrl + tokenDic['userId'] + '&cycleDate=' + tokenDic['cycleDate']
    resp_get = sess.get(getRetUrl)


    historyUrl = historyUrl + tokenDic['wid'] + '&lwUserId=' + tokenDic['userId']
    last_resp = sess.get(historyUrl)              # last judge

    if resp_post.text.find('true')!=-1 or last_resp.text.find(tokenDic['cycleDate'])!=-1:
        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(localTime + " " + "打卡成功")
    else:
        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(localTime + " " + "打卡失败")
        exit(-1)