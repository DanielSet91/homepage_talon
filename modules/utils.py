from flask_mail import Message

def send_email(form):
    msg = Message(
        'New Contact Form Submission',
        sender='Elessar.nazgul@gmail.com',
        recipients='Elessar.nazgul@gmail.com'
    )
    msg.body= f"Name: {form.name.data}\nEmail: {form.email.data}\n\n{form.message.data}"