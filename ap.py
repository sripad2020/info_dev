from flask import Flask,request,render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

app=Flask(__name__)
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
