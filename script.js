// script.js

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    
    fetch('http://your-backend-url/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Symptoms: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the backend
        displayBotMessage(data.Disease, data.Treatment, data.Procedure, data.Precautions);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function displayBotMessage(disease, treatment, procedure, precautions) {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `
        <div class="bot-message">
            <p>Based on your symptoms, you might have: ${disease}</p>
            <p>Recommended Ayurvedic Treatment: ${treatment}</p>
            <p>Procedure: ${procedure}</p>
            <p>Precautions: ${precautions}</p>
        </div>
    `;
}