---
layout: default
title: Python Requests Library - Complete Tutorial for Automation
---

# Python Requests Library - Complete Tutorial for Automation

## Table of Contents

1. [Introduction to Requests](#1-introduction-to-requests)
2. [Installation](#2-installation)
3. [Basic Requests](#3-basic-requests)
4. [HTTP Methods](#4-http-methods)
5. [Request Parameters](#5-request-parameters)
6. [Headers](#6-headers)
7. [Authentication](#7-authentication)
8. [Sessions](#8-sessions)
9. [Handling Responses](#9-handling-responses)
10. [Error Handling](#10-error-handling)
11. [Timeouts and Retries](#11-timeouts-and-retries)
12. [Working with JSON](#12-working-with-json)
13. [File Uploads/Downloads](#13-files-uploadsdownloads)
14. [Cookies](#14-cookies)
15. [SSL/TLS Verification](#15-ssltls-verification)
16. [Proxies](#16-proxies)
17. [Async Requests](#17-async-requests)
18. [Web Scraping](#18-web-scraping)
19. [API Integration](#19-api-integration)
20. [Best Practices](#20-best-practices)
21. [Automation Examples](#21-automation-examples)

---

## 1. Introduction to Requests

### What is the Requests Library?

**Requests** is a popular Python library for making HTTP requests. It provides a simple, human-friendly API for interacting with web services and APIs.

### Why Use Requests?

| Feature | Description |
|---------|-------------|
| **Simple API** | Intuitive methods for all HTTP operations |
| **Automatic Decoding** | Handles gzip, deflate, and charset decoding |
| **Session Support** | Persistent connections and cookies |
| **Authentication** | Built-in support for various auth methods |
| **Streaming** | Efficient handling of large files |
| **Unicode** | Automatic Unicode handling |

### HTTP Basics

```
Request                          Response
┌─────────────┐                 ┌─────────────┐
│  Method     │                 │  Status     │
│  URL        │    ────────►    │  Headers    │
│  Headers    │                 │  Body       │
│  Body       │                 └─────────────┘
└─────────────┘
```

### Common HTTP Methods

| Method | Description | Example |
|--------|-------------|---------|
| `GET` | Retrieve data | Fetch a webpage |
| `POST` | Create data | Submit a form |
| `PUT` | Update data | Update a resource |
| `PATCH` | Partial update | Modify part of resource |
| `DELETE` | Remove data | Delete a resource |
| `HEAD` | Get headers only | Check if resource exists |
| `OPTIONS` | Get allowed methods | CORS preflight |

---

## 2. Installation

### Installing Requests

```bash
pip install requests
```

### Verifying Installation

```python
import requests
print(requests.__version__)  # Should print version number
```

### Requirements

```txt
requests>=2.31.0
```

---

## 3. Basic Requests

### GET Request

```python
import requests

# Simple GET request
response = requests.get('https://api.github.com')
print(response.status_code)  # 200
print(response.text)         # Response body
```

### POST Request

```python
import requests

# Simple POST request
data = {'key': 'value'}
response = requests.post('https://httpbin.org/post', json=data)
print(response.json())
```

### Response Object

```python
response = requests.get('https://api.github.com')

# Response attributes
print(response.status_code)    # HTTP status code
print(response.headers)        # Response headers
print(response.text)           # Raw text
print(response.content)        # Raw bytes
print(response.json())         # Parsed JSON
print(response.url)            # Final URL (after redirects)
print(response.encoding)       # Encoding
print(response.elapsed)        # Request duration
```

---

## 4. HTTP Methods

### GET - Retrieve Data

```python
# Basic GET
response = requests.get('https://api.github.com/users/python')

# GET with parameters
response = requests.get('https://api.github.com/search/repositories', 
                       params={'q': 'python', 'sort': 'stars'})

# GET with headers
headers = {'User-Agent': 'MyApp/1.0'}
response = requests.get('https://api.github.com', headers=headers)
```

### POST - Create Data

```python
# POST with JSON
data = {'name': 'John', 'email': 'john@example.com'}
response = requests.post('https://httpbin.org/post', json=data)

# POST with form data
data = {'username': 'john', 'password': 'secret'}
response = requests.post('https://httpbin.org/post', data=data)

# POST with raw data
import json
data = json.dumps({'key': 'value'})
response = requests.post('https://httpbin.org/post', 
                        data=data,
                        headers={'Content-Type': 'application/json'})
```

### PUT - Update Data

```python
# PUT - Full update
data = {'name': 'Updated Name', 'email': 'updated@example.com'}
response = requests.put('https://httpbin.org/put', json=data)
```

### PATCH - Partial Update

```python
# PATCH - Partial update
data = {'name': 'New Name'}
response = requests.patch('https://httpbin.org/patch', json=data)
```

### DELETE - Remove Data

```python
# DELETE
response = requests.delete('https://httpbin.org/delete')
```

### HEAD - Headers Only

```python
# HEAD - Get headers without body
response = requests.head('https://api.github.com')
print(response.headers)
```

### OPTIONS - Allowed Methods

```python
# OPTIONS - Get allowed methods
response = requests.options('https://httpbin.org')
print(response.headers['Allow'])
```

---

## 5. Request Parameters

### Query Parameters

```python
# Using params argument
params = {
    'q': 'python',
    'sort': 'stars',
    'order': 'desc',
    'per_page': 10
}
response = requests.get('https://api.github.com/search/repositories', 
                       params=params)

# URL with parameters
print(response.url)  # https://api.github.com/search/repositories?q=python&sort=stars...

# List values for multiple parameters
params = {'key': ['value1', 'value2']}
response = requests.get('https://httpbin.org/get', params=params)
```

### URL Encoding

```python
# Requests automatically encodes special characters
params = {'search': 'hello world!'}
response = requests.get('https://httpbin.org/get', params=params)
# URL: ...?search=hello+world%21
```

### Path Parameters

```python
# Build URL with path parameters
user_id = 123
url = f'https://api.example.com/users/{user_id}'
response = requests.get(url)
```

---

## 6. Headers

### Setting Headers

```python
# Custom headers
headers = {
    'User-Agent': 'MyApp/1.0',
    'Accept': 'application/json',
    'Authorization': 'Bearer token123'
}
response = requests.get('https://api.github.com', headers=headers)
```

### Common Headers

```python
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token',
    'X-Custom-Header': 'custom-value'
}
```

### Reading Response Headers

```python
response = requests.get('https://api.github.com')

# Get all headers
print(response.headers)

# Get specific header
print(response.headers['Content-Type'])
print(response.headers.get('X-RateLimit-Remaining'))

# Case-insensitive access
print(response.headers['content-type'])
print(response.headers['Content-Type'])  # Same
```

### Header Dictionary

```python
# Headers are case-insensitive
response = requests.get('https://api.github.com')
print(response.headers['Content-Type'])
print(response.headers['content-type'])  # Works too
```

---

## 7. Authentication

### Basic Authentication

```python
from requests.auth import HTTPBasicAuth

# Basic auth
response = requests.get('https://httpbin.org/basic-auth/user/pass',
                       auth=HTTPBasicAuth('user', 'pass'))

# Alternative
response = requests.get('https://httpbin.org/basic-auth/user/pass',
                       auth=('user', 'pass'))
```

### Bearer Token Authentication

```python
# Bearer token
headers = {
    'Authorization': 'Bearer your_token_here'
}
response = requests.get('https://api.example.com/protected', 
                       headers=headers)
```

### API Key Authentication

```python
# API key in header
headers = {
    'X-API-Key': 'your_api_key'
}
response = requests.get('https://api.example.com/data', headers=headers)

# API key in query parameters
params = {
    'api_key': 'your_api_key'
}
response = requests.get('https://api.example.com/data', params=params)
```

### Digest Authentication

```python
from requests.auth import HTTPDigestAuth

response = requests.get('https://httpbin.org/digest-auth/auth/user/pass',
                       auth=HTTPDigestAuth('user', 'pass'))
```

### OAuth2

```python
from requests_oauthlib import OAuth2Session

# OAuth2 session
client_id = 'your_client_id'
client_secret = 'your_client_secret'
authorization_url = 'https://oauth.example.com/authorize'
token_url = 'https://oauth.example.com/token'

oauth = OAuth2Session(client_id)
authorization_url, state = oauth.authorization_url(authorization_url)

# After user authorization, get token
token = oauth.fetch_token(token_url, 
                         client_secret=client_secret,
                         authorization_response=authorization_response)

# Use authenticated session
response = oauth.get('https://api.example.com/protected')
```

---

## 8. Sessions

### Session Basics

```python
# Session persists cookies and headers
session = requests.Session()

# First request
response1 = session.get('https://httpbin.org/cookies/set/sessioncookie/12345')

# Second request - cookie is automatically sent
response2 = session.get('https://httpbin.org/cookies')
print(response2.json())
```

### Session with Headers

```python
session = requests.Session()
session.headers.update({
    'User-Agent': 'MyApp/1.0',
    'Authorization': 'Bearer token'
})

# All requests use these headers
response = session.get('https://api.example.com/data')
```

### Session with Authentication

```python
from requests.auth import HTTPBasicAuth

session = requests.Session()
session.auth = HTTPBasicAuth('user', 'pass')

# All requests use this auth
response = session.get('https://api.example.com/protected')
```

### Session Pooling

```python
# Sessions maintain connection pool
session = requests.Session()

# Reuse connections
for i in range(10):
    response = session.get('https://api.example.com/data')
    print(f"Request {i+1}")

# Close session when done
session.close()
```

### Session Context Manager

```python
with requests.Session() as session:
    session.headers.update({'User-Agent': 'MyApp/1.0'})
    response = session.get('https://api.example.com/data')
    # Session automatically closed
```

---

## 9. Handling Responses

### Status Codes

```python
response = requests.get('https://api.github.com')

# Check status
if response.status_code == 200:
    print("Success")
elif response.status_code == 404:
    print("Not found")
elif response.status_code == 500:
    print("Server error")

# Using raise_for_status()
try:
    response = requests.get('https://api.github.com/invalid-endpoint')
    response.raise_for_status()  # Raises exception for 4XX/5XX
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
```

### Common Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | OK | Success |
| 201 | Created | Resource created |
| 204 | No Content | Success, no body |
| 301 | Moved Permanently | Redirect |
| 400 | Bad Request | Invalid request |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Server Error | Server error |

### Response Content

```python
response = requests.get('https://api.github.com')

# Text content
print(response.text)

# Binary content
print(response.content)

# JSON content
data = response.json()
print(data)

# Raw response
print(response.raw)
```

### JSON Response

```python
# Parse JSON
response = requests.get('https://api.github.com/users/python')
data = response.json()

# Access JSON data
print(data['login'])
print(data['public_repos'])

# Check if response is JSON
if response.headers.get('content-type') == 'application/json':
    data = response.json()
```

### Encoding

```python
response = requests.get('https://api.github.com')

# Get encoding
print(response.encoding)  # utf-8

# Set encoding manually
response.encoding = 'iso-8859-1'
print(response.text)
```

---

## 10. Error Handling

### Exception Hierarchy

```
requests.exceptions.RequestException
├── requests.exceptions.HTTPError
├── requests.exceptions.ConnectionError
├── requests.exceptions.Timeout
├── requests.exceptions.TooManyRedirects
└── requests.exceptions.SSLError
```

### Basic Error Handling

```python
import requests

try:
    response = requests.get('https://api.example.com/data')
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
except requests.exceptions.Timeout as e:
    print(f"Timeout Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
```

### Handling Specific Errors

```python
# HTTP errors
try:
    response = requests.get('https://api.example.com/data')
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP {e.response.status_code}: {e}")

# Connection errors
try:
    response = requests.get('https://nonexistent-domain-12345.com')
except requests.exceptions.ConnectionError as e:
    print(f"Cannot connect: {e}")

# Timeout errors
try:
    response = requests.get('https://api.example.com/data', timeout=1)
except requests.exceptions.Timeout:
    print("Request timed out")
```

### Custom Error Handler

```python
def safe_request(method, url, **kwargs):
    """Wrapper for safe requests with error handling"""
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {e.response.status_code}: {e}")
    except requests.exceptions.ConnectionError:
        print("Connection failed")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return None

# Usage
response = safe_request('GET', 'https://api.example.com/data')
```

---

## 11. Timeouts and Retries

### Setting Timeouts

```python
# Single timeout (connect + read)
response = requests.get('https://api.example.com/data', timeout=5)

# Separate timeouts (connect, read)
response = requests.get('https://api.example.com/data', 
                       timeout=(3, 10))  # 3s connect, 10s read

# No timeout (not recommended)
response = requests.get('https://api.example.com/data', 
                       timeout=None)
```

### Retry Mechanism

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create session with retry strategy
session = requests.Session()

retry_strategy = Retry(
    total=3,                    # Total retries
    backoff_factor=1,          # Wait 1, 2, 4 seconds between retries
    status_forcelist=[429, 500, 502, 503, 504],  # Retry on these codes
    allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Use session
response = session.get('https://api.example.com/data')
```

### Custom Retry Logic

```python
import time

def retry_request(url, max_retries=3, delay=1):
    """Custom retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff

# Usage
response = retry_request('https://api.example.com/data')
```

---

## 12. Working with JSON

### Sending JSON Data

```python
# Using json parameter (automatically sets Content-Type)
data = {'name': 'John', 'age': 30}
response = requests.post('https://httpbin.org/post', json=data)

# Manual JSON
import json
data = json.dumps({'name': 'John', 'age': 30})
response = requests.post('https://httpbin.org/post',
                        data=data,
                        headers={'Content-Type': 'application/json'})
```

### Receiving JSON Data

```python
response = requests.get('https://api.github.com/users/python')

# Parse JSON
data = response.json()

# Check if JSON is valid
try:
    data = response.json()
except ValueError:
    print("Invalid JSON")
```

### JSON with Nested Data

```python
# Complex JSON structure
data = {
    'user': {
        'name': 'John',
        'email': 'john@example.com'
    },
    'items': [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'}
    ]
}

response = requests.post('https://httpbin.org/post', json=data)
result = response.json()
print(result['json'])
```

---

## 13. File Uploads/Downloads

### Downloading Files

```python
# Download small file
response = requests.get('https://example.com/file.pdf')
with open('file.pdf', 'wb') as f:
    f.write(response.content)

# Download large file (streaming)
response = requests.get('https://example.com/large-file.zip', stream=True)
with open('large-file.zip', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### Uploading Files

```python
# Upload single file
files = {'file': open('report.pdf', 'rb')}
response = requests.post('https://httpbin.org/post', files=files)

# Upload with filename
files = {'file': ('report.pdf', open('report.pdf', 'rb'))}
response = requests.post('https://httpbin.org/post', files=files)

# Upload multiple files
files = [
    ('file1', open('file1.pdf', 'rb')),
    ('file2', open('file2.pdf', 'rb'))
]
response = requests.post('https://httpbin.org/post', files=files)
```

### Uploading with Form Data

```python
# Upload file with additional form data
files = {'file': open('document.pdf', 'rb')}
data = {'description': 'Quarterly report', 'author': 'John'}
response = requests.post('https://httpbin.org/post', 
                        files=files, 
                        data=data)
```

### Download with Progress Bar

```python
import requests
from tqdm import tqdm

def download_with_progress(url, filename):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = f.write(chunk)
            bar.update(size)

# Usage
download_with_progress('https://example.com/large-file.zip', 'file.zip')
```

---

## 14. Cookies

### Reading Cookies

```python
response = requests.get('https://httpbin.org/cookies/set/sessioncookie/12345')
print(response.cookies)

# Access specific cookie
print(response.cookies['sessioncookie'])
```

### Sending Cookies

```python
# Send cookies with request
cookies = {'session_id': 'abc123'}
response = requests.get('https://httpbin.org/cookies', cookies=cookies)
print(response.json())
```

### Cookie Jar

```python
# Using CookieJar
jar = requests.cookies.RequestsCookieJar()
jar.set('cookie1', 'value1', domain='httpbin.org')
jar.set('cookie2', 'value2', domain='httpbin.org')

response = requests.get('https://httpbin.org/cookies', cookies=jar)
```

### Session Cookies

```python
# Session automatically handles cookies
session = requests.Session()

# First request sets cookie
session.get('https://httpbin.org/cookies/set/sessioncookie/12345')

# Second request sends cookie automatically
response = session.get('https://httpbin.org/cookies')
print(response.json())
```

### Cookie Persistence

```python
import pickle

# Save cookies
session = requests.Session()
session.get('https://example.com/login')
with open('cookies.pkl', 'wb') as f:
    pickle.dump(session.cookies, f)

# Load cookies
session = requests.Session()
with open('cookies.pkl', 'rb') as f:
    session.cookies.update(pickle.load(f))
```

---

## 15. SSL/TLS Verification

### Disable SSL Verification (Not Recommended)

```python
# Disable SSL verification (for testing only)
response = requests.get('https://example.com', verify=False)

# Suppress warning
import urllib3
urllib3.disable_warnings()
response = requests.get('https://example.com', verify=False)
```

### Custom CA Bundle

```python
# Use custom CA bundle
response = requests.get('https://example.com', 
                       verify='/path/to/cacert.pem')
```

### Client Certificates

```python
# Use client certificate
response = requests.get('https://example.com',
                       cert=('/path/to/client.cert', 
                             '/path/to/client.key'))
```

### SSL Error Handling

```python
try:
    response = requests.get('https://expired.badssl.com/')
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
```

---

## 16. Proxies

### HTTP Proxy

```python
# Use HTTP proxy
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}
response = requests.get('https://api.example.com/data', proxies=proxies)
```

### SOCKS Proxy

```python
# SOCKS proxy (requires requests[socks])
pip install requests[socks]

proxies = {
    'http': 'socks5://user:pass@proxy.example.com:1080',
    'https': 'socks5://user:pass@proxy.example.com:1080'
}
response = requests.get('https://api.example.com/data', proxies=proxies)
```

### Environment Variables

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### Session with Proxy

```python
session = requests.Session()
session.proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}
response = session.get('https://api.example.com/data')
```

---

## 17. Async Requests

### Using asyncio + aiohttp

```python
import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = [
        'https://api.github.com/users/python',
        'https://api.github.com/users/pallets',
        'https://api.github.com/users/requests'
    ]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

### Concurrent Requests with Threads

```python
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch_url(url):
    return requests.get(url).json()

urls = [
    'https://api.github.com/users/python',
    'https://api.github.com/users/pallets',
    'https://api.github.com/users/requests'
]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_url, urls))
    print(results)
```

---

## 18. Web Scraping

### Basic Scraping

```python
import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data
title = soup.find('h1').text
links = [a['href'] for a in soup.find_all('a', href=True)]

print(f"Title: {title}")
print(f"Links: {links}")
```

### Scraping with User-Agent

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get('https://example.com', headers=headers)
```

### Handling Pagination

```python
def scrape_all_pages(base_url):
    """Scrape all pages"""
    page = 1
    all_data = []
    
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        data = response.json()
        
        if not data['items']:
            break
        
        all_data.extend(data['items'])
        page += 1
    
    return all_data
```

---

## 19. API Integration

### GitHub API

```python
import requests

def get_github_user(username):
    """Get GitHub user info"""
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_user_repos(username):
    """Get user repositories"""
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Usage
user = get_github_user('python')
print(f"User: {user['login']}")
print(f"Repos: {user['public_repos']}")

repos = get_user_repos('python')
print(f"First repo: {repos[0]['name']}")
```

### REST API Client

```python
class APIClient:
    """Generic REST API client"""
    
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
    
    def get(self, endpoint, params=None):
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint, data=None):
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def put(self, endpoint, data=None):
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def delete(self, endpoint):
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.status_code == 204

# Usage
client = APIClient('https://api.example.com', api_key='your_key')
users = client.get('/users')
user = client.post('/users', data={'name': 'John'})
updated = client.put('/users/1', data={'name': 'Jane'})
client.delete('/users/1')
```

---

## 20. Best Practices

### 1. Use Sessions for Multiple Requests

```python
# ✅ GOOD - Use session
session = requests.Session()
for i in range(10):
    session.get('https://api.example.com/data')

# ❌ BAD - New connection each time
for i in range(10):
    requests.get('https://api.example.com/data')
```

### 2. Always Set Timeouts

```python
# ✅ GOOD - Set timeout
response = requests.get('https://api.example.com/data', timeout=10)

# ❌ BAD - No timeout (can hang forever)
response = requests.get('https://api.example.com/data')
```

### 3. Handle Errors Gracefully

```python
# ✅ GOOD - Handle errors
try:
    response = requests.get('https://api.example.com/data', timeout=10)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return None

# ❌ BAD - No error handling
response = requests.get('https://api.example.com/data')
return response.json()
```

### 4. Use Meaningful User-Agent

```python
# ✅ GOOD - Custom User-Agent
headers = {
    'User-Agent': 'MyApp/1.0 (contact@example.com)'
}
response = requests.get('https://api.example.com/data', headers=headers)

# ❌ BAD - Default User-Agent (may be blocked)
response = requests.get('https://api.example.com/data')
```

### 5. Respect Rate Limits

```python
import time

def rate_limited_request(url, delay=1):
    """Request with rate limiting"""
    time.sleep(delay)
    return requests.get(url)

# Or use session with retry
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)
```

### 6. Close Resources

```python
# ✅ GOOD - Close session
with requests.Session() as session:
    response = session.get('https://api.example.com/data')

# ✅ GOOD - Explicit close
session = requests.Session()
try:
    response = session.get('https://api.example.com/data')
finally:
    session.close()
```

---

## 21. Automation Examples

### Example 1: Automated Health Checks

```python
import requests
from datetime import datetime

def check_service_health(url, timeout=5):
    """Check if service is healthy"""
    try:
        start = datetime.now()
        response = requests.get(url, timeout=timeout)
        elapsed = (datetime.now() - start).total_seconds()
        
        return {
            'url': url,
            'status': 'healthy',
            'status_code': response.status_code,
            'response_time': elapsed,
            'timestamp': datetime.now().isoformat()
        }
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

# Monitor multiple services
services = [
    'https://api.github.com',
    'https://httpbin.org',
    'https://jsonplaceholder.typicode.com'
]

for service in services:
    result = check_service_health(service)
    print(f"{service}: {result['status']} ({result.get('response_time', 'N/A')}s)")
```

### Example 2: Automated Data Backup

```python
import requests
import json
from datetime import datetime

def backup_api_data(api_url, backup_file):
    """Backup API data to file"""
    try:
        # Fetch data
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        # Prepare backup
        backup = {
            'timestamp': datetime.now().isoformat(),
            'source': api_url,
            'data': response.json()
        }
        
        # Save to file
        with open(backup_file, 'w') as f:
            json.dump(backup, f, indent=2)
        
        print(f"Backup completed: {backup_file}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Backup failed: {e}")
        return False

# Usage
backup_api_data(
    'https://jsonplaceholder.typicode.com/users',
    f'backup_users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
)
```

### Example 3: Automated Form Submission

```python
import requests

def submit_form(form_url, form_data):
    """Submit form automatically"""
    try:
        response = requests.post(form_url, data=form_data)
        response.raise_for_status()
        
        if response.status_code == 200:
            print("Form submitted successfully")
            return True
        else:
            print(f"Unexpected status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Submission failed: {e}")
        return False

# Usage
form_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'message': 'Automated form submission'
}

submit_form('https://httpbin.org/post', form_data)
```

### Example 4: Automated Email Notifications

```python
import requests
import smtplib
from email.mime.text import MIMEText

def send_alert_via_webhook(webhook_url, message):
    """Send alert via webhook"""
    payload = {
        'text': message,
        'username': 'Alert Bot'
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("Alert sent successfully")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to send alert: {e}")
        return False

def send_alert_via_email(smtp_server, from_email, to_email, 
                        subject, message, password):
    """Send alert via email"""
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Usage
send_alert_via_webhook(
    'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
    '⚠️ Service Alert: Database connection failed'
)
```

### Example 5: Automated Report Generation

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_data_from_api(api_url, params=None):
    """Fetch data from API"""
    try:
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return []

def generate_report(data, output_file):
    """Generate report from data"""
    df = pd.DataFrame(data)
    
    # Add calculations
    if 'price' in df.columns:
        df['total'] = df['price'] * df['quantity']
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Report generated: {output_file}")
    return df

# Usage
# Fetch sales data for last 7 days
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

sales_data = fetch_data_from_api(
    'https://api.example.com/sales',
    params={
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
)

if sales_data:
    report = generate_report(
        sales_data,
        f'sales_report_{end_date.strftime("%Y%m%d")}.csv'
    )
    print(f"Total records: {len(report)}")
```

### Example 6: Automated Social Media Posting

```python
import requests
import json

class SocialMediaBot:
    """Automated social media posting"""
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api.socialmedia.com/v1'
    
    def post_tweet(self, text):
        """Post a tweet"""
        url = f"{self.base_url}/tweets"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        data = {'text': text}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Tweet posted: {text}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to post tweet: {e}")
            return None
    
    def schedule_post(self, text, schedule_time):
        """Schedule a post for later"""
        url = f"{self.base_url}/scheduled"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        data = {
            'text': text,
            'scheduled_at': schedule_time.isoformat()
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(f"Post scheduled for {schedule_time}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to schedule post: {e}")
            return None

# Usage
bot = SocialMediaBot('your_api_key', 'your_api_secret')
bot.post_tweet("Hello from Python! 🐍")
```

### Example 7: Automated File Sync

```python
import requests
import os
from pathlib import Path

def download_files_from_api(base_url, output_dir):
    """Download all files from API"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    try:
        # Get file list
        response = requests.get(f"{base_url}/files", timeout=30)
        response.raise_for_status()
        files = response.json()
        
        # Download each file
        for file_info in files:
            file_url = f"{base_url}/files/{file_info['id']}/download"
            file_path = output_path / file_info['name']
            
            print(f"Downloading: {file_info['name']}")
            response = requests.get(file_url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"Downloaded {len(files)} files to {output_dir}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Sync failed: {e}")
        return False

# Usage
download_files_from_api(
    'https://api.example.com',
    './downloads'
)
```

### Example 8: Automated Monitoring Dashboard

```python
import requests
import time
from datetime import datetime
from collections import deque

class ServiceMonitor:
    """Monitor service health over time"""
    
    def __init__(self, url, max_history=100):
        self.url = url
        self.history = deque(maxlen=max_history)
    
    def check(self):
        """Check service health"""
        try:
            start = time.time()
            response = requests.get(self.url, timeout=5)
            elapsed = time.time() - start
            
            status = {
                'timestamp': datetime.now(),
                'status_code': response.status_code,
                'response_time': elapsed,
                'healthy': response.status_code == 200
            }
            
            self.history.append(status)
            return status
            
        except requests.exceptions.RequestException as e:
            status = {
                'timestamp': datetime.now(),
                'status_code': None,
                'response_time': None,
                'healthy': False,
                'error': str(e)
            }
            self.history.append(status)
            return status
    
    def get_uptime(self):
        """Calculate uptime percentage"""
        if not self.history:
            return 0
        healthy = sum(1 for h in self.history if h['healthy'])
        return (healthy / len(self.history)) * 100
    
    def get_avg_response_time(self):
        """Get average response time"""
        times = [h['response_time'] for h in self.history if h['response_time']]
        return sum(times) / len(times) if times else 0
    
    def monitor(self, interval=60):
        """Continuous monitoring"""
        print(f"Monitoring {self.url} every {interval}s...")
        try:
            while True:
                status = self.check()
                print(f"[{status['timestamp']}] "
                      f"Status: {status['status_code']}, "
                      f"Time: {status['response_time']:.2f}s, "
                      f"Uptime: {self.get_uptime():.1f}%")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped")

# Usage
monitor = ServiceMonitor('https://api.github.com')
monitor.monitor(interval=30)
```

---

## Summary

### Key Concepts

| Concept | Description |
|---------|-------------|
| **GET/POST/PUT/PATCH/DELETE** | HTTP methods for different operations |
| **Headers** | Metadata for requests/responses |
| **Authentication** | Basic, Bearer, OAuth2, API keys |
| **Sessions** | Persistent connections and cookies |
| **Error Handling** | Graceful handling of network errors |
| **Timeouts** | Prevent hanging requests |
| **JSON** | Automatic serialization/deserialization |
| **File Uploads/Downloads** | Streaming for large files |
| **Cookies** | Session management |
| **Proxies** | Route requests through proxy servers |

### Best Practices Recap

1. Use sessions for multiple requests
2. Always set timeouts
3. Handle errors gracefully
4. Use meaningful User-Agent
5. Respect rate limits
6. Close resources properly
7. Use retry logic for transient failures
8. Stream large files
9. Validate responses
10. Log requests for debugging

---

## Practice Exercises

1. **Weather API**: Build a weather app that fetches data from OpenWeatherMap API
2. **File Downloader**: Create a bulk file downloader with progress bars
3. **API Wrapper**: Build a wrapper for your favorite API (GitHub, Twitter, etc.)
4. **Web Scraper**: Scrape product information from an e-commerce site
5. **Service Monitor**: Create a monitoring system for multiple services

---

## Additional Resources

- [Requests Documentation](https://requests.readthedocs.io/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Best Practices](https://restfulapi.net/)
- [OAuth 2.0](https://oauth.net/2/)
