from flask import Flask, render_template, request, redirect, url_for
import openai

app = Flask(__name__)

openai.api_key = 'FMBRKWHICQYOGP0P76O7RELVNDVX3JP71KQPOVLTUWUX9N7EA4X3Y5R0T2OP49RC'


session_data = {}

def ask_openai(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    session_data['questions'] = [
        "Is it a programming language?",
        "Is it used for web development?",
        "Is it a frontend technology?",
        "Is it a backend technology?",
        "Is it a part of the Hack Club workshops?"
    ]
    session_data['current_question'] = 0
    session_data['answers'] = []
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        answer = request.form['answer']
        session_data['answers'].append(answer)
        session_data['current_question'] += 1

        if session_data['current_question'] >= len(session_data['questions']):
            return redirect(url_for('guess'))

    question_text = session_data['questions'][session_data['current_question']]
    return render_template('question.html', question=question_text)

@app.route('/guess')
def guess():
    prompt = "The user answered the following questions:\n"
    for i, question in enumerate(session_data['questions']):
        prompt += f"Q: {question}\nA: {session_data['answers'][i]}\n"
    prompt += "Based on the above answers, what is the user thinking of?"

    guess_text = ask_openai(prompt)
    return render_template('guess.html', guess=guess_text)

if __name__ == '__main__':
    app.run(debug=True)
