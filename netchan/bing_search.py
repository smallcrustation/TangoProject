import requests, json
# Add your Microsoft Account Key to a file called bing.key

# allows you to run a search in cmd prompt
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

    # set root url to api (bing cog search docs)
    root_url = 'https://api.cognitive.microsoft.com/bing/v5.0/search'
    # set search query (keys are predetermined by bing search api)
    params = {  'q': search_terms,
                'count': '10',
                'offset': '0',
                'mkt': 'en-us',}

    # set bing api key in header (headers will be passed headers to api for our key)
    headers = {'Ocp-Apim-Subscription-Key': bing_api_key}
    
    try:
        # make GET request (root url looks for these arguments)
        response = requests.get(root_url, params=params, headers=headers)
    
        # pull the json out of response and return it as a python dictionary with json.loads and r.text    
        dict_response = json.loads(response.text) # .texts pulls all text information out of response

        # list that will carry the info from dict_response we want
        results = []

        # loop through dict_response pull out the information we want, place it in results list as dicts
        for result in dict_response['webPages']['value']: # inside the dict_response return info for ['webPages']['value']
            results.append({'title': result['name'], # inside the 2 deep key pull ['name'], ['url'] etc...
                            'link': result['url'],
                            'summary': result['snippet']})
    except:
        print('There was an error connecting/n{0}'.format(response.status_code))

    return results

    
if __name__ == '__main__':
    main()