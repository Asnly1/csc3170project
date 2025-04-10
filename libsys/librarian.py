import functools
import mysql.connector

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from libsys.db import get_db
from libsys.auth import admin_login_required

bp = Blueprint('librarian', __name__, url_prefix='/librarian')

@bp.route('/index', methods=['GET', 'POST'])
@admin_login_required
def index():
    if request.method == 'POST':
        pass
    return render_template('librarian/index.html')

@bp.route('/catalog', methods=['GET', 'POST'])
@admin_login_required
def catalog():
    if request.method == 'POST':
        book = {
            key: request.form[key] for key in ['id', 'title', 'author', 'year', 'isbn', 'copies']
        }
        session['book-to-update'] = book
        return redirect(url_for('librarian.update'))

    
    db = get_db()
    c = db.cursor()

    c.execute('SELECT * FROM books ORDER BY title ASC;')
    b = c.fetchall()

    books = []
    for book in b:
        books.append({
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'year': book[3],
            'isbn': book[4],
            'copies': book[5]
        })
    return render_template('librarian/catalog.html', books=books)

@bp.route('/newitem', methods=['GET', 'POST'])
@admin_login_required
def newitem():
    if request.method == 'POST':
        book = {
            key: request.form[key] for key in ['title', 'author', 'year', 'isbn', 'copies']
        }

        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO books (title, author, published_year, isbn, copies) VALUES (%s, %s, %s, %s, %s)",
                  (book['title'], book['author'], book['year'], book['isbn'], book['copies']))
        db.commit()
        return redirect(url_for('librarian.catalog'))

    return render_template('librarian/newitem.html')

@bp.route('/update', methods=['GET', 'POST'])
@admin_login_required
def update():
    if request.method == 'POST':
        pass
    b = session.get('book-to-update')
    if not b:
        return redirect(url_for('librarian.catalog'))
    return render_template('librarian/update.html', book=b)

@bp.route('/inventory', methods=['GET', 'POST'])
@admin_login_required
def inventory():
    if request.method == 'POST':
        pass
    db = get_db()
    c = db.cursor()

    c.execute('SELECT * FROM books ORDER BY title ASC;')
    b = c.fetchall()

    books = []
    for book in b:
        books.append({
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'year': book[3],
            'isbn': book[4],
            'copies': book[5]
        })
    return render_template('librarian/inventory.html', books=books)

@bp.route('/usage', methods=['GET', 'POST'])
@admin_login_required
def usage():
    if request.method == 'POST':
        pass
    

    return render_template('librarian/usage.html')

@bp.route('/complaints', methods=['GET', 'POST'])
@admin_login_required
def complaints():
    if request.method == 'POST':
        com = {key:request.form[key] for key in ['id', 'title', 'content']}
        session['complaint-to-reply'] = com
        return redirect(url_for('librarian.reply'))

    db = get_db()
    c = db.cursor()

    c.execute('SELECT * FROM complaints ORDER BY created_at DESC;')
    cps = c.fetchall()

    com = []
    scom = []
    for cp in cps:
        if cp[4] == 'open':
            com.append(
                {
                    'id': cp[0],
                    'patron_id': cp[1],
                    'title': cp[2],
                    'content': cp[3],
                    'status': cp[4],
                    'created_at': cp[5],
                    'resolved_at': cp[6],
                    'reply': cp[7]
                }
            )
        else:
            scom.append(
                {
                    'id': cp[0],
                    'patron_id': cp[1],
                    'title': cp[2],
                    'content': cp[3],
                    'status': cp[4],
                    'created_at': cp[5],
                    'resolved_at': cp[6],
                    'reply': cp[7]
                }
            )

    return render_template('librarian/complaints.html', complaints=com, solved_complaints=scom)

@bp.route('reply', methods=['GET', 'POST'])
@admin_login_required
def reply():
    if request.method == 'POST':
        pass
    
    com = session.get('complaint-to-reply')
    if not com:
        return redirect(url_for('librarian.complaints'))
    return render_template('librarian/reply.html', complaint=com)
