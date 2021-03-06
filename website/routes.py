from flask import render_template, url_for, flash, redirect, request
from website import app, db
from website.forms import LinkForm, EditForm
from website.models import Link


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/admin', methods=['GET'])
def admin():
    links = Link.query.all()
    return render_template('admin.html', links=links)



@app.route('/new', methods=['GET', 'POST'])
def new():
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(link=form.link.data, title=form.title.data, name = form.name.data, desc=form.desc.data, image=form.image.data, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        goodlink = link.link.replace(' ','-')
        goodlink = goodlink.replace('/','_')
        goodlink = goodlink.replace(':','-')
        goodlink = goodlink.replace('.','-')
        goodlink = goodlink.replace('?','-')
        goodlink = goodlink.replace(',','-')
        link.link = goodlink
        db.session.add(link)
        db.session.commit()
        flash(f'Created link http://allnewsnow.online/l/{link.link}', 'success')
        return redirect(url_for('home'))
    return render_template('new.html', form=form, legend='New Link')

@app.route('/l/<link_url>/edit', methods=['GET', 'POST'])
def edit(link_url):
    link = Link.query.filter_by(link=link_url).first()
    form = EditForm()
    if form.validate_on_submit():
        link.link = form.link.data
        link.url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        link.title = form.title.data
        link.name = form.name.data
        link.desc = form.desc.data
        link.image = form.image.data
        
        db.session.commit()
        flash('Successfully updated link!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.link.data = link.link
        # form.url.data = link.url
        form.title.data = link.title
        form.name.data = link.name
        form.desc.data = link.desc
        form.image.data = link.image
                
    return render_template('new.html', form=form, legend='Update Link')

@app.route('/l/<link_url>', methods=['GET'])
def redir(link_url):
    link = Link.query.filter_by(link=link_url).first()
    return render_template('redir.html', title=link.title, name=link.name, desc=link.desc, image=link.image, url=link.url)

@app.route('/l/<link_url>/delete', methods=['GET','POST'])
def delete(link_url):
    link = Link.query.filter_by(link=link_url).first()
    db.session.delete(link)
    db.session.commit()
    flash('Successfully deleted link!', 'success')
    return redirect(url_for('home'))