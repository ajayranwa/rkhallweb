from flask import Flask, render_template, redirect, url_for, request, session, logging, flash
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from functools import wraps
from flask_ckeditor import CKEditorField
# import mysql.connector

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Aliya###2021'
app.config['MYSQL_DATABASE_DB'] = 'rkhalldb'
# app.config['MYSQL_DATABASE_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)

app.config['CKEDITOR_PKG_TYPE'] = 'basic'
# ckeditor = CKEditor(app)

# cur = mysql.get_db().cursor()

# result = cur.execute("SELECT * FROM about WHERE id=11")

# data = cur.fetchone()

# print(data)


# Index
@app.route('/')
def index():
    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM about WHERE id=11")

    data = cur.fetchone()
    # print(data[1])

    if result > 0:
        return render_template('home.html', data=data)
    else:
        msg = 'No data Found'
        return render_template('home.html', msg=msg)


    # print(data[][1])

    return render_template('home.html')

@app.route('/illu')
def illu():
    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM photos WHERE category='ILLUMINATION' ORDER BY year DESC")

    photos = cur.fetchall()

    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM pages WHERE id=1")

    page_data = cur.fetchone()
    
    return render_template('pages.html',photos=photos, page_data=page_data)

@app.route('/rangoli')
def rangoli():
    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM photos WHERE category='RANGOLI' ORDER BY year DESC")

    photos = cur.fetchall()

    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM pages WHERE id=2")

    page_data = cur.fetchone()
    
    return render_template('pages.html',photos=photos, page_data=page_data)

@app.route('/gc')
def gc():
    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM photos ORDER BY year DESC")

    photos = cur.fetchall()

    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM pages WHERE id=3")

    page_data = cur.fetchone()
    
    return render_template('gc.html',photos=photos, page_data=page_data)

@app.route('/gallery')
def gallery():
    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM photos WHERE category='OTHER'")

    photos = cur.fetchall()

    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM pages WHERE id=4")

    page_data = cur.fetchone()
    
    return render_template('pages.html',photos=photos, page_data=page_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about_srk/')
def about_srk():
    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM aboutsrk WHERE id=1")

    data = cur.fetchone()
    # print(data[1])
    # print(data[4])
    if result > 0:
        return render_template('about_srk.html', data=data)
    else:
        msg = 'No data Found'
        return render_template('about_srk.html', msg=msg)

    return render_template('about_srk.html')

@app.route('/captains_secretaries')
def captains_secretaries():
    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM captains_secretaries")

    captains_secretaries_data = cur.fetchall()

    return render_template('captains_secretaries.html', captains_secretaries_data=captains_secretaries_data)

@app.route('/hallcouncil')
def hallcouncil():
    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM hallcouncil")

    hallcouncil_data = cur.fetchall()

    cur = mysql.get_db().cursor()

    # Get user by username
    result = cur.execute("SELECT * FROM captains_secretaries")

    captains_secretaries_data = cur.fetchall()

    return render_template('hallcouncil.html', hallcouncil_data=hallcouncil_data, captains_secretaries_data=captains_secretaries_data)

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    remember_me = BooleanField('Remember Me')
    # submit = SubmitField('Sign In')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.get_db().cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if password_candidate == password and username == data['username']:
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
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
@app.route('/logout/')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


class EditPageForm(Form):
    title = StringField('Title')
    body = CKEditorField('Body')
    backgroungimage = StringField('Background Image Link: (Drive image link must be: https://drive.google.com/uc?export=view&id=XXX   where XXX is photo id)')
    videolink = StringField('Youtube Video Link')
    videobuttontext = StringField ('Video Button Text:')
    Submit = SubmitField('Submit')

@app.route('/edit_aboutrk/', methods=['GET','POST'])
@is_logged_in
def edit_aboutrk():
    con = mysql.connect()
    cur = con.cursor()

    
    result = cur.execute("SELECT * FROM about WHERE id = 11")

    rk_data = cur.fetchone()

    form = EditPageForm(request.form)

    form.title.data = rk_data['title']
    form.body.data = rk_data['aboutrk']
    form.videolink.data = rk_data['videolink']

    if request.method == 'POST':
        title=request.form['title']
        body=request.form['body']
        videolink=request.form['videolink']

        con = mysql.connect()
        cur = con.cursor()

        cur.execute("UPDATE about SET title=%s, aboutrk=%s, videolink=%s where id=11",(title,body,videolink));
        con.commit()
        # cur.close()

        return redirect(url_for('index'))

    return render_template('edit_aboutrk.html', form=form)

@app.route('/edit_aboutsrk/', methods=['GET','POST'])
@is_logged_in
def edit_aboutsrk():
    con = mysql.connect()
    cur = con.cursor()

    
    result = cur.execute("SELECT * FROM aboutsrk WHERE id = 1")

    srk_data = cur.fetchone()

    form = EditPageForm(request.form)

    form.title.data = srk_data['title']
    form.body.data = srk_data['aboutsrk']

    if request.method == 'POST':
        title=request.form['title']
        body=request.form['body']

        con = mysql.connect()
        cur = con.cursor()

        cur.execute("UPDATE aboutsrk SET title=%s, aboutsrk=%s, profilephoto=%s where id=1",(title,body,profilephoto));
        con.commit()
        # cur.close()

        return redirect(url_for('about_srk'))

    return render_template('edit_aboutsrk.html', form=form)


# Edit Illu, Rangoli, GC page data
@app.route('/edit_page/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_pages(id):
    con = mysql.connect()
    cur = con.cursor()

    result = cur.execute("SELECT * FROM pages WHERE id = %s", (id))

    page_data = cur.fetchone()

    form = EditPageForm(request.form)

    form.title.data = page_data['title']
    form.videolink.data = page_data['videolink']
    form.videobuttontext.data = page_data['videobuttontext']
    form.backgroungimage.data = page_data['backgroungimage']

    if request.method == 'POST':
        title=request.form['title']
        videolink=request.form['videolink']
        videobuttontext=request.form['videobuttontext']
        backgroungimage=request.form['backgroungimage']

        con = mysql.connect()
        cur = con.cursor()

        cur.execute("UPDATE pages SET title=%s, videolink=%s, videobuttontext=%s, backgroungimage=%s where id=%s",(title,videolink,videobuttontext,backgroungimage,id));
        con.commit()
        # cur.close()

        return redirect(url_for('index'))

    return render_template('edit_pages.html', form=form)

class HallCouncilForm(Form):
    hcm_post = SelectField('hcm_Post', choices=[('HALL PRESIDENT', 'HALL PRESIDENT'), ('SECOND SENATE MEMBER', 'SECOND SENATE MEMBER'),('GENERAL SECRETARY Alumni Affairs','GENERAL SECRETARY Alumni Affairs'), ('GENERAL SECRETARY SOCIAL AND CULTURAL','GENERAL SECRETARY SOCIAL AND CULTURAL'), ('GENERAL SECRETARY SPORTS AND GAMES','GENERAL SECRETARY SPORTS AND GAMES'), ('GENERAL SECRETARY TECHNOLOGY','GENERAL SECRETARY TECHNOLOGY'), ('GENERAL SECRETARY MESS','GENERAL SECRETARY MESS'), ('GENERAL SECRETARY STUDENT WELFARE','GENERAL SECRETARY STUDENT WELFARE'),('WARDEN','WARDEN'),('ASS. WARDEN MAINTENENCE','ASS. WARDEN MAINTENENCE'),('ASS. WARDEN MESS','ASS. WARDEN MESS')])
    other_post = SelectField('Select One', choices=[('SECRETARY','SECRETARY'),('CAPTAIN','CAPTAIN'),('VICE CAPTAIN','VICE CAPTAIN'),('COORDINATOR','COORDINATOR')])
    title = StringField('Title (ex- BASKETBALL, TECHNOLOGY)')
    name = StringField('Name:', [validators.Length(min=1, max=200, message=('Link too long.'))])
    mobile = StringField('Mobile No')
    profilephoto = StringField('Profilephoto (Drive image link must be: https://drive.google.com/uc?export=view&id=XXX   where XXX is photo id)')
    email = StringField('Email')
    fbprofile = StringField('Fbprofile')
    inprofile = StringField('Website / Linkedin Profile Link')
    Submit = SubmitField('Submit')

@app.route('/add_hallcouncil/', methods=['GET','POST'])
@is_logged_in
def add_hallcouncil():
    form = HallCouncilForm(request.form)

    print (form.errors)
    if request.method == 'POST':
        hcm_post=request.form['hcm_post']
        name=request.form['name']
        mobile=request.form['mobile']
        profilephoto=request.form['profilephoto']
        email=request.form['email']
        fbprofile=request.form['fbprofile']
        inprofile=request.form['inprofile']

        # print(name + email)

        con = mysql.connect()
        cur = con.cursor()

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     con.commit()
        # else:
        cur.execute("INSERT INTO hallcouncil(name, profilephoto,email, mobile, fbprofile,inprofile,post) values(%s,%s,%s,%s,%s,%s,%s)", (name,profilephoto,email,mobile,fbprofile,inprofile,hcm_post));
        con.commit()
        # cur.close()
        return redirect(url_for('hallcouncil'))

    return render_template('add_hallcouncil.html', form=form)

@app.route('/edit_hcm_<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_hcm(id):
    # Create cursor
    con = mysql.connect()
    cur = con.cursor()

    
    result = cur.execute("SELECT * FROM hallcouncil WHERE id = %s", [id])

    hcm_data = cur.fetchone()

    form = HallCouncilForm(request.form)

    form.hcm_post.data = hcm_data['post']
    form.name.data = hcm_data['name']
    form.mobile.data = hcm_data['mobile']
    form.profilephoto.data = hcm_data['profilephoto']
    form.email.data = hcm_data['email']
    form.fbprofile.data = hcm_data['fbprofile']
    form.inprofile.data = hcm_data['inprofile']

    print (form.errors)
    if request.method == 'POST':
        hcm_post=request.form['hcm_post']
        name=request.form['name']
        mobile=request.form['mobile']
        profilephoto=request.form['profilephoto']
        email=request.form['email']
        fbprofile=request.form['fbprofile']
        inprofile=request.form['inprofile']

        # print(name + email)

        con = mysql.connect()
        cur = con.cursor()

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     con.commit()
        # else:
        cur.execute("UPDATE hallcouncil SET post=%s, name=%s, profilephoto=%s,email=%s, mobile=%s, fbprofile=%s,inprofile=%s where id=%s", (hcm_post,name,profilephoto,email,mobile,fbprofile,inprofile,id));
        con.commit()
        # cur.close()
        return redirect(url_for('hallcouncil'))

    return render_template('edit_hcm.html', form=form, hcm_data=hcm_data)

@app.route('/delete_hcm_<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_hcm(id):
    # Create cursor
    con = mysql.connect()
    cur = con.cursor()

    
    result = cur.execute("DELETE FROM hallcouncil WHERE id = %s", [id])

    con.commit()

    #Close connection
    #cur.close()

    flash('Data Deleted', 'success')

    return redirect(url_for('hallcouncil'))

@app.route('/add_captains_secretaries/', methods=['GET','POST'])
@is_logged_in
def add_captains_secretaries():
    form = HallCouncilForm(request.form)

    print (form.errors)
    if request.method == 'POST':
        other_post=request.form['other_post']
        title=request.form['title']
        name=request.form['name']
        mobile=request.form['mobile']
        profilephoto=request.form['profilephoto']
        email=request.form['email']
        fbprofile=request.form['fbprofile']
        inprofile=request.form['inprofile']

        # print(name + email)

        con = mysql.connect()
        cur = con.cursor()

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     con.commit()
        # else:
        cur.execute("INSERT INTO captains_secretaries(post, title, name, profilephoto,email, mobile, fbprofile,inprofile) values(%s,%s,%s,%s,%s,%s,%s,%s)", (other_post,title,name,profilephoto,email,mobile,fbprofile,inprofile));
        con.commit()
        # cur.close()
        return redirect(url_for('captains_secretaries'))

    return render_template('add_captains_secretaries.html', form=form)

@app.route('/edit_captains_secretaries_<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_captains_secretaries(id):
    # Create cursor
    con = mysql.connect()
    cur = con.cursor()

    
    result = cur.execute("SELECT * FROM captains_secretaries WHERE id = %s", [id])

    captains_secretaries_data = cur.fetchone()

    form = HallCouncilForm(request.form)

    form.other_post.data = captains_secretaries_data['post']
    form.title.data = captains_secretaries_data['title']
    form.name.data = captains_secretaries_data['name']
    form.mobile.data = captains_secretaries_data['mobile']
    form.profilephoto.data = captains_secretaries_data['profilephoto']
    form.email.data = captains_secretaries_data['email']
    form.fbprofile.data = captains_secretaries_data['fbprofile']
    form.inprofile.data = captains_secretaries_data['inprofile']

    print (form.errors)
    if request.method == 'POST':
        other_post=request.form['other_post']
        title=request.form['title']
        name=request.form['name']
        mobile=request.form['mobile']
        profilephoto=request.form['profilephoto']
        email=request.form['email']
        fbprofile=request.form['fbprofile']
        inprofile=request.form['inprofile']

        # print(name + email)

        con = mysql.connect()
        cur = con.cursor()

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     con.commit()
        # else:
        cur.execute("UPDATE captains_secretaries SET post=%s, title=%s, name=%s, profilephoto=%s,email=%s, mobile=%s, fbprofile=%s,inprofile=%s where id=%s", (other_post, title, name,profilephoto,email,mobile,fbprofile,inprofile,id));
        con.commit()
        # cur.close()
        return redirect(url_for('captains_secretaries'))

    return render_template('edit_captains_secretaries.html', form=form, captains_secretaries_data=captains_secretaries_data)

@app.route('/delete_captains_secretaries_<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_captains_secretaries(id):
    # Create cursor
    con = mysql.connect()
    cur = con.cursor()

    
    result = cur.execute("DELETE FROM captains_secretaries WHERE id = %s", [id])

    con.commit()

    #Close connection
    #cur.close()

    flash('Data Deleted', 'success')

    return redirect(url_for('captains_secretaries'))

class PhotoForm(Form):
    category = SelectField('Category of photo', choices=[('ILLUMINATION','ILLUMINATION'),('RANGOLI','RANGOLI'),('SPORTS & GAMES','SPORTS & GAMES'),('TECHNOLOGY','TECHNOLOGY'),('SOCIAL & CULTURAL','SOCIAL & CULTURAL'),('OTHER','OTHER')])
    title = StringField('Photo Title: ex- any themes, Gold')
    photolink = StringField('Photolink (Drive image link must be: https://drive.google.com/uc?export=view&id=XXX   where XXX is photo id)')
    year = IntegerField('Year (first year of session ex- for 2019-20 write 2019)')

@app.route('/add_photos/', methods=['GET','POST'])
@is_logged_in 
def add_photos():
    form = PhotoForm(request.form)

    if request.method == 'POST':
        category=request.form['category']
        title=request.form['title']
        photolink=request.form['photolink']
        year=request.form['year']

        # print(name + email)

        con = mysql.connect()
        cur = con.cursor()

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     con.commit()
        # else:
        cur.execute("INSERT INTO photos(category,title, photolink,year) values(%s,%s,%s,%s)", (category,title,photolink,year));
        con.commit()
        # cur.close()
        return redirect(url_for('index'))

    return render_template('add_photos.html', form=form)

@app.route('/delete_photo_<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_photo(id):
    # Create cursor
    con = mysql.connect()
    cur = con.cursor()

    
    result = cur.execute("DELETE FROM photos WHERE id = %s", [id])

    con.commit()

    #Close connection
    #cur.close()

    flash('Data Deleted', 'success')

    return redirect(url_for('index'))

    

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)