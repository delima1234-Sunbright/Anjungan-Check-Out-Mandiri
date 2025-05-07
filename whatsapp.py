import os 
from twilio.rest import Client 

client = Client()
from_whatsapp_number = 'whatsapp:+14155238886'
to_whatsapp_number = 'whatsapp:+6281269461717'
client.messages.create (body='Ahoy World!',
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
