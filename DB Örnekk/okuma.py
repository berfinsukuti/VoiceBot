import speech_recognition as sr
import pyttsx3

# Konuşma motorunu oluşturma
engine = pyttsx3.init()

# Kullanıcıdan ses alma
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sizi dinliyorum...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="tr")  # Sesli komutu metne dönüştürme
        print("Söylediğiniz: " + text)
        return text
    except sr.UnknownValueError:
        print("Anlayamadım")
    except sr.RequestError as e:
        print("Bir hata oluştu: {0}".format(e))

    return ""

# Sesli yanıt verme
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Ana döngü
while True:
    command = listen()

    if "merhaba" in command:
        speak("Merhaba, size nasıl yardımcı olabilirim?")

    elif "nasılsınız" in command:
        speak("Teşekkür ederim, iyiyim. Siz nasılsınız?")

    elif "hoşça kal" in command:
        speak("Görüşmek üzere!")
        break

    else:
        speak("Üzgünüm, anlamadım. Lütfen tekrarlayın.")

