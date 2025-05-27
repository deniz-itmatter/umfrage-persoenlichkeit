from flask import Blueprint, request, jsonify, session
from models import db, SurveyAnswer, SurveySession
from utils import get_or_create_session, calculate_user_results, get_question_by_id, mark_session_completed, update_daily_stats
from settings import SURVEY_QUESTIONS, DEUTSCHLAND_DURCHSCHNITT, DIMENSION_LABELS

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/questions')
def get_questions():
    """API-Endpoint für Fragen"""
    return jsonify(SURVEY_QUESTIONS)

@api_bp.route('/answer', methods=['POST'])
def submit_answer():
    """Speichert eine einzelne Antwort"""
    try:
        session_id = session.get('survey_session_id')
        if not session_id:
            return jsonify({'error': 'Keine gültige Session'}), 400
        
        data = request.get_json()
        question_id = data.get('question_id')
        answer_value = data.get('answer_value')
        
        if not question_id or not answer_value:
            return jsonify({'error': 'Ungültige Daten'}), 400
        
        if not (1 <= answer_value <= 6):
            return jsonify({'error': 'Antwort muss zwischen 1 und 6 liegen'}), 400
        
        # Finde die entsprechende Frage
        question = get_question_by_id(question_id)
        if not question:
            return jsonify({'error': 'Ungültige Frage'}), 400
        
        # Lösche vorherige Antwort falls vorhanden
        SurveyAnswer.query.filter_by(session_id=session_id, question_id=question_id).delete()
        
        # Speichere neue Antwort
        answer = SurveyAnswer(
            session_id=session_id,
            question_id=question_id,
            answer_value=answer_value,
            dimension=question['dimension']
        )
        
        db.session.add(answer)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Fehler beim Speichern: {str(e)}'}), 500

@api_bp.route('/complete', methods=['POST'])
def complete_survey():
    """Schließt die Umfrage ab und berechnet Ergebnisse"""
    try:
        session_id = session.get('survey_session_id')
        if not session_id:
            return jsonify({'error': 'Keine gültige Session'}), 400
        
        # Prüfe ob alle Fragen beantwortet wurden
        answer_count = SurveyAnswer.query.filter_by(session_id=session_id).count()
        if answer_count != len(SURVEY_QUESTIONS):
            return jsonify({'error': 'Nicht alle Fragen beantwortet'}), 400
        
        # Markiere Session als abgeschlossen
        mark_session_completed(session_id)
        
        # Berechne Ergebnisse
        user_results = calculate_user_results(session_id)
        if not user_results:
            return jsonify({'error': 'Fehler beim Berechnen der Ergebnisse'}), 500
        
        # Aktualisiere tägliche Statistiken
        update_daily_stats()
        
        # Bereite Antwort vor
        response_data = {
            'user_results': user_results,
            'deutschland_durchschnitt': DEUTSCHLAND_DURCHSCHNITT,
            'dimension_labels': DIMENSION_LABELS,
            'session_completed': True
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'Fehler beim Abschließen: {str(e)}'}), 500

@api_bp.route('/stats/today')
def today_stats():
    """Heutige Statistiken"""
    try:
        from utils import get_daily_stats
        stats = get_daily_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': f'Fehler beim Laden der Statistiken: {str(e)}'}), 500

@api_bp.route('/progress')
def get_progress():
    """Aktueller Fortschritt der Session"""
    try:
        session_id = session.get('survey_session_id')
        if not session_id:
            return jsonify({'progress': 0, 'answered_questions': 0})
        
        survey_session = SurveySession.query.get(session_id)
        if not survey_session:
            return jsonify({'progress': 0, 'answered_questions': 0})
        
        answered_questions = survey_session.answers.count()
        progress = survey_session.completion_rate
        
        return jsonify({
            'progress': progress,
            'answered_questions': answered_questions,
            'total_questions': len(SURVEY_QUESTIONS),
            'is_completed': survey_session.is_completed
        })
        
    except Exception as e:
        return jsonify({'error': f'Fehler beim Laden des Fortschritts: {str(e)}'}), 500