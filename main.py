from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///library.db"
db=SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()





@app.route('/')
def home():
    all_books = []
    all_books=Book.query.all()
    return render_template("index.html", books=all_books)

@app.route('/change', methods=["GET","POST"])
def change():
    if request.method=="POST":
        bookid = request.args.get("id")
        print(bookid)
        newrating = request.form.get("rating")
        book = Book.query.get(bookid)
        book.rating = newrating
        db.session.commit()
        return redirect(url_for("home"))



    bookid = request.args.get("id")
    print(bookid)
    # newrating = request.args.get("rating")
    book=Book.query.get(bookid)
    # book.rating = newrating
    # db.session.commit()
    return render_template("change.html", book=book)
    # return redirect(url_for("home"))


@app.route('/delete', methods=["GET","POST"])
def delete():

        bookid = request.args.get("id")
        print(bookid)
        book = Book.query.get(bookid)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/add", methods=["GET","POST"])
def add():

    if request.method=="POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        new_book=Book(title=title,author=author,rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return  redirect(url_for("home"))

    return render_template("add.html" )


if __name__ == "__main__":
    app.run(debug=True)

