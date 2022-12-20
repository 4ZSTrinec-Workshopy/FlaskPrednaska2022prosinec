# Ukazka CRUD systemu v Flask-SQLAlchemy 
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Vytvoříme instanci Flasku
app = Flask(__name__)

# Zde definujeme cestu k databázi, v tomto případě MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/test'

# Zde definujeme instanci SQLAlchemy
db = SQLAlchemy(app)

# Zde definujeme model databáze, v tomto případě User s atributy id, name a email
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Zde zaregitrujeme stránku index.html
@app.route('/', methods=['POST', 'GET', 'DELETE'])
def index():
    # Zde definujeme funkci, která bude vracet všechny uživatele
    if request.method == 'GET':
        users = get_users()
        return render_template('index.html', users=users)
    return render_template('index.html')

# Zde definujeme funkce, která bude vytvářet uživatele a posílat je ve formátu JSON
@app.route('/create_users', methods=['POST'])
def create_user():
    user = insert_user(request.form['name'], request.form['email'])
    return redirect(url_for('index'))

def insert_user(name, email):
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    json = """{{
        name: {name},
        email: {email}
    }}
    """.format(name=name, email=email)

    return json

# Zde definujeme funkci, která bude mazat uživatele podle ID
@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

# Zde definujeme funkci, která bude vracet všechny uživatele
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['email'] = user.email
        output.append(user_data)
    return output

if __name__ == '__main__':
    app.run(debug=True)