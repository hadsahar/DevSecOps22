---
layout: default
title: Python Lesson 11 - Flask Web Framework
---

# Flask Web Framework

Flask is a lightweight, micro web framework for Python. It's perfect for building REST APIs, web applications, and microservices. This lesson covers everything from basics to advanced concepts.

---

## 1. What is Flask?

Flask is a **WSGI** (Web Server Gateway Interface) micro-framework. "Micro" means it doesn't require particular tools or libraries — it keeps the core simple but extensible.

**Key Features:**

- Lightweight and modular
- Built-in development server
- RESTful request dispatching
- Jinja2 templating
- Secure cookies support
- Easy to learn and use

---

## 2. Installation

```bash
pip install flask
```

Verify installation:

```python
import flask
print(flask.__version__)
```

---

## 3. Your First Flask Application

```python
from flask import Flask

app = Flask(__name__)

@app.get('/')
def home():
    return 'Hello, World!'

app.run(port=5000, debug=True)
```

**Explanation:**

- `Flask(__name__)` — Creates the Flask application instance
- `@app.get('/')` — Decorator that binds a URL route to a function
- `app.run()` — Starts the development server

**Parameters for `app.run()`:**
| Parameter | Description |
|-----------|-------------|
| `port` | Port number (default: 5000) |
| `debug` | Enable debug mode with auto-reload |
| `host` | Host address (use `'0.0.0.0'` for external access) |

---

## 4. Routing

Routes define URL patterns that map to Python functions.

### Basic Routes

```python
@app.get('/about')
def about():
    return 'About Page'

@app.get('/contact')
def contact():
    return 'Contact Page'
```

### Dynamic Routes (URL Parameters)

```python
# String parameter
@app.get('/user/<username>')
def show_user(username):
    return f'User: {username}'

# Integer parameter
@app.get('/post/<int:post_id>')
def show_post(post_id):
    return f'Post ID: {post_id}'

# Float parameter
@app.get('/price/<float:amount>')
def show_price(amount):
    return f'Price: ${amount}'
```

**URL Converters:**
| Converter | Description |
|-----------|-------------|
| `string` | Default, accepts any text without slashes |
| `int` | Accepts positive integers |
| `float` | Accepts positive floating point values |
| `path` | Like string but also accepts slashes |
| `uuid` | Accepts UUID strings |

---

## 5. HTTP Methods

Flask supports all HTTP methods for building REST APIs.

### Method Decorators (Modern Syntax)

```python
from flask import Flask, request

app = Flask(__name__)

@app.get('/items')
def get_items():
    return {'items': ['item1', 'item2']}

@app.post('/items')
def create_item():
    return {'status': 'created'}, 201

@app.put('/items/<int:id>')
def update_item(id):
    return {'status': 'updated', 'id': id}

@app.patch('/items/<int:id>')
def patch_item(id):
    return {'status': 'patched', 'id': id}

@app.delete('/items/<int:id>')
def delete_item(id):
    return {'status': 'deleted', 'id': id}
```

### Traditional Syntax (Using `methods` Parameter)

```python
@app.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        return {'items': []}
    elif request.method == 'POST':
        return {'status': 'created'}, 201
```

---

## 6. The Request Object

The `request` object contains all data sent by the client.

```python
from flask import Flask, request

app = Flask(__name__)

@app.post('/login')
def login():
    # JSON data
    data = request.get_json()

    # Form data
    username = request.form.get('username')

    # Query parameters (?key=value)
    page = request.args.get('page', default=1, type=int)

    # Headers
    auth_header = request.headers.get('Authorization')

    # Request method
    method = request.method

    # Full URL
    url = request.url

    # Client IP
    ip = request.remote_addr

    return {'status': 'ok'}
```

**Common `request` Attributes:**
| Attribute | Description |
|-----------|-------------|
| `request.method` | HTTP method (GET, POST, etc.) |
| `request.args` | Query string parameters |
| `request.form` | Form data |
| `request.json` | Parsed JSON data |
| `request.get_json()` | Method to get JSON data |
| `request.headers` | Request headers |
| `request.cookies` | Request cookies |
| `request.files` | Uploaded files |
| `request.url` | Full request URL |
| `request.path` | URL path without query string |

---

## 7. Response and Status Codes

### Returning Responses

```python
# Return string
@app.get('/text')
def text_response():
    return 'Plain text'

# Return dict (auto-converted to JSON)
@app.get('/json')
def json_response():
    return {'key': 'value'}

# Return list (auto-converted to JSON)
@app.get('/list')
def list_response():
    return [1, 2, 3]

# Return with status code
@app.post('/create')
def create_response():
    return {'status': 'created'}, 201

# Return with headers
@app.get('/custom')
def custom_response():
    return {'data': 'value'}, 200, {'X-Custom-Header': 'MyValue'}
```

### Common HTTP Status Codes

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 200  | OK - Success                           |
| 201  | Created - Resource created             |
| 204  | No Content - Success with no body      |
| 400  | Bad Request - Invalid input            |
| 401  | Unauthorized - Authentication required |
| 403  | Forbidden - Access denied              |
| 404  | Not Found - Resource doesn't exist     |
| 500  | Internal Server Error                  |

---

## 8. Building a Complete REST API

Here's a full CRUD example for managing users:

```python
from flask import Flask, request

app = Flask(__name__)

# In-memory database
users = [
    {'id': 1, 'username': 'alice', 'email': 'alice@example.com'},
    {'id': 2, 'username': 'bob', 'email': 'bob@example.com'},
]

# Helper function
def find_user(id):
    for user in users:
        if user['id'] == id:
            return user
    return None

# GET all users
@app.get('/users')
def get_users():
    return users

# GET user by ID
@app.get('/users/<int:id>')
def get_user(id):
    user = find_user(id)
    if user:
        return user
    return {'error': 'User not found'}, 404

# POST - Create new user
@app.post('/users')
def create_user():
    data = request.get_json()

    # Validation
    if not data or 'username' not in data or 'email' not in data:
        return {'error': 'Missing required fields'}, 400

    # Create new user
    new_id = max(u['id'] for u in users) + 1 if users else 1
    new_user = {
        'id': new_id,
        'username': data['username'],
        'email': data['email']
    }
    users.append(new_user)
    return new_user, 201

# PUT - Replace entire user
@app.put('/users/<int:id>')
def update_user(id):
    data = request.get_json()

    if not data or 'username' not in data or 'email' not in data:
        return {'error': 'Missing required fields'}, 400

    for i, user in enumerate(users):
        if user['id'] == id:
            users[i] = {
                'id': id,
                'username': data['username'],
                'email': data['email']
            }
            return users[i]
    return {'error': 'User not found'}, 404

# PATCH - Partial update
@app.patch('/users/<int:id>')
def patch_user(id):
    data = request.get_json()
    user = find_user(id)

    if not user:
        return {'error': 'User not found'}, 404

    # Update only provided fields
    for key, value in data.items():
        if key != 'id':  # Prevent ID modification
            user[key] = value

    return user

# DELETE - Remove user
@app.delete('/users/<int:id>')
def delete_user(id):
    user = find_user(id)
    if user:
        users.remove(user)
        return {'message': f'User {id} deleted'}
    return {'error': 'User not found'}, 404

# DELETE all users
@app.delete('/users')
def delete_all_users():
    users.clear()
    return {'message': 'All users deleted'}


app.run(port=5000, debug=True)
```

---

## 9. Before and After Request Hooks

Execute code before or after each request.

```python
from flask import Flask, request, g
import datetime

app = Flask(__name__)

@app.before_request
def before_request_func():
    # Runs before every request
    g.start_time = datetime.datetime.now()
    print(f'[{g.start_time}] {request.method} {request.path}')

@app.after_request
def after_request_func(response):
    # Runs after every request (must return response)
    duration = datetime.datetime.now() - g.start_time
    print(f'Request completed in {duration.total_seconds():.3f}s')
    return response

@app.teardown_request
def teardown_request_func(exception):
    # Runs after request, even if an exception occurred
    # Good for cleanup (closing DB connections, etc.)
    pass

@app.get('/')
def home():
    return 'Hello!'

app.run(port=5000, debug=True)
```

**The `g` Object:**

- `g` is a global namespace for storing data during a request
- Data stored in `g` is available throughout the request lifecycle
- Automatically cleared after each request

---

## 10. Error Handling

### Custom Error Handlers

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Resource not found'}, 404

@app.errorhandler(500)
def server_error(error):
    return {'error': 'Internal server error'}, 500

@app.errorhandler(400)
def bad_request(error):
    return {'error': 'Bad request'}, 400
```

### Using `abort()`

```python
from flask import Flask, abort

app = Flask(__name__)

@app.get('/users/<int:id>')
def get_user(id):
    user = find_user(id)
    if not user:
        abort(404)  # Triggers 404 error handler
    return user
```

---

## 11. HTML Templates with Jinja2

Flask uses Jinja2 for templating. Templates must be in a `templates/` folder.

### Project Structure

```
my_app/
├── app.py
├── templates/
│   ├── base.html
│   ├── home.html
│   └── users.html
└── static/
    ├── css/
    └── js/
```

### Rendering Templates

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def home():
    return render_template('home.html', title='Home Page')

@app.get('/users')
def users():
    user_list = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25}
    ]
    return render_template('users.html', users=user_list)
```

### Template Example (home.html)

```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ title }}</title>
  </head>
  <body>
    <h1>Welcome to {{ title }}</h1>

    {% if users %}
    <ul>
      {% for user in users %}
      <li>{{ user.name }} - Age: {{ user.age }}</li>
      {% endfor %}
    </ul>
    {% else %}
    <p>No users found.</p>
    {% endif %}
  </body>
</html>
```

### Jinja2 Syntax Summary

| Syntax                                 | Purpose                      |
| -------------------------------------- | ---------------------------- |
| `{{ variable }}`                       | Output a variable            |
| `{% raw %}{% statement %}{% endraw %}` | Control flow (if, for, etc.) |
| `{# comment #}`                        | Comments                     |
| `{{ variable\|filter }}`               | Apply filters                |

**Common Filters:**

- `{{ name|upper }}` — Uppercase
- `{{ name|lower }}` — Lowercase
- `{{ name|title }}` — Title Case
- `{{ list|length }}` — List length
- `{{ text|safe }}` — Render HTML

---

## 12. Serving Static Files

Static files (CSS, JS, images) go in the `static/` folder.

### In Templates

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" />
```

---

## 13. Returning HTML Directly

For simple cases, return HTML strings directly:

```python
@app.get('/inline')
def inline_html():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inline HTML</title>
        <style>
            body { font-family: Arial; text-align: center; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Hello from Flask!</h1>
        <p>This is inline HTML.</p>
    </body>
    </html>
    '''
```

---

## 14. Query Parameters

Access URL query parameters with `request.args`:

```python
# URL: /search?q=python&page=2&limit=10
@app.get('/search')
def search():
    query = request.args.get('q', default='', type=str)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    return {
        'query': query,
        'page': page,
        'limit': limit
    }
```

---

## 15. JSON Responses with `jsonify`

While Flask auto-converts dicts to JSON, `jsonify` gives more control:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.get('/data')
def get_data():
    return jsonify(
        status='success',
        data={'id': 1, 'name': 'Test'},
        count=1
    )
```

---

## 16. Redirects

```python
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.get('/old-page')
def old_page():
    return redirect('/new-page')

@app.get('/new-page')
def new_page():
    return 'This is the new page!'

# Using url_for (recommended)
@app.get('/go-home')
def go_home():
    return redirect(url_for('home'))  # 'home' is the function name
```

---

## 17. Blueprints (Organizing Large Apps)

Blueprints help organize code into modules.

### users_bp.py

```python
from flask import Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.get('/')
def get_users():
    return {'users': []}

@users_bp.get('/<int:id>')
def get_user(id):
    return {'user_id': id}
```

### app.py

```python
from flask import Flask
from users_bp import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp)

app.run(port=5000, debug=True)
```

---

## 18. Configuration

### From Object

```python
class Config:
    DEBUG = True
    SECRET_KEY = 'your-secret-key'
    DATABASE_URI = 'sqlite:///app.db'

app.config.from_object(Config)
```

### From Environment Variables

```python
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-key')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'
```

### Accessing Config

```python
secret = app.config['SECRET_KEY']
```

---

## 19. CORS (Cross-Origin Resource Sharing)

For APIs accessed from different domains:

```bash
pip install flask-cors
```

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Or for specific routes
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

## 20. Testing Flask APIs

### Using curl

```bash
# GET request
curl http://localhost:5000/users

# POST request with JSON
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com"}'

# PUT request
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username": "john_updated", "email": "john@example.com"}'

# PATCH request
curl -X PATCH http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}'

# DELETE request
curl -X DELETE http://localhost:5000/users/1
```

### Using Python requests

```python
import requests

# GET
response = requests.get('http://localhost:5000/users')
print(response.json())

# POST
response = requests.post(
    'http://localhost:5000/users',
    json={'username': 'john', 'email': 'john@example.com'}
)
print(response.status_code, response.json())
```

---

## 21. Best Practices

1. **Use Environment Variables** for sensitive data (API keys, secrets)
2. **Never run with `debug=True` in production**
3. **Use Blueprints** to organize large applications
4. **Validate all input** from requests
5. **Return proper status codes** for different scenarios
6. **Use a production WSGI server** (Gunicorn, uWSGI) not `app.run()`
7. **Implement proper error handling**
8. **Use HTTPS in production**

---

## 22. Quick Reference

### Route Decorators

```python
@app.get('/path')      # GET request
@app.post('/path')     # POST request
@app.put('/path')      # PUT request
@app.patch('/path')    # PATCH request
@app.delete('/path')   # DELETE request
@app.route('/path', methods=['GET', 'POST'])  # Multiple methods
```

### Request Data

```python
request.get_json()     # JSON body
request.form           # Form data
request.args           # Query parameters
request.headers        # HTTP headers
request.method         # HTTP method
request.path           # URL path
```

### Response Patterns

```python
return 'text'                          # Plain text
return {'key': 'value'}                # JSON (dict)
return [1, 2, 3]                       # JSON (list)
return data, 201                       # With status code
return data, 201, {'Header': 'Value'}  # With headers
```

---

## Summary

Flask provides a simple yet powerful foundation for web development in Python. Key concepts covered:

- **Routing** — Map URLs to functions
- **HTTP Methods** — GET, POST, PUT, PATCH, DELETE
- **Request Handling** — JSON, forms, query params
- **Responses** — JSON, HTML, status codes
- **Hooks** — before_request, after_request
- **Templates** — Jinja2 for HTML rendering
- **Error Handling** — Custom error handlers
- **Blueprints** — Code organization

Flask's minimalist design makes it ideal for APIs and microservices, while its extensibility supports complex applications when needed.
