from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flaskext.mysql import MySQL
import pymysql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, FileField
from passlib.hash import sha256_crypt
from functools import wraps
 
app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"
  
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'landhoteles'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
  
# Register Form Class
class RegisterForm(Form):
    fullname= StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=1, max=50)])
    country = StringField('Country', [validators.Length(min=1, max=25)])
    city = StringField('City', [validators.Length(min=6, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    typeUsers = StringField('TypeUsers', [validators.Length(min=1, max=50)])
    
 
# Article Form Class
class ArticleForm(Form):
    cuidad = StringField('Cuidad', [validators.Length(min=1, max=200)])
    pais = StringField('Pais', [validators.Length(min=1, max=200)])
    direccion = StringField('Direccion', [validators.Length(min=1, max=200)])
    ubicacion = StringField('Ubicacion', [validators.Length(min=1, max=200)])
    habitacion = TextAreaField('Habitacion', [validators.Length(min=1, max=200)])
    imagen =  FileField('Imagen')
    foto =  FileField('Foto')
    valor = StringField('Valor', [validators.Length(min=1, max=200)])
    resena = StringField('Resena', [validators.Length(min=1, max=200)])
    
  
# Index
@app.route('/')
def index():
    return render_template('home.html')
  
@app.route('/layout')
def layout():
    return render_template('layout.php')
# About
@app.route('/about')
def about():
    return render_template('about.html')
# administracion
@app.route('/administracion')
def administracion():
    return render_template("administracion.html")
# Articles
@app.route('/articles')
def articles():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get articles
    result = cur.execute("SELECT * FROM producto")
    productos = cur.fetchall()
    if result > 0:
        return render_template('articles.html', productos=productos)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()
 
#Single Article
@app.route('/article/<string:idproducto>/')
def article(idproducto):
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get article
    result = cur.execute("SELECT * FROM producto WHERE idproducto = %s", [idproducto])
    producto = cur.fetchone()
    return render_template('article.html', producto=producto)
  
# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        fullname = form.fullname.data
        email = form.email.data
        username = form.username.data
        country = form.country.data
        city = form.city.data
        password = sha256_crypt.encrypt(str(form.password.data))
        typeUsers = form.typeUsers.data
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        # Execute query
        cur.execute("INSERT INTO users( fullname, email, username, country, city, password, typeUsers) VALUES (%s,%s,%s,%s,%s,%s,%s)", ( fullname, email, username, country, city, password, typeUsers))    
        # Commit to DB
        conn.commit()
        # Close connection
        cur.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)
 
# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('administracion'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')
 
# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
 
# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))
  
# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    result = cur.execute("SELECT * FROM producto WHERE idproducto = %s", [session['username']])
  
    productos = cur.fetchall()
  
    if result > 0:
        return render_template('dashboard.html', productos=productos)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()
 
# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        cuidad = form.cuidad.data
        pais = form.pais.data
        direccion = form.direccion.data
        ubicacion = form.ubicacion.data
        habitacion = form.habitacion.data
        imagen = form.imagen.data
        foto  = form.foto.data
        resena = form.resena.data
        # Create Cursor
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
  
        # Execute
        cur.execute("INSERT INTO producto(cuidad, pais, direccion, ubicacion, habitacion, imagen, foto, resena) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,)",(cuidad, pais, direccion, ubicacion, habitacion, imagen, foto, resena, session['username']))
        # Commit to DB
        conn.commit()
        #Close connection
        cur.close()
        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)
 
# Edit Article
@app.route('/edit_article/<string:idproducto>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(idproducto):
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Get article by id
    result = cur.execute("SELECT * FROM producto WHERE idproducto = %s", [idproducto])
    producto = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)
    # Populate article form fields
    form.cuidad.data = producto['cuidad']
    form.pais.data = producto['pais']
    form.direccion.data = producto['direccion']
    form.ubicacion.data = producto['ubicacion']
    form.habitacion.data = producto['habitacion']
    form.imagen.data = producto['imagen']
    form.foto.data = producto['foto']
    form.resena.data = producto['resena']
    
    if request.method == 'POST' and form.validate():
        cuidad = request.form['cuidad']
        pais = request.form['pais']
        direccion = request.form['direccion']
        ubicacion = request.form['ubicacion']
        habitacion = request.form['habitacion']
        imagen = request.form['imagen']
        foto = request.form['foto']
        resena = request.form['resena']
        
        # Create Cursor
        cur = conn.cursor(pymysql.cursors.DictCursor)
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE producto SET cuidad=%s, pais=%s, direccion=%s, ubicacion=%s, habitacion=%s, imagen=%s, foto=%s, resena=%s WHERE idproducto=%s",(cuidad, pais, direccion, ubicacion, habitacion, imagen, foto, resena, idproducto))
        # Commit to DB
        conn.commit()
        #Close connection
        cur.close()
        flash('Article Updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)
  
  
# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    # Execute
    cur.execute("DELETE FROM producto WHERE idproducto = %s", [idproducto])
    # Commit to DB
    conn.commit()
    #Close connection
    cur.close()
    flash('Article Deleted', 'success')
    return redirect(url_for('dashboard'))
  
if __name__ == '__main__':
 app.run(debug=True)