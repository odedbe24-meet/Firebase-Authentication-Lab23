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
  "databaseURL": "https://originalname-4859a-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()


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
       name = request.form["name"]
       username = request.form["username"]
       bio = request.form["bio"]

       try:
           login_session["user"] = auth.create_user_with_email_and_password(email,password)
           UID = login_session["user"]["localId"]
           user = {"email" : email, "password": password, "name": name, "username":username,"bio":bio}
           db.child("Users").child(UID).set(user)
           return redirect(url_for('add_tweet'))
       except:
           error = 'auth error'
           print(error)
           return render_template('signup.html', error=error)
    else:
        return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if(request.method == "POST"):
        title = request.form['title']
        text = request.form['text']
        tweet = {"title": title, "text": text, "uid":login_session["user"]["localId"] }
        
        db.child("Tweets").push(tweet)

        return redirect(url_for('all_tweets'))
    else:
        return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    
    all_tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", tweets=all_tweets)


if __name__ == '__main__':
    app.run(debug=True)