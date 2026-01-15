from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import db, PrayerRequest, Prayer, Encouragement, Report, PrayerStats
from app.forms import PrayerRequestForm, EncouragementForm, PrayerNoteForm
from datetime import date
from sqlalchemy import desc, func

bp = Blueprint('prayers', __name__, url_prefix='/prayers')

@bp.route('/feed')
def feed():
    # Get filter parameters
    category = request.args.get('category', 'all')
    sort_by = request.args.get('sort', 'recent')  # recent, most_prayed
    page = request.args.get('page', 1, type=int)
    
    # Base query
    query = PrayerRequest.query.filter_by(is_public=True, is_private=False)
    
    # Apply category filter
    if category != 'all':
        query = query.filter_by(category=category)
    
    # Apply sorting
    if sort_by == 'most_prayed':
        # Get requests with prayer counts
        subquery = db.session.query(
            Prayer.request_id,
            func.count(Prayer.id).label('prayer_count')
        ).group_by(Prayer.request_id).subquery()
        
        query = query.outerjoin(
            subquery,
            PrayerRequest.id == subquery.c.request_id
        ).order_by(desc(subquery.c.prayer_count))
    elif sort_by == 'urgent':
        query = query.filter_by(is_urgent=True).order_by(desc(PrayerRequest.created_at))
    else:  # recent
        query = query.order_by(desc(PrayerRequest.created_at))
    
    # Paginate
    from config import Config
    pagination = query.paginate(page=page, per_page=Config.REQUESTS_PER_PAGE, error_out=False)
    requests = pagination.items
    
    # Get categories for filter
    categories = ['Family', 'Health', 'Finances', 'Relationships', 'Grief', 'Gratitude']
    
    return render_template('prayers/feed.html',
                         requests=requests,
                         pagination=pagination,
                         categories=categories,
                         current_category=category,
                         current_sort=sort_by)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PrayerRequestForm()
    
    if form.validate_on_submit():
        prayer_request = PrayerRequest(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            bible_verse=form.bible_verse.data,
            is_anonymous=form.is_anonymous.data,
            is_private=form.is_private.data,
            is_urgent=form.is_urgent.data,
            user_id=current_user.id,
            is_public=True  # Auto-approve for now, can add moderation later
        )
        
        db.session.add(prayer_request)
        db.session.commit()
        
        flash('Your prayer request has been submitted.', 'success')
        return redirect(url_for('prayers.view', id=prayer_request.id))
    
    return render_template('prayers/create.html', form=form)

@bp.route('/view/<int:id>')
def view(id):
    prayer_request = PrayerRequest.query.get_or_404(id)
    
    # Check access permissions
    if prayer_request.is_private:
        if not current_user.is_authenticated or \
           (current_user.id != prayer_request.user_id and not current_user.is_admin):
            abort(403)
    
    # Get prayers (public ones for display)
    public_prayers = Prayer.query.filter_by(
        request_id=id,
        is_private=False
    ).order_by(desc(Prayer.created_at)).all()
    
    # Get encouragements
    encouragements = Encouragement.query.filter_by(
        request_id=id
    ).order_by(desc(Encouragement.created_at)).all()
    
    # Check if current user has prayed
    has_prayed = False
    if current_user.is_authenticated:
        has_prayed = Prayer.query.filter_by(
            user_id=current_user.id,
            request_id=id
        ).first() is not None
    
    return render_template('prayers/view.html',
                         prayer_request=prayer_request,
                         public_prayers=public_prayers,
                         encouragements=encouragements,
                         has_prayed=has_prayed)

@bp.route('/pray/<int:id>', methods=['POST'])
@login_required
def pray(id):
    prayer_request = PrayerRequest.query.get_or_404(id)
    
    # Check if user already prayed
    existing_prayer = Prayer.query.filter_by(
        user_id=current_user.id,
        request_id=id
    ).first()
    
    if existing_prayer:
        flash('You have already prayed for this request.', 'info')
        return redirect(url_for('prayers.view', id=id))
    
    # Create prayer
    prayer = Prayer(
        user_id=current_user.id,
        request_id=id
    )
    
    db.session.add(prayer)
    
    # Update prayer stats
    today = date.today()
    stat = PrayerStats.query.filter_by(
        user_id=current_user.id,
        date=today
    ).first()
    
    if stat:
        stat.prayers_offered += 1
    else:
        stat = PrayerStats(
            user_id=current_user.id,
            date=today,
            prayers_offered=1
        )
        db.session.add(stat)
    
    db.session.commit()
    
    flash('Thank you for praying!', 'success')
    return redirect(url_for('prayers.view', id=id))

@bp.route('/pray-note/<int:id>', methods=['GET', 'POST'])
@login_required
def pray_with_note(id):
    prayer_request = PrayerRequest.query.get_or_404(id)
    form = PrayerNoteForm()
    
    if form.validate_on_submit():
        # Check if user already prayed
        existing_prayer = Prayer.query.filter_by(
            user_id=current_user.id,
            request_id=id
        ).first()
        
        if existing_prayer:
            flash('You have already prayed for this request.', 'info')
            return redirect(url_for('prayers.view', id=id))
        
        # Create prayer with note
        prayer = Prayer(
            user_id=current_user.id,
            request_id=id,
            prayer_note=form.prayer_note.data,
            is_private=form.is_private.data
        )
        
        db.session.add(prayer)
        
        # Update prayer stats
        today = date.today()
        stat = PrayerStats.query.filter_by(
            user_id=current_user.id,
            date=today
        ).first()
        
        if stat:
            stat.prayers_offered += 1
        else:
            stat = PrayerStats(
                user_id=current_user.id,
                date=today,
                prayers_offered=1
            )
            db.session.add(stat)
        
        db.session.commit()
        
        flash('Thank you for praying!', 'success')
        return redirect(url_for('prayers.view', id=id))
    
    return render_template('prayers/pray_note.html', form=form, prayer_request=prayer_request)

@bp.route('/encourage/<int:id>', methods=['GET', 'POST'])
@login_required
def encourage(id):
    prayer_request = PrayerRequest.query.get_or_404(id)
    form = EncouragementForm()
    
    if form.validate_on_submit():
        encouragement = Encouragement(
            user_id=current_user.id,
            request_id=id,
            content=form.content.data,
            bible_verse=form.bible_verse.data
        )
        
        db.session.add(encouragement)
        db.session.commit()
        
        flash('Your encouragement has been shared.', 'success')
        return redirect(url_for('prayers.view', id=id))
    
    return render_template('prayers/encourage.html', form=form, prayer_request=prayer_request)

@bp.route('/mark-answered/<int:id>', methods=['POST'])
@login_required
def mark_answered(id):
    prayer_request = PrayerRequest.query.get_or_404(id)
    
    # Only owner can mark as answered
    if prayer_request.user_id != current_user.id:
        abort(403)
    
    testimony = request.form.get('testimony', '')
    
    prayer_request.is_answered = True
    prayer_request.testimony = testimony
    
    db.session.commit()
    
    flash('Prayer marked as answered! Glory to God!', 'success')
    return redirect(url_for('prayers.view', id=id))

@bp.route('/answered')
def answered():
    page = request.args.get('page', 1, type=int)
    
    query = PrayerRequest.query.filter_by(
        is_answered=True,
        is_public=True
    ).order_by(desc(PrayerRequest.updated_at))
    
    from config import Config
    pagination = query.paginate(page=page, per_page=Config.REQUESTS_PER_PAGE, error_out=False)
    requests = pagination.items
    
    return render_template('prayers/answered.html',
                         requests=requests,
                         pagination=pagination)

@bp.route('/report/<int:id>', methods=['POST'])
@login_required
def report(id):
    prayer_request = PrayerRequest.query.get_or_404(id)
    reason = request.form.get('reason', '')
    
    if not reason:
        flash('Please provide a reason for reporting.', 'error')
        return redirect(url_for('prayers.view', id=id))
    
    report = Report(
        request_id=id,
        user_id=current_user.id,
        reason=reason
    )
    
    db.session.add(report)
    db.session.commit()
    
    flash('Report submitted. Thank you for helping keep our community safe.', 'info')
    return redirect(url_for('prayers.view', id=id))

@bp.route('/my-requests')
@login_required
def my_requests():
    requests = PrayerRequest.query.filter_by(
        user_id=current_user.id
    ).order_by(desc(PrayerRequest.created_at)).all()
    
    return render_template('prayers/my_requests.html', requests=requests)

@bp.route('/my-prayers')
@login_required
def my_prayers():
    # Get all prayers by current user
    prayers = Prayer.query.filter_by(
        user_id=current_user.id
    ).order_by(desc(Prayer.created_at)).all()
    
    # Get stats
    today = date.today()
    today_stat = PrayerStats.query.filter_by(
        user_id=current_user.id,
        date=today
    ).first()
    
    today_count = today_stat.prayers_offered if today_stat else 0
    total_count = Prayer.query.filter_by(user_id=current_user.id).count()
    
    return render_template('prayers/my_prayers.html',
                         prayers=prayers,
                         today_count=today_count,
                         total_count=total_count)
