from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import os, time, sys
from flask import session
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
app.secret_key = "dev secret"

app.logger.handlers.clear()

# Set the logging level and format
app.logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# Create a handler and set the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler to the logger
app.logger.addHandler(handler)
app.config['API_ENDPOINT'] = os.environ.get('API_ENDPOINT', 'https://langtools.io')
CORS(app, resources={r"/*": {"origins": app.config['API_ENDPOINT']}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pie/')
@app.route('/pie')
def proto(proto_lang = 'pie'):
    #session['proto_lang'] = proto_lang    
    selected_language = 'English'  # set the selected language to English by default
    return render_template('proto.html', debug = app.debug, proto_lang = proto_lang
                           , languages=[("English", 7333), ("German", 1815)], submitted = False
                           , selected_language = selected_language, submitted_value = "")

@app.route('/tinder/')
@app.route('/tinder')
def engdeu():
    #conn = get_connection('engdeu')
    #conn.close()
    return render_template('engdeu.html', proto_lang  = 'tinder'
                           , languages = [('English', 4626), ('German', 4626)]
                           , submitted = False, selected_language = 'English', submitted_value = ""
                           )

@app.route('/<proto_lang>/s', methods=['GET'])
@app.route('/<proto_lang>/search', methods=['GET'])
def search(proto_lang):
    print(proto_lang)
    #proto_lang = session.get('proto_lang', proto_lang)
    session['proto_lang'] = proto_lang
    print(proto_lang)

    term = request.args.get('w')
    language = request.args.get('l')

    # Define the API endpoint and parameters
    api_url = f"{app.config['API_ENDPOINT']}/api/{proto_lang}/get_term_info"
    print(api_url)
    params = {
        'proto_lang': proto_lang,
        'term': term,
        'language': language
    }
    # Make the GET request to the API
    print(params)
    response = requests.get(api_url, params=params)
    data = response.json()  # Directly use the response data
    print(data)
    # Prepare the context data for the template
    if proto_lang == 'pie':
        context = {
            'debug': app.debug,
            'proto_lang': proto_lang,
            'languages': data.get('languages', []),
            'results': data.get('results', []),
            'related_words': data.get('related_words', []),
            'submitted': data.get('submitted', False),
            'selected_language': language,
            'submitted_value': term,
            'language_family': "Germanic", # simplification
            'version': '0.0.0'  # Assume version is defined
        }
    elif proto_lang in ['tinder', 'zunder']:
        context = {
            'proto_lang': proto_lang,
            'languages': [('English', 4626), ('German', 4626)],
            'results': data.get('results', []),
            'submitted': data.get('submitted', False),
            'selected_language': language,
            'submitted_value': term,
            'version': '0.0.0'  # Assume version is defined
        }
    if proto_lang in ['tinder', 'zunder']:
        print('engdeu')
        #return render_template('engdeu.html', proto_lang  = 'tinder', languages = [('English', 4626), ('German', 4626)], submitted = False, selected_language = 'English', submitted_value = "", version = '0.0.0')
        return render_template('engdeu.html', **context)
    else:
        return render_template('proto.html', **context)
    
def random_term():
    import random
    terms = ['stream', 'work', 'drink', 'think', 'thumb']
    return random.choice(terms)

@app.route('/<proto_lang>/random/')
@app.route('/<proto_lang>/random')
def random(proto_lang):
    language = request.args.get('l')
    term = random_term()
    return redirect(url_for("search", proto_lang = proto_lang, l=language, w=term))

@app.route('/tinder/r')
def rnd(pair = 'engdeu'):
    language = request.args.get('l')
    term = random_term()
    return redirect(url_for("search", proto_lang  = 'tinder', l=language, w=term))