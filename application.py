from flask import Flask, render_template, redirect, url_for, request, session, logging, flash
# from flask_session import Session
# from flaskext.mysql import MySQL
import psycopg2
import psycopg2.extras
# from pymysql.cursors import DictCursor
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from functools import wraps
from flask_ckeditor import CKEditorField
from werkzeug.security import check_password_hash
# import mysql.connector

application = app = Flask(__name__)
app.secret_key = 'AjaySuperJosaa@2016KgpRKjvhvhv ghjvgv hvj'

# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'Aliya###2021'
# app.config['MYSQL_DATABASE_DB'] = 'rkhalldb'
# app.config['MYSQL_DATABASE_CURSORCLASS'] = 'DictCursor'
# init MYSQL
# mysql = MySQL(cursorclass=DictCursor)
# mysql.init_app(app)

conn = psycopg2.connect(host="ec2-34-234-228-127.compute-1.amazonaws.com", port="5432", user="dtqufuqcrdufjm", password="da12df8d94ff1a397c9122d049305b6a45967bec553c32f16466fdf6bbe9f89c", database="dapmmh4qk7ihei", sslmode="require")
conn.autocommit = True


app.config['CKEDITOR_PKG_TYPE'] = 'basic'


# Index
@app.route('/')
def index():
    # cur = mysql.get_db().cursor()

    # 
    # result = cur.execute("SELECT * FROM about WHERE id=11")

    # data = cur.fetchone()
    # # print(data[1])

    # if result > 0:
    #     return render_template('home.html', data=data)
    # else:
    #     msg = 'No data Found'
    #     return render_template('home.html', msg=msg)


    # # print(data[][1])

    # return render_template('home.html')

    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    result = cur.execute("SELECT * FROM photos WHERE category='OTHER'")

    photos = cur.fetchall()

    result = cur.execute("SELECT * FROM pages WHERE id=4")

    page_data = cur.fetchone()

    return render_template('home.html', photos=photos, page_data=page_data)

@app.route('/illu')
def illu():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("SELECT * FROM photos WHERE category='ILLUMINATION' ORDER BY year DESC")

    photos = cur.fetchall()

    result = cur.execute("SELECT * FROM pages WHERE id=1")

    page_data = cur.fetchone()
    
    return render_template('pages.html',photos=photos, page_data=page_data)

@app.route('/rangoli')
def rangoli():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("SELECT * FROM photos WHERE category='RANGOLI' ORDER BY year DESC")

    photos = cur.fetchall()

    
    result = cur.execute("SELECT * FROM pages WHERE id=2")

    page_data = cur.fetchone()
    
    return render_template('pages.html',photos=photos, page_data=page_data)

class GCForm(Form):
    head = SelectField('Select Head', choices=[('Sports & Games', 'Sports & Games'),('Social & Cultural', 'Social & Cultural'),('Technology', 'Technology')])
    subhead = StringField('Subhead')
    event = StringField('Event')
    captain = StringField('Captain')
    vcaptain = StringField('Vice Captain')
    laststanding = SelectField ('Last Year Standing', choices=[('None', 'None'),('Gold', 'Gold'),('Silver', 'Silver'),('Bronze', 'Bronze')])
    Submit = SubmitField('Submit')

@app.route('/gc')
def gc():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    result = cur.execute("SELECT * FROM photos WHERE category ='GENERAL CHAMPIONSHIP' ORDER BY year DESC")

    photos = cur.fetchall()
    
    result = cur.execute("SELECT * FROM pages WHERE id=3")

    page_data = cur.fetchone()

    result = cur.execute("SELECT * FROM gc")

    gc_data = cur.fetchall()

    result = cur.execute("SELECT distinct head,subhead from gc")

    subhead_data = cur.fetchall()
    
    return render_template('gc.html',photos=photos, page_data=page_data, gc_data=gc_data, subhead_data=subhead_data)



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about_srk/')
def about_srk():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("SELECT * FROM aboutsrk WHERE id=1")

    data = cur.fetchone()
    # print(data[1])
    # print(data[4])
    return render_template('about_srk.html', data=data)


@app.route('/hallcouncil')
def hallcouncil():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("SELECT * FROM hallcouncil")

    hallcouncil_data = cur.fetchall()

    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
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
    submit = SubmitField('Sign In')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        # Get stored hash
        data = cur.fetchone()
        if data is None:
            error = 'Invalid login'
            return render_template('login.html', error=error)

        password = data['password']
        print("\n")
        print(password)
        print("\n")

        # Compare Passwords
        if check_password_hash(password,password_candidate):
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


class PageForm(Form):
    title = StringField('Title')
    body = CKEditorField('Body')
    backgroungimage = StringField('Background Image Link: (Drive image link must be: https://drive.google.com/uc?export=view&id=XXX   where XXX is photo id)')
    videolink = StringField('Youtube Video Link')
    videobuttontext = StringField ('Video Button Text:')
    Submit = SubmitField('Submit')


@app.route('/edit_aboutsrk/', methods=['GET','POST'])
@is_logged_in
def edit_aboutsrk():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #cur = con.cursor()

    
    result = cur.execute("SELECT * FROM aboutsrk WHERE id = 1")

    srk_data = cur.fetchone()

    form = PageForm(request.form)

    form.title.data = srk_data['title']
    form.body.data = srk_data['aboutsrk']

    if request.method == 'POST':
        title=request.form['title']
        body=request.form['body']

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #cur = con.cursor()

        cur.execute("UPDATE aboutsrk SET title=%s, aboutsrk=%s where id=1",(title,body));
        conn.commit()
        # cur.close()

        return redirect(url_for('about_srk'))

    return render_template('edit_aboutsrk.html', form=form)


# Edit Illu, Rangoli, GC page data
@app.route('/edit_page/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_pages(id):
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #cur = con.cursor()

    result = cur.execute("SELECT * FROM pages WHERE id = %s", (id))

    page_data = cur.fetchone()

    form = PageForm(request.form)

    form.title.data = page_data['title']
    form.videolink.data = page_data['videolink']
    form.videobuttontext.data = page_data['videobuttontext']
    form.backgroungimage.data = page_data['backgroungimage']
    form.body.data=page_data['body']

    if request.method == 'POST':
        title=request.form['title']
        videolink=request.form['videolink']
        videobuttontext=request.form['videobuttontext']
        backgroungimage=request.form['backgroungimage']
        body=request.form['body']

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #cur = con.cursor()

        cur.execute("UPDATE pages SET title=%s, videolink=%s, videobuttontext=%s, backgroungimage=%s, body=%s where id=%s",(title,videolink,videobuttontext,backgroungimage,body,id));
        conn.commit()
        # cur.close()

        if id == 1:
            return redirect(url_for('illu'))
        if id == 2:
            return redirect(url_for('rangoli'))
        if id == 3:
            return redirect(url_for('gc'))
        if id == 4:
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

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #cur = con.cursor()

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("INSERT INTO hallcouncil(name, profilephoto,email, mobile, fbprofile,inprofile,post) values(%s,%s,%s,%s,%s,%s,%s)", (name,profilephoto,email,mobile,fbprofile,inprofile,hcm_post));
        conn.commit()
        # cur.close()
        return redirect(url_for('hallcouncil'))

    return render_template('add_hallcouncil.html', form=form)

@app.route('/edit_hcm_<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_hcm(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #cur = con.cursor()

    
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

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #cur = con.cursor()

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("UPDATE hallcouncil SET post=%s, name=%s, profilephoto=%s,email=%s, mobile=%s, fbprofile=%s,inprofile=%s where id=%s", (hcm_post,name,profilephoto,email,mobile,fbprofile,inprofile,id));
        conn.commit()
        # cur.close()
        return redirect(url_for('hallcouncil'))

    return render_template('edit_hcm.html', form=form, hcm_data=hcm_data)

@app.route('/delete_hcm_<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_hcm(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #cur = con.cursor()

    
    result = cur.execute("DELETE FROM hallcouncil WHERE id = %s", [id])

    conn.commit()

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

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("INSERT INTO captains_secretaries(post, title, name, profilephoto,email, mobile, fbprofile,inprofile) values(%s,%s,%s,%s,%s,%s,%s,%s)", (other_post,title,name,profilephoto,email,mobile,fbprofile,inprofile));
        conn.commit()
        # cur.close()
        return redirect(url_for('captains_secretaries'))

    return render_template('add_captains_secretaries.html', form=form)

@app.route('/edit_captains_secretaries_<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_captains_secretaries(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
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

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("UPDATE captains_secretaries SET post=%s, title=%s, name=%s, profilephoto=%s,email=%s, mobile=%s, fbprofile=%s,inprofile=%s where id=%s", (other_post, title, name,profilephoto,email,mobile,fbprofile,inprofile,id));
        conn.commit()
        # cur.close()
        return redirect(url_for('captains_secretaries'))

    return render_template('edit_captains_secretaries.html', form=form, captains_secretaries_data=captains_secretaries_data)

@app.route('/delete_captains_secretaries_<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_captains_secretaries(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("DELETE FROM captains_secretaries WHERE id = %s", [id])

    conn.commit()

    #Close connection
    #cur.close()

    flash('Data Deleted', 'success')

    return redirect(url_for('captains_secretaries'))

class PhotoForm(Form):
    category = SelectField('Category of photo', choices=[('ILLUMINATION','ILLUMINATION'),('RANGOLI','RANGOLI'),('GENERAL CHAMPIONSHIP','GENERAL CHAMPIONSHIP'),('OTHER','OTHER')])
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

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("INSERT INTO photos(category,title, photolink,year) values(%s,%s,%s,%s)", (category,title,photolink,year));
        conn.commit()
        # cur.close()
        return redirect(url_for('index'))

    return render_template('add_photos.html', form=form)

@app.route('/delete_photo_<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_photo(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("DELETE FROM photos WHERE id = %s", [id])

    conn.commit()

    #Close connection
    #cur.close()

    flash('Data Deleted', 'success')

    return redirect(url_for('index'))



@app.route('/add_gc_event/', methods=['GET','POST'])
@is_logged_in
def add_gc_event():
    form = GCForm(request.form)

    print (form.errors)
    if request.method == 'POST':
        head=request.form['head']
        subhead=request.form['subhead']
        event=request.form['event']
        captain=request.form['captain']
        vcaptain=request.form['vcaptain']
        laststanding=request.form['laststanding']

        # print(name + email)

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("INSERT INTO gc (head, subhead, event, captain,vcaptain, laststanding) values(%s,%s,%s,%s,%s,%s)", (head,subhead,event,captain,vcaptain,laststanding));
        conn.commit()
        # cur.close()
        return redirect(url_for('add_gc_event'))

    return render_template('add_gc_event.html', form=form)

@app.route('/edit_gc_event_<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_gc_event(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("SELECT * FROM gc WHERE id = %s", [id])

    gc_event_data = cur.fetchone()

    form = GCForm(request.form)

    form.head.data = gc_event_data['head']
    form.subhead.data = gc_event_data['subhead']
    form.event.data = gc_event_data['event']
    form.captain.data = gc_event_data['captain']
    form.vcaptain.data = gc_event_data['vcaptain']
    form.laststanding.data = gc_event_data['laststanding']

    print (form.errors)
    if request.method == 'POST':
        head=request.form['head']
        subhead=request.form['subhead']
        event=request.form['event']
        captain=request.form['captain']
        vcaptain=request.form['vcaptain']
        laststanding=request.form['laststanding']
        # print(name + email)

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("UPDATE gc SET head=%s, subhead=%s, event=%s, captain=%s,laststanding=%s, vcaptain=%s where id=%s", (head, subhead, event,captain,laststanding,vcaptain,id));
        conn.commit()
        # cur.close()
        return redirect(url_for('gc'))

    return render_template('edit_gc_event.html', form=form, gc_event_data=gc_event_data)

@app.route('/delete_gc_event_<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_gc_event(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("DELETE FROM gc WHERE id = %s", [id])

    conn.commit()

    #Close connection
    #cur.close()

    flash('Data Deleted', 'success')

    return redirect(url_for('gc'))
    

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0', port='84')