# Payment-Gateway

It is a project for TailNode related with Payment Gateway.

To test this project you just need to do following steps-

1 - Clone this project in to your system

2 - Make sure you have installed python 3.0+ and django.

3 - Create a virtual environment of this project.

4 - Install the requirements.txt file **pip intsall -r requirements.txt**

5 - Connect with the database I have used MySql for this

6 - Run migration command **python manage.py migrate**

7 - Create a superuser to access the admin **python manage.py createsuperuser**

8 - Run the server with **python manage.py runserver**

9 - You will be redirected to the swagger URL with all the API listing register a user and with register API.

10 - Login the user you will get the token copy that token and authorize the user.

11 - Go to the POST request of **/payment_gateway_app/user_payment/** and fill the deatails.

12 - You will get the Response as asked.
