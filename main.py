import requests, json, re, os

# session = requests.session()
# 网站的域名
url = os.environ.get('URL')
# 配置用户名（一般是邮箱(换行)密码）
config = os.environ.get('CONFIG')


login_url = '{}/login'.format(url)
check_url = '{}/mod/sing_in.php'.format(url)

def sign(order,user,pwd):
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
                check_res_str = session.post(url=check_url,headers=header).text
                print(check_res_str)
				print('===账号签到结束===\n')
				
				
if __name__ == '__main__':
        configs = config.splitlines()
        if len(configs) %2 != 0 or len(configs) == 0:
                print('配置文件格式错误')
                exit()
        user_quantity = len(configs)
        # user_quantity = user_quantity // 2
        print(f'cfg length：{user_quantity}')
        for i in range(0,user_quantity,2):
                user = configs[i]
                pwd = configs[i+1]
                sign(i,user,pwd)
        
