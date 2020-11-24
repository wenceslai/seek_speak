from flask import Flask,render_template, request
import os
from helper_funcs import *

app = Flask(__name__)
app.config['VOICE_DATA'] = 'static/voice_data'

@app.route("/") #home screen
def home():
    #maybe promazavani voice data dir pokud se budou data ukladat

    return render_template(None)

@app.route("/recognize", methods=['GET', 'POST'])
def recognize():

    if request.methods = 'POST':

        voice_track = request.values['voice_track']
        #removing noise
        #converting to 16kHz if needed

        #saving voice track to /voice data
        phonemes = get_phonemes(os.path.join(app.config['VOICE_DATA'], filename))

        return render_template(None)