
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let isSending = false;
let sendButton = document.getElementById('send-button');

function sendMessage() {
    if (isSending) return;
    isSending = true;
    const formData = new FormData();
    const imageInput = document.getElementById('image');
    formData.append('image', imageInput.files[0]);

    if (formData) {
        let chatBox = document.querySelector('.chat-box');
        let userMessage = document.createElement('div');
        sendButton.disabled = true;
        //user message
        let imgInput = document.getElementById('image');
        let imgFiles = imgInput.files[0];
        if(imgFiles){
            let img = document.createElement('img');
            img.src = URL.createObjectURL(imgFiles);
            img.alt = '用户上传图片';
            img.style.maxWidth = '100%';
            img.style.borderRadius = '15px';
            userMessage.appendChild(img);
        }
        chatBox.appendChild(userMessage);
        // loading
        let loadingMessage = document.createElement('div');
        loadingMessage.classList.add('message', 'bot-message');
        loadingMessage.innerText = '正在生成回复,请等一下~';
        chatBox.appendChild(loadingMessage);
        //formData
        fetch('/chat/', {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrftoken
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            loadingMessage.innerText = '';
            let botMessage = document.createElement('div');
            botMessage.classList.add('message', 'bot-message');
            botMessage.innerText = data.response;
            loadingMessage.replaceWith(botMessage);
        })
        .catch(error => {
            console.error('Error:', error);
            loadingMessage.innerText = '出错了，请稍后重试';
        })
        .finally(() => {
            sendButton.disabled = false;
            isSending = false;
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    }
    else{
        isSending = false;
    }
}
document.getElementById('send-button').addEventListener('click', sendMessage);
