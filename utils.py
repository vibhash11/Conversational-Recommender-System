from wit import Wit
from gnewsclient import gnewsclient
import urllib.request

access_token = 'XZBEDHIR3TDVY6Z57KMBIN3E3IR3UXEG'

client = Wit(access_token = access_token)
def wit_response(message_text):
	resp = client.message(message_text)
	categories = {}
	entities = list(resp['entities'])
	for entity in entities:
		categories[entity] = resp['entities'][entity][0]['value']
	return categories

def get_news_elements(categories):
	news_client = gnewsclient()
	news_client.query = ''
	if 'news_type' in categories.keys():
		news_client.query+=categories['news_type']+' '
	if 'location' in categories.keys():
		news_client.query+=categories['location']
	news_items = news_client.get_news()
	elements = []
	for item in news_items:
		element = {'title':item['title'],
			   'buttons':[{
				   	'type':'web_url',
					'title':'Read More',
					'url':item['link']
				  	 }],
			   'image_url':item['img']
			   }
		elements.append(element)
	return elements

def get_images(keywords):
	if type(keywords)==str:
		keywords = keywords.split()
	term = ""
	for i in keywords:
		term+="+"+i
	term = term[1:]
	headers = {}
	url = "https://www.google.co.in/search?q="+term+"&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj41djLoaLUAhUETY8KHZiTAOAQ_AUICigB&biw=1920&bih=1080#imgrc=_"
	headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
	req =  urllib.request.Request(url, headers = headers)
	resp =  urllib.request.urlopen(req)
	respData = str(resp.read())
	def extract_image(s):
		start_line = s.find('"class="rg_meta"')         
		start_content =	s.find('"ou"',start_line+1)         
		end_content = s.find(',"ow"',start_content+1)         
		content_raw = str(s[start_content+6:end_content-1])         
		return content_raw, end_content
	images = []
	end = 0
	for _ in range(5):
		img_url,end = extract_image(respData)
		respData = respData[end:]
		images.append(img_url)
	elements = []
	for item in images:
		element = {'title':term,
				'buttons':[{'type':'web_url','title':'Go to image','url':item}],
		           'image_url':item}
		elements.append(element)
	return elements
	

