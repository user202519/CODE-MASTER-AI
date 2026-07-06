// ================================
// CodeMaster AI - FINAL SCRIPT
// ================================

const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const loading = document.getElementById("loading");
const historyBox = document.getElementById("chat-history");
const newChatBtn = document.getElementById("new-chat-btn");

let sessionId = null;


// ================================
// SCROLL TO BOTTOM
// ================================
function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}


// ================================
// ESCAPE HTML
// ================================
function escapeHTML(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}


// ================================
// ADD MESSAGE
// ================================
function addMessage(message, sender) {

    const div = document.createElement("div");
    div.className = sender + "-message";

    if (sender === "bot" && typeof marked !== "undefined") {
        div.innerHTML = marked.parse(message);
    } else {
        div.innerHTML = escapeHTML(message);
    }

    chatBox.appendChild(div);

    // highlight code if available
    if (typeof hljs !== "undefined") {
        document.querySelectorAll("pre code").forEach(block => {
            hljs.highlightElement(block);
        });
    }

    scrollToBottom();
}


// ================================
// SEND MESSAGE
// ================================
async function sendMessage() {

    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    loading.style.display = "block";

    try {

        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        const data = await res.json();

        sessionId = data.session_id;
        addMessage(data.reply, "bot");

        loadSessions();

    } catch (err) {
        addMessage("❌ Error: " + err.message, "bot");
    }

    loading.style.display = "none";
}


// ================================
// LOAD SESSIONS (WITH DELETE)
// ================================
async function loadSessions() {

    try {

        const res = await fetch("/sessions");
        const sessions = await res.json();

        historyBox.innerHTML = "";

        if (!sessions || sessions.length === 0) {
            historyBox.innerHTML = "<p>No chats yet</p>";
            return;
        }

        sessions.forEach(chat => {

            const item = document.createElement("div");
            item.className = "history-item";

            const title = document.createElement("div");
            title.className = "history-title";
            title.innerText = chat.title;

            title.onclick = () => loadConversation(chat.session_id);

            const del = document.createElement("button");
            del.className = "delete-btn";
            del.innerHTML = "🗑";

            del.onclick = async (e) => {
                e.stopPropagation();
                await fetch("/delete/" + chat.session_id, {
                    method: "DELETE"
                });

                if (sessionId === chat.session_id) {
                    sessionId = null;
                    chatBox.innerHTML = "";
                }

                loadSessions();
            };

            item.appendChild(title);
            item.appendChild(del);

            historyBox.appendChild(item);
        });

    } catch (err) {
        console.log("Session load error:", err);
    }
}


// ================================
// LOAD CONVERSATION
// ================================
async function loadConversation(id) {

    sessionId = id;
    chatBox.innerHTML = "";

    try {

        const res = await fetch("/history/" + id);
        const chats = await res.json();

        chats.forEach(c => {
            addMessage(c.user_message, "user");
            addMessage(c.bot_reply, "bot");
        });

    } catch (err) {
        console.log(err);
    }
}


// ================================
// NEW CHAT
// ================================
newChatBtn.onclick = () => {
    sessionId = null;
    chatBox.innerHTML = "";
    input.focus();
};


// ================================
// EVENTS
// ================================
sendBtn.onclick = sendMessage;

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});


// ================================
// START
// ================================
window.onload = () => {
    loadSessions();
    input.focus();
};