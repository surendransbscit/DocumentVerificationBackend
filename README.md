# DocumentVerificationBackend
1. Clone the repository or extract the backend zip.
2. Navigate into the backend project directory.
3. Create a virtual environment and activate it:
 - Windows: python -m venv env && env\Scripts\activate
 - Linux/Mac: python3 -m venv env && source env/bin/activate
4. Install required packages:
 pip install -r requirements.txt
5. Run migrations:
 python manage.py makemigrations
 python manage.py migrate
6. Run the development server:
 python manage.py runserver
7. Access the API at: http://127.0.0.1:8000/
