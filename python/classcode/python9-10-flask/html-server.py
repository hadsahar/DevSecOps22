import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.get('/')
def home():
    return 'welcome'


@app.get('/yabadabadooo')
def yabadabadooo():
    return f"date time {datetime.datetime.now()}"


@app.get('/home')
def homehtml():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My First Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: red;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
        }
        button {
            padding: 10px 20px;
            border: none;
            background-color: #007BFF;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

    <h1>Welcome to My Website</h1>
    <p>This is a simple HTML page.</p>
    
    <button onclick="showMessage()">Click Me</button>

    <script>
        function showMessage() {
            alert("Hello! You clicked the button.");
        }
    </script>

</body>
</html>
'''


@app.get('/html')
def html():
    return render_template("code.html")




app.run(port=5005)
