from flask import Flask, render_template, redirect, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False




responses = []

@app.route('/')
def go_home():
    # set question accessibility in the session at 0 at the beginning
    session['q_index'] = 0

    return render_template('home.html',survey=satisfaction_survey)

@app.route('/questions/<num>')
def make_question(num):
    q_index = session.get('q_index')
    
    if int(num) != int(q_index):
        flash('Please do not access survey out of order.')
        return redirect(f"/questions/{q_index}")
    else:
        question = satisfaction_survey.questions[int(q_index)]
        if q_index >= len(satisfaction_survey.questions):
            return render_template('thanks.html')
        else:
            return render_template('questions.html',question=question, q_index=q_index)

@app.route('/answers', methods=['POST'])
def accept_answers():
    q_index = session.get('q_index')        #get the current q_index 
    next_q_index = int(q_index) + 1         #set the next_q_index by incrementing the q_index by 1 
    session['q_index'] = next_q_index       #increment the session's q_index by one after the respondent answers another question to get access to next question
    answer = request.form['qanswer']
    responses.append(answer)
    if next_q_index >= len(satisfaction_survey.questions):
        return redirect('/thanks')
    else:
        return redirect(f"/questions/{next_q_index}")
    

@app.route('/thanks')
def thank_you():
    return render_template("thanks.html")