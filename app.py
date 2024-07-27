from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import os

# Initialize the Flask application
app = Flask(__name__)

# Set your API key directly
API_KEY = "AIzaSyAUHtY0Ni_8-XwN4afkWSeV5G0h0YWqpVY"
os.environ["GOOGLE_API_KEY"] = API_KEY

# Configure the API key
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Generator</title>
    <style>
        /* Basic Reset */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            width: 100%;
            max-width: 600px;
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
            font-size: 24px;
            color: #333;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            font-size: 16px;
            color: #333;
            display: block;
            margin-bottom: 10px;
        }
        textarea {
            width: calc(100% - 22px);
            height: 100px;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
            resize: vertical;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #218838;
        }
        #result {
            display: none;
        }
        h2 {
            margin-top: 20px;
            font-size: 20px;
            color: #333;
        }
        p#text {
            font-size: 18px;
            color: #555;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Text Generator</h1>
        <form id="text-form">
            <label for="prompt">Enter your prompt or question:</label>
            <textarea id="prompt" name="prompt" required></textarea>
            <button type="submit">Generate Text</button>
        </form>
        <div id="result">
            <h2>Generated Text:</h2>
            <p id="text"></p>
        </div>
    </div>
    <script>
        document.getElementById('text-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const prompt = document.getElementById('prompt').value;

            fetch('/generate_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.text) {
                    document.getElementById('text').innerText = data.text;
                    document.getElementById('result').style.display = 'block';
                } else {
                    throw new Error('No text received');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('text').innerText = 'An error occurred. Please try again.';
                document.getElementById('result').style.display = 'block';
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt')
    try:
        # Generating content
        response = model.generate_content(prompt)
        print("Full response:", response)  # Debug: print full response

        if response and response.parts:
            # Check if the response contains valid content
            text_content = response.parts[0].text if response.parts else 'No text found'
        else:
            text_content = 'No valid response received'
        return jsonify({'text': text_content})
    except Exception as e:
        print(f"Error generating text: {e}")
        return jsonify({'text': 'An error occurred while generating text. Please try again.'}), 500

if __name__ == "__main__":
    app.run(debug=True)
