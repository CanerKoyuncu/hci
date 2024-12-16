import speech_recognition as sr
import pyautogui  # type: ignore


def voice_to_text():
	recognizer = sr.Recognizer()
	with sr.Microphone() as source:
		print("Konuşmayı başlatabilirsiniz (2 saniye boyunca sessiz kalırsanız işlem sonlanacak)...")
		try:
			ses = recognizer.listen(source, timeout=2, phrase_time_limit=10)
			print("Konuşma tamamlandı, metne dönüştürülüyor...")
			metin = recognizer.recognize_google(ses, language="tr-TR")
			print(f"Tespit edilen metin: {metin}")
			if metin:
				return metin
			else:
				return ""
		except sr.WaitTimeoutError:
			print("2 saniye boyunca konuşma algılanmadı, işlem sonlandırılıyor.")
		except sr.UnknownValueError:
			print("Ses anlaşılamadı. Lütfen tekrar deneyin.")
		except sr.RequestError as e:
			print(f"Konuşma tanıma servisine bağlanırken hata oluştu: {e}")
