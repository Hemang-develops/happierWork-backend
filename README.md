# happierWork-backend

Django Real-Time WebSocket Backend:  
This project implements a Django-based backend for a real-time dashboard application. It allows multiple users (e.g., CEO, CFO) to view and update a list of positions and respective salary budgets. Updates are synchronized across users in real-time using WebSockets.

Features:  
Real-time synchronization: Multiple users can add, delete, or modify data, and changes will appear instantly for all connected users.  
WebSocket-based communication: Efficient and low-latency data exchange between frontend and backend.  
RESTful API: Supports RESTful endpoints for CRUD operations.  

Tech Stack:  
Backend: Django, Django Channels  
WebSocket: Django Channels for WebSocket support  
Database: JSON (can be replaced with PostgreSQL, MySQL, etc.)  
Frontend: Angular (or any frontend consuming WebSocket APIs)  

Requirements:  
Before you begin, ensure you have the following installed:  
  
Python 3.7+  
Django 3.2+  
Django Channels  
Uvicorn  
aiofiles  
WebSocket client (for testing)  
  
Installation  

1. Clone the Repository  
git clone https://github.com/yourusername/yourproject.git  
cd yourproject  
  
2. Set up a Virtual Environment  
python -m venv env  
source env/bin/activate  # On Windows: env\Scripts\activate  
  
3. Install Dependencies  
pip install -r requirements.txt  
  
4. Migrate the Database  
python manage.py migrate  
  
5. Start the Django Development Server  
python manage.py runserver  
  
6. Start the WebSocket Server  
uvicorn -b 0.0.0.0 -port 8001 backend.asgi:application  
Note: Ensure that both Django HTTP server (default port: 8000) and the WebSocket server (port: 8001) are running. "-b 0.0.0.0" is optional  
  
WebSocket Endpoints  
WebSocket URL: ws://localhost:8001/ws/dashboard/  
  
Actions:  
  
add: Adds a new position.  
delete: Deletes a position by id.  
Example JSON payload for adding a position:  
  
["add", "UI", "Engineering", "50000", "Ahmedabad"]  
  
How to Use  
Adding Data:  
Open the web application on two devices (e.g., CEO and CFO).    
Both users can add a position with a salary budget.  
Once a position is added on one device, it will be synced and appear on the other device in real-time.  

Deleting Data:  
Select a position and click "Delete".  
The deletion will be reflected in real-time across all connected users.