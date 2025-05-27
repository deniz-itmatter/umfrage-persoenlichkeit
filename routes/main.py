from flask import Blueprint, render_template, session
from utils import get_or_create_session
from settings import SURVEY_QUESTIONS, SURVEY_TEXTS

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Hauptseite der Umfrage"""
    try:
        from flask import request
        session_id = get_or_create_session(request, session)
        return render_template('index.html', 
                             questions=SURVEY_QUESTIONS,
                             texts=SURVEY_TEXTS)
    except Exception as e:
        return f"Fehler beim Laden der Umfrage: {str(e)}", 500

@main_bp.route('/admin')
def admin_dashboard():
    """Admin-Dashboard für Statistiken"""
    from utils import get_daily_stats, get_trending_dimensions
    from models import SurveySession
    from datetime import date
    
    try:
        # Heutige Statistiken
        today_stats = get_daily_stats()
        
        # Gesamtstatistiken
        total_sessions = SurveySession.query.count()
        completed_sessions = SurveySession.query.filter(
            SurveySession.completed_at.isnot(None)
        ).count()
        
        # Trends
        trends = get_trending_dimensions()
        
        stats = {
            'today': today_stats,
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'completion_rate': (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
            'trends': trends
        }
        
        return render_template('admin.html', stats=stats)
    except Exception as e:
        return f"Fehler beim Laden des Admin-Dashboards: {str(e)}", 500