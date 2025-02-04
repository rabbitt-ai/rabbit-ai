from flask import Flask, request, jsonify, render_template_string
from model import BERTChatbot
import traceback

app = Flask(__name__)
chatbot = None

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chatbot</title>
    <style>
        body { max-width: 800px; margin: auto; padding: 20px; font-family: Arial; }
        #chatbox { height: 300px; border: 1px solid #ddd; margin: 20px 0; padding: 10px; overflow-y: auto; }
        #userInput { width: 80%; padding: 10px; }
        button { padding: 10px 20px; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>BERT Chatbot</h1>
    <div id="chatbox"></div>
    <input type="text" id="userInput" placeholder="Mesajınızı yazın...">
    <button onclick="sendMessage()">Gönder</button>

    <script>
        function sendMessage() {
            var userInput = document.getElementById('userInput');
            var message = userInput.value;
            if (message.trim() === '') return;

            // Kullanıcı mesajını göster
            var chatbox = document.getElementById('chatbox');
            chatbox.innerHTML += '<p><strong>Siz:</strong> ' + message + '</p>';
            userInput.value = '';

            // API'ye istek gönder
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                let messageClass = data.error ? 'error' : '';
                chatbox.innerHTML += '<p class="' + messageClass + '"><strong>Bot:</strong> ' + data.response + '</p>';
                chatbox.scrollTop = chatbox.scrollHeight;
            })
            .catch(error => {
                chatbox.innerHTML += '<p class="error"><strong>Hata:</strong> Bir iletişim hatası oluştu.</p>';
                chatbox.scrollTop = chatbox.scrollHeight;
            });
        }

        // Enter tuşu ile gönderme
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

def initialize_chatbot():
    global chatbot
    try:
        if chatbot is None:
            chatbot = BERTChatbot()
        return True
    except Exception as e:
        print(f"Chatbot başlatılırken hata oluştu: {str(e)}")
        return False

@app.route('/')
def home():
    if not initialize_chatbot():
        return "Chatbot başlatılamadı. Lütfen konsol hatalarını kontrol edin.", 500
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    if not initialize_chatbot():
        return jsonify({
            'error': True,
            'response': 'Chatbot başlatılamadı. Lütfen sayfayı yenileyin.'
        }), 500

    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({
                'error': True,
                'response': 'Lütfen bir mesaj yazın.'
            })
        
        response = chatbot.process_message(user_message)
        return jsonify({
            'error': False,
            'response': response
        })
    except Exception as e:
        traceback.print_exc()  # Konsola detaylı hata bas
        return jsonify({
            'error': True,
            'response': f'Bir hata oluştu: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')