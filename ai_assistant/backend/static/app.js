// frontend logic

const API_URL = "https://probable-invention-69wrpv5q7wq2xx4-8000.app.github.dev/";

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
    } catch(error){
        console.error("Error:", error);
        addMessage("Error: " + error.message, "error");
    }
}

function addMessage(text, sender)
{
    const messagesDiv = document.getElementById("messages");
    const msgDiv = document.createElement("div");

    let bgColor = "bg-blue-600";
    if (sender === "assistant") bgColor = "bg-gray-700";
    if (sender === "error") bgColor = "bg-red-600";

    msgDiv.className = `text-right`;
    msgDiv.innerHTML = `<span class="inline-block p-3 rounded ${bgColor}">${text}</span>`;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

}

document.getElementById("sendBtn").onclick = sendMessage;
document.getElementById("userInput").onkeypress = (e) => {
    if (e.key === "Enter") sendMessage();
};