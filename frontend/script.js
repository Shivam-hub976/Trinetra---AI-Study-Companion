// Placeholder JS for frontend interactions


document.getElementById('uploadForm').onsubmit = async function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('notesFile');
    const summaryDiv = document.getElementById('summary');
    if (!fileInput.files.length) {
        summaryDiv.innerText = 'Please select a file.';
        return;
    }
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    summaryDiv.innerText = 'Summarizing...';
    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (data.summary) {
            summaryDiv.innerText = data.summary;
        } else {
            summaryDiv.innerText = data.error || 'No summary returned.';
        }
    } catch (err) {
        summaryDiv.innerText = 'Error: ' + err;
    }
};


// Dynamic subject/priority input logic
const subjectsContainer = document.getElementById('subjectsContainer');
document.getElementById('addSubject').onclick = function() {
    const row = document.createElement('div');
    row.className = 'subjectRow';
    row.innerHTML = `
        <input type="text" class="subjectName" placeholder="Subject name">
        <input type="number" class="subjectPriority" min="1" max="5" value="3" title="Priority (1=Low, 5=High)">
        <input type="number" class="subjectDifficulty" min="1" max="5" value="3" title="Difficulty (1=Easy, 5=Hard)">
        <input type="number" class="subjectProficiency" min="1" max="5" value="3" title="Proficiency (1=Weak, 5=Strong)">
        <input type="date" class="subjectExamDate" title="Exam Date">
        <input type="number" class="subjectMinHours" min="0" step="0.5" placeholder="Min hrs" title="Minimum hours">
        <input type="number" class="subjectMaxHours" min="0" step="0.5" placeholder="Max hrs" title="Maximum hours">
        <button type="button" class="removeSubject">Remove</button>
    `;
    row.querySelector('.removeSubject').onclick = function() {
        row.remove();
    };
    subjectsContainer.appendChild(row);
};
Array.from(document.getElementsByClassName('removeSubject')).forEach(btn => {
    btn.onclick = function() {
        btn.parentElement.remove();
    };
});

document.getElementById('plannerForm').onsubmit = async function(e) {
    e.preventDefault();
    const hours = document.getElementById('studyHours').value;
    const planDiv = document.getElementById('plan');
    const subjectRows = subjectsContainer.getElementsByClassName('subjectRow');
    const topics = [];
        for (let row of subjectRows) {
            const name = row.querySelector('.subjectName').value.trim();
            const priority = parseInt(row.querySelector('.subjectPriority').value) || 1;
            const difficulty = parseInt(row.querySelector('.subjectDifficulty').value) || 1;
            const proficiency = parseInt(row.querySelector('.subjectProficiency').value) || 3;
            const exam_date = row.querySelector('.subjectExamDate').value;
            const min_hours = parseFloat(row.querySelector('.subjectMinHours').value) || 0;
            const max_hours = parseFloat(row.querySelector('.subjectMaxHours').value) || undefined;
            if (name) {
                topics.push({ name, priority, difficulty, proficiency, exam_date, min_hours, max_hours });
            }
        }
    if (!hours || !topics.length) {
        planDiv.innerText = 'Please enter study hours and at least one subject.';
        return;
    }
    planDiv.innerText = 'Generating plan...';
    try {
        const response = await fetch('/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hours: Number(hours), topics })
        });
        const data = await response.json();
        if (data.plan) {
            let planText = '';
            for (const topic in data.plan) {
                planText += `${topic}: ${data.plan[topic]} hours\n`;
            }
            planDiv.innerText = planText;
        } else {
            planDiv.innerText = data.error || 'No plan returned.';
        }
    } catch (err) {
        planDiv.innerText = 'Error: ' + err;
    }
};
