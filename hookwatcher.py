import requests
import browser_cookie3

domain = 'localhost'
port = '3059'
host = 'http://%s%s' %(domain, (':%s'%(port) if port else ''))

auth_cookies = {}
cookies_jar = browser_cookie3.load()

# find session cookie
for cookie in cookies_jar:
    if cookie.domain == domain:
        auth_cookies[cookie.name] = cookie.value

# format header cookie string
header_cookie_str = ''
for key, value in auth_cookies.items():
    header_cookie_str += '%s=%s; ' %(key, value)

headers = {'Cookie': header_cookie_str}

# search webhooks
def get_hooks():
    url = '%s/financeiro/atual/dashboard/webhooks'%(host)
    r = requests.get(url = url, headers = headers)
    return r.json()

# process webhooks
def process_hooks():
    url = '%s/financeiro/atual/cron/webhooks'%(host)
    params = {'forcarProcessamento': '1'}
    r = requests.get(url = url, headers = headers, params = params)
    return r.json()

# check for existing webhooks and process it
def watch():

    print("Watching...")

    data = get_hooks()
    status = int(data.get('status'))

    # status check
    if status == 200:

        data_result = data.get('data')

        # process webhooks
        if int(data_result.get('criando')) > 0:
            print('Processando %s webhooks...' %(data_result.get('criando')))
            process_hooks()
            print('Itens processados!')

    elif status == 401:
        print('Voce nao esta logado')
    else:
        print('Nao foi possivel comunicar com o sistema')

# init
watch()
