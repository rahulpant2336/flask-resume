import os
from flask import Flask, render_template, url_for, request, flash, session, redirect
from flask_sqlalchemy import SQLAlchemy
from form import ContactForm
from flask_migrate import Migrate  #pip install Flask-Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = '3315'

############################################
########### SQL DATABASE SECTION ###########
###########################################


#getting path of base directory
basedir = os.path.abspath(os.path.dirname(__file__))
#__file__ --> c:/users/rahul/desktop/myflask/app.py


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app,db)

############################################
######### MODELS ##########################
##########################################
class FormData(db.Model):

    #MANUAL TABLE NAME CHOICE!
    __tablename__ = 'formsinput'

    id = db.Column('form_id', db.Integer, primary_key = True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    subject = db.Column(db.Text)
    message = db.Column(db.Text)

    def __init__(self,name,email,subject,message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message

    def __repr__(self):
        return f"Name: {self.name}, Email: {self.email}, Subject: {self.subject}, Message: {self.message}"


###########################################
#### VIEW FUNCTIONS -- HAVE FORMS #########
##########################################

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = ContactForm()

    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['subject'] = form.subject.data
        session['message'] = form.message.data

        flash('Thank you for submiting the form. Here is the info you gave me:')
        flash(f'Name: {session["name"]}')
        flash(f'Email: {session["email"]}')
        flash(f'Subject: {session["subject"]}')
        flash(f'Message: {session["message"]}')

        form_insert = FormData(form.name.data,form.email.data,form.subject.data,form.message.data)
        db.session.add(form_insert)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('index.html', form=form)

@app.route('/list_to_check_3315')
def list_data():

    form_records = FormData.query.all()

    return render_template('list.html', form_records=form_records)



if __name__ == '__main__':
   app.run(debug = True)
