const chatEl = document.getElementById("chat");
const inputEl = document.getElementById("input");
const sendBtn = document.getElementById("send");

const messages = [];

function renderMessage(role, content) {
  const container = document.createElement("div");
  container.className = `message ${role}`;

  const roleEl = document.createElement("div");
  roleEl.className = "role";
  roleEl.textContent = role;

  const contentEl = document.createElement("div");
  contentEl.className = "content";
  contentEl.textContent = content;

  container.appendChild(roleEl);
  container.appendChild(contentEl);
  chatEl.appendChild(container);
  chatEl.scrollTop = chatEl.scrollHeight;

  return contentEl;
}

function setBusy(isBusy) {
  sendBtn.disabled = isBusy;
  inputEl.disabled = isBusy;
}

async function streamChat() {
  const userText = inputEl.value.trim();
  if (!userText) return;

  inputEl.value = "";
  messages.push({ role: "user", content: userText });
  renderMessage("user", userText);

  const assistantContentEl = renderMessage("assistant", "");
  messages.push({ role: "assistant", content: "" });

  setBusy(true);

  try {
    const response = await fetch("/api/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages }),
    });

    if (!response.ok || !response.body) {
      throw new Error(`Request failed: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let assistantText = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.startsWith("data:")) continue;
        const payload = line.replace("data:", "").trim();

        if (payload === "[DONE]") {
          messages[messages.length - 1].content = assistantText;
          return;
        }

        if (payload.startsWith("[ERROR]")) {
          assistantContentEl.textContent = payload;
          return;
        }

        assistantText += payload;
        assistantContentEl.textContent = assistantText;
      }
    }
  } catch (err) {
    assistantContentEl.textContent = `Error: ${err.message}`;
  } finally {
    setBusy(false);
  }
}

sendBtn.addEventListener("click", streamChat);
inputEl.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    streamChat();
  }
});
