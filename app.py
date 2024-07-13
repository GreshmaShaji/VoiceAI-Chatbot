from flask import Flask, render_template, request, jsonify
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import speech_recognition as sr
from gtts import gTTS
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the BlenderBot model and tokenizer
model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

# Ensure the audio directory exists
if not os.path.exists('audio'):
    os.makedirs('audio')

app = Flask(__name__)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def generate_response(prompt):
    inputs = tokenizer([prompt], return_tensors='pt')
    reply_ids = model.generate(**inputs)
    response = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
    return response

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("audio/response.mp3")
    os.system("mpg321 audio/response.mp3")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listen", methods=["POST"])
def listen():
    user_input = speech_to_text()
    response = generate_response(user_input)
    text_to_speech(response)
    return jsonify({"user_input": user_input, "response": response})

if __name__ == "__main__":
    app.run(debug=True)
