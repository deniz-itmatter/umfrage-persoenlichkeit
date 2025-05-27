from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import uuid

db = SQLAlchemy()

class SurveySession(db.Model):
    """Umfrage-Session Modell"""
    __tablename__ = 'survey_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = db.Column(db.DateTime, index=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    
    # Beziehung zu Antworten
    answers = db.relationship('SurveyAnswer', backref='session', lazy='dynamic', 
                            cascade='all, delete-orphan')
    
    @property
    def is_completed(self):
        """Prüft ob die Umfrage abgeschlossen ist"""
        return self.completed_at is not None
    
    @property
    def completion_rate(self):
        """Berechnet den Fortschritt in Prozent"""
        total_questions = 10
        answered_questions = self.answers.count()
        return min(100, (answered_questions / total_questions) * 100)

class SurveyAnswer(db.Model):
    """Antworten-Modell"""
    __tablename__ = 'survey_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('survey_sessions.id'), 
                          nullable=False, index=True)
    question_id = db.Column(db.Integer, nullable=False, index=True)
    answer_value = db.Column(db.Integer, nullable=False)
    dimension = db.Column(db.String(50), nullable=False, index=True)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('session_id', 'question_id', name='unique_session_question'),
    )

class DailyStats(db.Model):
    """Tägliche Statistiken"""
    __tablename__ = 'daily_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    dimension = db.Column(db.String(50), nullable=False, index=True)
    avg_score = db.Column(db.Float, nullable=False)
    total_responses = db.Column(db.Integer, nullable=False)
    min_score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    std_deviation = db.Column(db.Float)
    
    __table_args__ = (
        db.UniqueConstraint('date', 'dimension', name='unique_daily_dimension'),
    )

class WeeklyStats(db.Model):
    """Wöchentliche Statistiken"""
    __tablename__ = 'weekly_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    dimension = db.Column(db.String(50), nullable=False, index=True)
    avg_score = db.Column(db.Float, nullable=False)
    total_responses = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('year', 'week', 'dimension', name='unique_weekly_dimension'),
    )