import sounddevice
from scipy.io.wavfile import write

f = 16e3 #16kHz
secs = 5

print("recording......")
voice_track = sounddevice.rec(int(secs * f), samplerate=f, channels=1)
sounddevice.wait()
write("out.wav", f, voice_track)