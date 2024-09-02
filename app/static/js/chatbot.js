const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotContainer = document.getElementById('chatbot-container');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotMessages = document.getElementById('chatbot-messages');
const chatbotInput = document.querySelector('#chatbot-input input');
const chatbotSend = document.querySelector('#chatbot-input button');

chatbotToggle.addEventListener('click', () => {
    chatbotContainer.style.display = 'flex';
    chatbotToggle.style.display = 'none';
});

chatbotClose.addEventListener('click', () => {
    chatbotContainer.style.display = 'none';
    chatbotToggle.style.display = 'block';
});

function showTypingIndicator() {
    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('typing-indicator');
    typingIndicator.innerHTML = '<span></span><span></span><span></span>';
    chatbotMessages.appendChild(typingIndicator);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    return typingIndicator;
}

function removeTypingIndicator(indicator) {
    if (indicator && indicator.parentNode === chatbotMessages) {
        chatbotMessages.removeChild(indicator);
    }
}

function addMessage(sender, message, isStreaming = false) {
    let messageElement = chatbotMessages.querySelector(`.${sender.toLowerCase()}-message:last-child`);
    
    if (!isStreaming || !messageElement) {
        messageElement = document.createElement('div');
        messageElement.className = `chat-message ${sender.toLowerCase()}-message`;
        messageElement.innerHTML = `<strong>${sender}:</strong> <span>${message}</span>`;
        chatbotMessages.appendChild(messageElement);
    } else {
        messageElement.querySelector('span').textContent = message;
    }
    
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    return messageElement;
}

async function sendMessage(message = null, diseaseContext = '') {
    if (!message) {
        message = chatbotInput.value.trim();
        chatbotInput.value = '';
    }

    if (message === '') return;

    addMessage('You', message);
    const typingIndicator = showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, disease_context: diseaseContext }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let aiResponse = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value);
            aiResponse += chunk;
            addMessage('AI', aiResponse, true);
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('AI', 'Sorry, there was an error processing your request.');
    } finally {
        removeTypingIndicator(typingIndicator);
    }
}

chatbotSend.addEventListener('click', () => sendMessage());
chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function initializeChatbot(diseaseContext = '') {
    sendMessage(`Tell me about ${diseaseContext || 'plant health'} in general.`, diseaseContext);
}
