from models import db, SurveySession, SurveyAnswer, DailyStats, WeeklyStats
from settings import SURVEY_QUESTIONS, DEUTSCHLAND_DURCHSCHNITT
from datetime import datetime, date
from sqlalchemy import func, and_
import statistics

def get_or_create_session(request, session):
    """Erstellt oder lädt eine Umfrage-Session"""
    if 'survey_session_id' not in session:
        # Neue Session erstellen
        survey_session = SurveySession(
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500]
        )
        db.session.add(survey_session)
        try:
            db.session.commit()
            session['survey_session_id'] = survey_session.id
            session.permanent = True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating survey session: {e}")
    
    return session.get('survey_session_id')

def calculate_user_results(session_id):
    """Berechnet die Ergebnisse für einen Nutzer"""
    answers = SurveyAnswer.query.filter_by(session_id=session_id).all()
    
    if not answers or len(answers) != len(SURVEY_QUESTIONS):
        return None
    
    # Gruppiere Antworten nach Dimensionen
    dimension_scores = {}
    for answer in answers:
        if answer.dimension not in dimension_scores:
            dimension_scores[answer.dimension] = []
        dimension_scores[answer.dimension].append(answer.answer_value)
    
    # Berechne Durchschnittswerte
    results = {}
    for dimension, scores in dimension_scores.items():
        results[dimension] = sum(scores) / len(scores)
    
    return results

def get_question_by_id(question_id):
    """Findet eine Frage anhand der ID"""
    return next((q for q in SURVEY_QUESTIONS if q['id'] == question_id), None)

def mark_session_completed(session_id):
    """Markiert eine Session als abgeschlossen"""
    survey_session = SurveySession.query.get(session_id)
    if survey_session and not survey_session.completed_at:
        survey_session.completed_at = datetime.utcnow()
        db.session.commit()
        return True
    return False

def update_daily_stats():
    """Aktualisiert die täglichen Statistiken"""
    today = date.today()
    
    for dimension in DEUTSCHLAND_DURCHSCHNITT.keys():
        # Hole alle Antworten für diese Dimension von heute
        today_answers = db.session.query(SurveyAnswer.answer_value).join(SurveySession).filter(
            SurveyAnswer.dimension == dimension,
            func.date(SurveySession.completed_at) == today,
            SurveySession.completed_at.isnot(None)
        ).all()
        
        if today_answers:
            scores = [answer[0] for answer in today_answers]
            avg_score = statistics.mean(scores)
            min_score = min(scores)
            max_score = max(scores)
            std_dev = statistics.stdev(scores) if len(scores) > 1 else 0
            
            # Zähle einzigartige Sessions
            total_responses = db.session.query(SurveySession.id).filter(
                func.date(SurveySession.completed_at) == today,
                SurveySession.completed_at.isnot(None)
            ).count()
            
            # Aktualisiere oder erstelle Statistik
            daily_stat = DailyStats.query.filter_by(date=today, dimension=dimension).first()
            if daily_stat:
                daily_stat.avg_score = avg_score
                daily_stat.total_responses = total_responses
                daily_stat.min_score = min_score
                daily_stat.max_score = max_score
                daily_stat.std_deviation = std_dev
            else:
                daily_stat = DailyStats(
                    date=today,
                    dimension=dimension,
                    avg_score=avg_score,
                    total_responses=total_responses,
                    min_score=min_score,
                    max_score=max_score,
                    std_deviation=std_dev
                )
                db.session.add(daily_stat)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error updating daily stats: {e}")

def get_daily_stats(target_date=None):
    """Holt die täglichen Statistiken"""
    if target_date is None:
        target_date = date.today()
    
    stats = DailyStats.query.filter_by(date=target_date).all()
    
    result = {}
    for stat in stats:
        result[stat.dimension] = {
            'avg_score': stat.avg_score,
            'total_responses': stat.total_responses,
            'min_score': stat.min_score,
            'max_score': stat.max_score,
            'std_deviation': stat.std_deviation
        }
    
    return result

def get_trending_dimensions():
    """Ermittelt die trending Dimensionen der letzten 7 Tage"""
    from datetime import timedelta
    
    last_week = date.today() - timedelta(days=7)
    
    recent_stats = DailyStats.query.filter(
        DailyStats.date >= last_week
    ).all()
    
    # Gruppiere nach Dimensionen und berechne Trends
    dimension_trends = {}
    for stat in recent_stats:
        if stat.dimension not in dimension_trends:
            dimension_trends[stat.dimension] = []
        dimension_trends[stat.dimension].append(stat.avg_score)
    
    # Berechne Trend (steigend/fallend)
    trends = {}
    for dimension, scores in dimension_trends.items():
        if len(scores) >= 2:
            trend = scores[-1] - scores[0]  # Letzter - Erster Wert
            trends[dimension] = trend
    
    return trends