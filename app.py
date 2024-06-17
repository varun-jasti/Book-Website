from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'Sunny@7890'

db.init_app(app)


@app.before_request
def create_tables():
    print("Creating tables...")
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')




@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']
        new_book = Book(title=title, author=author, genre=genre, price=price)
        db.session.add(new_book)
        db.session.commit()
        flash('Book Added Successfully!')
        return redirect(url_for('index'))
    return render_template('add_book.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.price = request.form['price']
        db.session.commit()
        flash('Book Updated Successfully!')
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)


@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book Deleted Successfully!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
