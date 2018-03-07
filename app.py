import os,sys
from flask import Flask,request
from pymessenger import Bot
from utils import wit_response, get_news_elements,get_images
from recommendations import recommend
app = Flask(__name__)

PAGE_ACCESS_TOKEN = '<insert your page acess token here>'

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/',methods=['GET'])
def verify():
	# Webhook verification
	if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token")=="hello":
			return "Verification token mismatch",403
		return request.args["hub.challenge"],200
	return "Hello world",200

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)
	if data['object']=='page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:
				#IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']
				if messaging_event.get('message'):
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'
					categories = wit_response(messaging_text)
					if 'greetings' in categories.keys():
						if 'name' in categories.keys():
							bot.send_text_message(sender_id,"Cheers,{}. Hope you are having a nice day.".format(str(categories['name'])))
						else:
							bot.send_text_message(sender_id,"Hi. What can I do for you?")	
					elif 'task' in categories.keys():
						req = categories['task']
						for_images = ['images']
						for_recommend = ['Recommendation','Recommend']
						if req in for_images:	
							choices = ['category','location','name','movie_name','character','adjective']
							search = " "
							for i in choices:
								if i in categories.keys():
									search+=" "+str(categories[i])
							bot.send_generic_message(sender_id,get_images(search))
						elif req in for_recommend:
							bot.send_text_message(sender_id,'\n'.join(recommend()))
						else:
							elements = get_news_elements(categories)
							bot.send_generic_message(sender_id,elements)
	return "ok",200

def log(message):
	print(message)
	sys.stdout.flush()

if __name__=="__main__":
	app.run(debug=True,port=80)
