from flask import Flask,request,render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import google.generativeai as genai
from nltk import sent_tokenize, word_tokenize, FreqDist
from nltk.corpus import stopwords
import re

app=Flask(__name__)

sender_email="sripadkarthik@gmail.com"
password='soob dlvs mvlc iyhk'

def convert_paragraph_to_points(paragraph, num_points=10):
    sentences = sent_tokenize(paragraph)
    words = word_tokenize(paragraph.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    freq_dist = FreqDist(filtered_words)
    sentence_scores = {}
    for sentence in sentences:
        sentence_word_tokens = word_tokenize(sentence.lower())
        sentence_word_tokens = [word for word in sentence_word_tokens if word.isalnum()]
        score = sum(freq_dist.get(word, 0) for word in sentence_word_tokens)
        sentence_scores[sentence] = score
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    key_points = sorted_sentences[:num_points]
    return key_points

def clean_text(text):
    return re.sub(r'\*\*|\*', '', text)


@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/connect',methods=['GET',"POST"])
def connect():
    return render_template('contact.html')

@app.route('/connection',methods=['GET','POST'])
def conn():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        description = request.form.get('description')

        genai.configure(api_key='AIzaSyAM8hWwGWv5B9pTCnf14Q-Ck_gkukWUrN8')
        model = genai.GenerativeModel('gemini-1.5-flash')
        content = model.generate_content(f"based on the {description} give me the subject in short i need just a line")
        generated_text = content.text
        key_points = convert_paragraph_to_points(generated_text)
        key_points = [clean_text(item) for item in key_points]


        genai.configure(api_key='AIzaSyAM8hWwGWv5B9pTCnf14Q-Ck_gkukWUrN8')
        model = genai.GenerativeModel('gemini-1.5-flash')
        content = model.generate_content(f"If this {description} seems to be spam message or scam message or irrelevant message   give me as True only ")
        generated_text = content.text
        key_ponts = convert_paragraph_to_points(generated_text)
        key_poins = [clean_text(item) for item in key_ponts]

        if key_poins[0]==True:
            return render_template('index.html')

        genai.configure(api_key='AIzaSyAM8hWwGWv5B9pTCnf14Q-Ck_gkukWUrN8')
        model = genai.GenerativeModel('gemini-1.5-flash')
        content = model.generate_content(f"if the description message {description} is greeting or requesting to talk about a project or requesting for any research or requesting for any application development or requesting for any computer science tution give me as True in single word")
        generated_text = content.text
        keys = convert_paragraph_to_points(generated_text)
        keys = [clean_text(item) for item in keys]
        if keys[0]==True:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = key_points[0]
            descrp=("Please reach out to me by Phone contact and send your details in whatsapp "
                    "as my contact is +91 9398755799 and please send me your requirements.")

            msg.attach(MIMEText(f"" + descrp, 'html'))
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = sender_email
        emil=email.split('@')[0]
        msg['Subject'] = f"{emil}" +key_points[0]

        msg.attach(MIMEText(f"The message is from {name} and email is {email} and message is "+description, 'html'))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()

if __name__=='__main__':
    app.run()