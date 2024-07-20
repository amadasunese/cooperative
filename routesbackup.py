# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# # from flask_twofactor import TwoFactor
# import random
# import string
# from models import User, Member, Loan, Investment, Repayment, Contribution, Dividend, Announcement, Meeting, Event
# from models import Document, Poll, Option, News, Resource, RSVP
# from app import app

# from flask import send_file
# import qrcode
# import io


from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import current_user, login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from werkzeug.utils import secure_filename
from forms import MemberForm, MeetingForm
from models import generate_account_number
from models import User, Member, Loan, Investment, Repayment, Contribution, Dividend, Announcement, Meeting, Event
from models import Document, Poll, Option, News, Resource, RSVP
import qrcode
import io
import pyotp
import random
import string
from flask import send_file
import qrcode
import io

# @login_manager.user_loader
# def load_user(user_id):
#     return Member.query.get(int(user_id))

# @login_manager.user_loader
# def load_user(user_id):
#     return Member.query.get(int(user_id))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @app.route('/')
# def index():
#     events = Event.query.all()
#     meetings = Meeting.query.all()
#     polls = Poll.query.all()
#     news_items = News.query.order_by(News.date_added.desc()).limit(5).all()
#     return render_template('index.html',
#                            events=events,
#                            meetings=meetings,
#                            polls=polls,
#                            news_items=news_items)

@app.route('/')
@login_required
def index():
    events = Event.query.order_by(Event.date.desc()).all()
    meetings = Meeting.query.order_by(Meeting.date.desc()).all()
    polls = Poll.query.all()
    news_items = News.query.order_by(News.date_added.desc()).limit(3).all()
    return render_template('index.html',
                           events=events,
                           meetings=meetings,
                           polls=polls,
                           news_items=news_items)


    return render_template('events.html', )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



# @app.route('/register')
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         # Generate a unique account number
#         account_number = generate_account_number()

#         # Create a new member instance
#         new_user = User(username=username, email=email, password=password, account_number=account_number)
#         db.session.add(new_user)
#         db.session.commit()

#         new_member = Member(name=username, email=email, user_id=new_user.id)
#         db.session.add(new_member)
#         db.session.commit()

#         # Generate QR code for 2FA
#         qr = qrcode.make(new_user.get_totp_uri())
#         img_io = io.BytesIO()
#         qr.save(img_io, 'PNG')
#         img_io.seek(0)

#         flash('Registration successful! Your account number is {}'.format(account_number))
#         return send_file(img_io, mimetype='image/png', as_attachment=True, attachment_filename='qrcode.png')

#     return render_template('register.html')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         # Generate a unique account number
#         account_number = generate_account_number()

#         # Create a new member instance
#         new_user = User(username=username, email=email, password=password, account_number=account_number)
#         db.session.add(new_user)
#         db.session.commit()

#         new_member = Member(name=username, email=email, user_id=new_user.id)
#         db.session.add(new_member)
#         db.session.commit()

#         # Generate QR code for 2FA
#         qr = qrcode.make(new_user.get_totp_uri())
#         img_io = io.BytesIO()
#         qr.save(img_io, 'PNG')
#         img_io.seek(0)

#         flash('Registration successful! Your account number is {}'.format(account_number))
#         # return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
#     return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()
#         if user and user.verify_password(password):
#             login_user(user)
#             return redirect(url_for('two_factor_auth'))
#         else:
#             flash('Invalid email or password')
#     return render_template('login.html')

# @app.route('/two_factor_auth', methods=['GET', 'POST'])
# @login_required
# def two_factor_auth():
#     if request.method == 'POST':
#         token = request.form['token']
#         if current_user.verify_totp(token):
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid token')
#     return render_template('two_factor_auth.html')

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html')

# def generate_account_number():
#     return ''.join(random.choices(string.digits, k=10))

# def generate_account_number():
#     # Generate a random alphanumeric account number
#     letters_and_digits = string.ascii_letters + string.digits
#     return ''.join(random.choices(letters_and_digits, k=10))


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         # Generate a unique account number
#         account_number = generate_account_number()

#         # Create a new member instance
#         new_user = User(username=username, email=email, password=password, account_number=account_number)
#         db.session.add(new_user)
#         db.session.commit()

#         new_member = Member(name=username, email=email, user_id=new_user.id)
#         db.session.add(new_member)
#         db.session.commit()

#         # Generate QR code for 2FA
#         qr = qrcode.make(new_user.get_totp_uri())
#         img_io = io.BytesIO()
#         qr.save(img_io, 'PNG')
#         img_io.seek(0)

#         flash('Registration successful! Your account number is {}'.format(account_number))
#         # return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()
#         if user and user.verify_password(password):
#             login_user(user)
#             return redirect(url_for('two_factor_auth'))
#         else:
#             flash('Invalid email or password')
#     return render_template('login.html')

# @app.route('/two_factor_auth', methods=['GET', 'POST'])
# @login_required
# def two_factor_auth():
#     if request.method == 'POST':
#         token = request.form['token']
#         if current_user.verify_totp(token):
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid token')
#     return render_template('two_factor_auth.html')

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# def generate_account_number():
#     return ''.join(random.choices(string.digits, k=10))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Generate a unique account number
        account_number = generate_account_number()

        # Create a new user instance
        new_user = User(username=username, email=email, account_number=account_number)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Create a new member instance
        # new_member = Member(name=username, email=email, user_id=new_user.id)
        # db.session.add(new_member)
        # db.session.commit()

        # flash('Registration successful! Your account number is {}'.format(account_number))
        # return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()
#         if user and user.check_password(password):
#             login_user(user)
#             return redirect(url_for('two_factor_verify'))
#         else:
#             flash('Invalid email or password')
#     return render_template('login.html')


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# @app.route('/two_factor_setup')
# @login_required
# def two_factor_setup():
#     return two_factor.two_factor_setup()

# @app.route('/two_factor_verify', methods=['POST'])
# @login_required
# def two_factor_verify():
#     return two_factor.two_factor_verify()

# @app.route('/')
# @login_required
# def index():
#     return render_template('index.html')

@app.route('/members')
@login_required
def members():
    members = Member.query.all()
    form = MemberForm()
    return render_template('members.html', members=members, form=form)

@app.route('/members_list', methods=['GET'])
def members_list():
    all_members = Member.query.all()
    return render_template('members_list.html', members=all_members)


@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    form = MemberForm()
    if form.validate_on_submit():
        surname = form.surname.data
        other_names = form.other_names.data
        home_address = form.home_address.data
        email = form.email.data
        date_of_birth = form.date_of_birth.data
        telephone_number = form.telephone_number.data
        occupation = form.occupation.data
        next_of_kin_name = form.next_of_kin_name.data
        next_of_kin_phone_number = form.next_of_kin_phone_number.data
        relationship_with_next_of_kin = form.relationship_with_next_of_kin.data
        address_of_next_of_kin = form.address_of_next_of_kin.data
        monthly_savings = form.monthly_savings.data
        share_capital = form.share_capital.data
        passport_photograph = form.passport_photograph.data
        agreement = form.agreement.data

        # Save the passport photograph
        if passport_photograph:
            filename = secure_filename(passport_photograph.filename)
            passport_path = f'uploads/{filename}'
            passport_photograph.save(passport_path)
        else:
            passport_path = None


        # Generate a unique account number
        account_number = generate_account_number()

        # Create a new user instance
        new_user = User(username=surname, email=email, account_number=account_number)
        new_user.set_password('1234567')
        db.session.add(new_user)
        db.session.commit()

        # Create a new member instance
        new_member = Member(
            surname=surname, 
            other_names=other_names, 
            home_address=home_address, 
            email=email,
            date_of_birth=date_of_birth,
            telephone_number=telephone_number, 
            occupation=occupation, 
            next_of_kin_name=next_of_kin_name, 
            next_of_kin_phone_number=next_of_kin_phone_number, 
            relationship_with_next_of_kin=relationship_with_next_of_kin, 
            address_of_next_of_kin=address_of_next_of_kin, 
            monthly_savings=monthly_savings, 
            share_capital=share_capital, 
            passport_photograph=passport_path, 
            agreement=agreement, 
            user_id=new_user.id
        )
        db.session.add(new_member)
        db.session.commit()

        flash('Member added successfully with account number {}'.format(account_number))
        return redirect(url_for('members'))

    return render_template('add_member.html', form=form)


@app.route('/loans')
@login_required
def loans():
    loans = Loan.query.all()
    return render_template('loans.html', loans=loans)

@app.route('/add_loan', methods=['POST'])
@login_required
def add_loan():
    if request.method == 'POST':
        member_id = request.form['member_id']
        amount = request.form['amount']
        interest_rate = request.form['interest_rate']
        new_loan = Loan(member_id=member_id, amount=amount, interest_rate=interest_rate)
        db.session.add(new_loan)
        db.session.commit()
        flash('Loan added successfully!')
        return redirect(url_for('loans'))

@app.route('/repay_loan', methods=['POST'])
@login_required
def repay_loan():
    if request.method == 'POST':
        loan_id = request.form['loan_id']
        amount = request.form['amount']
        repayment = Repayment(loan_id=loan_id, amount=amount)
        db.session.add(repayment)
        db.session.commit()
        flash('Repayment added successfully!')
        return redirect(url_for('loans'))
    

@app.route('/investments')
@login_required
def investments():
    investments = Investment.query.all()
    return render_template('investments.html', investments=investments)

@app.route('/add_investment', methods=['POST'])
@login_required
def add_investment():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        new_investment = Investment(description=description, amount=amount)
        db.session.add(new_investment)
        db.session.commit()
        flash('Investment added successfully!')
        return redirect(url_for('investments'))


@app.route('/contributions')
@login_required
def contributions():
    contributions = Contribution.query.all()
    return render_template('contributions.html', contributions=contributions)

@app.route('/add_contribution', methods=['POST'])
@login_required
def add_contribution():
    if request.method == ['POST']:
        member_id = request.form['member_id']
        amount = request.form['amount']
        new_contribution = Contribution(member_id=member_id, amount=amount)
        db.session.add(new_contribution)
        db.session.commit()
        flash('Contribution added successfully!')
        return redirect(url_for('contributions'))

from functools import wraps

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    return render_template('admin.html')


@app.route('/dividends')
@login_required
def dividends():
    dividends = Dividend.query.all()
    return render_template('dividends.html', dividends=dividends)

@app.route('/add_dividend', methods=['POST'])
@login_required
def add_dividend():
    if request.method == ['POST']:
        member_id = request.form['member_id']
        amount = request.form['amount']
        new_dividend = Dividend(member_id=member_id, amount=amount)
        db.session.add(new_dividend)
        db.session.commit()
        flash('Dividend added successfully!')
        return redirect(url_for('dividends'))
    

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

@app.route('/financial_reports')
@login_required
def financial_reports():
    contributions = Contribution.query.all()
    dividends = Dividend.query.all()

    contributions_data = [(c.member_id, c.amount, c.date) for c in contributions]
    dividends_data = [(d.member_id, d.amount, d.date) for d in dividends]

    df_contributions = pd.DataFrame(contributions_data, columns=['Member ID', 'Amount', 'Date'])
    df_dividends = pd.DataFrame(dividends_data, columns=['Member ID', 'Amount', 'Date'])

    # Contribution summary
    total_contributions = df_contributions['Amount'].sum()
    total_dividends = df_dividends['Amount'].sum()

    # Generate plots
    fig, ax = plt.subplots()
    df_contributions.groupby('Member ID')['Amount'].sum().plot(kind='bar', ax=ax)
    ax.set_title('Total Contributions per Member')
    ax.set_xlabel('Member ID')
    ax.set_ylabel('Total Contributions')

    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('financial_reports.html', total_contributions=total_contributions, total_dividends=total_dividends, plot_url=plot_url)


@app.route('/announcements')
@login_required
def announcements():
    announcements = Announcement.query.all()
    return render_template('announcements.html', announcements=announcements)

@app.route('/add_announcement', methods=['POST'])
@login_required
def add_announcement():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_announcement = Announcement(title=title, content=content)
        db.session.add(new_announcement)
        db.session.commit()
        flash('Announcement added successfully!')
        return redirect(url_for('announcements'))

@app.route('/meeting_list')
@login_required
def meeting_list():
    meetings = Meeting.query.all()
    return render_template('meeting_list.html', meetings=meetings)

@app.route('/meetings')
def meetings():
    meetings = Meeting.query.all()
    return render_template('meetings.html', meetings=meetings)


# @app.route('/add_meeting', methods=['POST'])
# @login_required
# def add_meeting():
#     if request.method == 'POST':
#         title = request.form['title']
#         date = request.form['date']
#         location = request.form['location']
#         description = request.form['description']
#         new_meeting = Meeting(title=title, date=date, location=location, description=description)
#         db.session.add(new_meeting)
#         db.session.commit()
#         flash('Meeting added successfully!')
#         return redirect(url_for('meetings'))


@app.route('/add_meeting', methods=['GET', 'POST'])
@login_required
def add_meeting():
    form = MeetingForm()
    if form.validate_on_submit():
        title = form.title.data
        date = form.date.data
        location = form.location.data
        description = form.description.data
        new_meeting = Meeting(title=title, date=date, location=location, description=description)
        db.session.add(new_meeting)
        db.session.commit()
        flash('Meeting added successfully!')
        return redirect(url_for('dashboard'))  # Redirect to meetings page

    return render_template('meetings.html', form=form)

@app.route('/events')
@login_required
def events():
    events = Event.query.all()
    meetings = Meeting.query.all()
    return render_template('events.html', events=events, meetings=meetings)

@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    if request.method == ['POST']:
        title = request.form['title']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']
        new_event = Event(title=title, date=date, location=location, description=description)
        db.session.add(new_event)
        db.session.commit()
        flash('Event added successfully!')
        return redirect(url_for('events'))


@app.route('/rsvp/<int:meeting_id>', methods=['POST'])
@login_required
def rsvp(meeting_id):
    status = request.form['status']
    new_rsvp = RSVP(member_id=current_user.id, meeting_id=meeting_id, status=status)
    db.session.add(new_rsvp)
    db.session.commit()
    flash('RSVP status updated!')
    return redirect(url_for('meetings'))


import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/documents')
@login_required
def documents():
    documents = Document.query.all()
    return render_template('documents.html', documents=documents)

@app.route('/upload_document', methods=['POST'])
@login_required
def upload_document():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        title = request.form['title']
        new_document = Document(title=title, filename=filename)
        db.session.add(new_document)
        db.session.commit()
        flash('Document uploaded successfully!')
        return redirect(url_for('documents'))

@app.route('/download_document/<int:document_id>')
@login_required
def download_document(document_id):
    document = Document.query.get(document_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], document.filename)


@app.route('/polls')
@login_required
def polls():
    polls = Poll.query.all()
    return render_template('polls.html', polls=polls)

@app.route('/add_poll', methods=['POST'])
@login_required
def add_poll():
    if request.method == ['POST']:
        question = request.form['question']
        options = request.form.getlist('options')
        new_poll = Poll(question=question)
        db.session.add(new_poll)
        db.session.commit()
        for option in options:
            new_option = Option(text=option, poll_id=new_poll.id)
            db.session.add(new_option)
        db.session.commit()
        flash('Poll created successfully!')
        return redirect(url_for('polls'))

@app.route('/vote/<int:option_id>', methods=['POST'])
@login_required
def vote(option_id):
    option = Option.query.get(option_id)
    option.votes += 1
    db.session.commit()
    flash('Vote recorded!')
    return redirect(url_for('polls'))


@app.route('/resources')
@login_required
def resources():
    resources = Resource.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/add_resource', methods=['POST'])
@login_required
def add_resource():
    if request.method == ['POST']:
        title = request.form['title']
        content = request.form['content']
        new_resource = Resource(title=title, content=content)
        db.session.add(new_resource)
        db.session.commit()
        flash('Resource added successfully!')
        return redirect(url_for('resources'))


@app.route('/news')
@login_required
def news():
    news_items = News.query.all()
    return render_template('news.html', news_items=news_items)




@app.route('/news/<int:news_id>')
@login_required
def news_detail(news_id):
    news_item = News.query.get_or_404(news_id)
    return render_template('news_detail.html', news_item=news_item)

@app.route('/add_news', methods=['POST'])
@login_required
def add_news():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_news = News(title=title, content=content)
        db.session.add(new_news)
        db.session.commit()
        flash('News added successfully!')
        return redirect(url_for('news'))


@app.route('/dashboard')
@login_required
def dashboard():
    # Add logic to gather summary data for the dashboard
    total_members = Member.query.count()
    total_loans = Loan.query.count()
    total_events = Meeting.query.count()
    total_polls = Poll.query.count()
    return render_template('dashboard.html', total_members=total_members, total_loans=total_loans, total_events=total_events, total_polls=total_polls)


@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    members = Member.query.filter(Member.name.contains(query)).all()
    documents = Document.query.filter(Document.title.contains(query)).all()
    return render_template('search_results.html', members=members, documents=documents, query=query)

