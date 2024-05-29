import sounddevice as sd
import wavio
import speech_recognition as sr
import pyttsx3
import os

def record_audio(filename, duration=5, samplerate=44100, channels=1):
    print("Ses kaydediliyor...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()
    wavio.write(filename, myrecording, rate=samplerate)
    print("Ses kaydı tamamlandı.")

def listen(filename):
    recognizer = sr.Recognizer()

    # Dosyanın var olup olmadığını kontrol edin
    if not os.path.isfile(filename):
        print(f"Dosya bulunamadı: {filename}")
        return ""

    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="tr-TR")
            return text
        except sr.UnknownValueError:
            print("Ne dediğinizi anlayamadım.")
            return ""
        except sr.RequestError as e:
            print(f"Google Speech Recognition servisine ulaşılamadı; {e}")
            return ""

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main_menu():
    print("Hangi işlemi yapmak istiyorsunuz?")
    print("Seçenek 1: Yazdığım yazıyı sesli olarak dinleme")
    print("Seçenek 2: Sesli söylediklerimi yazıya çevirme")
    print("Seçenek 3: Ses dosyasını yazıya çevirme")
    choice = input("Seçiminizi yapın (1, 2 veya 3): ")
    return choice

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "1":
            text = input("Dinlemek istediğiniz metni girin: ")
            text_to_speech(text)
        elif choice == "2":
            filename = "recorded_audio.wav"
            print("\nDinlemeyi başlatmak için ENTER tuşuna basın (Çıkmak için 'q' tuşuna basın)")
            input()
            record_audio(filename)
            spoken_text = listen(filename)
            if spoken_text.lower() == "q":
                break
            if spoken_text:
                print("Sesiniz yazıya çevrildi.")
                print("Yazıya çevrilen metin: ", spoken_text)
        elif choice == "3":
            filename = input("Yazıya çevrilecek ses dosyasının adını girin: ")
            text = listen(filename)
            if text:
                print("Sesiniz yazıya çevrildi.")
                print("Yazıya çevrilen metin: ", text)
        else:
            print("Geçersiz seçim! Lütfen 1, 2 veya 3 girin.")
