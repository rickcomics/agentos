const API_URL = "https://your-api-domain.com";
const API_KEY = "your-api-key";

async function loadStatus() {
    const res = await fetch(`${API_URL}/status`, {
        headers: { "Authorization": `Bearer ${API_KEY}` }
    });

    const data = await res.json();
    document.getElementById("system-status").innerText =
        `Система: ${data.system}, агенты: ${data.agents}`;
}

async function sendRequest() {
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    const res = await fetch(`${API_URL}/data/new`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${API_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, message })
    });

    document.getElementById("response").innerText = "Заявка отправлена!";
}

loadStatus();
