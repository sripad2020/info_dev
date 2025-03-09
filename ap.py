from flask import Flask,request,render_template,redirect,url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

app=Flask(__name__)

sender_email="sripadkarthik@gmail.com"
password='soob dlvs mvlc iyhk'


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
        msg['Subject'] = f"{emil}"

        msg.attach(MIMEText(f"""
    <html>
        <body>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong></p>
            <div style="margin-top: 30px; padding: 10px; line-height: 1.6; white-space: pre-line;">
                {description}
            </div>
        </body>
    </html>
""", 'html'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return redirect(url_for('connect'))

if __name__=='__main__':
    app.run()
