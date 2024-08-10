# Proof of concept for my startup Seek Speak

The goal of the project is to create a speech therapy app that can rate a person's pronounciation automatically. 

1. A phrase is generated that person is supposed to pronounce
2. We lookup the phonemes words in the sentence have (ground truth)
3. Speech is recorded and passed into Google Cloud's Speech API that recognises phonemes that were pronounced
4. We compare the ground truth phonemes with pronounced phonemes and tell the user which parts of words were mispronounced.
