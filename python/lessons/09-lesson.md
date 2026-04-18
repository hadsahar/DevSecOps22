---
layout: default
title: Python Lesson 9 - REST API
---

# RESTful API

A REST API (Representational State Transfer API) enables communication between client and server over HTTP. It exchanges data typically in JSON format using standard web protocols.

![alt text](https://media.geeksforgeeks.org/wp-content/uploads/20260302171142613665/http_request.webp)

- Uses HTTP methods like GET, POST, PUT, PATCH, and DELETE.
- Client sends requests to server endpoints (URLs).
- Server returns responses such as JSON, XML, HTML, or images.
- Maps HTTP methods to CRUD operations (Create, Read, Update, Delete).

## Common HTTP Methods Used in REST API

In REST architecture, the main HTTP methods are GET, POST, PUT, PATCH, and DELETE, which map to CRUD operations. Other less commonly used methods include HEAD and OPTIONS.

1. GET Method
   The HTTP GET method retrieves a resource. On success, it returns data (usually JSON or XML) with 200 OK, and on error, it commonly returns 404 Not Found or 400 Bad Request.

```bash
GET /users/123
# This request fetches data for the user with ID 123.
```

2. POST Method
   The POST method creates new resources. On success, it returns 201 Created with a Location header pointing to the new resource.

```bash
POST /users
{
  "name": "Anne",
  "email": "gfg@example.com"
}
#This request creates a new user with the given data.

 Note:  POST is neither safe nor idempotent.
```

3. PUT Method
   PUT is used to update or create a resource. It sends the complete resource in the request body and replaces the existing one at the specified URL.

```bash
PUT /users/123
{
  "name": "Anne",
  "email": "gfg@example.com"
}
# This request updates the user with ID 123 or creates a new user if one doesn't exist.
```

4. PATCH Method
   PATCH is used to partially update a resource. It sends only the fields to be modified, instead of replacing the entire resource.

```bash
PATCH /users/123
{
  "email": "new.email@example.com"
}
# This request updates only the email of the user with ID 123, leaving the rest of the user data unchanged.
```

## Differences Between PUT and PATCH

Both PATCH and PUT are used to update resources on the server, but they differ in how they handle the update process:

| PUT                                       | PATCH                                 |
| ----------------------------------------- | ------------------------------------- |
| Replaces the entire resource              | Updates only specified fields         |
| Must send full data                       | Only sends changes                    |
| Idempotent                                | Not always idempotent                 |
| Example: Updating a user’s entire profile | Example: Changing just a user’s email |

5. DELETE Method
   It is used to delete a resource identified by a URI. On successful deletion, return HTTP status 200 (OK) along with a response body.

```bash
DELETE /users/123
# This request deletes the user with ID 123.
```

Idempotence: An HTTP method is idempotent if making the same request multiple times results in the same server state as making it once. Repeated requests do not cause additional changes beyond the initial application.

## The Big Picture: 3-Tier Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT TIER (Frontend)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Browser    │  │ Mobile App   │  │  Desktop App │  │  IoT Device  │     │
│  │  (React/Vue) │  │ (iOS/Android)│  │  (Electron)  │  │  (Sensor)    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │                 │             │
│         └─────────────────┴─────────────────┴─────────────────┘             │
│                                    │                                        │
│                                 INTERNET                                    │
│                                    │                                        │
├────────────────────────────────────┼────────────────────────────────────────┤
│                           API TIER (Backend)                                │
├────────────────────────────────────┼────────────────────────────────────────┤
│         ┌──────────────────────────┴───────────────────────────┐            │
│         │                                                      │            │
│    ┌────▼────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    │            │
│    │  Load   │───▶│  API    │───▶│  Auth   │───▶│  Rate   │    │            │
│    │Balancer │    │ Gateway │    │ Service │    │ Limiter │    │            │
│    └─────────┘    └────┬────┘    └─────────┘    └─────────┘    │            │
│                        │                                       │            │
│         ┌──────────────┼──────────────────────────────┐        │            │
│         │              │                              │        │            │
│    ┌────▼────┐    ┌────▼──────┐                 ┌─────▼─────┐  │            │
│    │ Flask/  │    │  Business │                 │  Cache    │  │            │
│    │Django   │───▶│  Logic    │◀───────────────▶│ (Redis)   │  │            │
│    │ Server  │    │  Layer    │                 │           │  │            │
│    └────┬────┘    └─────┬─────┘                 └───────────┘  │            │
│         │               │                                      │            │
│         └───────────────┼──────────────────────────────────────┘            │
│                         │                                                   │
├─────────────────────────┼───────────────────────────────────────────────────┤
│                    DATA TIER (Database)                                     │
├─────────────────────────┼───────────────────────────────────────────────────┤
│         ┌───────────────┼───────────────┬───────────────┐                   │
│         │               │               │               │                   │
│    ┌────▼────┐     ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐            │
│    │  SQL    │     │   NoSQL   │   │  File     │   │  Message  │            │
│    │(Postgre)│     │(MongoDB)  │   │  Storage  │   │  Queue    │            │
│    └─────────┘     └───────────┘   └───────────┘   └───────────┘            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Complete Request/Response Flow

```
USER ACTION: Clicks "Place Order" button
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 1. BROWSER (Frontend) │
│ - JavaScript constructs HTTP Request │
│ - Method: POST │
│ - Headers: {Content-Type: application/json} │
│ - Body: {"item": "Pizza", "price": 12.99} │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 2. DNS RESOLUTION │
│ - Check browser cache │
│ - Check OS cache │
│ - Query DNS server (8.8.8.8) │
│ - Receive IP: 192.168.1.100 │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 3. TCP CONNECTION (3-way handshake) │
│ Client: "SYN" (Can we talk?) │
│ Server: "SYN-ACK" (Yes, I'm listening) │
│ Client: "ACK" (Great, here's my request) │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 4. LOAD BALANCER (If multiple servers) │
│ - Receives request │
│ - Checks which server is least busy │
│ - Forwards request to Server #2 │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 5. API GATEWAY / WEB SERVER (Nginx/Apache) │
│ - Terminates SSL (if HTTPS) │
│ - Checks rate limiting │
│ - Routes to Flask application │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 6. FLASK APPLICATION (Python code) │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ @app.route('/orders', methods=['POST']) │ │
│ │ def create_order(): │ │
│ │ data = request.get_json() # Parse body │ │
│ │ validate_input(data) # Check required fields │ │
│ │ save_to_database(data) # Store in DB │ │
│ │ return jsonify(order), 201 # Return response │ │
│ └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 7. BUSINESS LOGIC LAYER │
│ - Validate data (price > 0, item name not empty) │
│ - Apply business rules (discount calculation) │
│ - Generate order ID │
│ - Set default status to "pending" │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 8. DATABASE LAYER │
│ - INSERT INTO orders (item, price, status) VALUES (...) │
│ - Commit transaction │
│ - Return new order ID │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 9. RESPONSE CONSTRUCTION │
│ - Create JSON response │
│ - Add status code: 201 CREATED │
│ - Add headers: Content-Type, CORS headers │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 10. RESPONSE TRAVELS BACK │
│ - Through web server │
│ - Through load balancer │
│ - Across internet │
│ - Back to browser │
└──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 11. BROWSER PROCESSES RESPONSE │
│ - Checks status code (201 = success) │
│ - Parses JSON body │
│ - Updates DOM with new order │
│ - Shows success message to user │
└──────────────────────────────────────────────────────────────────────────┘
```

## Types of HTTP Requests (Visual Chart)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           HTTP REQUEST METHODS COMPLETE CHART                       │
├──────────────┬─────────────┬──────────────┬────────────┬────────────┬───────────────┤
│    METHOD    │   CRUD      │  HAS BODY?   │IDEMPOTENT? │  SAFE?     │   CACHEABLE?  │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  GET         │  Read       │    ❌ No     │   ✅ Yes   │  ✅ Yes     │   ✅ Yes      │
│              │             │              │            │            │               │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  POST        │  Create     │    ✅ Yes    │   ❌ No    │  ❌ No     │   ⚠️ Only with │
│              │             │              │            │            │    freshness   │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  PUT         │  Update/    │    ✅ Yes    │   ✅ Yes   │  ❌ No     │   ❌ No       │
│              │  Replace    │              │            │            │               │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  PATCH       │  Partial    │    ✅ Yes    │   ❌ No    │  ❌ No     │   ❌ No       │
│              │  Update     │              │            │            │               │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  DELETE      │  Delete     │    ⚠️ Maybe  │   ✅ Yes   │  ❌ No     │   ❌ No       │
│              │             │              │            │            │               │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  HEAD        │  Headers    │    ❌ No     │   ✅ Yes   │  ✅ Yes    │   ✅ Yes      │
│              │  Only       │              │            │            │               │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  OPTIONS     │  Discover   │    ❌ No     │   ✅ Yes   │  ✅ Yes    │   ❌ No       │
│              │  Methods    │              │            │            │               │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  TRACE       │  Debug      │    ❌ No     │   ✅ Yes   │  ✅ Yes    │   ❌ No       │
│              │             │              │            │            │               │
├──────────────┼─────────────┼──────────────┼────────────┼────────────┼───────────────┤
│              │             │              │            │            │               │
│  CONNECT     │  Tunnel/    │    ✅ Yes    │   ❌ No    │  ❌ No     │   ❌ No       │
│              │  Proxy      │              │            │            │               │
└──────────────┴─────────────┴──────────────┴────────────┴────────────┴───────────────┘
```

## Terms Explained:

- **CRUD**: Create, Read, Update, Delete operations
- **Idempotent**: Multiple identical requests have same effect as one
- **Safe**: Doesn't modify data on server
- **Cacheable**: Response can be stored and reused

## Request/Response Examples for Each Method

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ METHOD: GET                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ REQUEST:                                                                    │
│   GET /orders/1 HTTP/1.1                                                    │
│   Host: api.example.com                                                     │
│   Authorization: Bearer token123                                            │
│                                                                             │
│ RESPONSE:                                                                   │
│   HTTP/1.1 200 OK                                                           │
│   Content-Type: application/json                                            │
│                                                                             │
│   {"id": 1, "item": "Pizza", "status": "pending"}                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ METHOD: POST                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ REQUEST:                                                                    │
│   POST /orders HTTP/1.1                                                     │
│   Host: api.example.com                                                     │
│   Content-Type: application/json                                            │
│                                                                             │
│   {"item": "Burger", "price": 8.99}                                        │
│                                                                             │
│ RESPONSE:                                                                   │
│   HTTP/1.1 201 Created                                                      │
│   Location: /orders/42                                                      │
│   Content-Type: application/json                                            │
│                                                                             │
│   {"id": 42, "item": "Burger", "price": 8.99, "status": "pending"}        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ METHOD: PUT (Full Replace)                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ REQUEST:                                                                    │
│   PUT /orders/1 HTTP/1.1                                                    │
│   Host: api.example.com                                                     │
│   Content-Type: application/json                                            │
│                                                                             │
│   {"item": "New Pizza", "price": 15.99, "status": "ready"}                │
│                                                                             │
│ RESPONSE:                                                                   │
│   HTTP/1.1 200 OK                                                           │
│   Content-Type: application/json                                            │
│                                                                             │
│   {"id": 1, "item": "New Pizza", "price": 15.99, "status": "ready"}       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ METHOD: PATCH (Partial Update)                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ REQUEST:                                                                    │
│   PATCH /orders/1 HTTP/1.1                                                  │
│   Host: api.example.com                                                     │
│   Content-Type: application/json                                            │
│                                                                             │
│   {"status": "delivered"}                                                  │
│                                                                             │
│ RESPONSE:                                                                   │
│   HTTP/1.1 200 OK                                                           │
│   Content-Type: application/json                                            │
│                                                                             │
│   {"id": 1, "item": "Pizza", "price": 12.99, "status": "delivered"}       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ METHOD: DELETE                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ REQUEST:                                                                    │
│   DELETE /orders/1 HTTP/1.1                                                 │
│   Host: api.example.com                                                     │
│                                                                             │
│ RESPONSE:                                                                   │
│   HTTP/1.1 204 No Content                                                   │
│   (or 200 OK with confirmation message)                                     │
│                                                                             │
│   {"message": "Order 1 deleted successfully"}                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Synchronous vs Asynchronous Flow

```
Client Server Database
│ │ │
│──── POST /orders ──────→│ │
│ │ │
│ │──── INSERT ─────────────→│
│ │ │
│ │←─────── OK ──────────────│
│ │ │
│←─── 201 Created ────────│ │
│ │ │

⏱️ Client waits (blocked) during entire operation
✅ Simple to understand
❌ Can be slow for long operations

Client API Gateway Message Queue Worker Database
│ │ │ │ │
│── POST /orders─→│ │ │ │
│ │ │ │ │
│ │─── Queue Message──→│ │ │
│ │ │ │ │
│←──202 Accepted─→│ │ │ │
│ │ │ │ │
│ (Client continues working) │ │ │
│ │ │ │ │
│ │ │─── Get Message──→│ │
│ │ │ │ │
│ │ │ │──INSERT──────→│
│ │ │ │ │
│ │ │ │←───OK─────────│
│ │ │ │ │
│ │ │←─── Acknowledge─│ │
│ │ │ │ │
│──GET /orders/1─→│ │ │ │
│ │─────────────────────────────────────→│ │
│ │←─────────────────────────────────────│ │
│←─── 200 OK ─────│ │ │ │

⏱️ Client gets immediate response (202)
✅ Better for long operations
✅ Better scalability
❌ More complex

```

# Common Architecture Patterns

- 1. Monolithic Architecture (Simple)

```

┌─────────────────────────────────────┐
│ ONE APPLICATION │
│ ┌─────────┐ ┌─────────┐ ┌────────┐ │
│ │ UI │ │ API │ │ DB │ │
│ │ Layer │ │ Layer │ │ Layer │ │
│ └─────────┘ └─────────┘ └────────┘ │
└─────────────────────────────────────┘

```

    ✅ Simple to build
    ✅ Easy to deploy
    ❌ Hard to scale
    ❌ One bug breaks everything

- 2. Microservices Architecture (Advanced)

```

┌──────────┐ ┌──────────┐ ┌──────────┐
│ Order │ │ Payment │ │ User │
│ Service │◀──▶│ Service │◀──▶│ Service │
└──────────┘ └──────────┘ └──────────┘
▲ ▲ ▲
│ │ │
└───────────────┼───────────────┘
│
┌──────────────┐
│ API Gateway │
└──────────────┘
▲
│
┌───┴───┐
│Client│
└──────┘

```

    ✅ Independent scaling
    ✅ Different technologies per service
    ❌ Complex to manage
    ❌ Network latency

- 3. Layered (N-Tier) Architecture (Most Common)

```

┌────────────┐
│ Client │ (Presentation Tier)
└─────┬──────┘
│
┌─────▼──────┐
│ API │ (Application Tier)
└─────┬──────┘
│
┌─────▼──────┐
│ Database │ (Data Tier)
└────────────┘

```

    ✅ Separation of concerns
    ✅ Each layer can scale independently
    ✅ Easier to maintain
    ❌ Extra network hops

# main flow

```

┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPLETE API REQUEST LIFECYCLE │
└─────────────────────────────────────────────────────────────────────────────┘

    USER
     │
     │ 1. Types URL / Clicks button
     ▼

┌─────────┐
│ Browser │
└────┬────┘
│
│ 2. DNS Lookup
▼
┌─────────┐ ┌─────────┐
│ DNS │────▶│ IP │
└─────────┘ │ Address │
└─────────┘
│
│ 3. TCP Connection (3-way handshake)
▼
┌─────────┐ SYN ──────────▶
│ Client │ ◀───────── SYN-ACK
└─────────┘ ACK ──────────▶
│
│ 4. TLS/SSL Handshake (if HTTPS)
▼
┌─────────┐ ClientHello ──▶
│ SSL │ ◀─── ServerHello
│ Tunnel │ Key Exchange
└─────────┘ ◀─── Finished
│
│ 5. Send HTTP Request
▼
┌─────────┐
│ Load │ 6. Distribute traffic
│Balancer │
└────┬────┘
│
│ 7. Forward to API Server
▼
┌─────────┐
│ API │ 8. Authenticate & Authorize
│ Gateway │
└────┬────┘
│
│ 9. Route to endpoint
▼
┌─────────┐
│ Flask │ 10. Parse request
│ App │ 11. Validate input
└────┬────┘ 12. Apply business logic
│
│ 13. Query/Update database
▼
┌─────────┐
│Database │ 14. Execute SQL
└────┬────┘ 15. Return results
│
│ 16. Process results
▼
┌─────────┐
│ Flask │ 17. Format JSON response
│ App │ 18. Add status code & headers
└────┬────┘
│
│ 19. Send response back
▼
┌─────────┐
│ Browser │ 20. Parse JSON
└────┬────┘ 21. Check status code
│ 22. Update DOM
│
▼
    USER (Sees result)
```
