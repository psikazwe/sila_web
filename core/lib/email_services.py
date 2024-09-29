from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage

def send_email(recipient, subject, template_name, context=None):
    """
    Sends an email to the specified recipient using an HTML template.

    :param recipient: The email address of the recipient.
    :param subject: The subject of the email.
    :param template_name: The name of the HTML template to use for the email body.
    :param context: A dictionary containing the context to render the template with.
    """
    # Render the HTML template with the provided context
    html_content = render_to_string(template_name, context)

    # You can customize the sender's email address here.
    # If not specified, Django will use the DEFAULT_FROM_EMAIL setting.
    sender = settings.DEFAULT_FROM_EMAIL

    # Create the email message
    email = EmailMultiAlternatives(subject, '', sender, [recipient])
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send()

def send_email_with_attachment(subject, message, from_email, recipient_list, attachment_path):
    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list
    )
    email.attach_file(attachment_path)
    email.send()