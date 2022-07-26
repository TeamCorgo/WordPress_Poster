import os, json, requests
from flask import Flask, request, jsonify
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# Manual set env keys to test with
# os.environ["WP_URL"] = ''
# os.environ["WP_Username"] = ''
# os.environ["WP_Passowrd"] = ''

app = Flask(__name__)
@app.route('/json', methods = ['GET', 'POST'])
def receive():
    if request.method == 'GET':
        print("🕑 Send JSON POST information to this location")
        return "🕑 Send JSON POST information to this location" \

    if request.method == 'POST':
        try:
            print('📨 Post received to /JSON')
            json_data = request.json
            print(json_data)

            wp = Client(
                os.getenv('WP_URL'),
                os.getenv('WP_Username'),
                os.getenv('WP_Passowrd'),
            )

            post = WordPressPost()
            post.title = json_data['Title']
            post.content = json_data['Content']
            post.terms_names = {
                'post_tag': json_data['Tags'],
                'category': json_data['Categories']
            }
            post.post_status = 'publish'
            # Send the request to publish the post
            wp.call(NewPost(post))

            print('📝 Sent to blog to get posted')
        except:
            print('❗ Request to Wordpress Failed')
    return '❗ Page did not receive GET or POST'

@app.route('/test', methods = ['GET'])
def test():
	url = request.url_root  + '/json'
	json_data = { 
        "Title": "Python - Sample Post Title", 
        "Content": "Python - Sample Post Content", 
        "Tags": ["Python - Sample Post Tags"],
        "Categories": ["Python - Sample Post Categories"],
    } 
	headers = {'Content-Type': 'application/json'}

    # Send the test request to the page
	requests.post(url, data=json.dumps(json_data), headers=headers)
	# extracting data in json format
	return 'Sent sample JSON file'

@app.route('/', methods = ['GET'])
def index():
	return \
        f'curl -X POST {os.environ["WP_URL"]} ' \
        "-H 'Content-Type: application/json' "\
        '-d \'{"login":"my_login","password":"my_password"}\'' \
        '<p><form action="/test">' \
            '<input type="submit" value="Try to create WordPress Post" />' \
        '</form></p>'

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True, port=80)
