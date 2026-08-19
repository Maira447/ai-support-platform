document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const logsContainer = document.getElementById('logs-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Generate a simple conversation ID for this session
    const sessionId = 'session-' + Math.random().toString(36).substring(7);

    function getTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user' : 'system'}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = text;
        
        msgDiv.appendChild(bubble);
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function addLog(agent, message, type = "normal") {
        const logDiv = document.createElement('div');
        logDiv.className = `log-entry ${agent.toLowerCase()} ${type}`;
        
        const timeSpan = document.createElement('span');
        timeSpan.className = 'log-time';
        timeSpan.textContent = getTime();

        const badge = document.createElement('div');
        badge.className = `agent-badge ${agent.toLowerCase()}`;
        badge.textContent = agent;

        const msgSpan = document.createElement('div');
        msgSpan.className = 'log-msg';
        msgSpan.textContent = message;

        logDiv.appendChild(timeSpan);
        logDiv.appendChild(badge);
        logDiv.appendChild(msgSpan);
        
        logsContainer.appendChild(logDiv);
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        addMessage(text, true);
        userInput.value = '';
        
        // Show orchestrator thinking log
        addLog('Orchestrator', 'Analyzing intent...', 'orchestrator');

        try {
            const response = await fetch('/api/local/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Agent-Api-Key': 'local-dev-key'
                },
                body: JSON.stringify({
                    user_id: 'web-user',
                    conversation_id: sessionId,
                    message: text,
                    agent: 'orchestrator'
                })
            });

            const data = await response.json();

            if (data.success) {
                // Determine routing logic from metadata
                const routedAgent = data.metadata.original_selection || data.agent;
                
                addLog('Orchestrator', `Routed query to: [${routedAgent.toUpperCase()}] agent`);
                
                // Show tools used if any
                if (data.metadata.tools_used && data.metadata.tools_used.length > 0) {
                    const tools = [...new Set(data.metadata.tools_used)].join(', ');
                    addLog(routedAgent, `Executed tools: ${tools}`, 'tool');
                }

                // Add final response
                addMessage(data.response, false);
                addLog(routedAgent, `Generated final response.`);

            } else {
                addMessage("Sorry, an error occurred.", false);
                addLog('System', `Error: ${data.metadata?.error || 'Unknown'}`, 'system');
            }

        } catch (err) {
            addMessage("Network error. Please try again.", false);
            addLog('System', `Fetch Error: ${err.message}`, 'system');
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
