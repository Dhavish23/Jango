
Airline Training App (Made with Django)

This is a school project I made using Django. It's kind of like a mini system for training in an airline — where students can sign up for training, trainers can see their students, and coordinators can see everything.

---

 Thew Main Features

- You can sign up and log in
- See a list of training modules
- Students can enroll in stuff
- Trainers can see who's in their module
- Coordinators get their own special dashboard
- Has a few automatic tests to make sure it works
- Comes with an admin page too 

---

The Roles

- The Student – signs up and joins training stuff
- TheTrainer – teaches the module and checks who's in it
- The Coordinator – kind of like a manager, they see everything
- The Admin – full access with Django admin

---

Tech That Was Used

- Django 5 ( runs it)
- Python 3.13
- SQLite (Django’s built-in database)
- HTML, CSS and Bootstrap for the layout

---

How To Use It

1. Download or clone the code:

   git clone https://github.com/your-username/mytraining.git
   cd mytraining
   

2. Make a virtual environment and install stuff:
   
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   

3. Run this to set up the database:

   py manage.py migrate
   

4. Make a superuser (admin):

   py manage.py createsuperuser
  

5. Start the server:
   bash
   py manage.py runserver
   

6. Open your browser and go to:
   
   http://127.0.0.1:8000/
   

---

Tests

You can test the site like this:

py manage.py test


---

  Files I Submitted

 Design1_UseCases.pdf – has the use case diagram
 Design2_ERD.pdf – database diagram
 Design3_tests.zip – the test code in a zip file

---

 Notes

This was made for my Web Framework Development module  (3rd year, TUD). It's not really fancy but I had fun doing this project and leanred many new things 
