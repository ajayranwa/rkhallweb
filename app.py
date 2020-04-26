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
from werkzeug.security import generate_password_hash,check_password_hash
from convertdrivelink import create_embed_link
from addtogsheets import addtoregistration_sheet, addtopledge_sheet
from datetime import datetime
import datetime
# import mysql.connector


application = app = Flask(__name__)
app.secret_key = 'AjaySuperJosaa2hbh016KgpRKjvhvhv ghjvgv hvj'

# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'Aliya###2021'
# app.config['MYSQL_DATABASE_DB'] = 'rkhalldb'
# app.config['MYSQL_DATABASE_CURSORCLASS'] = 'DictCursor'
# init MYSQL
# mysql = MySQL(cursorclass=DictCursor)
# mysql.init_app(app)

conn = psycopg2.connect(host="xyz", port="5432", user="postgres", password="xyz", database="rkdb", sslmode="require")
conn.autocommit = True


# app.config['CKEDITOR_PKG_TYPE'] = 'classic'


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
    
    result = cur.execute("SELECT * FROM photos WHERE category='OTHER' ORDER BY year DESC")

    photos = cur.fetchall()

    result = cur.execute("SELECT * FROM insights")

    insight_data = cur.fetchone()

    result = cur.execute("SELECT * FROM pages WHERE id=4")

    page_data = cur.fetchone()

    result = cur.execute("SELECT * FROM hallawardee order by id")

    hallawardee_data = cur.fetchall()

    result = cur.execute("SELECT * FROM awardeelist ORDER BY year")

    awardeelist = cur.fetchall()

    result = cur.execute("SELECT * FROM articles where type='Story' and is_approved='APPROVED' ")

    articles = cur.fetchall()

    return render_template('home.html', photos=photos, articles=articles , page_data=page_data, insight_data=insight_data, hallawardee_data=hallawardee_data,awardeelist=awardeelist)

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
    
    result = cur.execute("SELECT * FROM pages WHERE id=2")

    page_data = cur.fetchone()

    result = cur.execute("select distinct year from photos where category='RANGOLI' ORDER BY year DESC")

    year_data = cur.fetchall()
    # print(year_data)
    albums = {}
    for year in year_data:
        albums[year[0]]={}
        result = cur.execute("SELECT photolink FROM photos WHERE category='RANGOLI' and year = %s",(year))

        photolink = cur.fetchone()

        albums[year[0]]['year']=year[0]
        albums[year[0]]['photolink']=photolink[0]

        result = cur.execute("SELECT * FROM photos WHERE category='RANGOLI' and year=%s",(year))

        photos = cur.fetchall()

        albums[year[0]]['photos']=photos
        # print(year[0])
    # print(albums)
    # for album in albums:
    #     # print(albums[album]['photolink'])
    #     # print("\n")
    #     # print(album)
    #     for photo in albums[album]['photos']:
    #         print(album)
    #         print("-----")
    #         print(photo['id'])
    #         print("\n")

    
    return render_template('pages.html',photos=photos, page_data=page_data, albums=albums)

class GCForm(Form):
    head = SelectField('Select Head', choices=[('Sports & Games', 'Sports & Games'),('Social & Cultural', 'Social & Cultural'),('Technology', 'Technology')])
    subhead = StringField('Subhead', validators=[DataRequired()])
    event = StringField('Event', validators=[DataRequired()])
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



@app.route('/alumni', methods=['GET','POST'])
def alumni():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    result = cur.execute("SELECT * FROM photos WHERE category ='ALUMNI' ORDER BY year")

    photos = cur.fetchall()

    result = cur.execute("SELECT * FROM pages WHERE id=5")

    page_data = cur.fetchone()

    result = cur.execute("SELECT * FROM articles where type='RECENT_DEVELOPMENTS' and is_approved='APPROVED' ")

    RECENT_DEVELOPMENTS = cur.fetchall()

    result = cur.execute("SELECT * FROM articles where type='FUTURE_PROPOSALS' and is_approved='APPROVED' ")

    FUTURE_PROPOSALS = cur.fetchall()

    # form = AlumniForm(request.form)

    if request.method == 'POST':
        # Get Form Fields
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        batchof = request.form['batchof']
        department = request.form['department']
        location = request.form['location']
        # amount = request.form['amount']
        now = datetime.datetime.now()

        List = []
        List.append(now.strftime("%Y-%m-%d %H:%M:%S"))
        List.append(name)
        List.append(email)
        List.append(mobile)
        List.append(batchof)
        List.append(department)
        List.append(location)
        if 'amount' in request.form:
            amount = request.form['amount']
            List.append(amount)
            addtopledge_sheet(List)
        else:
            addtoregistration_sheet(List)
        # print(List)

    return render_template('alumni.html',photos=photos,page_data=page_data, RECENT_DEVELOPMENTS=RECENT_DEVELOPMENTS, FUTURE_PROPOSALS=FUTURE_PROPOSALS)

class ArticlesForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    batchof = StringField('Batch of.', validators=[DataRequired()])
    titleimage = StringField('Card Title Image.', validators=[DataRequired()])
    title = StringField('Card Title', validators=[DataRequired()])
    description = StringField('Card Description', validators=[DataRequired()])
    timetoread = IntegerField ('Time to read.', validators=[DataRequired()])
    body = CKEditorField('Body: (Keep default font size=16, most optimum photo width for article= 200px height=auto)', validators=[DataRequired()])
    type = SelectField('Select one:', choices=[('Story','Story'),('RECENT_DEVELOPMENTS','RECENT_DEVELOPMENTS'),('FUTURE_PROPOSALS','FUTURE_PROPOSALS')])
    Submit = SubmitField('Submit')

@app.route('/article/<string:id>', methods=['GET', 'POST'])
def article(id):
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    result = cur.execute("SELECT * FROM articles where id=%s",[id])

    article = cur.fetchone()

    result = cur.execute("select create_date from articles where id=%s",[id])

    result = cur.execute("select * from comments where article_id=%s",[id])
    comments_data = cur.fetchall()

    article_data = {}

    for comment in comments_data:
        article_data[comment[0]]={}
        article_data[comment[0]]['id']=[comment[0]]
        article_data[comment[0]]['comment']=[comment[1]]
        article_data[comment[0]]['name']=[comment[3]]
        article_data[comment[0]]['batchof'] =[comment[4]]
        article_data[comment[0]]['create_date']=[comment[5]]
        result = cur.execute("select * from replies where comment_id=%s",[comment[0]])
        reply_data = cur.fetchall()
        article_data[comment[0]]['replies'] = reply_data
 
    if request.method == 'POST':
        if 'comment' in request.form:
            comment = request.form['comment']
            name = request.form['name']
            batchof = request.form['batchof']

            cur.execute("INSERT INTO comments(comment,name, batchof, article_id) values(%s,%s,%s,%s)", (comment,name,batchof,id));
            conn.commit()

        return redirect(url_for('article',id=id))

    return render_template('article.html',article=article, article_data=article_data)


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about_srk/')
def about_srk():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    result = cur.execute("SELECT * FROM aboutsrk WHERE id=1")

    data = cur.fetchone()
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


class INSIGHTSForm(Form):
    playground = IntegerField('No. of Playgrounds:',validators=[DataRequired()])
    hallmember = IntegerField('No. of Hall Members:',validators=[DataRequired()])
    rooms = IntegerField('No. of Rooms:',validators=[DataRequired()])
    shops = IntegerField('No. of Shops:',validators=[DataRequired()])
    illuminationdiyas = IntegerField('No. of Illumination Diyas:',validators=[DataRequired()])
    sportsgc = IntegerField('No. of Sports GC:',validators=[DataRequired()])
    socultgc = IntegerField('No. of Socult GC:',validators=[DataRequired()])
    startups = IntegerField('No. of Startups:',validators=[DataRequired()])
    Submit = SubmitField('Submit')

@app.route('/edit_insights/', methods=['GET','POST'])
@is_logged_in
def edit_insights():
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #cur = con.cursor()

    
    result = cur.execute("SELECT * FROM insights WHERE id = 1")

    insight_data = cur.fetchone()

    form = INSIGHTSForm(request.form)

    form.playground.data = insight_data['playground']
    form.hallmember.data = insight_data['hallmember']
    form.rooms.data = insight_data['rooms']
    form.illuminationdiyas.data = insight_data['illuminationdiyas']
    form.shops.data = insight_data['shops']
    form.sportsgc.data = insight_data['sportsgc']
    form.socultgc.data = insight_data['socultgc']
    form.startups.data = insight_data['startups']

    if request.method == 'POST':
        playground=request.form['playground']
        hallmember=request.form['hallmember']
        rooms=request.form['rooms']
        illuminationdiyas=request.form['illuminationdiyas']
        shops=request.form['shops']
        sportsgc=request.form['sportsgc']
        socultgc=request.form['socultgc']
        startups=request.form['startups']

        # print(name + email)

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #cur = con.cursor()

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("UPDATE insights SET playground=%s, hallmember=%s, illuminationdiyas=%s,shops=%s, rooms=%s, sportsgc=%s,socultgc=%s, startups=%s where id=1", (playground,hallmember,illuminationdiyas,shops,rooms,sportsgc,socultgc,startups));
        conn.commit()
        # cur.close()
        return redirect(url_for('index'))

    return render_template('edit_insights.html', form=form, insight_data=insight_data)


class PageForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = CKEditorField('Body: (Keep default font size=16)')
    backgroungimage = StringField('Background Image Link: (Shareable Drive Photo Link or any other direct photo link)',validators=[DataRequired()])
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
        backgroungimage=create_embed_link(request.form['backgroungimage'])
        body=request.form['body']

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #cur = con.cursor()

        cur.execute("UPDATE pages SET title=%s, videolink=%s, videobuttontext=%s, backgroungimage=%s, body=%s where id=%s",(title,videolink,videobuttontext,backgroungimage,body,id));
        conn.commit()
        # cur.close()

        if id == '1':
            return redirect(url_for('illu'))
        elif id == '2':
            return redirect(url_for('rangoli'))
        elif id == '3':
            return redirect(url_for('gc'))
        elif id == '4':
            return redirect(url_for('index'))
        elif id == '5':
            return redirect(url_for('alumni'))

    return render_template('edit_pages.html', form=form)

class HallCouncilForm(Form):
    hcm_post = SelectField('hcm_Post', choices=[('HALL PRESIDENT', 'HALL PRESIDENT'), ('SECOND SENATE MEMBER', 'SECOND SENATE MEMBER'),('GENERAL SECRETARY ALUMNI AFFAIRS','GENERAL SECRETARY ALUMNI AFFAIRS'),('GENERAL SECRETARY MAINTENENCE','GENERAL SECRETARY MAINTENENCE'), ('GENERAL SECRETARY SOCIAL AND CULTURAL','GENERAL SECRETARY SOCIAL AND CULTURAL'), ('GENERAL SECRETARY SPORTS AND GAMES','GENERAL SECRETARY SPORTS AND GAMES'), ('GENERAL SECRETARY TECHNOLOGY','GENERAL SECRETARY TECHNOLOGY'), ('GENERAL SECRETARY MESS','GENERAL SECRETARY MESS'), ('GENERAL SECRETARY STUDENT WELFARE','GENERAL SECRETARY STUDENT WELFARE'),('WARDEN','WARDEN'),('ASST. WARDEN MAINTENENCE','ASST. WARDEN MAINTENENCE'),('ASST. WARDEN MESS','ASST. WARDEN MESS')])
    other_post = SelectField('Select One', choices=[('SECRETARY','SECRETARY'),('CAPTAIN','CAPTAIN'),('VICE CAPTAIN','VICE CAPTAIN'),('COORDINATOR','COORDINATOR')])
    title = StringField('Title (ex- BASKETBALL, TECHNOLOGY)')
    name = StringField('Name:', validators=[DataRequired()])
    mobile = StringField('Mobile No')
    profilephoto = StringField('Profilephoto (Shareable Drive Photo Link or any other direct photo link)',validators=[DataRequired()])
    email = StringField('Email')
    fbprofile = StringField('Fbprofile')
    inprofile = StringField('Website / Linkedin Profile Link')
    Submit = SubmitField('Submit')

@app.route('/add_hallcouncil/', methods=['GET','POST'])
@is_logged_in
def add_hallcouncil():
    form = HallCouncilForm(request.form)

    if request.method == 'POST':
        hcm_post=request.form['hcm_post']
        name=request.form['name']
        mobile=request.form['mobile']
        profilephoto=create_embed_link(request.form['profilephoto'])
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

    if request.method == 'POST':
        hcm_post=request.form['hcm_post']
        name=request.form['name']
        mobile=request.form['mobile']
        profilephoto=create_embed_link(request.form['profilephoto'])
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


    return redirect(url_for('hallcouncil'))

@app.route('/add_cordi_secretaries/', methods=['GET','POST'])
@is_logged_in
def add_cordi_secretaries():
    form = HallCouncilForm(request.form)

    if request.method == 'POST':
        other_post=request.form['other_post']
        title=request.form['title']
        name=request.form['name']
        mobile=request.form['mobile']
        profilephoto=create_embed_link(request.form['profilephoto'])
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
        return redirect(url_for('hallcouncil'))

    return render_template('add_cordi_secretaries.html', form=form)

@app.route('/edit_cordi_secretaries_<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_cordi_secretaries(id):
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

    if request.method == 'POST':
        other_post=request.form['other_post']
        title=request.form['title']
        name=request.form['name']
        mobile=request.form['mobile']
        profilephoto=create_embed_link(request.form['profilephoto'])
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
        return redirect(url_for('hallcouncil'))

    return render_template('edit_cordi_secretaries.html', form=form, captains_secretaries_data=captains_secretaries_data)

@app.route('/delete_cordi_secretaries_<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_cordi_secretaries(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("DELETE FROM captains_secretaries WHERE id = %s", [id])

    conn.commit()

    #Close connection
    #cur.close()


    return redirect(url_for('hallcouncil'))

class PhotoForm(Form):
    category = SelectField('Category of photo', choices=[('ILLUMINATION','ILLUMINATION'),('RANGOLI','RANGOLI'),('GENERAL CHAMPIONSHIP','GENERAL CHAMPIONSHIP'),('ALUMNI','ALUMNI'),('OTHER','OTHER')])
    title = StringField('Photo Title: ex- any themes, Gold')
    photolink = StringField('Shareable Drive Photo Link or any other direct photo link',validators=[DataRequired()])
    year = IntegerField('Year (first year of session ex- for 2019-20 write 2019)',validators=[DataRequired()])

@app.route('/add_photos/', methods=['GET','POST'])
@is_logged_in 
def add_photos():
    form = PhotoForm(request.form)

    if request.method == 'POST':
        category=request.form['category']
        title=request.form['title']
        photolink= create_embed_link(request.form['photolink'])
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


    return redirect(url_for('index'))



@app.route('/add_gc_event/', methods=['GET','POST'])
@is_logged_in
def add_gc_event():
    form = GCForm(request.form)

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


    return redirect(url_for('gc'))
 
@app.route('/add_article/<string:type>/', methods=['GET','POST'])
def add_article(type):
    form = ArticlesForm(request.form)

    if request.method == 'POST':
        titleimage=create_embed_link(request.form['titleimage'])
        title=request.form['title']
        description=request.form['description']
        body=request.form['body']

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        if 'name' in request.form:
            name=request.form['name']
            batchof=request.form['batchof']
            timetoread=request.form['timetoread']

            cur.execute("INSERT INTO articles (name, batchof, titleimage,title, description,timetoread,body,type) values(%s,%s,%s,%s,%s,%s,%s,%s)", (name,batchof,titleimage,title,description,timetoread,body,type));
            conn.commit()
            cur.close()
            return redirect(url_for('index'))
        else:
            cur.execute("INSERT INTO articles (name, batchof, titleimage,title, description,body,type) values('NULL','NULL',%s,%s,%s,%s,%s)", (titleimage,title,description,body,type));
            conn.commit()
            cur.close()
            return redirect(url_for('alumni'))

    return render_template('add_article.html', form=form, type=type)

@app.route('/article_dashboard/')
def article_dashboard():
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    return render_template('article_dashboard.html',articles=articles)

@app.route('/edit_article/<string:id>/', methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article_data = cur.fetchone()

    form = ArticlesForm(request.form)

    form.name.data = article_data['name']
    form.batchof.data = article_data['batchof']
    form.titleimage.data = article_data['titleimage']
    form.title.data = article_data['title']
    form.description.data = article_data['description']
    form.timetoread.data = article_data['timetoread']
    form.body.data = article_data['body']
    form.type.data = article_data['type']

    if request.method == 'POST':
        name=request.form['name']
        batchof=request.form['batchof']
        titleimage=create_embed_link(request.form['titleimage'])
        title=request.form['title']
        description=request.form['description']
        timetoread=request.form['timetoread']
        body=request.form['body']
        type=request.form['type']

        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        # if warden_post != '':
        #     cur.execute("UPDATE warden SET name=%s,profilephoto=%s,email=%s,fbprofile=%s,inprofile=%s where post=%s", (name,profilephoto,email,fbprofile,inprofile,warden_post));
        #     conn.commit()
        # else:
        cur.execute("UPDATE articles SET name=%s, batchof=%s, titleimage=%s, title=%s,description=%s, timetoread=%s,body=%s, type=%s where id=%s", (name, batchof, titleimage,title,description,timetoread,body,type,id));
        conn.commit()
        # cur.close()
        return redirect(url_for('article',id=id))

    return render_template('edit_article.html', form=form, article_data=article_data)

@app.route('/delete_article_<string:id>/', methods=['GET','POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    
    result = cur.execute("DELETE FROM articles WHERE id = %s", [id])

    conn.commit()

    #Close connection
    #cur.close()


    return redirect(url_for('index'))

@app.route('/approve_article/<string:id>/', methods=['GET','POST'])
@is_logged_in
def approve_article(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute("UPDATE articles SET is_approved='APPROVED' where id=%s", (id));
    
    conn.commit()
        # cur.close()
    return redirect(url_for('index'))

@app.route('/disapprove_article/<string:id>/', methods=['GET','POST'])
@is_logged_in
def disapprove_article(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute("UPDATE articles SET is_approved='DISAPPROVED' where id=%s", (id));
    
    conn.commit()
        # cur.close()
    return redirect(url_for('index'))

@app.route('/delete_comment_<string:id>/', methods=['GET','POST'])
@is_logged_in
def delete_comment(id):
    # Create cursor
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    result = cur.execute("SELECT article_id FROM comments where id=%s",[id])

    article_id = cur.fetchone()
    # print(article_id[0])

    result = cur.execute("DELETE FROM comments WHERE id = %s", [id])

    conn.commit()

    #Close connection
    #cur.close()


    return redirect(url_for('article', id=article_id[0]))
   

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0', port='80')