import requests, json, re, os, sys
import zstandard as zstd

#from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')
# session = requests.session()
# 网站的域名
url = os.environ.get('URL')
# 配置用户名（一般是邮箱(换行)密码）
user_name = os.environ.get('UN')
password = os.environ.get('PW')

login_url = '{}/login/'.format(url)
check_url = '{}/mod/sing_in.php'.format(url)
task_page_url = '{}/task.php'.format(url)

def sign(user,pwd):
    
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "cookie": "_safe=PqndvTcraOCvF7Aa; kt_lang=zh; deviceId=dev_svk445tgtj; kt_tcookie=1; cw_conversation=eyJhbGciOiJIUzI1NiJ9.eyJzb3VyY2VfaWQiOiIwZmVjZmY2NS02Yjc2LTQ0NjItODQ4NC0wZmVjMGNmYzE5ZmYiLCJpbmJveF9pZCI6MTA5MzIxLCJleHAiOjE3OTQ0MDM4NTEsImlhdCI6MTc3ODg1MTg1MX0.vpHZTgUopVaF_3bFv4vcEw2Ef1Bd1OUBhro18c1ZuHs; kt_vid=056391202fa84982a161f35402b19925; server_session_afa45114=6a50d204b5630e5e2f90a57904af65b6; kt_ips=120.234.36.82%2C183.239.165.202%2C103.151.172.71; PHPSESSID=engajnqbff48381oubvhuln3v9; selectedSourceKey=Line1; kt_sid=2a73f9f830fcf886.1789635148",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": url,
        "sec-ch-ua": "\"Microsoft Edge\";v=\"153\", \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"153\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0"
    }

    data = {
        'username': user,
        'pass': pwd,
        'action': 'login',
        'email_link': '{}/email/'.format(url),
        'format': 'json',
        'mode': 'async',
    }
    data_2 = {
        'user_id': 185920,
        "action":"sign_in",
        "lang":"zh",
        'csrf_token': ''
    }
    try:
        session = requests.session()
        
        # 1. 先 GET 登录页，拿 CSRF token
        #print(f'===进登录页面...===')
        #login_page = session.get('',headers=header,)
        #soup = BeautifulSoup(login_page.text, 'html.parser')
        #print(f'===登录页面...===')
        #print(login_page.text[100])
        #raise SystemExit(1)
        #print(f'===账号进行登录...===')
        # 进行登录
        
        login_res = session.post(url=login_url,headers=header,data=data)
        print('登录结果：')
        print(login_res.status_code)
        print(login_res.reason)
        print(login_res.text)
        #print(login_res.url)           # 最终请求的地址
       # print(login_res.history)       # 重定向历史
        
        print('任务中心页面>>>login_res.headers')
        print(login_res.headers)
        
        print(f'===访问任务中心页面获取...csrf_token')
        task_page = session.get(task_page_url,headers=header,)
        print('task_page.headers:',task_page.headers.get('Content-Encoding'))
        print('status:', task_page.status_code)
        print('encoding:', task_page.encoding)
        print('content length:', len(task_page.content))
        #print('content 前200字节:', task_page.content[:200])
        print('text 前200字符:')
        #print(task_page.text[:200])
        
        #html = task_page.text[:300]
        print(task_page.url)
        print('任务中心页面>>>')
        #print(html)
        
        # 解压原始字节
        dctx = zstd.ZstdDecompressor()
        html_bytes = dctx.stream_reader(task_page.content).read()
        html2 = html_bytes.decode('utf-8', errors='replace')

        print('解压页面>>>')
       #print(html2)

        csrf_token = ''
        match = re.search(r'CSRF_TOKEN\s*=\s*"([^"]+)"', html2)
        if match:
            csrf_token = match.group(1)
            print(csrf_token)
        else:
            print('没找到 CSRF_TOKEN')
            
        
        print(f'===账号进行签到...===')
        check_res_str = session.post(url=check_url,headers=header,json={
            'user_id': 185920,
            "action":"sign_in",
            "lang":"zh",
            'csrf_token': csrf_token
        }).text
        print('签到结果：')
        print(check_res_str.encode().decode('unicode-escape'))
    except Exception as e:
        print('签到失败')
        print(e)
    print('===账号签到结束===\n')

if __name__ == '__main__':
	user = user_name
	pwd = password
	sign(user,pwd)
        
