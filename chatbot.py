from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
import random
import nltk
from nltk.stem import WordNetLemmatizer
import time
import string

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

app = Flask(__name__)

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'supersecretkey'
Session(app)

lemmatizer = WordNetLemmatizer()

def preprocess_input(sentence):
    sentence = sentence.translate(str.maketrans('', '', string.punctuation)).lower()
    try:
        words = nltk.word_tokenize(sentence)
    except LookupError:
        words = sentence.split()
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

intents = [
    {
        "tag": "greeting",
        "patterns": ["hi", "hello", "hey"],
        "responses": ["Hello! How can I help you today?", "Hi there! What can I do for you?"]
    },
    {
        "tag": "services",
        "patterns": [
            "what services do you offer", 
            "tell me about your services", 
            "what do you do",
            "services",
            "what are your services"
        ],
        "responses": [
            "We offer a wide range of services including:",
            "1. **Graphic Design**: Creative and professional design solutions.",
            "2. **SEO**: Search Engine Optimization to improve your online visibility.",
            "3. **Digital Marketing**: Comprehensive digital marketing strategies.",
            "4. **E-commerce**: Building and optimizing e-commerce platforms.",
            "5. **App Development**: Custom mobile app development for iOS and Android.",
            "6. **Website Development**: Responsive and user-friendly website design and development."
        ]
    },
    {
        "tag": "contact",
        "patterns": [
            "how can I contact you", 
            "what is your email", 
            "where are you located",
            "contact", 
            "contact info", 
            "contact information"
        ],
        "responses": ["You can contact us at info@novanectar.co.in or call +91 8979891708. We are located in Dehradun, Uttarakhand, India."]
    },
    {
        "tag": "faq",
        "patterns": ["what is novanectar", "who are you", "tell me about novanectar"],
        "responses": ["Novanectar is an IT solutions company offering web development, app development, SEO, and digital marketing services."]
    },
    {
        "tag": "why_choose_us",
        "patterns": ["why should I choose you", "why choose novanectar", "what makes you different", "why choose us"],
        "responses": [
            "Here's why you should choose us:",
            "1. **Reliability**: We deliver consistent and dependable services.",
            "2. **Scalability**: Our solutions grow with your business.",
            "3. **Security**: We prioritize the safety of your data and systems.",
            "4. **Time Efficiency**: We deliver projects on time without compromising quality.",
            "5. **Customization**: Our solutions are tailored to meet your unique needs.",
            "6. **Expert Teams**: Our team consists of skilled professionals with years of experience.",
            "7. **24/7 Support**: We provide round-the-clock support to address your concerns.",
            "8. **On-time Delivery**: We ensure timely delivery of all projects."
        ]
    },
    {
        "tag": "goodbye",
        "patterns": ["bye", "goodbye", "see you later"],
        "responses": ["Thank you for your valuable time. Goodbye! Have a great day!", "See you later! Feel free to reach out if you need anything."]
    }
]

intents = [{**intent, "processed_patterns": set(preprocess_input(pattern) for pattern in intent["patterns"])} for intent in intents]

def get_response(user_input):
    user_input = preprocess_input(user_input)

    for intent in intents:
        if any(pattern in user_input for pattern in intent["processed_patterns"]):
            if intent["tag"] == "services":
                return "\n".join(intent["responses"])
            
            elif intent["tag"] == "why_choose_us":
                return "\n".join(intent["responses"])
            
            else:
                return random.choice(intent["responses"])

    return "I'm sorry, I didn't understand that. Feel free to contact us for more information:\n\nEmail: info@novanectar.co.in\nPhone: +91 8979891708\nLocation: Dehradun, Uttarakhand, India."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    session.setdefault('chat_history', []).append({"user": user_input})
    response = get_response(user_input)
    session['chat_history'].append({"bot": response})
    time.sleep(1)
    return jsonify({"response": response, "chat_history": session['chat_history']})

if __name__ == '__main__':
    app.run(debug=True)
