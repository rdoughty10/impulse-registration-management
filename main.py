import csv
import json 
import sys
import pandas as pd
import imaplib
import email
import os
import base64

def getFileFromEmail():
    email_user = input('Email: ')
    email_pass = input('Password: ')
    filePath = ''

    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(email_user, email_pass)

    mail.select("Inbox")
    mail.list()
    result, data = mail.uid('search', None, "ALL")
    inbox_item_list = data[0].split()

    subject = ''
    emailLoc = -1
    while (subject != "Submissions data for Classes Payment"):
        emails = inbox_item_list[emailLoc]
        result2, email_data = mail.uid('fetch', emails, '(RFC822)')
        raw_email = email_data[0][1].decode("utf-8")
        email_message = email.message_from_string(raw_email)
        subject = email_message['Subject']
        print("Testing email: ", subject)
        if (subject == "Submissions data for Classes Payment"):
            print("EMAIL FOUND")

            for part in email_message.walk():
                # this part comes from the snipped I don't understand yet... 
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()
                if bool(fileName):
                    filePath = os.path.join('/Users/ryand/impulse-data/', fileName)
                    print(filePath)
                    if not os.path.isfile(filePath) :
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                    print("Downloaded " + fileName + " from email titled " + email_message['Subject'])
            break
        emailLoc -= 1
    return filePath

registration = getFileFromEmail()
print(registration)

with open(registration, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader)

    studentInformation = []
    studentInformationCSV = []
    for line in csv_reader:
        #get the data that I want
        parentName = line[1] + ' ' + line[2]
        parentEmail = line[9]
        parentPhoneNumber = line[10]
        classes = line[11]
        studentName = line[15] + ' ' + line[16]
        studentEmail = line[18]
        studentAge = line[17]
        studentSchool = line[19]

        #array for adding to student record json
        student = {"StudentName": studentName, "StudentEmail": studentEmail, "StudentSchool": studentSchool, "StudentAge": studentAge, "Classes": classes, "ParentName": parentName, "ParentEmail": parentEmail, "ParentPhoneNumber": parentPhoneNumber}
        studentInformation.append(student)


#dump the student information data into json and csv file
with open("C:/Users/ryand/impulse-data/student_information.json", "w") as write_file:
    json.dump(studentInformation, write_file, indent=4)

#initiate full email list with two lists, parent and student
all_parent_emails = [sub['ParentEmail'] for sub in studentInformation]
all_student_emails = [sub['StudentEmail'] for sub in studentInformation]
parent_and_student_emails = all_parent_emails + all_student_emails
all_emails = {"Full Email List": parent_and_student_emails, "Parent Emails": all_parent_emails, "Student Emails": all_student_emails}

with open("C:/Users/ryand/impulse-data/full_email_list.json", "w") as write_file2:
    json.dump(all_emails, write_file2, indent=4)


classes = []
#for each student, get the class they are in
for student in studentInformation:
    studentClass = student['Classes']
    studentEmail = student['StudentEmail']
    parentEmail = student['ParentEmail']

    #then find where that class is stored and store their email in it
    classFound = False
    for classEmailList in classes:
        specificClass = classEmailList['Class']
        if (specificClass == studentClass):
            classFound = True
            classEmailList["Emails"][0].append(studentEmail)
            classEmailList["Emails"][1].append(parentEmail)


    #if class is not found in classes list of class email lists, create a new email list with the class title and add that to the classes list
    if (not classFound):
        class_student_emails = []
        class_student_emails.append(studentEmail)
        class_parent_emails = []
        class_parent_emails.append(parentEmail)

        class_emails = []
        class_emails.append(class_student_emails)
        class_emails.append(class_parent_emails)

        classEmailList = {"Class": studentClass}
        classEmailList["Emails"] = class_emails

        
        classes.append(classEmailList)
print(classes)


with open("C:/Users/ryand/impulse-data/class_email_lists.json", "w") as write_file3:
    json.dump(classes, write_file3, indent=4)


#plan to add csv file support




#loop through classes, if there is one that already exist then add the email to that list, else create a list with the name of that class and add the emails to those classes
#add all the classes list to another more encompassing list
#dump these onto a json file
#maybe make a students json file and an email list json file

#2 - Parent Name
#3 - Parent Last Name
#9 - Parent Email
#11 - Classes
#13 - Student First Name
#14 - Student Last Name
#16 - Student Email

    