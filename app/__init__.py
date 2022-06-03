from flask import Flask, render_template, request, redirect
import csv
import random

app = Flask(__name__)

@app.route("/")
def home():
    '''Displays the page where the user can start a game.'''
    return render_template('home.html')

@app.route("/game")
def game():
    '''Actual game page.'''
    names = []
    with open("names.txt") as fnames: # from usna.edu
        freader = csv.reader(fnames)
        for row in freader:
            names.append(row)
    randelement = random.choice(names)
    temp = []
    temp.append(randelement)
    with open("displaynames.txt", 'w') as dnames:
        fwriter = csv.writer(dnames)
        fwriter.writerow(temp)
    displaynames = []
    with open("displaynames.txt") as seenames:
        reader = csv.reader(seenames)
        for row in reader:
            displaynames.append(row)
    return render_template('game.html', display=displaynames)

@app.route("/remember")
def remember():
    '''Displays page so that the user can enter the names they remember.'''
    return render_template('remember.html')

@app.route("/answer", methods=["GET", "POST"])
def answer():
    '''Checks if it is correct.'''
    displaynames = []
    with open("displaynames.txt") as seenames:
        reader = csv.reader(seenames)
        for row in reader:
            displaynames.append(row)
    try:
        names = []
        answer = request.args.get('ans')
        if ',' in answer:
            names = answer.split(",")
        else:
            names.append(answer[0]) 
        if names == displaynames:
            return redirect("/game")
        else:
            message = "Your score is " + names.displaynames() - 1
            with open("displaynames.txt", 'r') as delnames:
                delnames.truncate()
            return render_template('home.html', msg=message)
    except:
        message = "Sorry, an unknown error occurred. Please try again."
        return render_template('home.html', msg=message)

if __name__ == "__main__":
        app.debug = True
        app.run()