from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    rate = db.Column(db.Integer, nullable=False)

# Создаём функцию для инициализации БД
def init_db():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        rate = int(request.form['rate'])
        
        if text and 1 <= rate <= 5:
            new_review = Review(text=text, rate=rate)
            db.session.add(new_review)
            db.session.commit()
        
        return redirect(url_for('index'))
    
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)

if __name__ == '__main__':
    init_db()  # Инициализируем БД при запуске
    app.run(debug=True)