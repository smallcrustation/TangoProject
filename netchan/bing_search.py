import requests, json
# Add your Microsoft Account Key to a file called bing.key

def main():
    query = input('Please enter your search: ')
    results = run_query(query)
    
    for result in results:
        print(result['title'],result['link'],result['summary'])
    

def read_bing_key():
	"""
	reads the BING API key from a file called 'bing.key'
	returns: a string which is either None, i.e. no key found, or with a key
	remember to put bing.key in your .gitignore file to avoid committing it to the repo.
	"""
	
	# See Python Anti-Patterns - it is an awesome resource to improve your python code
	# Here we using "with" when opening documents
	# http://docs.quantifiedcode.com/python-anti-patterns/maintainability/not_using_with_to_open_files.html
	
	bing_api_key = None
	try:
		with open('bing.key','r') as f:
			bing_api_key = f.readline()
	except:
		raise IOError('bing.key file not found')
		
	return bing_api_key
	

def run_query(search_terms):
    
    # get and test if we have a bing key
    bing_api_key = read_bing_key()
    if not bing_api_key:
        raise KeyError('Bing Key not found')

    # set root url to api
    root_url = 'https://api.cognitive.microsoft.com/bing/v5.0/search'
    # set search query
    params = {  'q': search_terms,
                'count': '10',
                'offset': '0',
                'mkt': 'en-us',}

    # set bing api key in header
    headers = {'Ocp-Apim-Subscription-Key': bing_api_key}
    
    try:
        # make GET request
        response = requests.get(root_url, params=params, headers=headers)
    
        # pull the json out of response and return it as a python dictionary with json.loads and r.text    
        dict_response = json.loads(response.text)

        # list that will carry the info from dict_response we want
        results = []

        # loop through dict_response pull out the information we want, place it in results list as dicts
        for result in dict_response['webPages']['value']:
            results.append({'title': result['name'],
                            'link': result['url'],
                            'summary': result['snippet']})
    except:
        print('There was an error connecting/n{0}'.format(response.status_code))

    return results

    
if __name__ == '__main__':
    main()