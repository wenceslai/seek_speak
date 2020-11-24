import os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from pocketsphinx import get_model_path, get_data_path

MODELDIR = get_model_path()
DATADIR = get_data_path()
#DATADIR = "voice_data"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
config.set_string('-allphone', os.path.join(MODELDIR, 'en-us-phone.lm.dmp'))
config.set_float('-lw', 2.0)
config.set_float('-beam', 1e-10)
config.set_float('-pbeam', 1e-10)

# Decode streaming data.
decoder = Decoder(config)

def get_phonemes(filepath=f2bjrop1.0.wav):
  decoder.start_utt()
  #stream = open(os.path.join(DATADIR, 'f2bjrop1.0.wav'), 'rb')
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