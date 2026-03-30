// state management
let domBodies = [];

// 1. Initialization
window.onload = () => {
    setupInteractions();
    fetchEmail(); // Initial fetch
};

// 2. Interactions (Drag & Drop + Buttons)
function setupInteractions() {
    const emailCard = document.getElementById('email-element');
    const dropZones = document.querySelectorAll('.drop-zone');

    emailCard.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', 'email');
        emailCard.style.opacity = '0.5';
    });

    emailCard.addEventListener('dragend', () => {
        emailCard.style.opacity = '1';
        dropZones.forEach(zone => zone.classList.remove('active'));
    });

    dropZones.forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('active');
        });

        zone.addEventListener('dragleave', () => {
            zone.classList.remove('active');
        });

        zone.addEventListener('drop', async (e) => {
            e.preventDefault();
            const category = zone.getAttribute('data-category');
            await performTriage(category);
        });

        zone.addEventListener('click', async () => {
            const category = zone.getAttribute('data-category');
            await performTriage(category);
        });
    });

    document.getElementById('reset-btn').onclick = () => fetchEmail();
}

async function performTriage(category) {
    const action = {
        category: category,
        priority: category === 'urgent' ? 'high' : (category === 'spam' ? 'low' : 'medium'),
        response: `Manual triage: Moved to ${category}`,
        strategic_priority: 0.5
    };

    try {
        const response = await fetch('/step', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(action)
        });
        const result = await response.json();
        updateUI(result.observation, result.reward, result.info);
    } catch (err) {
        console.error("Triage failed:", err);
    }
}

// 3. API & UI Updates
async function fetchEmail(task = "full") {
    const btn = document.getElementById('reset-btn');
    btn.innerHTML = '<span class="spinner"></span> Loading...';
    btn.disabled = true;

    try {
        const response = await fetch(`/reset?task=${task}`);
        const data = await response.json();
        updateUI(data, null, null);
        addToHistory(`[New Instance] Case #${data.email_id ?? '??'} pulled from dataset (Urgency: ${data.urgency})`);
    } catch (error) {
        console.error("Fetch failed:", error);
    } finally {
        btn.innerHTML = 'New Email';
        btn.disabled = false;
    }
}

function updateUI(obs, reward, info) {
    if (obs) {
        document.getElementById('email-text').innerText = obs.email_text;
        document.getElementById('sender').innerText = `From: ${obs.sender}`;
        
        const gravityBadge = document.getElementById('gravity-display');
        gravityBadge.innerText = `Urgency: ${obs.urgency}`;
        
        // Dynamic color based on urgency
        const gVal = parseFloat(obs.urgency);
        if (gVal > 0.7) gravityBadge.style.color = '#ff4d4d';
        else if (gVal > 0.4) gravityBadge.style.color = '#ffcc00';
        else gravityBadge.style.color = '#00ffcc';
    }
    
    if (reward) {
        document.getElementById('reward-val').innerText = reward.score.toFixed(2);
        addToHistory(`Triage Reward: ${reward.score.toFixed(2)} | Action: ${reward.contribution}`);
    }

    if (info && info.score !== undefined) {
        document.getElementById('score-val').innerText = info.score.toFixed(2);
    }
}

function addToHistory(text) {
    const historyList = document.getElementById('history-list');
    const item = document.createElement('div');
    item.className = 'history-item';
    item.innerText = `> ${text}`;
    historyList.prepend(item);
}
