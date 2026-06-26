import pyttsx3
import speech_recognition as sr
import datetime 
import wikipedia
import webbrowser
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
 
 engine.setProperty('voice' voices[0].id)

 engine.setProperty('rate' , 170)

def speak(text):
    """Converts text into spoken words."""
    engine.say(text)
    engine.runAndWait()


def wish_me();
    """Greets the User based on the time of day """

    hour = datetime.datetime.now().hour
    if 0 <= hour < 12 
      speak("Good morning , sir")
    elif 12 <= hour < 18
      speak("Good Afternoon sir") 
    else: 
        speak("Good evening sir")
  speak("Hii , i am depy . How may i help you today")



def take_command():
    """Listens to the microphone and returns the speech as a text string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 # Wait for 1 second of silence before processing
        r.adjust_for_ambient_noise(source) # Filters out background noise
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            # Uses Google's free Web Speech API
            query = r.recognize_google(audio, language='en-US')
            print(f"You said: {query}\n")
            
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you repeat it?")
            return "None"
        except sr.RequestError:
            print("Network error. Please check your internet connection.")
            return "None"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "None"
            
    return query.lower()

# --------------------------------------------------------
# 4. Main Logic Loop
# --------------------------------------------------------
if __name__ == "__main__":
    wish_me()
    
    while True:
        query = take_command()

        # If the microphone didn't pick anything up, loop back and listen again
        if query == "none":
            continue

        # --- Commands ---
        
        # Search Wikipedia
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                # Fetch 2 sentences from the Wikipedia summary
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are too many results for that query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find any information on that.")

        # Open Websites
        elif 'open youtube' in query:
            speak("Opening YouTube.")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google.")
            webbrowser.open("google.com")

        # Tell the Time
        elif 'time' in query:
            str_time = datetime.datetime.now().strftime("%I:%M %p")    
            speak(f"Sir, the time is {str_time}")

        # Exit Program
        elif 'quit' in query or 'exit' in query or 'stop' in query or 'sleep' in query:
            speak("Goodbye, sir. Powering down.")
            break