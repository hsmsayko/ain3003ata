from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os  # Import os module to access environment variables

app = Flask(__name__,template_folder='templates')

# Retrieve MONGO_URI from environment variable
mongo_uri = os.getenv('MONGO_URI')  # Provide default value if env var is not set

# Connect to MongoDB using the MONGO_URI
client = MongoClient(mongo_uri)
db = client.BOOKSTORE
books_collection = db.bookstore

@app.route('/')
def index():
    books = books_collection.find()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        year = int(request.form['year'])
        price = float(request.form['price'])
        page = int(request.form['page'])
        category = request.form['category']
        coverPhoto = request.form['coverPhoto']
        publisher = {"name": request.form['publisher_name'], "year": int(request.form['publisher_year'])}
        author = {"name": request.form['author_name'], "dob": request.form['author_dob']}

        books_collection.insert_one({
            "isbn": isbn,
            "title": title,
            "year": year,
            "price": price,
            "page": page,
            "category": category,
            "coverPhoto": coverPhoto,
            "publisher": publisher,
            "author": author
        })

        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_book(id):
    book = books_collection.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        books_collection.update_one({"_id": ObjectId(id)}, {
            "$set": {
                "isbn": request.form['isbn'],
                "title": request.form['title'],
                "year": int(request.form['year']),
                "price": float(request.form['price']),
                "page": int(request.form['page']),
                "category": request.form['category'],
                "coverPhoto": request.form['coverPhoto'],
                "publisher": {"name": request.form['publisher_name'], "year": int(request.form['publisher_year'])},
                "author": {"name": request.form['author_name'], "dob": request.form['author_dob']}
            }
        })
        return redirect(url_for('index'))

    return render_template('edit_book.html', book=book)

@app.route('/delete/<id>')
def delete_book(id):
    books_collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
