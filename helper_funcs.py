import os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from pocketsphinx import get_model_path, get_data_path
import pickle
from numpy import exp, log

def get_phonemes(filepath):
  MODELDIR = get_model_path()
  
  # Create a decoder with certain model
  config = Decoder.default_config()

  config.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
  config.set_string('-allphone', os.path.join(MODELDIR, 'en-us-phone.lm.dmp'))
  #config.set_string('-hmm', os.path.join(MODELDIR, 'cmusphinx-en-us-8khz-5.2'))

  #config.set_string('-dict', os.path.join(MODELDIR, 'cmudict-en-us.dict'))
  #config.set_string('-jsgf', os.path.join(MODELDIR, 'with-align.jsgf'))
  #config.set_string('-backtrace', 'yes')
  #config.set_string('fsgusefiller', 'no')
  #config.set_string('bestpath', 'no')
  #NEEDED??
  config.set_float('-lw', 2.0)
  config.set_float('-beam', 1e-20)
  config.set_float('-pbeam', 1e-20)
  config.set_string('backtrace', 'yes')

  # Decode streaming data.
  decoder = Decoder(config)
  decoder.start_utt()

  stream = open(filepath, 'rb')
  
  while True:
    buf = stream.read(1024)
    if buf:
      decoder.process_raw(buf, False, False)
    else:
      break
  decoder.end_utt()

  hypothesis = decoder.hyp()
  phonemes = [seg.word for seg in decoder.seg()]
  print ('Phonemes: ', phonemes)
  
  return phonemes


def txt_to_dict(filepath, save_as_pickle=True):
  with open(filepath, "r") as f:
      lines = f.readlines()
      lines = [line.split() for line in lines]
    
  word_to_phonemes = {}
  
  for i in range(len(lines)): 
    word = lines[i][0]
    
    if word[-1] == ')':
      word = word[:-3]

    if word not in list(word_to_phonemes.keys()):
      word_to_phonemes[word] = []

    word_to_phonemes[word].append(lines[i][1:]) #appending all possible pronounciation
  
  if save_as_pickle == True:
    with open('word_to_phonemes.pickle', 'wb') as f:
      pickle.dump(word_to_phonemes, f, protocol=pickle.HIGHEST_PROTOCOL) 

  return word_to_phonemes


def bleu_score(pred_phonemes, gt_phonemes_variatns, print_gt=False): #Bilingual LanguagE Understudy
    candidate_sum = 0; reference_sum = 0

    if print_gt == True: print(gt_phonemes_variatns)

    if len(pred_phonemes) == 0: return -1
    
    for phoneme in list(set(pred_phonemes)):
      count = pred_phonemes.count(phoneme)
      candidate_sum += count

      count_clip = 0
      for gt_phonemes in gt_phonemes_variatns: #to account for homographs
        count_clip = max(count_clip, gt_phonemes.count(phoneme))
      reference_sum += count_clip
    
    e = 2.7182
    ref_len = len(gt_phonemes_variatns[0])
    hyp_len = len(pred_phonemes)
    B = e**(1 - ref_len / hyp_len) if ref_len > hyp_len else 1
    
    if reference_sum == 0: return 0 #to avoid error in log
    return B * e**(log(reference_sum / candidate_sum))


def dumb_metric(pred_phonemes, gt_phonemes_variations):
  score = 0

  for phoneme in pred_phonemes:
    for gt_phonemes in gt_phonemes_variations:
      if phoneme in gt_phonemes: 
        score += 1
        break

  return score / len(gt_phonemes_variations[0])

  