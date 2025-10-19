// frontend logic

const API_URL = "https://probable-invention-69wrpv5q7wq2xx4-8000.app.github.dev/";

async function sendMessage()
{
    const input = document.getElementById("userInput");
    const message = input.value.trim();

    if(! message) return;

    // show user message
    addMessage(message,"user");
    input.value = ""; // clears the input box after displaying the message

    try{
        // send to backend
        const response = await fetch(`https://probable-invention-69wrpv5q7wq2xx4-8000.app.github.dev/api/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({message: message})
        });
        const data = await response.json();
        addMessage(data.response, "assistant");
    } catch(error){
        addMessage("Error: Could not connect to backend", "error");
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