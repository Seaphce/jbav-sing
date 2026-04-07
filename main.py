import requests, json, re, os

# session = requests.session()
# 网站的域名
url = os.environ.get('URL')
# 配置用户名（一般是邮箱(换行)密码）
user_name = os.environ.get('UN')
password = os.environ.get('PW')

login_url = '{}/login'.format(url)
check_url = '{}/mod/sing_in.php'.format(url)

def sign(user,pwd):
    global url
    header = {
        'origin': url,
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
    try:
        print(f'===账号进行登录...===')
        # 进行登录
        session = requests.session()
        login_res_str = session.post(url=login_url,headers=header,data=data).text
        print(login_res_str)
        response = json.loads(login_res_str)
        print('1-登录完成')
        #
        check_res_str = session.post(url=check_url,headers=header,data={"user_id": 185920}).text
        print(check_res_str)
    except Exception as e:
        content = '签到失败'
        print(e)
    print('===账号签到结束===\n')

if __name__ == '__main__':
	user = user_name
	pwd = password
	sign(user,pwd)
        
