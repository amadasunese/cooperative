from flask import send_from_directory, render_template, request, redirect, url_for, flash, send_file

from flask_login import current_user, login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from werkzeug.utils import secure_filename
from forms import MemberForm, MeetingForm, DocumentForm, NewsForm, RSVPForm
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
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from werkzeug.utils import secure_filename
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
# @login_required
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


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Generate a unique account number
        account_number = generate_account_number()

        # Create a new user instance
        new_user = User(username=username,
                        email=email,
                        account_number=account_number)
        
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

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

@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    member = Member.query.get_or_404(member_id)
    form = MemberForm(obj=member)

    if form.validate_on_submit():
        try:
            form.populate_obj(member)
            db.session.commit()
            flash('Member details updated successfully!', 'success')
            return redirect(url_for('members_list'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", 'danger')

    return render_template('edit_member.html', form=form, member=member)


@app.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    try:
        db.session.delete(member)
        db.session.commit()
        flash('Member removed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", 'danger')
    return redirect(url_for('members_list'))


@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    form = MemberForm()
    if form.validate_on_submit():
        try:
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
            new_user = User(username=surname,
                            email=email,
                            account_number=account_number)
            
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

            flash('Member added successfully with account number {}'.format(account_number), 'success')
            return redirect(url_for('members'))
        
        except Exception as e:
            db.session.rollback()  # Rollback the session to avoid any inconsistent state
            flash(f"An error occurred: {str(e)}", 'danger')

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
        new_loan = Loan(member_id=member_id,
                        amount=amount,
                        interest_rate=interest_rate)
        
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
    if request.method == 'POST':
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
    return render_template('dividends.html',
                           dividends=dividends)

@app.route('/add_dividend', methods=['POST'])
@login_required
def add_dividend():
    if request.method == 'POST':
        member_id = request.form['member_id']
        amount = request.form['amount']
        new_dividend = Dividend(member_id=member_id,
                                amount=amount)
        db.session.add(new_dividend)
        db.session.commit()
        flash('Dividend added successfully!')
        return redirect(url_for('dividends'))
    

# @app.route('/financial_reports')
# @login_required
# def financial_reports():
#     contributions = Contribution.query.all()
#     dividends = Dividend.query.all()

#     contributions_data = [(c.member_id, c.amount, c.date) for c in contributions]
#     dividends_data = [(d.member_id, d.amount, d.date) for d in dividends]

#     df_contributions = pd.DataFrame(contributions_data, columns=['Member ID', 'Amount', 'Date'])
#     df_dividends = pd.DataFrame(dividends_data, columns=['Member ID', 'Amount', 'Date'])

#     # Contribution summary
#     total_contributions = df_contributions['Amount'].sum()
#     total_dividends = df_dividends['Amount'].sum()

#     # Generate plots
#     fig, ax = plt.subplots()
#     df_contributions.groupby('Member ID')['Amount'].sum().plot(kind='bar', ax=ax)
#     ax.set_title('Total Contributions per Member')
#     ax.set_xlabel('Member ID')
#     ax.set_ylabel('Total Contributions')

#     # Save plot to a BytesIO object
#     img = BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode()

#     return render_template('financial_reports.html',
#                            total_contributions=total_contributions,
#                            total_dividends=total_dividends,
#                            plot_url=plot_url)


@app.route('/financial_reports')
@login_required
def financial_reports():
    try:
        contributions = Contribution.query.all()
        dividends = Dividend.query.all()

        if not contributions or not dividends:
            raise ValueError("No contributions or dividends found")

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

        return render_template('financial_reports.html',
                               total_contributions=total_contributions,
                               total_dividends=total_dividends,
                               plot_url=plot_url)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('dashboard'))



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
    rsvp = RSVP.query.all()
    form = MeetingForm()
    return render_template('meeting_list.html',
                           meetings=meetings,
                           rsvp=rsvp,
                           form=form)


@app.route('/meetings')
def meetings():
    meetings = Meeting.query.all()
    form = RSVPForm()
    return render_template('meetings.html',
                           meetings=meetings,
                           form=form)


# @app.route('/add_meeting', methods=['GET', 'POST'])
# @login_required
# def add_meeting():
#     form = MeetingForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         date = form.date.data
#         location = form.location.data
#         description = form.description.data

#         new_meeting = Meeting(title=title,
#                               date=date,
#                               location=location,
#                               description=description)
        
#         db.session.add(new_meeting)
#         db.session.commit()
#         flash('Meeting added successfully!')
#         return redirect(url_for('dashboard'))

#     return render_template('meetings.html', form=form)

# @app.route('/add_meeting', methods=['GET', 'POST'])
# @login_required
# def add_meeting():
#     form = MeetingForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         date = form.date.data
#         location = form.location.data
#         description = form.description.data

#         new_meeting = Meeting(title=title, date=date, location=location, description=description)
        
#         try:
#             db.session.add(new_meeting)
#             db.session.commit()
#             flash('Meeting added successfully!', 'success')
#             return redirect(url_for('meetings_list'))
        
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error adding meeting: {e}', 'danger')
#             return render_template('meetings.html', form=form)
    
#     return render_template('meetings.html', form=form)


# @app.route('/add_meeting', methods=['GET', 'POST'])
# @login_required
# def add_meeting():
#     form = MeetingForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         date = form.date.data
#         location = form.location.data
#         description = form.description.data

#         new_meeting = Meeting(title=title, date=date, location=location, description=description)
        
#         try:
#             db.session.add(new_meeting)
#             db.session.commit()
#             flash('Meeting added successfully!', 'success')
#             return redirect(url_for('meeting_list'))
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error adding meeting: {e}', 'danger')
    
#     # Log form validation errors if any
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(f'Error in the {getattr(form, field).label.text} field - {error}', 'danger')
    
#     return render_template('meetings.html', form=form)

@app.route('/add_meeting', methods=['GET', 'POST'])
@login_required
def add_meeting():
    form = MeetingForm()
    if form.validate_on_submit():
        title = form.title.data
        date_str = form.date.data
        location = form.location.data
        description = form.description.data

        # Convert date string to datetime object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except ValueError as e:
            flash('Invalid date format.', 'danger')
            return render_template('meetings.html', form=form)

        new_meeting = Meeting(title=title, date=date, location=location, description=description)
        
        try:
            db.session.add(new_meeting)
            db.session.commit()
            flash('Meeting added successfully!', 'success')
            return redirect(url_for('meeting_list'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding meeting: {e}', 'danger')
            return render_template('meetings.html', form=form)

    meetings = Meeting.query.all()
    return render_template('meetings.html', form=form, meetings=meetings)


@app.route('/rsvp/<int:meeting_id>', methods=['POST'])
@login_required
def rsvp(meeting_id):
    status = request.form['status']
    new_rsvp = RSVP(member_id=current_user.id, meeting_id=meeting_id, status=status)
    db.session.add(new_rsvp)
    db.session.commit()
    flash('RSVP status updated!')
    return redirect(url_for('meetings'))

@app.route('/edit_meeting/<int:meeting_id>', methods=['GET', 'POST'])
@login_required
def edit_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    form = MeetingForm(obj=meeting)
    if form.validate_on_submit():
        meeting.title = form.title.data
        meeting.date = form.date.data
        meeting.location = form.location.data
        meeting.description = form.description.data

        try:
            db.session.commit()
            flash('Meeting updated successfully!', 'success')
            return redirect(url_for('meetings'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating meeting: {e}', 'danger')
    return render_template('edit_meeting.html', form=form, meeting=meeting)

@app.route('/delete_meeting/<int:meeting_id>', methods=['POST'])
@login_required
def delete_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    try:
        db.session.delete(meeting)
        db.session.commit()
        flash('Meeting deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting meeting: {e}', 'danger')
    return redirect(url_for('meeting_list'))


@app.route('/events')
@login_required
def events():
    events = Event.query.all()
    meetings = Meeting.query.all()
    return render_template('events.html', events=events, meetings=meetings)

@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']
        new_event = Event(title=title, date=date,
                          location=location,
                          description=description)
        
        db.session.add(new_event)
        db.session.commit()
        flash('Event added successfully!')
        return redirect(url_for('events'))


# @app.route('/rsvp/<int:meeting_id>', methods=['POST'])
# @login_required
# def rsvp(meeting_id):
#     status = request.form['status']
#     new_rsvp = RSVP(member_id=current_user.id,
#                     meeting_id=meeting_id,
#                     status=status)
#     db.session.add(new_rsvp)
#     db.session.commit()
#     flash('RSVP status updated!')
#     return redirect(url_for('meetings'))


# @app.route('/rsvp/<int:meeting_id>', methods=['POST'])
# @login_required
# def rsvp(meeting_id):
#     status = request.form.get('status')
    
#     if not status:
#         flash('Invalid RSVP status.', 'danger')
#         return redirect(url_for('meetings'))
    
#     # Check if the meeting exists
#     meeting = Meeting.query.get(meeting_id)
#     if not meeting:
#         flash('Meeting not found.', 'danger')
#         return redirect(url_for('meetings'))
    
#     # Check if the user has already RSVPed
#     existing_rsvp = RSVP.query.filter_by(member_id=current_user.id, meeting_id=meeting_id).first()
#     if existing_rsvp:
#         existing_rsvp.status = status
#         flash('RSVP status updated!', 'success')
#     else:
#         new_rsvp = RSVP(member_id=current_user.id, meeting_id=meeting_id, status=status)
#         db.session.add(new_rsvp)
#         flash('RSVP status added!', 'success')
    
#     try:
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         flash(f'Error updating RSVP: {e}', 'danger')

#     return redirect(url_for('meetings'))

# @app.route('/rsvp/<int:meeting_id>', methods=['POST'])
# @login_required
# def rsvp(meeting_id):
#     status = request.form['status']
#     new_rsvp = RSVP(member_id=current_user.id, meeting_id=meeting_id, status=status)
#     db.session.add(new_rsvp)
#     db.session.commit()
#     flash('RSVP status updated!')
#     return redirect(url_for('meetings'))


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/documents')
@login_required
def documents():
    documents = Document.query.all()
    return render_template('documents_list.html', documents=documents)

# @app.route('/upload_document', methods=['GET', 'POST'])
# @login_required
# def upload_document():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if file:
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         title = request.form['title']
#         new_document = Document(title=title, filename=filename)
#         db.session.add(new_document)
#         db.session.commit()
#         flash('Document uploaded successfully!')
#         return redirect(url_for('documents'))



# @app.route('/download_document/<int:document_id>')
# @login_required
# def download_document(document_id):
#     document = Document.query.get(document_id)
#     return send_from_directory(app.config['UPLOAD_FOLDER'], document.filename)

# @app.route('/download_document/<int:document_id>')
# @login_required
# def download_document(document_id):
#     document = Document.query.get_or_404(document_id)
#     return send_from_directory('uploads', document.filename)

# @app.route('/download_document/<int:document_id>')
# @login_required
# def download_document(document_id):
#     document = Document.query.get_or_404(document_id)
#     return send_from_directory(app.config['UPLOAD_FOLDER'], document.filename)


@app.route('/upload_document', methods=['GET', 'POST'])
@login_required
def upload_document():
    form = DocumentForm()
    if form.validate_on_submit():
        title = form.title.data
        file = form.filename.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_document = Document(title=title, filename=filename)
        db.session.add(new_document)
        db.session.commit()
        
        flash('Document uploaded successfully.')
        return redirect(url_for('documents'))

    return render_template('add_documents.html', form=form)

@app.route('/download_document/<int:document_id>')
@login_required
def download_document(document_id):
    document = Document.query.get_or_404(document_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], document.filename)


@app.route('/delete_document/<int:document_id>', methods=['POST'])
@login_required
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], document.filename))
        db.session.delete(document)
        db.session.commit()
        flash('Document deleted successfully.')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting document: {str(e)}', 'danger')
    return redirect(url_for('documents'))


@app.route('/polls')
@login_required
def polls():
    polls = Poll.query.all()
    return render_template('polls.html', polls=polls)

@app.route('/add_poll', methods=['POST'])
@login_required
def add_poll():
    if request.method == 'POST':
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
    return render_template('resources.html',
                           resources=resources)

@app.route('/add_resource', methods=['POST'])
@login_required
def add_resource():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_resource = Resource(title=title,
                                content=content)
        db.session.add(new_resource)
        db.session.commit()
        flash('Resource added successfully!')
        return redirect(url_for('resources'))


# @app.route('/news')
# @login_required
# def news():
#     news_items = News.query.all()
#     return render_template('news.html',
#                            news_items=news_items)


@app.route('/news/<int:news_id>')
# @login_required
def news_detail(news_id):
    news_item = News.query.get_or_404(news_id)
    news = News.query.all()

    return render_template('news_detail.html',
                           news_item=news_item,
                           news=news)

@app.route('/blog')
def blog():
    news = News.query.all()
    news_items = News.query.order_by(News.date_added.desc()).all()  # Fetch all news sorted by date (descending)
    form = NewsForm()
    return render_template('blog.html',
    news_items=news_items,
    news=news,
    form=form)


# @app.route('/add_news', methods=['POST'])
# @login_required
# def add_news():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         new_news = News(title=title, content=content)
#         db.session.add(new_news)
#         db.session.commit()
#         flash('News added successfully!')
#         return redirect(url_for('news'))

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        filename = None
        if form.thumbnail.data:
            filename = secure_filename(form.thumbnail.data.filename)
            form.thumbnail.data.save(f'static/uploads/{filename}')
        news_item = News(
            title=form.title.data,
            content=form.content.data,
            thumbnail=f'uploads/{filename}' if filename else None,
            date_added=datetime.utcnow()
        )
        db.session.add(news_item)
        db.session.commit()
        flash('News item added successfully', 'success')
        return redirect(url_for('blog'))
    return render_template('news.html', form=form)

@app.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    news = News.query.get_or_404(news_id)
    form = NewsForm()
    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        # Handle the thumbnail upload if necessary
        if form.thumbnail.data:
            filename = secure_filename(form.thumbnail.data.filename)
            form.thumbnail.data.save(f'static/uploads/{filename}')
            news.thumbnail = f'uploads/{filename}'
        db.session.commit()
        flash('News item updated successfully', 'success')
        return redirect(url_for('news_detail', news_id=news_id))
    elif request.method == 'GET':
        form.title.data = news.title
        form.content.data = news.content
    # news = News.query.all()
    return render_template('edit_news.html', form=form, news=news)

@app.route('/delete_news/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    news_item = News.query.get_or_404(news_id)
    db.session.delete(news_item)
    db.session.commit()
    flash('News item deleted successfully', 'success')
    return redirect(url_for('blog'))


@app.route('/dashboard')
@login_required
def dashboard():
    total_members = Member.query.count()
    total_loans = Loan.query.count()
    total_events = Meeting.query.count()
    total_polls = Poll.query.count()
    return render_template('dashboard.html',
                           total_members=total_members,
                           total_loans=total_loans,
                           total_events=total_events,
                           total_polls=total_polls)


@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    members = Member.query.filter(Member.name.contains(query)).all()
    documents = Document.query.filter(Document.title.contains(query)).all()

    return render_template('search_results.html',
                           members=members,
                           documents=documents,
                           query=query)


@app.route('/management_committee')
def management_committee():
    members = [
        {
            "name": "John Doe",
            "position": "President",
            "photo": "images/image.png"
        },
        {
            "name": "Jane Smith",
            "position": "Vice President",
            "photo": "images/image.png"
        },
        {
            "name": "Samuel Brown",
            "position": "General Secretary",
            "photo": "images/image.png"
        },
        {
            "name": "Emily Johnson",
            "position": "Treasurer",
            "photo": "images/image.png"
        },
        {
            "name": "Michael Davis",
            "position": "Assistant General Secretary",
            "photo": "images/image.png"
        },
        {
            "name": "Sophia Wilson",
            "position": "Financial Secretary",
            "photo": "images/image.png"
        },
        {
            "name": "Daniel Thompson",
            "position": "Ex-Officio",
            "photo": "images/image.png"
        }
    ]
    return render_template('management_committee.html',
                           members=members)