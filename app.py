from flask import Flask, render_template, redirect, url_for, request, session, logging, flash

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('home.html')

    

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)