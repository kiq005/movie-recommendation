import requests, webbrowser, os, sys, json

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
API_KEY = ""

def get_details(session_id):
	url = "https://api.themoviedb.org/3/account?api_key=%s&session_id=%s"%(API_KEY, session_id)
	r = requests.get(url)
	if r.status_code == 200:
		return r.json()
	else:
		print("Error:", r.status_code)
		print(r.json()['status_message'])
		return None

def get_session(session_token):
	url = "https://api.themoviedb.org/3/authentication/session/new?api_key=%s"%(API_KEY)
	body = {"request_token":session_token}
	r = requests.post(url, data=body)
	if r.status_code == 200:
		return r.json()['session_id']
	else:
		print("Error:", r.status_code)
		print(r.json()['status_message'])
		return None
	

def get_ranked(user_id, session_id):
	rank = []
	p_num = 1
	while True:
		url = "https://api.themoviedb.org/3/account/%s/rated/movies?api_key=%s&session_id=%s&page=%d"%(user_id, API_KEY, session_id, p_num)
		r = requests.get(url)
		if r.status_code == 200:
			if len(r.json()['results']) > 0:
				for movie_data in r.json()['results']:
					rank.append({'title':movie_data['title'], 'rating':movie_data['rating']})
			else:
				break
		else:
			print("Error:", r.status_code)
			print(r.json()['status_message'])
			return None
		print("Página: %d, coletado: %d"%(p_num, len(rank)))
		p_num += 1
	return rank


if __name__ == '__main__':
	# Get API Key
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
	# Get session token
	with open(os.path.join(DIR, 'session.json')) as file:
		data = json.load(file)
	# Generate new session
	sid = get_session(data['session_token'])
	if sid == None:
		exit(-1)
	# Get user Data
	uid = get_details(sid)
	if uid == None:
		exit(-1)
	uid = uid['id']
	# Get ranked movies
	rank = get_ranked(uid, sid)
	if rank == None:
		exit(-1)
	# Save to file
	with open(os.path.join(DIR, 'user_movies.json'), 'w') as file:
		json.dump(rank, file)
		
