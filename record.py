import sounddevice
from scipy.io.wavfile import write
from helper_funcs import *
import numpy as np

with open('word_to_phonemes.pickle', 'rb') as f:
    word_to_phonemes = pickle.load(f)

f = 16000 #16kHz
secs = 2

print("recording......")
voice_track = sounddevice.rec(int(secs * f), samplerate=f, channels=1, dtype='int16')
sounddevice.wait()

write("static/voice_data/out2.wav", f, voice_track)


phoneme_preds = get_phonemes("static/voice_data/out2.wav")

gt_phoneme_variatns = word_to_phonemes["teacher"]
print("bleu: ", bleu_score(phoneme_preds, gt_phoneme_variatns))
print("recall:", dumb_metric(phoneme_preds, gt_phoneme_variatns))