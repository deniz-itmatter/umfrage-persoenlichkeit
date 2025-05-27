class SurveyApp {
    constructor() {
        this.currentQuestion = 0;
        this.answers = {};
        this.questions = window.surveyData.questions;
        this.texts = window.surveyData.texts;
        this.isTransitioning = false;
        
        this.init();
    }
    
    init() {
        this.hideLoading();
        this.showIntro();
        this.loadProgress();
    }
    
    hideLoading() {
        document.getElementById('loadingState').classList.add('hidden');
    }
    
    showIntro() {
        document.getElementById('introScreen').classList.remove('hidden');
    }
    
    startSurvey() {
        this.hideScreen('introScreen');
        this.showScreen('surveyScreen');
        this.showQuestion(0);
    }
    
    showQuestion(questionIndex) {
        if (this.isTransitioning) return;
        
        this.currentQuestion = questionIndex;
        const question = this.questions[questionIndex];
        
        // Update UI
        this.updateProgressBar();
        this.updateQuestionCounter();
        this.updateBackButton();
        
        // Show question with animation
        this.animateQuestionChange(() => {
            document.getElementById('questionText').textContent = 
                `${questionIndex + 1}. ${question.text}`;
            this.renderScaleButtons();
        });
    }
    
    animateQuestionChange(callback) {
        const container = document.getElementById('questionContainer');
        
        this.isTransitioning = true;
        container.classList.add('transform', 'translate-x-8', 'opacity-0');
        
        setTimeout(() => {
            callback();
            container.classList.remove('transform', 'translate-x-8', 'opacity-0');
            this.isTransitioning = false;
        }, 250);
    }
    
    renderScaleButtons() {
        const container = document.getElementById('scaleButtons');
        const colors = [
            'from-red-400 to-red-500',
            'from-orange-400 to-orange-500',
            'from-yellow-400 to-yellow-500',
            'from-lime-400 to-lime-500',
            'from-green-400 to-green-500',
            'from-blue-400 to-blue-500'
        ];
        
        container.innerHTML = '';
        
        for (let i = 1; i <= 6; i++) {
            const button = document.createElement('button');
            const isSelected = this.answers[this.currentQuestion] === i;
            
            button.className = `
                aspect-square rounded-2xl font-bold text-2xl text-white shadow-lg 
                transform transition-all duration-300 ease-out flex items-center justify-center
                hover:scale-110 hover:shadow-2xl hover:-rotate-1
                active:scale-95 active:rotate-0
                bg-gradient-to-br ${colors[i-1]}
                ${isSelected ? 'ring-4 ring-white ring-opacity-70 scale-105 shadow-2xl' : 'hover:shadow-xl'}
            `;
            
            button.innerHTML = `
                <span class="transition-transform duration-200 ${isSelected ? 'scale-110' : ''}">${i}</span>
            `;
            
            button.addEventListener('click', () => this.selectAnswer(i));
            container.appendChild(button);
            
            // Staggered animation
            setTimeout(() => {
                button.style.animation = `fadeIn 0.6s ease-out ${i * 80}ms both`;
            }, 10);
        }
    }
    
    async selectAnswer(value) {
        if (this.isTransitioning) return;
        
        this.answers[this.currentQuestion] = value;
        
        // Save answer to server
        try {
            const response = await fetch('/api/answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question_id: this.questions[this.currentQuestion].id,
                    answer_value: value
                })
            });
            
            if (!response.ok) {
                throw new Error('Fehler beim Speichern der Antwort');
            }
            
            // Update UI to show selection
            this.renderScaleButtons();
            
            // Auto-advance after short delay
            setTimeout(() => {
                this.nextQuestion();
            }, 800);
            
        } catch (error) {
            console.error('Error saving answer:', error);
            this.showError('Fehler beim Speichern der Antwort. Bitte versuchen Sie es erneut.');
        }
    }
    
    nextQuestion() {
        if (this.currentQuestion < this.questions.length - 1) {
            this.showQuestion(this.currentQuestion + 1);
        } else {
            this.completeSurvey();
        }
    }
    
    goBack() {
        if (this.currentQuestion > 0) {
            this.showQuestion(this.currentQuestion - 1);
        }
    }
    
    async completeSurvey() {
        try {
            const response = await fetch('/api/complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error('Fehler beim Abschließen der Umfrage');
            }
            
            const results = await response.json();
            this.showResults(results);
            
        } catch (error) {
            console.error('Error completing survey:', error);
            this.showError('Fehler beim Abschließen der Umfrage. Bitte versuchen Sie es erneut.');
        }
    }
    
    async showResults(results) {
        this.hideScreen('surveyScreen');
        this.showScreen('resultsScreen');
        
        this.renderResults(results);
        await this.loadTodayStats();
    }
    
renderResults(results) {
    const container = document.getElementById('resultCharts');
    const userResults = results.user_results;
    const germanAverage = results.deutschland_durchschnitt;
    const labels = results.dimension_labels;
    
    // Sort dimensions by user score
    const sortedDimensions = Object.entries(userResults)
        .sort(([,a], [,b]) => b - a)
        .map(([dim]) => dim);
    
    const colors = {
        status: 'from-blue-400 to-cyan-500',
        erlebnisse: 'from-yellow-400 to-orange-500',
        nachhaltigkeit: 'from-green-400 to-emerald-500',
        wohlbefinden: 'from-purple-400 to-pink-500',
        tradition: 'from-amber-400 to-orange-500'
    };
    
    // Define icons for each dimension
    const icons = {
        status: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trophy w-6 h-6"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path></svg>`,
        
        erlebnisse: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles w-6 h-6"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"></path><path d="M20 3v4"></path><path d="M22 5h-4"></path><path d="M4 17v2"></path><path d="M5 18H3"></path></svg>`,
        
        nachhaltigkeit: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-leaf w-6 h-6"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path></svg>`,
        
        wohlbefinden: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-heart w-6 h-6"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>`,
        
        tradition: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield w-6 h-6"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path></svg>`
    };
    
    container.innerHTML = '';
    
    sortedDimensions.forEach(dimension => {
        const userScore = userResults[dimension];
        const germanScore = germanAverage[dimension];
        const label = labels[dimension];
        const color = colors[dimension];
        const icon = icons[dimension] || icons.status; // fallback to status icon
        
        const resultDiv = document.createElement('div');
        resultDiv.className = `bg-gradient-to-r from-${dimension === 'status' ? 'blue' : dimension === 'erlebnisse' ? 'yellow' : dimension === 'nachhaltigkeit' ? 'green' : dimension === 'wohlbefinden' ? 'purple' : 'amber'}-50 to-${dimension === 'status' ? 'blue' : dimension === 'erlebnisse' ? 'yellow' : dimension === 'nachhaltigkeit' ? 'green' : dimension === 'wohlbefinden' ? 'purple' : 'amber'}-50 border-2 border-${dimension === 'status' ? 'blue' : dimension === 'erlebnisse' ? 'yellow' : dimension === 'nachhaltigkeit' ? 'green' : dimension === 'wohlbefinden' ? 'purple' : 'amber'}-200 rounded-2xl p-6`;
        
        resultDiv.innerHTML = `
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                    <div class="bg-gradient-to-r ${color} text-white p-3 rounded-xl mr-4">
                        ${icon}
                    </div>
                    <div>
                        <h3 class="text-xl font-bold text-${dimension === 'status' ? 'blue' : dimension === 'erlebnisse' ? 'yellow' : dimension === 'nachhaltigkeit' ? 'green' : dimension === 'wohlbefinden' ? 'purple' : 'amber'}-700">
                            ${label}
                        </h3>
                        <p class="text-gray-600 text-sm">
                            Du: ${userScore.toFixed(2)} • Deutschland: ${germanScore.toFixed(2)}
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="space-y-3">
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-gray-700">Du</span>
                    <div class="flex-1 mx-4">
                        <div class="w-full bg-white rounded-full h-4 shadow-inner">
                            <div class="bg-gradient-to-r ${color} h-4 rounded-full transition-all duration-1000 ease-out flex items-center justify-end pr-2" 
                                 style="width: ${(userScore / 6) * 100}%">
                                <span class="text-xs font-bold text-white">${userScore.toFixed(1)}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-gray-500">Deutschland</span>
                    <div class="flex-1 mx-4">
                        <div class="w-full bg-white rounded-full h-3 shadow-inner">
                            <div class="bg-gray-400 h-3 rounded-full transition-all duration-1000 ease-out flex items-center justify-end pr-2"
                                 style="width: ${(germanScore / 6) * 100}%">
                                <span class="text-xs font-medium text-white">${germanScore.toFixed(1)}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(resultDiv);
    });
}
    
    async loadTodayStats() {
        try {
            const response = await fetch('/api/stats/today');
            if (response.ok) {
                const stats = await response.json();
                this.renderTodayStats(stats);
            }
        } catch (error) {
            console.error('Error loading today stats:', error);
        }
    }
    
    renderTodayStats(stats) {
        const container = document.getElementById('todayStatsContainer');
        
        if (Object.keys(stats).length === 0) {
            container.innerHTML = '<p class="text-gray-500">Noch keine Daten für heute verfügbar.</p>';
            return;
        }
        
        let html = '<div class="grid grid-cols-1 md:grid-cols-5 gap-4">';
        
        Object.entries(stats).forEach(([dimension, data]) => {
            html += `
                <div class="text-center">
                    <h4 class="font-semibold text-gray-800 capitalize">${dimension}</h4>
                    <p class="text-lg font-bold text-indigo-600">${data.avg_score.toFixed(2)}</p>
                    <p class="text-xs text-gray-600">${data.total_responses} Teilnahmen heute</p>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }
    
    updateProgressBar() {
        const progress = ((this.currentQuestion + 1) / this.questions.length) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;
    }
    
    updateQuestionCounter() {
        document.getElementById('questionCounter').textContent = 
            `${this.currentQuestion + 1} / ${this.questions.length}`;
    }
    
    updateBackButton() {
        const backButton = document.getElementById('backButton');
        if (this.currentQuestion > 0) {
            backButton.classList.remove('hidden');
        } else {
            backButton.classList.add('hidden');
        }
    }
    
    async loadProgress() {
        try {
            const response = await fetch('/api/progress');
            if (response.ok) {
                const progress = await response.json();
                if (progress.is_completed) {
                    // User has already completed the survey
                    // Could redirect to results or show message
                }
            }
        } catch (error) {
            console.error('Error loading progress:', error);
        }
    }
    
    showScreen(screenId) {
        document.getElementById(screenId).classList.remove('hidden');
    }
    
    hideScreen(screenId) {
        document.getElementById(screenId).classList.add('hidden');
    }
    
    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        this.hideScreen('surveyScreen');
        this.showScreen('errorScreen');
    }
    
    restartSurvey() {
        // Clear session and reload
        fetch('/api/restart', { method: 'POST' })
            .then(() => location.reload())
            .catch(() => location.reload());
    }
}

// Global functions for HTML event handlers
let surveyApp;

function startSurvey() {
    surveyApp.startSurvey();
}

function goBack() {
    surveyApp.goBack();
}

function restartSurvey() {
    surveyApp.restartSurvey();
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    surveyApp = new SurveyApp();
});