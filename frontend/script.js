// const chatBox = document.getElementById('chat-box');
// const userInput = document.getElementById('user-input');
// const sendBtn = document.getElementById('send-btn');
// const micBtn = document.getElementById('mic-btn');
// const statusIndicator = document.getElementById('mic-status');
// const themeBtn = document.getElementById('theme-btn');
// const clearBtn = document.getElementById('clear-btn');
// const settingsBtn = document.getElementById('settings-btn');

// /* =============================================
//    1. ADD MESSAGE & SAVE HISTORY
//    ============================================= */
// function addMessage(text, isUser = false) {
//     const msgDiv = document.createElement('div');
//     msgDiv.className = `message ${isUser ? 'user' : 'bot'}`;
//     if (!isUser) {
//         msgDiv.innerHTML = `<span>Jarvis:</span> ${text}`;
//     } else {
//         msgDiv.textContent = text;
//     }
//     chatBox.appendChild(msgDiv);
//     chatBox.scrollTop = chatBox.scrollHeight;

//     // ====== SAVE TO LOCAL STORAGE FOR SIDEBAR HISTORY ======
//     saveMessageToHistory(text, isUser);
// }

// function saveMessageToHistory(text, isUser) {
//     const history = JSON.parse(localStorage.getItem('jarvisHistory') || '[]');
//     history.push({
//         text: text,
//         isUser: isUser,
//         timestamp: new Date().toISOString()
//     });
//     localStorage.setItem('jarvisHistory', JSON.stringify(history));
//     renderSidebarHistory(); // Refresh the sidebar
// }

// function renderSidebarHistory() {
//     const sidebar = document.querySelector('.history-sidebar');
//     if (!sidebar) return;

//     const history = JSON.parse(localStorage.getItem('jarvisHistory') || '[]');
//     const today = new Date().toDateString();
//     const yesterday = new Date(Date.now() - 86400000).toDateString();

//     // Group by date
//     const groups = { Today: [], Yesterday: [], Older: [] };

//     history.forEach(item => {
//         const date = new Date(item.timestamp).toDateString();
//         if (date === today) groups.Today.push(item);
//         else if (date === yesterday) groups.Yesterday.push(item);
//         else groups.Older.push(item);
//     });

//     // Clear sidebar and rebuild
//     sidebar.innerHTML = '';
//     for (const [label, items] of Object.entries(groups)) {
//         if (items.length === 0) continue;

//         const heading = document.createElement('h3');
//         heading.textContent = `📅 ${label}`;
//         sidebar.appendChild(heading);

//         // Only show latest 5 items per day to keep it clean
//         items.slice(-5).reverse().forEach(item => {
//             const div = document.createElement('div');
//             div.className = 'hist-item';
//             div.textContent = item.isUser ? `You: ${item.text}` : `Jarvis: ${item.text}`;
//             sidebar.appendChild(div);
//         });
//     }
// }

// /* =============================================
//    2. SEND QUERY TO BACKEND & TTS
//    ============================================= */
// async function sendQuery(query) {
//     if (!query.trim()) return;
//     addMessage(query, true);
//     userInput.value = '';

//     try {
//         const response = await fetch('/api/command', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ query: query })
//         });
//         const data = await response.json();
//         if (data.error) {
//             addMessage('Error: ' + data.error);
//             return;
//         }
//         if (data.reply) {
//             addMessage(data.reply);
//             speakText(data.reply);
//         }
//         if (data.action === 'open_url' && data.data) {
//             window.open(data.data, '_blank');
//         } else if (data.action === 'shutdown') {
//             alert('Shutting down system... (demo)');
//         } else if (data.action === 'quit') {
//             setTimeout(() => window.close(), 2000);
//         }
//     } catch (error) {
//         addMessage('Network error: ' + error.message);
//     }
// }

// function speakText(text) {
//     if (!window.speechSynthesis) {
//         console.warn("Speech synthesis not supported");
//         return;
//     }
//     window.speechSynthesis.cancel();
//     const utterance = new SpeechSynthesisUtterance(text);
//     utterance.rate = 0.9;
//     utterance.pitch = 1;
//     utterance.lang = 'en-US';
//     const voices = window.speechSynthesis.getVoices();
//     const preferredVoice = voices.find(v => v.lang.includes('en') && v.name.includes('Female'));
//     if (preferredVoice) utterance.voice = preferredVoice;
//     if (voices.length === 0) {
//         window.speechSynthesis.onvoiceschanged = () => {
//             const newVoices = window.speechSynthesis.getVoices();
//             const betterVoice = newVoices.find(v => v.lang.includes('en'));
//             if (betterVoice) utterance.voice = betterVoice;
//             window.speechSynthesis.speak(utterance);
//         };
//         return;
//     }
//     window.speechSynthesis.speak(utterance);
// }

// // Enable Speech after first click
// let speechEnabled = false;
// document.addEventListener('click', () => {
//     if (!speechEnabled) {
//         speechEnabled = true;
//         const dummy = new SpeechSynthesisUtterance(' ');
//         speechSynthesis.speak(dummy);
//         setTimeout(() => speechSynthesis.cancel(), 100);
//     }
// });

// /* =============================================
//    3. EVENT LISTENERS (SEND, CLEAR, THEME, SETTINGS)
//    ============================================= */
// sendBtn.addEventListener('click', () => sendQuery(userInput.value));
// userInput.addEventListener('keydown', (e) => {
//     if (e.key === 'Enter') sendQuery(userInput.value);
// });

// // Clear Chat
// clearBtn.addEventListener('click', () => {
//     chatBox.innerHTML = '';
//     // Optional: clear localStorage history as well
//     localStorage.removeItem('jarvisHistory');
//     renderSidebarHistory();
//     addMessage('🧹 Chat and history cleared.');
// });

// // ** FIXED THEME TOGGLE (Runs on click, not on load) **
// themeBtn.addEventListener('click', () => {
//     document.body.classList.toggle('light-theme');
//     themeBtn.textContent = document.body.classList.contains('light-theme') ? '☀️' : '🌙';
// });

// // Settings Button
// settingsBtn.addEventListener('click', () => {
//     alert('⚙️ Settings\n\n' +
//         '1. Mic: Always ON\n' +
//         '2. Wake word: "Jarvis"\n' +
//         '3. AI Provider: Groq\n' +
//         '4. Volume: 80%\n\n' +
//         'More settings coming soon...');
// });

// /* =============================================
//    4. CONTINUOUS MIC – WAKE WORD "JARVIS"
//    ============================================= */
// let recognition = null;
// let isListening = false;

// function startContinuousListening() {
//     if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
//         addMessage('❌ Your browser does not support speech recognition. Please use Chrome or Edge.');
//         return;
//     }

//     const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
//     recognition = new SpeechRecognition();
//     recognition.lang = 'en-IN';
//     recognition.continuous = true;
//     recognition.interimResults = false;
//     recognition.maxAlternatives = 1;

//     updateMicStatus(true);

//     recognition.onresult = (event) => {
//         const last = event.results.length - 1;
//         const transcript = event.results[last][0].transcript.trim().toLowerCase();
//         console.log('Heard:', transcript);

//         if (transcript.startsWith('jarvis')) {
//             let command = transcript.replace(/^jarvis\s*/, '').trim();
//             if (command) {
//                 addMessage(`🎤 (voice) ${command}`, true);
//                 sendQuery(command);
//             }
//         }
//     };

//     recognition.onerror = (event) => {
//         console.warn('Recognition error:', event.error);
//         if (event.error === 'not-allowed') {
//             addMessage('❌ Microphone access denied. Please allow microphone in browser settings.');
//             updateMicStatus(false);
//             return;
//         }
//         restartRecognition();
//     };

//     recognition.onend = () => {
//         if (isListening) {
//             restartRecognition();
//         }
//     };

//     recognition.start();
//     isListening = true;
// }

// function restartRecognition() {
//     if (recognition) {
//         try { recognition.stop(); } catch (e) {}
//     }
//     setTimeout(() => {
//         if (isListening) {
//             startContinuousListening();
//         }
//     }, 500);
// }

// function stopListening() {
//     isListening = false;
//     if (recognition) {
//         try { recognition.stop(); } catch (e) {}
//         recognition = null;
//     }
//     updateMicStatus(false);
// }

// function updateMicStatus(active) {
//     if (micBtn) {
//         micBtn.textContent = active ? '🎤' : '⏹';
//         micBtn.style.background = active ? '#4CAF50' : '#444';
//         micBtn.title = active ? 'Microphone is listening' : 'Microphone is off';
//     }
//     if (statusIndicator) {
//         statusIndicator.textContent = active ? '🔴 Listening...' : '⏸️ Mic off';
//         statusIndicator.style.color = active ? '#4CAF50' : '#888';
//     }
// }

// /* =============================================
//    ✅ MANUAL TOGGLE: AGAR ON HAI TOH OFF, AGAR OFF HAI TOH ON
//    ============================================= */
// micBtn.addEventListener('click', () => {
//     if (isListening) {
//         stopListening();
//         addMessage('⏹️ Microphone stopped.', false);
//     } else {
//         startContinuousListening();
//         addMessage('🎤 Microphone started. Say "Jarvis" followed by your command.', false);
//     }
// });

// /* =============================================
//    5. PAGE LOAD & GREETING
//    ============================================= */
// window.addEventListener('load', () => {
//     // Load history from storage when page refreshes
//     renderSidebarHistory();

//     setTimeout(() => {
//         startContinuousListening();
//         addMessage('🎤 Microphone is active. Say "Jarvis" followed by your command.', false);
//     }, 1000);
// });

// fetch('/api/greeting')
//     .then(res => res.json())
//     .then(data => {
//         if (data.greeting) {
//             addMessage(data.greeting);
//             setTimeout(() => speakText(data.greeting), 300);
//         }
//     })
//     .catch(() => {});



// /* =============================================
// STOP SPEAKER (MUTE BUTTON)
// ============================================= */
// const muteBtn = document.getElementById('mute-btn');

// muteBtn.addEventListener('click', () => {
//     // This stops the browser from speaking (stops the speaker)
//     window.speechSynthesis.cancel();

//     // Visual feedback so you know it worked
//     muteBtn.textContent = '🔇';
//     muteBtn.style.color = '#ff4444'; // Turns red briefly

//     setTimeout(() => {
//         muteBtn.style.color = ''; // Reverts back to normal
//     }, 500);
// });

const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const statusIndicator = document.getElementById('mic-status');
const themeBtn = document.getElementById('theme-btn');
const clearBtn = document.getElementById('clear-btn');
const settingsBtn = document.getElementById('settings-btn');
const muteBtn = document.getElementById('mute-btn');

// 👇 NEW: This keeps track of whether the speaker is ON or OFF
let isSpeakerOn = true;

/* =============================================
   1. ADD MESSAGE & SAVE HISTORY
   ============================================= */
function addMessage(text, isUser = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    if (!isUser) {
        msgDiv.innerHTML = `<span>Jarvis:</span> ${text}`;
    } else {
        msgDiv.textContent = text;
    }
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    saveMessageToHistory(text, isUser);
}

function saveMessageToHistory(text, isUser) {
    const history = JSON.parse(localStorage.getItem('jarvisHistory') || '[]');
    history.push({
        text: text,
        isUser: isUser,
        timestamp: new Date().toISOString()
    });
    localStorage.setItem('jarvisHistory', JSON.stringify(history));
    renderSidebarHistory();
}

function renderSidebarHistory() {
    const sidebar = document.querySelector('.history-sidebar');
    if (!sidebar) return;

    const history = JSON.parse(localStorage.getItem('jarvisHistory') || '[]');
    const today = new Date().toDateString();
    const yesterday = new Date(Date.now() - 86400000).toDateString();

    const groups = { Today: [], Yesterday: [], Older: [] };

    history.forEach(item => {
        const date = new Date(item.timestamp).toDateString();
        if (date === today) groups.Today.push(item);
        else if (date === yesterday) groups.Yesterday.push(item);
        else groups.Older.push(item);
    });

    sidebar.innerHTML = '';
    for (const [label, items] of Object.entries(groups)) {
        if (items.length === 0) continue;

        const heading = document.createElement('h3');
        heading.textContent = `📅 ${label}`;
        sidebar.appendChild(heading);

        items.slice(-5).reverse().forEach(item => {
            const div = document.createElement('div');
            div.className = 'hist-item';
            div.textContent = item.isUser ? `You: ${item.text}` : `Jarvis: ${item.text}`;
            sidebar.appendChild(div);
        });
    }
}

/* =============================================
   2. TYPING INDICATOR
   ============================================= */
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing-indicator';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `<span>Jarvis:</span> <div class="dot"></div><div class="dot"></div><div class="dot"></div>`;
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTypingIndicator() {
    const typingDiv = document.getElementById('typing-indicator');
    if (typingDiv) typingDiv.remove();
}

/* =============================================
   3. SEND QUERY TO BACKEND & TTS
   ============================================= */
async function sendQuery(query) {
    if (!query.trim()) return;
    addMessage(query, true);
    userInput.value = '';

    showTypingIndicator();

    try {
        const response = await fetch('/api/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        const data = await response.json();

        hideTypingIndicator();

        if (data.error) {
            addMessage('Error: ' + data.error);
            return;
        }
        if (data.reply) {
            addMessage(data.reply);
            // 👇 This will check if Speaker is ON before speaking
            speakText(data.reply);
        }
        if (data.action === 'open_url' && data.data) {
            window.open(data.data, '_blank');
        } else if (data.action === 'shutdown') {
            alert('Shutting down system... (demo)');
        } else if (data.action === 'quit') {
            setTimeout(() => window.close(), 2000);
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('Network error: ' + error.message);
    }
}

/* =============================================
   4. TEXT TO SPEECH (CHECKS IF SPEAKER IS ON)
   ============================================= */
function speakText(text) {
    // 👇 CRITICAL: If user turned the speaker OFF, do not speak.
    if (!isSpeakerOn) {
        console.log("Speaker is OFF. Silent mode active.");
        return;
    }

    if (!window.speechSynthesis) {
        console.warn("Speech synthesis not supported");
        return;
    }
    window.speechSynthesis.cancel();

    muteBtn.classList.remove('muted');
    muteBtn.classList.add('speaking');
    muteBtn.textContent = '🔊';

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.lang = 'en-US';

    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.lang.includes('en') && v.name.includes('Female'));
    if (preferredVoice) utterance.voice = preferredVoice;

    if (voices.length === 0) {
        window.speechSynthesis.onvoiceschanged = () => {
            const newVoices = window.speechSynthesis.getVoices();
            const betterVoice = newVoices.find(v => v.lang.includes('en'));
            if (betterVoice) utterance.voice = betterVoice;
            window.speechSynthesis.speak(utterance);
        };
        return;
    }

    utterance.onend = () => {
        muteBtn.classList.remove('speaking');
        // 👇 Keep the icon correct based on whether it's ON or OFF
        muteBtn.textContent = isSpeakerOn ? '🔊' : '🔇';
    };

    window.speechSynthesis.speak(utterance);
}

// Enable Speech after first click (Browser requirement)
let speechEnabled = false;
document.addEventListener('click', () => {
    if (!speechEnabled) {
        speechEnabled = true;
        const dummy = new SpeechSynthesisUtterance(' ');
        speechSynthesis.speak(dummy);
        setTimeout(() => speechSynthesis.cancel(), 100);
    }
});

/* =============================================
   5. EVENT LISTENERS
   ============================================= */
sendBtn.addEventListener('click', () => sendQuery(userInput.value));
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendQuery(userInput.value);
});

clearBtn.addEventListener('click', () => {
    chatBox.innerHTML = '';
    localStorage.removeItem('jarvisHistory');
    renderSidebarHistory();
    addMessage('🧹 Chat and history cleared.');
});

themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-theme');
    themeBtn.textContent = document.body.classList.contains('light-theme') ? '☀️' : '🌙';
});

settingsBtn.addEventListener('click', () => {
    alert('⚙️ Settings\n\n' +
        '1. Mic: Always ON\n' +
        '2. Wake word: "Jarvis"\n' +
        '3. AI Provider: Groq\n' +
        '4. Volume: 80%\n\n' +
        'More settings coming soon...');
});

/* =============================================
   6. SPEAKER TOGGLE (ON/OFF SWITCH)
   ============================================= */
muteBtn.addEventListener('click', () => {
    // Toggle the state (If it was true, becomes false. If false, becomes true)
    isSpeakerOn = !isSpeakerOn;

    if (isSpeakerOn) {
        // --- TURNED ON ---
        muteBtn.classList.remove('muted');
        muteBtn.classList.remove('speaking');
        muteBtn.textContent = '🔊';
        muteBtn.title = "Speaker is ON";
    } else {
        // --- TURNED OFF (MUTED) ---
        window.speechSynthesis.cancel(); // Stop Jarvis immediately if talking
        muteBtn.classList.remove('speaking');
        muteBtn.classList.add('muted');
        muteBtn.textContent = '🔇';
        muteBtn.title = "Speaker is OFF";
    }
});

/* =============================================
   7. CONTINUOUS MIC – WAKE WORD "JARVIS"
   ============================================= */
let recognition = null;
let isListening = false;

function startContinuousListening() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        addMessage('❌ Your browser does not support speech recognition. Please use Chrome or Edge.');
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    updateMicStatus(true);

    recognition.onresult = (event) => {
        const last = event.results.length - 1;
        const transcript = event.results[last][0].transcript.trim().toLowerCase();
        console.log('Heard:', transcript);

        if (transcript.startsWith('jarvis')) {
            let command = transcript.replace(/^jarvis\s*/, '').trim();
            if (command) {
                addMessage(`🎤 (voice) ${command}`, true);
                sendQuery(command);
            }
        }
    };

    recognition.onerror = (event) => {
        console.warn('Recognition error:', event.error);
        if (event.error === 'not-allowed') {
            addMessage('❌ Microphone access denied. Please allow microphone in browser settings.');
            updateMicStatus(false);
            return;
        }
        restartRecognition();
    };

    recognition.onend = () => {
        if (isListening) {
            restartRecognition();
        }
    };

    recognition.start();
    isListening = true;
}

function restartRecognition() {
    if (recognition) {
        try { recognition.stop(); } catch (e) {}
    }
    setTimeout(() => {
        if (isListening) {
            startContinuousListening();
        }
    }, 500);
}

function stopListening() {
    isListening = false;
    if (recognition) {
        try { recognition.stop(); } catch (e) {}
        recognition = null;
    }
    updateMicStatus(false);
}

function updateMicStatus(active) {
    if (micBtn) {
        micBtn.textContent = active ? '🎤' : '⏹';
        micBtn.style.background = active ? '#4CAF50' : '#444';
        micBtn.title = active ? 'Microphone is listening' : 'Microphone is off';
    }
    if (statusIndicator) {
        statusIndicator.textContent = active ? '🔴 Listening...' : '⏸️ Mic off';
        statusIndicator.style.color = active ? '#4CAF50' : '#888';
    }
}

micBtn.addEventListener('click', () => {
    if (isListening) {
        stopListening();
        addMessage('⏹️ Microphone stopped.', false);
    } else {
        startContinuousListening();
        addMessage('🎤 Microphone started. Say "Jarvis" followed by your command.', false);
    }
});

/* =============================================
   8. PAGE LOAD & GREETING
   ============================================= */
window.addEventListener('load', () => {
    renderSidebarHistory();

    setTimeout(() => {
        startContinuousListening();
        addMessage('🎤 Microphone is active. Say "Jarvis" followed by your command.', false);
    }, 1000);
});

fetch('/api/greeting')
    .then(res => res.json())
    .then(data => {
        if (data.greeting) {
            addMessage(data.greeting);
            setTimeout(() => speakText(data.greeting), 300);
        }
    })
    .catch(() => {});