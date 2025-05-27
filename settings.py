"""
Statische Einstellungen und Konstanten für die Werte-Umfrage
"""

# Fragen der Umfrage
SURVEY_QUESTIONS = [
    {
        "id": 1,
        "text": "Es ist ihr/ihm wichtig, traditionelle Werte und Überzeugungen zu bewahren.",
        "dimension": "tradition"
    },
    {
        "id": 2,
        "text": "Es ist ihr/ihm wichtig, das Leben in vollen Zügen zu genießen.",
        "dimension": "erlebnisse"
    },
    {
        "id": 3,
        "text": "Es ist ihr/ihm wichtig, zum Schutz der Natur so wenig Ressourcen wie möglich zu verbrauchen.",
        "dimension": "nachhaltigkeit"
    },
    {
        "id": 4,
        "text": "Es ist ihr/ihm wichtig, reich zu sein.",
        "dimension": "status"
    },
    {
        "id": 5,
        "text": "Es ist ihr/ihm wichtig, ein Leben ganz ohne Stress und Druck zu führen.",
        "dimension": "wohlbefinden"
    },
    {
        "id": 6,
        "text": "Es ist ihr/ihm wichtig, sich um die Natur zu kümmern.",
        "dimension": "nachhaltigkeit"
    },
    {
        "id": 7,
        "text": "Es ist ihr/ihm wichtig, so oft wie möglich unterschiedliche Dinge auszuprobieren.",
        "dimension": "erlebnisse"
    },
    {
        "id": 8,
        "text": "Es ist ihr/ihm wichtig, das Leben ganz nach ihren/seinen innersten Empfindungen auszurichten.",
        "dimension": "wohlbefinden"
    },
    {
        "id": 9,
        "text": "Es ist ihr/ihm wichtig, sehr erfolgreich zu sein.",
        "dimension": "status"
    },
    {
        "id": 10,
        "text": "Es ist ihr/ihm wichtig, dass das Leben immer in geordneten Bahnen verläuft.",
        "dimension": "tradition"
    }
]

# Deutschland-Durchschnittswerte 
DEUTSCHLAND_DURCHSCHNITT = {
    "status": 2.87,
    "erlebnisse": 3.64,
    "nachhaltigkeit": 3.86,
    "wohlbefinden": 3.89,
    "tradition": 3.94
}

# Labels für die Dimensionen
DIMENSION_LABELS = {
    "status": "Status",
    "erlebnisse": "Erlebnisse",
    "nachhaltigkeit": "Nachhaltigkeit",
    "wohlbefinden": "Wohlbefinden",
    "tradition": "Tradition"
}

# Farben für die Visualisierung
DIMENSION_COLORS = {
    "status": {
        "light": "from-blue-400 to-cyan-500",
        "bg": "bg-blue-50",
        "border": "border-blue-200",
        "text": "text-blue-700"
    },
    "erlebnisse": {
        "light": "from-yellow-400 to-orange-500",
        "bg": "bg-yellow-50",
        "border": "border-yellow-200",
        "text": "text-yellow-700"
    },
    "nachhaltigkeit": {
        "light": "from-green-400 to-emerald-500",
        "bg": "bg-green-50",
        "border": "border-green-200",
        "text": "text-green-700"
    },
    "wohlbefinden": {
        "light": "from-purple-400 to-pink-500",
        "bg": "bg-purple-50",
        "border": "border-purple-200",
        "text": "text-purple-700"
    },
    "tradition": {
        "light": "from-amber-400 to-orange-500",
        "bg": "bg-amber-50",
        "border": "border-amber-200",
        "text": "text-amber-700"
    }
}

# Skala-Optionen
SCALE_OPTIONS = [
    {"value": 1, "label": "1", "description": "Ist mir überhaupt nicht ähnlich"},
    {"value": 2, "label": "2", "description": ""},
    {"value": 3, "label": "3", "description": ""},
    {"value": 4, "label": "4", "description": ""},
    {"value": 5, "label": "5", "description": ""},
    {"value": 6, "label": "6", "description": "Ist mir sehr ähnlich"}
]

# Umfrage-Texte
SURVEY_TEXTS = {
    "title": "Werte-Umfrage",
    "subtitle": "Wir beschreiben Ihnen nun kurz verschiedene Personen. Bitte lesen Sie jede Beschreibung durch und denken Sie darüber nach, inwieweit Ihnen die Person ähnlich oder nicht ähnlich ist.",
    "intro_features": [
        {"icon": "10", "text": "Fragen zu Ihren persönlichen Werten"},
        {"icon": "📊", "text": "Vergleich mit dem Deutschland-Durchschnitt"},
        {"icon": "⏱️", "text": "Dauert ca. 3-5 Minuten"}
    ],
    "start_button": "Umfrage starten",
    "back_button": "Zurück zur vorherigen Frage",
    "result_title": "Dein Werteprofil",
    "result_subtitle": "Im Vergleich zum Deutschland-Durchschnitt",
    "restart_button": "Umfrage wiederholen"
}