import smtplib,ssl

from cowin_api import CoWinAPI
import os
from datetime import datetime
from email.message import EmailMessage
import traceback

#Getting current date
date = datetime.today().strftime('%d-%m-%y')

f= open("Vaccine_Slot.txt","w+")


def append_new_line(file_name, text_to_append):
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)
    file_object.close()


vaccine_info = ''
#Pincodes you want to enter
pin_codes = ['411007','412115','411006','411026']
min_age_limit = 18  # Optional. By default returns centers without filtering by min_age_limit 

cowin = CoWinAPI()

for i in range(len(pin_codes)):
    # print(pin_codes[i],min_age_limit)
    available_centers = cowin.get_availability_by_pincode(pin_codes[i],date ,min_age_limit)
    # print(available_centers)
    if(len(available_centers['centers']) > 1):
        for j in range (len(available_centers['centers'])):
            for k in range (len(available_centers['centers'][j]['sessions'])):
                if(available_centers['centers'][j]['sessions'][k]['available_capacity'] == 0):
                    continue
                else:
                    cen_info = 'Name: '+ available_centers['centers'][j]['name'] +' Address: '+ available_centers['centers'][j]['address'] + ' Fee Type: ' + available_centers['centers'][j]['fee_type']
                    if(vaccine_info != cen_info):
                        vaccine_info = cen_info
                        append_new_line('Vaccine_Slot.txt',vaccine_info)    
                    slots_info = 'Vaccine Type: ' + available_centers['centers'][j]['sessions'][k]['vaccine'] +' Date: '+ available_centers['centers'][j]['sessions'][k]['date'] +' available_capacity: '+ str(available_centers['centers'][j]['sessions'][k]['available_capacity'])
                # print(slots_info)
                    append_new_line('Vaccine_Slot.txt',slots_info)
f.close()
if(os.stat("Vaccine_Slot.txt").st_size == 0):
    print("Any message")
    os.remove("Vaccine_Slot.txt")  
else:
    with open('Vaccine_Slot.txt') as fp:
        msg = EmailMessage()
        msg.set_content(fp.read())
        fp.close()
    os.remove("Vaccine_Slot.txt")    
    msg['Subject'] = f'The contents of Vaccine'
    msg['From'] = 'senders_email_id'
    msg['To'] = 'reciever_email_id'
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "senders_email_id"
    password = 'Pass"'
# Create a secure SSL context
    context = ssl.create_default_context()
# log into server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo()
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.send_message(msg)
        print('Email Sent')
    except Exception as e:
    # Print any error or exception messages to stdout
        print('Code broke')
        traceback.print_exc()
    finally:
        server.quit() 
        
