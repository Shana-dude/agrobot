const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');
const micBtn = document.getElementById('mic-btn');

// ===============================
// GEOLOCATION (GPS)
// ===============================
let userLocation = { lat: null, lon: null };

function updateLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation.lat = position.coords.latitude;
                userLocation.lon = position.coords.longitude;
                console.log("Location updated:", userLocation);
            },
            (error) => {
                console.warn("Location access denied or failed:", error.message);
            }
        );
    }
}

// Initial location fetch
updateLocation();

// ===============================
// VOICE INPUT (STT)
// ===============================
let isRecording = false;
const recognition = window.webkitSpeechRecognition ? new webkitSpeechRecognition() : null;

if (recognition) {
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';

    micBtn.onclick = () => {
        if (isRecording) {
            recognition.stop();
        } else {
            recognition.start();
        }
    };

    recognition.onstart = () => {
        isRecording = true;
        micBtn.classList.add('recording');
        userInput.placeholder = 'Listening... / கேட்டுக்கொண்டிருக்கிறேன்...';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
    };

    recognition.onend = () => {
        isRecording = false;
        micBtn.classList.remove('recording');
        userInput.placeholder = 'Speak or Type... / பேசவும் அல்லது தட்டச்சு செய்யவும்...';
    };
} else {
    micBtn.style.display = 'none';
}

// ===============================
// CHAT LOGIC
// ===============================

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    let message = userInput.value.trim();
    if (!message) return;

    // Refresh location on submission to ensure accuracy
    updateLocation();

    message = message.replace(/\s+/g, ' ');

    addMessage(message, 'user');
    userInput.value = '';

    const botMsgDiv = addMessage('Thinking... / சிந்திக்கிறார்...', 'bot');

    try {
        const response = await fetch('/api/tomato-chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: message,
                lat: userLocation.lat,
                lon: userLocation.lon
            })
        });

        const data = await response.json();
        const cleanAnswer = data.answer.replace(/\*/g, '');

        updateBotMessage(botMsgDiv, cleanAnswer);
        addAudioButton(botMsgDiv, cleanAnswer);

    } catch (error) {
        updateBotMessage(botMsgDiv, 'Error connecting to server. / சர்வர் பிழை.');
    }
});

function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.innerHTML = `<div class="bubble">${text}</div>`;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return msgDiv;
}

function updateBotMessage(div, text) {
    const bubble = div.querySelector('.bubble');
    bubble.innerHTML = text.replace(/\n/g, '<br>');
}

function addAudioButton(div, text) {
    const audioBtn = document.createElement('button');
    audioBtn.className = 'audio-btn';
    audioBtn.innerHTML = '🔊 Hear Advice / ஆலோசனையைக் கேளுங்கள்';
    audioBtn.onclick = () => speakText(text);
    div.appendChild(audioBtn);
}

function speakText(text) {
    window.speechSynthesis.cancel();

    const parts = text.split('\n');

    parts.forEach(part => {
        if (!part.trim()) return;

        const utterance = new SpeechSynthesisUtterance(part);

        if (/[\u0B80-\u0BFF]/.test(part)) {
            utterance.lang = 'ta-IN';
        } else {
            utterance.lang = 'en-US';
        }

        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
    });
}

function askQuick(query) {
    userInput.value = query;
    chatForm.dispatchEvent(new Event('submit'));
}
