from flask import Flask, render_template, redirect, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

response_key = ''

@app.route('/')
def go_home():
    # set question accessibility in the session at 0 at the beginning
    session['q_index'] = 0
    # set responses to empty if moved back to beginning
    session[response_key] = []

    return render_template('home.html',survey=satisfaction_survey)

@app.route('/questions/<int:num>')
def make_question(num):
    q_index = int(session.get('q_index'))
    
    if num != q_index:
        flash('Please do not access survey out of order.')
        return redirect(f"/questions/{q_index}")
    
    question = satisfaction_survey.questions[q_index]
    if q_index >= len(satisfaction_survey.questions):
        return render_template('thanks.html')
    
    return render_template('questions.html',question=question, q_index=q_index)

@app.route('/answers', methods=['POST'])
def accept_answers():
    q_index = int(session.get('q_index'))        #get the current q_index 
    next_q_index = q_index + 1                  #set the next_q_index by incrementing the q_index by 1 
    session['q_index'] = next_q_index           #increment the session's q_index by one after the respondent answers another question to get access to next question
    
    answer = request.form['qanswer']
    responses = session[response_key]
    responses.append(answer)
    session[response_key] = responses
    print(session[response_key])
    
    
    if next_q_index >= len(satisfaction_survey.questions):
        return redirect('/thanks')
    return redirect(f"/questions/{next_q_index}")
    

@app.route('/thanks')
def thank_you():
    return render_template("thanks.html")