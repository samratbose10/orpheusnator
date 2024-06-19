from flask import Flask, render_template, request, redirect, url_for
import akinator

app = Flask(__name__)
orpheus = akinator.Akinator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    try:
        orpheus.start_game()
        return redirect(url_for('question'))
    except Exception as e:
        return render_template('error.html', message=str(e))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == 'yes':
            orpheus.answer("y")
        elif answer == 'no':
            orpheus.answer("n")
        elif answer == 'idk':
            orpheus.answer("idk")
        elif answer == 'probably':
            orpheus.answer("p")
        elif answer == 'probably not':
            orpheus.answer("pn")

    if orpheus.progression >= 80:
        return redirect(url_for('guess'))

    question = orpheus.question
    return render_template('question.html', question=question)

@app.route('/guess')
def guess():
    orpheus.win()
    name = orpheus.first_guess['name']
    description = orpheus.first_guess['description']
    picture = orpheus.first_guess['absolute_picture_path']
    return render_template('guess.html', name=name, description=description, picture=picture)

if __name__ == '__main__':
    app.run(debug=True)