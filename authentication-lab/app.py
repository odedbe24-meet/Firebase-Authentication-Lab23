from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


Config = {
  "apiKey": "AIzaSyCKmONTBKYQ66RLlt3ZzOh3Pmfk1emxQZk",
  "authDomain": "originalname-4859a.firebaseapp.com",
  "projectId": "originalname-4859a",
  "storageBucket": "originalname-4859a.appspot.com",
  "messagingSenderId": "276151677934",
  "appId": "1:276151677934:web:7499ec07edc5b49f7514ff",
  "measurementId": "G-RE91HDNEVT",
  "databaseURL": ""
}


firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():


    if request.method == "POST":
        email =  request.form["email"]
        password = request.form["password"]
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            error = 'auth_error'
            return render_template("signin.html", error=error)
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if(request.method == "POST"):
       email =  request.form["email"]
       password = request.form["password"]

       try:
           login_session["user"] = auth.create_user_with_email_and_password(email,password)
           return redirect(url_for('add_tweet'))
       except:
           error = 'auth error'
           print(error)
           return render_template('signup.html', error=error)
    else:
        return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")




if __name__ == '__main__':
    app.run(debug=True)