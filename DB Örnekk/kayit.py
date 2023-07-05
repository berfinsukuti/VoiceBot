import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *


import sqlite3 as sql
import sqlite3
# from giris import *

import speech_recognition as sr
from datetime import datetime
import webbrowser
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#import os
import pyaudio
import wave
#import datetime

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
# from os import path
import os.path
import playsound
import random
from moviepy.editor import AudioFileClip
import pyttsx3

AudioSegment.converter = 'C:\\path\\to\\ffmpeg.exe'
AudioSegment.ffprobe = 'C:\\path\\to\\ffprobe.exe'

# # ffmpeg programının tam yolunu belirtin
# ffmpeg_path = '/path/to/ffmpeg'  # veya 'C:\\path\\to\\ffmpeg' (Windows için)

# # ffprobe programının tam yolunu belirtin
# ffprobe_path = '/path/to/ffprobe'  # veya 'C:\\path\\to\\ffprobe' (Windows için)

# # ffmpeg ve ffprobe programlarının yolunu PATH'e ekleyin
# os.environ['PATH'] += os.pathsep + ffmpeg_path + os.pathsep + ffprobe_path
# Konuşma motorunu oluşturma
engine = pyttsx3.init() 

def create_table():
    conn = sql.connect("Kullanicidata.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Kullanicidata(
        id INTEGER PRIMARY KEY,
        isim TEXT,
        soyisim TEXT,
        parola TEXT, 
        email TEXT,
        adres TEXT,
        telefon TEXT,
        cinsiyet TEXT
    )""")
    conn.commit()
    conn.close()

def insert(isim, soyisim, parola, email, adres, telefon, cinsiyet):
    conn = sqlite3.connect("Kullanicidata.db")
    cursor = conn.cursor()

    add_command = """INSERT INTO Kullanicidata(isim, soyisim, parola, email, adres, telefon, cinsiyet) values(?, ?, ?, ?, ?, ?, ?)"""
    #data = (entry_isim, entry_soyisim, entry_parola, entry_email, entry_adres, entry_telefon, entry_cinsiyet)

    cursor.execute(add_command, (isim, soyisim, parola, email, adres, telefon, cinsiyet))

    conn.commit()
    conn.close()

def update_password(email, newParola):
    conn = sql.connect('Kullanicidata.db')
    cursor = conn.cursor()

    upd_command = """UPDATE Kullanicidata SET parola = '{}' WHERE email = '{}'"""
    cursor.execute(upd_command.format(newParola, email))

    conn.commit()
    conn.close()

def delete_account(email):
    conn = sql.connect('Kullanicidata.db')
    cursor = conn.cursor()

    dlt_command = """DELETE FROM Kullanicidata WHERE email = '{}'"""
    cursor.execute(dlt_command.format(email))

    conn.commit()
    conn.close()

def delete_table():
    conn = sql.connect('Kullanicidata.db')
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE Kullanicidata""")

    conn.commit()
    conn.close()


window = tk.Tk()

window.geometry("800x500")
window.title("Kayıt Sayfası")

def giriswindow():
    window.destroy()
    
    giriswindow = tk.Tk()
    giriswindow.geometry("800x500")
    giriswindow.title("Giriş Sayfası")

    labelg = tk.Label(giriswindow, text = "GİRİŞ SAYFASI", font = "Times 16", fg = "black")
    labelg.place(x = 350, y = 10)

    labelemail = tk.Label(giriswindow, text = "E-Mail: ", font = "Times 12", fg = "black")
    labelemail.place(x=30, y=60)

    labelparola = tk.Label(giriswindow, text = "Parola: ", font = "Times 12", fg = "black")
    labelparola.place(x=30, y=120)

    entry_email =tk.Entry(giriswindow, width=50)
    entry_email.insert(string="@gmail.com", index =0)
    entry_email.place(x = 120, y = 60)

    entry_parola =tk.Entry(giriswindow, width=50)
    entry_parola.insert(string="", index =0)
    entry_parola.place(x = 120, y = 125)

    # def mainwindow():
    #     mainwindow = tk.Tk()
    #     mainwindow.geometry("800x500")
    #     mainwindow.title("Ana Sayfa")
        
    #     label = tk.Label(mainwindow, text = "ANA SAYFA", font = "Times 16", fg = "black")
    #     label.place(x = 350, y = 10)
    
    #     entry_veri = tk.Entry(mainwindow, width=200)
    #     entry_veri.insert(string="", index =0)
    #     entry_veri.place(x = 120, y = 70)
    def get_user_by_email(email):
            conn = sql.connect('Kullanicidata.db')
            cursor = conn.cursor()

            sel_command = """SELECT * FROM Kullanicidata WHERE email = '{}'"""
            cursor.execute(sel_command.format(email))

            user = cursor.fetchone()

            conn.commit()
            conn.close()

            return user
    
    def check_password(email, parola):
        user = get_user_by_email(email)

        if user and user[3] == parola:
            return True
        else:
            return False

    def giris_onay():
        
        email = entry_email.get()
        parola = entry_parola.get()

        if get_user_by_email(email):
            if check_password(email, parola):
                messagebox.showinfo("Giriş Başarılı", "Hoş Geldiniz!")
            else:
                messagebox.showerror("Hatalı Parola", "Girdiğiniz parola yanlış.")
        else:
            messagebox.showerror("Hatalı E-Mail", "Girdiğiniz e-mail adresi kayıtlı değil.")


        
        mainwindow = tk.Tk()
        mainwindow.geometry("800x500")
        mainwindow.title("Ana Sayfa")
        # window.destroy()

        def sesi_yazma():
            # entry_veri = tk.Entry(mainwindow, width=100)
            # entry_veri.insert(string="Nasıl yardımcı olabilirim?", index =0)
            # entry_veri.place(x = 120, y = 70)
            r = sr.Recognizer()

            def record(ask = False):
                with sr.Microphone() as source:
      
                    if ask:
                        print(ask)
                    audio = r.listen(source)
                    voice = ""
                    try:
                        voice = r.recognize_google(audio, language = 'tr-TR')
                    except sr.UnknownValueError:
                        entry_veri.delete(0, tk.END)
                        entry_veri.insert(tk.END, "Anlayamadım..")
                    except sr.RequestError:
                        entry_veri.delete(0, tk.END)
                        entry_veri.insert(tk.END, "Sistem Çalışmıyor.")
                    return voice
            
            def response(voice):
                if "nasılsın" in voice:
                    entry_veri.delete(0, tk.END)
                    entry_veri.insert(tk.END, "İyi senden?")

                if "sesli kayıt yapmak istiyorum" in voice:
                    # Kayıt ayarları
                    CHUNK = 1024  # ses blokları
                    FORMAT = pyaudio.paInt16  # ses formatı
                    CHANNELS = 2  # ses kanalları
                    RATE = 44100  # örnekleme hızı
                    RECORD_SECONDS = 30  # kaydedilecek süre
                    FILE_PATH = os.path.join("C:\kayitproje", f"kayit_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav")  # kaydedilecek dosya yolu

                    audio = pyaudio.PyAudio()

                    # Ses kaydı
                    stream = audio.open(format=FORMAT, channels=CHANNELS,
                                        rate=RATE, input=True,
                                        frames_per_buffer=CHUNK)

                    #print("Kayıt başladı...")
                    entry_veri.delete(0, tk.END)
                    entry_veri.insert(tk.END, "Kayıt başladı...")


                    frames = []

                    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                        data = stream.read(CHUNK)
                        frames.append(data)

                    print("Kayıt bitti.")
                    entry_veri.delete(0, tk.END)
                    entry_veri.insert(tk.END, "Kayıt bitti...")

                    # Ses dosyasına yazma
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()

                    wf = wave.open(FILE_PATH, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(audio.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()

                    # if "oku" in voice:
                    #     def metni_sese_cevir(metin, dil='tr'):
                    #         tts = gTTS(text=metin, lang=dil)
                    #         ses_dosyasi = 'ses.mp3'
                    #         tts.save(ses_dosyasi)

                    #         ses = AudioSegment.from_mp3(ses_dosyasi)
                    #         play(ses)

                    #     #metin = input("Metni girin: ")
                    #     metin = entry_veri.get()
                    #     entry_veri.delete(0, tk.END)
                    #     entry_veri.insert(tk.END, "Metni girin: ")
                    #     entry_veri.delete(0, tk.END)
                    #     metni_sese_cevir(metin)
                if "saat kaç" in voice:
                    #print(datetime.now().strftime("%H:%M:%S"))
                    entry_veri.delete(0, tk.END)
                    entry_veri.insert(tk.END, "Saat: " + str(datetime.now().strftime("%H")))
                    labelSaat = tk.Label(mainwindow, text="Saat: "+ str(datetime.now().strftime("%H:%M:%S")), font = "Times 12", fg = "black")
                    labelSaat.place(x = 100, y = 250)
                if "arama yap" in voice:
                    entry_veri.delete(0, tk.END)
                    entry_veri.insert(tk.END, "Ne aramak istiyorsun?")
                    search = record("ne aramak istiyorsun")
                    url = "https://google.com/search?q="+search
                    webbrowser.get().open(url)
                    #print(search+ " için bulduklarım")
                # if "mail gönder" in voice:
                #     sender_email = "@gmail.com"
                #     sender_password = ""
                #     receiver_email = "@hotmail.com"

                #     msg = MIMEMultipart()
                #     msg['From'] = sender_email
                #     msg['To'] = receiver_email
                #     msg['Subject'] = "Test Email from Python"
                #     body = "Hello, this is a test email sent using Python!"
                #     msg.attach(MIMEText(body, 'plain'))

                #     smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                #     smtp_server.starttls()
                #     smtp_server.login(sender_email, sender_password)
                #     text = msg.as_string()
                #     smtp_server.sendmail(sender_email, receiver_email, text)
                #     smtp_server.quit()
                    #print("Mail Gönderildi!")
                if "tamamdır" in voice:
                    #print("görüşürüz")
                    exit()

            # entry_veri = tk.Entry(mainwindow, width=100)
            # entry_veri.insert(string="Nasıl yardımcı olabilirim?", index =0)
            # entry_veri.place(x = 120, y = 70)

            time.sleep(1)
            while 1:
                voice=record()
                #print(voice)
                entry_veri.delete(0, tk.END)
                entry_veri.insert(tk.END, " " + voice)
                response(voice)
            

        def yaziyi_okuma():
            metin = "Bu bir bitirme projesidir."
            def speak(voice):
                engine.say(voice)
                engine.runAndWait()
        
            r = sr.Recognizer()

            def record(ask = False):
                with sr.Microphone() as source:
      
                    if ask:
                        print(ask)
                    audio = r.listen(source)
                    voice = ""
                    try:
                        voice = r.recognize_google(audio, language = 'tr-TR')
                    except sr.UnknownValueError:
                        #print("anlayamadım.")
                        labelValueError = tk.Label(mainwindow, text="Anlayamadım.", font = "Times 12", fg = "black")
                        labelValueError.place(x = 100, y = 250)
                    except sr.RequestError:
                        #print("sistem çalışmıyor.")
                        labelReqError = tk.Label(mainwindow, text="Sistem Çalışmıyor...", font = "Times 12", fg = "black")
                        labelReqError.place(x = 100, y = 280)
                    return voice
            
            
            # Ana döngü
            while True:
                command = record()

                if "merhaba" in command:
                    speak("Merhaba, size nasıl yardımcı olabilirim?")

                elif "nasılsınız" in command:
                    speak("Teşekkür ederim, iyiyim. Siz nasılsınız?")

                elif "senin adın ne" in command:
                    speak("Benim adım VoiceBot. Tanıştığıma memnun oldum.")

                elif "bana bir tekerleme söyle" in command:
                    speak("Dal sarkar kartal kalkar. Kartal kalkar dal sarkar.")

                elif "hoşça kal" in command:
                    speak("Görüşmek üzere!")
                    break

                else:
                    speak("Üzgünüm, anlamadım. Lütfen tekrarlayın.")
            # def metni_sese_cevir(metin, dil='tr'):
                
                                        
            #     tts = gTTS(text=metin, lang=dil)
            #     #rand = random.randint(1, 100000)
            #     #ses_dosyasi = "ses-"+str(rand)+".mp3"
            #     tts.save(ses_dosyasi.mp3)

            #     #ses = AudioSegment.from_wav(ses_dosyasi)
            #     #ses_dosyasi = AudioFileClip("ses.mp3")
            #     ses_dosyasi = AudioSegment.from_mp3("ses_dosyasi.mp3")
            #     playsound(ses_dosyasi) 
            #     os.remove(ses_dosyasi)       

            #             #metin = input("Metni girin: ")
                        
            # metni_sese_cevir(metin)
            # time.sleep(1)
            # while 1:
            #     voice=record()
            #     #print(voice)
            #     entry_veri.delete(0, tk.END)
            #     entry_veri.insert(tk.END, " " + voice)
            #     responsee(voice)  
        
        label = tk.Label(mainwindow, text = "VoiceBot", font = "Times 16", fg = "black")
        label.place(x = 350, y = 10)
    
        entry_veri = tk.Entry(mainwindow, width=100)
        entry_veri.insert(string="", index =0)
        entry_veri.place(x = 120, y = 70)

        yazdirma = tk.Button(mainwindow, text="Yazdır", fg = "black", command=sesi_yazma)
        yazdirma.place(x=120, y=200)

        okuma = tk.Button(mainwindow, text="Oku", fg = "black", command=yaziyi_okuma)
        okuma.place(x = 200, y = 200)

    girisyap = tk.Button(giriswindow, text = "Giriş Yap", fg = "black", command=giris_onay)
    girisyap.place(x = 120, y = 200)

class Kullanicilar:
    def __init__(self, isim=None, soyisim=None, parola=None, email=None, adres=None, telefon=None, cinsiyet=None):
        self.isim = isim
        self.soyisim = soyisim
        self.parola = parola
        self.email = email
        self.adres = adres
        self.telefon = telefon
        self.cinsiyet = cinsiyet
        self.conn = sqlite3.connect("Kullanicidata.db")
        self.cursor = self.conn.cursor()

    # def get_user_by_email(self, email):
    #     query = "SELECT email FROM Kullanicidata WHERE email = ?"
    #     self.cursor.execute(query, (email,))
    #     Kullanicidata = self.cursor.fetchone()
    #     return Kullanicidata
    
    # def __del__(self):
    #     self.connection.close()

create_table()
def kullanici_kayit():
    isim = entry_isim.get()
    soyisim = entry_soyisim.get()
    parola = entry_parola.get()
    email = entry_email.get()
    adres = entry_adres.get()
    telefon = entry_telefon.get()
    cinsiyet = entry_cinsiyet.get()
    
    insert(isim, soyisim, parola, email, adres, telefon, cinsiyet)
    # print("kayıt başarılı")
    messagebox.showinfo("Başarılı", "Kayıt Başarılı")
    kullanicilar = Kullanicilar()
    kullanicilar.Kullanicilar(isim, soyisim, parola, email, adres, telefon, cinsiyet)
    
    return

def temizle():
    entry_isim.delete(0, tk.END)
    entry_soyisim.delete(0, tk.END)
    entry_parola.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_adres.delete(0, tk.END)
    entry_telefon.delete(0, tk.END)
    entry_cinsiyet.delete(0, tk.END)

# def geri():
#     window.destroy()
#     giriswindow()




labelg = tk.Label(window, text = "KAYIT SAYFASI", font = "Times 16", fg = "black")
labelg.place(x = 350, y = 10)

labelisim = tk.Label(window, text = "İsim: ", font = "Times 12", fg = "black")
labelisim.place(x = 25, y = 50)

labelsoyisim = tk.Label(window, text = "Soysim: ", font = "Times 12", fg = "black")
labelsoyisim.place(x = 25, y = 80)

labelparola = tk.Label(window, text = "Parola: ", font = "Times 12", fg = "black")
labelparola.place(x=25, y=110)

labelemail = tk.Label(window, text = "E-Mail: ", font = "Times 12", fg = "black")
labelemail.place(x=25, y=140)

labeladres = tk.Label(window, text = "Adres: ", font = "Times 12", fg = "black")
labeladres.place(x=25, y=170)

labeltel = tk.Label(window, text = "Telefon: ", font = "Times 12", fg = "black")
labeltel.place(x=25, y=200)

labelcinsiyet = tk.Label(window, text = "Cinsiyet: ", font = "Times 12", fg = "black")
labelcinsiyet.place(x=25, y=230)

entry_isim =tk.Entry(window, width=50)
entry_isim.insert(string="", index =0)
entry_isim.place(x = 120, y = 50)

entry_soyisim =tk.Entry(window, width=50)
entry_soyisim.insert(string="", index =0)
entry_soyisim.place(x = 120, y = 80)

entry_parola =tk.Entry(window, width=50, show="*")
entry_parola.insert(string="", index =0)
entry_parola.place(x = 120, y = 110)

entry_email =tk.Entry(window, width=50)
entry_email.insert(string="@gmail.com", index =0)
entry_email.place(x = 120, y = 140)

entry_adres =tk.Entry(window, width=50)
entry_adres.insert(string="", index =0)
entry_adres.place(x = 120, y = 170)

entry_telefon =tk.Entry(window, width=50)
entry_telefon.insert(string="", index =0)
entry_telefon.place(x = 120, y = 200)

entry_cinsiyet =tk.Entry(window, width=50)
entry_cinsiyet.insert(string="", index =0)
entry_cinsiyet.place(x = 120, y = 230)

giris = tk.Button(window, text = "Giriş Yap", fg = "black" , command=giriswindow)
giris.place(x = 120, y = 260)

kayit = tk.Button(window, text = "Kayıt Ol", fg = "black", command = kullanici_kayit)
kayit.place(x = 120, y = 290)

button_temizle = tk.Button(window, text="Temizle", font="Times 12", fg="black", command = temizle)
button_temizle.place(x=120, y=320)

# button_geri = tk.Button(window, text="Geri", font="Times 12", fg="black", command = geri)
# button_geri.place(x=180, y=290)


window.mainloop()