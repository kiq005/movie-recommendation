import requests, webbrowser, os, sys, json

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
API_KEY = ""

def get_token():
	url = "https://api.themoviedb.org/3/authentication/token/new?api_key=%s"%(API_KEY)
	r = requests.get(url)
	if r.status_code == 200:
		return r.json()['request_token']
	else:
		return None

if __name__ == '__main__':
	# Get API KEY
	if len(sys.argv) == 2:
		API_KEY = sys.argv[1]
	else:
		try:
			with open(os.path.join(DIR, 'tmdb_token.json')) as file:
				data = json.load(file)
				API_KEY = data['api_token']
		except:
			pass
	if len(API_KEY) < 1:
		print("Erro ao obter API KEY")
		exit(-1)
	# Gera novo Token
	token = get_token()
	# 
	webbrowser.open('https://www.themoviedb.org/authenticate/%s'%(token))
	with open(os.path.join(DIR, 'session.json'), 'w') as file:
		json.dump({"session_token":token}, file)

