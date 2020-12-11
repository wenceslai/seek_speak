from flask import Flask,render_template, request
import os
from helper_funcs import *

app = Flask(__name__)
app.config['VOICE_DATA'] = 'static/voice_data'

with open('word_to_phonemes.pickle', 'rb') as f:
    word_to_phonemes = pickle.load(f)

@app.route("/") #home screen
def home():
    #maybe promazavani voice data dir pokud se budou data ukladat
    for file in os.listdir(app.config['VOICE_DATA']): 

    file_path = os.path.join(app.config['VOICE_DATA'], file)

    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path): 
            shutil.rmtree(file_path)

    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


    return render_template(None)

@app.route("/recognize", methods=['GET', 'POST'])
def recognize():

    if request.methods = 'POST':

        voice_track = request.values['voice_track']
        gt_word = request.values['word'] 
        #removing noise
        #converting to 16kHz if needed

        #saving voice track to /voice data
        phonemes = get_phonemes(os.path.join(app.config['VOICE_DATA'], filename))
        gt_phonemes = word_to_phonemes[gt_word]

        score = bleu_precision(phonemes, gt_phonemes)

        return render_template(None)


if __name__ == "__main__":
        app.run(host='0.0.0.0',port="8000",debug=True)