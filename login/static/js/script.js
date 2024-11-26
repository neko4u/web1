
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let isSending = false;
let sendButton = document.getElementById('send-button');

function sendMessage() {
    if (isSending) return;
    isSending = true;
    let inputField = document.getElementById('user-input');
    let message = inputField.value.trim();

    if (message) {
        let chatBox = document.querySelector('.chat-box');
        inputField.disabled = true;
        sendButton.disabled = true;
        //user message
        let userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.innerText = message;
        chatBox.appendChild(userMessage);
        // loading
        let loadingMessage = document.createElement('div');
        loadingMessage.classList.add('message', 'bot-message');
        loadingMessage.innerText = '正在生成回复,请等一下~';
        chatBox.appendChild(loadingMessage);

        fetch('/index/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 
                message: message
            }),
        })
        .then(response => response.json())
        .then(data => {
            loadingMessage.innerText = '';
            let botMessage = document.createElement('div');
            botMessage.classList.add('message', 'bot-message');
            botMessage.innerText = data.response;
            // chatBox.appendChild(botMessage);
            loadingMessage.replaceWith(botMessage)
        })
        .catch(error => {
            console.error('Error:', error);
            loadingMessage.innerText = '出错了，请稍后重试';
        })
        .finally(() => {
            inputField.disabled = false;
            sendButton.disabled = false;
            isSending = false;
            chatBox.scrollTop = chatBox.scrollHeight;
        });
        inputField.value = '';
        inputField.focus();
    }
    else{
        isSending = false;
    }
}

document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !isSending) {
        event.preventDefault();
        sendMessage();
    }
});

document.getElementById('send-button').addEventListener('click', sendMessage);
