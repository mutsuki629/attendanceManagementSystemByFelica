import wave
import pyaudio

beepLoca = 'audio/click.wav'

def beep(filename):
    wf = wave.open(filename, "r")
    # ストリーム開始
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)
    while(data != ''):
        stream.write(data)
        data = wf.readframes(1024)
    stream.close()      # ストリーム終了
    p.terminate()