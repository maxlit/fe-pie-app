from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import os, time, sys
from flask import session
from flask_cors import CORS
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
CORS(app, resources={r"/*": {"origins": "https://langtools.io"}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pie/')
@app.route('/pie')
def proto(proto_lang = 'pie'):
    proto_lang == 'pie'
    session['proto_lang'] = proto_lang    
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

@app.route('/<proto_lang>/random/')
@app.route('/<proto_lang>/random')
def random(proto_lang):
    app.logger.info("random")
    proto_lang = session.get('proto_lang', proto_lang)
    language = request.args.get('l')
    term = "strength"
    return redirect(url_for("search", proto_lang = proto_lang, l=language, w=term))