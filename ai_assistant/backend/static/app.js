// Initialize Web Speech API
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';

let isListening = false;

async function sendMessage()
{
    const input = document.getElementById("userInput");
    const message = input.value.trim();

    if(!message) return;

    addMessage(message,"user");
    input.value = "";

    try{
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({message: message})
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        addMessage(data.response, "assistant");
        
        // Speak the response
        speak(data.response);
    } catch(error){
        console.error("Error:", error);
        addMessage("Error: " + error.message, "error");
    }
}

function addMessage(text, sender)
{
    const messagesDiv = document.getElementById("messages");
    const msgDiv = document.createElement("div");

    if (sender === "user") {
        msgDiv.className = "message-user flex justify-end";
        msgDiv.innerHTML = `<div class="bg-blue-600 text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-xs shadow-lg">${text}</div>`;
    } else if (sender === "assistant") {
        msgDiv.className = "message-assistant flex justify-start";
        msgDiv.innerHTML = `<div class="bg-slate-700 text-gray-100 rounded-2xl rounded-tl-none px-4 py-3 max-w-xs shadow-lg">${text}</div>`;
    } else if (sender === "error") {
        msgDiv.className = "message-assistant flex justify-start";
        msgDiv.innerHTML = `<div class="bg-red-900 text-red-100 rounded-2xl rounded-tl-none px-4 py-3 max-w-xs shadow-lg">${text}</div>`;
    }
    
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Text-to-Speech
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;
    speechSynthesis.speak(utterance);
}

// Voice Input (Microphone)
function startListening() {
    console.log("startListening called");
    if (!isListening) {
        isListening = true;
        document.getElementById("voiceBtn").style.background = "red";
        document.getElementById("voiceBtn").textContent = "🔴 Listening...";
        console.log("Starting recognition...");
        recognition.start();
    } else {
        console.log("Already listening");
    }
}

recognition.onstart = () => {
    console.log("Recognition started");
};

recognition.onresult = (event) => {
    console.log("Got result:", event.results);
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
    }
    
    console.log("Final transcript:", transcript);
    document.getElementById("userInput").value = transcript;
};

recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    alert("Mic Error: " + event.error);
};

recognition.onend = () => {
    console.log("Recognition ended");
    isListening = false;
    document.getElementById("voiceBtn").style.background = "";
    document.getElementById("voiceBtn").textContent = "🎤";
};

// Button Events
document.getElementById("sendBtn").onclick = sendMessage;
document.getElementById("voiceBtn").onclick = startListening;
document.getElementById("stopBtn").onclick = () => {
    speechSynthesis.cancel();
    console.log("Speech stopped");
};
document.getElementById("userInput").onkeypress = (e) => {
    if (e.key === "Enter") sendMessage();
};