from flask import Flask, render_template, request, redirect
import csv
import random

app = Flask(__name__)

@app.route("/")
def home():
    '''Displays the page where the user can start a game.'''
    return render_template('home.html')

def listnames():
    displaynames = []
    with open("displaynames.txt") as seenames:
        reader = csv.reader(seenames)
        for row in reader:
            displaynames.append(row[0])
    return displaynames
    
@app.route("/game")
def game():
    '''Actual game page.'''
    names = []
    with open("names.txt") as fnames: # from usna.edu
        freader = csv.reader(fnames)
        for row in freader:
            names.append(row)
    randelement = random.choice(names)[0]
    # print(randelement)
    temp = []
    temp.append(randelement)
    with open("displaynames.txt", 'a') as dnames:
        fwriter = csv.writer(dnames)
        fwriter.writerow(temp)
    displaynames = listnames() 
    return render_template('game.html', display=displaynames)

@app.route("/remember")
def remember():
    '''Displays page so that the user can enter the names they remember.'''
    displaynames = listnames() 
    return render_template('remember.html', num=len(displaynames))

@app.route("/answer", methods=["GET", "POST"])
def answer():
    '''Checks if it is correct.'''
    displaynames = listnames()
    try:
        num = str(len(displaynames))
        answer = request.args.get(num).strip()
        # print(answer)
        names = answer.split(",")
        # print(names)
        # print(displaynames)
        # print(names != displaynames)
        if names == displaynames:
            return redirect("/game")
        else:
            message = "Your score is " + str(len(displaynames) - 1)
            f = open("displaynames.txt", "a")
            f.truncate(0)
            f.close()
            return render_template('home.html', msg=message)
    except:
        message = "Sorry, an unknown error occurred. Please try again."
        return render_template('home.html', msg=message)

if __name__ == "__main__":
        app.debug = True
        app.run()