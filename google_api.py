import os
import sounddevice
from scipy.io.wavfile import write
import numpy as np
import os

from google.cloud import speech_v1p1beta1 as speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/wenceslai/Downloads/vocal-lead-304519-1fb110e28e33.json"

client = speech.SpeechClient()

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
    enable_word_confidence=True,
)

file_path = "static/voice_data/out2.wav"


def record(target_sentence):
    f = 16000 #16kHz
    
    secs = (0.80 * len(target_sentence.split())) // 1

    print("say:  ", target_sentence)
    print(f"recording for {secs}s...")
    
    voice_track = sounddevice.rec(int(secs * f), samplerate=f, channels=1, dtype='int16')
    sounddevice.wait()

    write(file_path, f, voice_track)


def assess(target_sentence):
    
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    with open("homophones.txt", "r") as txt:
        lines = txt.readlines()
        homophone_groups = [line[:-1].split(';') for line in lines]

    audio = speech.RecognitionAudio(content=content)

    response = client.recognize(config=config, audio=audio)

    target_words = target_sentence.split()

    hard_prec_scores = []; soft_prec_scores = []
    
    for result in response.results:

        for prediction in result.alternatives:
            corr_cnt = 0 #measuring recall - number of target words which appear in prediction
            conf_sum = 0

            for pred_word in prediction.words:
                print(pred_word.word, pred_word.confidence)

                if pred_word.word.lower() in target_words:
                    corr_cnt += 1
                    conf_sum += pred_word.confidence
                else: #checking if homophemes of pred_word
                    for homophone_group in homophone_groups:
                        if any(pred_word.word.lower() in homophone_group and target_word in homophone_group for target_word in target_words):
                            corr_cnt += 1
                            conf_sum += pred_word.confidence

            hard_prec_scores.append(corr_cnt / len(prediction.words)) #how many of predicted words were in target
            soft_prec_scores.append(conf_sum / len(prediction.words))

    print("top hard prec: ", max(hard_prec_scores))
    print("top soft prec: ", max(soft_prec_scores))

target_sentence = "the sun is yellow"

record(target_sentence)

assess(target_sentence)



