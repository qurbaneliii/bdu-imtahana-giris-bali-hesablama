document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSeminars();
    initCalculator();
});

// --- Theme Management ---
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    const icon = themeToggle.querySelector('.icon');
    const text = themeToggle.querySelector('.text');
    
    // Check saved preference
    const savedTheme = localStorage.getItem('bdu_theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark');
        updateThemeUI(true);
    }

    themeToggle.addEventListener('click', () => {
        const isDark = body.classList.toggle('dark');
        localStorage.setItem('bdu_theme', isDark ? 'dark' : 'light');
        updateThemeUI(isDark);
    });

    function updateThemeUI(isDark) {
        icon.textContent = isDark ? '☀️' : '🌙';
        text.textContent = isDark ? 'Açıq rejim' : 'Tünd rejim';
    }
}

// --- Seminar Inputs Management ---
function initSeminars() {
    const seminarCountSelect = document.getElementById('seminarCount');
    const container = document.getElementById('seminarInputsContainer');

    function renderInputs() {
        const count = parseInt(seminarCountSelect.value) || 0;
        container.innerHTML = '';
        
        // Create 0-10 options string once
        let options = '';
        for(let i=0; i<=10; i++) {
            options += `<option value="${i}">${i}</option>`;
        }

        for (let i = 1; i <= count; i++) {
            const div = document.createElement('div');
            div.className = 'input-group';
            div.innerHTML = `
                <label>Sem. ${i}</label>
                <select class="form-select seminar-input" required>
                    ${options}
                </select>
            `;
            // Set default value to 5 as mid-point
            div.querySelector('select').value = "5"; 
            container.appendChild(div);
        }
    }

    seminarCountSelect.addEventListener('change', renderInputs);
    // Initial render
    renderInputs();
}

// --- Calculator Logic ---
function initCalculator() {
    const form = document.getElementById('calculatorForm');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // 1. Dərs saatı
        const hoursInput = document.querySelector('input[name="courseHours"]:checked');
        const courseHours = hoursInput ? parseInt(hoursInput.value) : 0;

        // 2. Kollekvium (Average * 0.6)
        const coll1 = parseInt(document.getElementById('coll1').value) || 0;
        const coll2 = parseInt(document.getElementById('coll2').value) || 0;
        const coll3 = parseInt(document.getElementById('coll3').value) || 0;
        const collAvg = (coll1 + coll2 + coll3) / 3;
        const collScore = collAvg * 0.6;

        // 3. Seminar (Average * 0.4)
        const seminarInputs = document.querySelectorAll('.seminar-input');
        let seminarSum = 0;
        let seminarCount = 0;
        
        seminarInputs.forEach(input => {
            seminarSum += parseInt(input.value) || 0;
            seminarCount++;
        });
        
        const seminarAvg = seminarCount > 0 ? (seminarSum / seminarCount) : 0;
        const seminarScore = seminarAvg * 0.4;

        // 4. Davamiyyət
        // Logic: hours >= 60 ? penalty 0.33 : penalty 0.5
        // Score = 10 - (absences * penalty)
        const absences = parseInt(document.getElementById('absences').value) || 0;
        const penalty = courseHours >= 60 ? 0.33 : 0.5;
        let attendanceScore = 10 - (absences * penalty);
        
        // Clamping logic
        if (attendanceScore < 0) attendanceScore = 0;
        if (attendanceScore > 10) attendanceScore = 10;

        // 5. Sərbəst iş
        const independentWork = parseInt(document.getElementById('independentWork').value) || 0;

        // 6. Yekun Hesablama
        // Base scale: 30 (6+4+10+10). Target scale: 50.
        const baseTotal = collScore + seminarScore + attendanceScore + independentWork;
        const finalScore50 = baseTotal * (50 / 30);

        // Display Results
        displayResults({
            coll: { score: collScore, avg: collAvg },
            sem: { score: seminarScore, avg: seminarAvg },
            att: attendanceScore,
            ind: independentWork,
            final: finalScore50
        });
    });
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    
    // Update DOM
    document.getElementById('resultColl').textContent = 
        `${data.coll.score.toFixed(2)} (ort: ${data.coll.avg.toFixed(1)})`;
    
    document.getElementById('resultSem').textContent = 
        `${data.sem.score.toFixed(2)} (ort: ${data.sem.avg.toFixed(1)})`;
        
    document.getElementById('resultAtt').textContent = data.att.toFixed(2);
    document.getElementById('resultInd').textContent = data.ind.toFixed(2);
    
    document.getElementById('finalScore').textContent = `${data.final.toFixed(2)} / 50`;

    // Show and scroll
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function resetForm() {
    document.getElementById('calculatorForm').reset();
    document.getElementById('results').classList.add('hidden');
    document.getElementById('seminarCount').dispatchEvent(new Event('change'));
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
