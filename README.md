# happierWork-backend

# Clone or pull the repository
git clone <repository-url>
cd <project-directory>
git pull origin <branch-name>

# Set up the backend
pip install -r requirements.txt
python manage.py migrate
uvicorn backend.asgi:application
<!-- python manage.py runserver -->

# Set up the frontend
npm install
ng serve