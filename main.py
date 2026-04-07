import requests, json, re, os

# session = requests.session()
# 网站的域名
url = os.environ.get('URL')
# 配置用户名（一般是邮箱(换行)密码）
user_name = os.environ.get('UN')
password = os.environ.get('PW')

login_url = '{}/login/'.format(url)
check_url = '{}/mod/sing_in.php'.format(url)

def sign(user,pwd):
    global url
    header = {
        'origin': url,
		'Content-Type': 'application/json',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
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
        'user_id': 185920
    }
    try:
        print(f'===账号进行登录...===')
        # 进行登录
        session = requests.session()
        #login_res_str = session.post(url=login_url,headers=header,data=data)
        print('登录结果：')
		print(login_res_str.status_code)
		print(login_res_str.reason)
        print(login_res_str.text)
        
        print(f'===账号进行签到...===')
        #
        check_res_str = session.post(url=check_url,headers=header,json=data_2).text
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
        
