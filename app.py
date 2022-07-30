"""
Setup webpage to convert JSON to Wordpress Post
"""
import os
from flask import Flask, request
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# Manual set env keys to test with:
#   os.environ["WP_URL"] = ''
#   os.environ["WP_Username"] = ''
#   os.environ["WP_Passowrd"] = ''

app = Flask('Wordpress Poster')
@app.route('/', methods = ['GET', 'POST'])
def index():
    """
    Index URL to process requests
    """
    if request.method == 'GET':
        print("🕑 Send JSON POST information to this location")
        return "🕑 Send JSON POST information to this location" \

    if request.method == 'POST':
        try:
            print('📨 Post received to /JSON')
            json_data = request.json

            client = Client(
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
            client.call(NewPost(post))
            print('📝 Sent to blog to get posted')
        except:
            print('❗ Request to Wordpress Failed')
        return
    return

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True, port=80)
