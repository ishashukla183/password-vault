# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 15:09:33 2022

@author: DELL
"""

import sqlite3             #Self contained file based SQL database to store all data
from tkinter import *      #for gui based apps
from functools import partial    #to pass argument to functions which will be called using buttons

FONT_STYLE =("Consolas", 19)             #pre defined styles
SMALL_FONT_STYLE = ("Consolas", 10)
BUTTON_FONT_STYLE = ("Consolas", 15)
#bgColor = "#001064"
bgColor = "#51C4D3"
#fgColor = "#F1F6F9"
fgColor = "#000000"
LoginId=""

def encrypt(data):                   #encrypt function to encrypt all usernames and passwords
    encrypted=""
    
    for i in range(len(data)):
        
        char=data[i]
        if char.isalpha():              #if character is alphabet
            encrypted+=chr(ord(char)+1)    #convert character into its ascii value and add 1
        elif char.isdigit():            #if character is number
            encrypted+=chr(ord(char)+1)    #convert character into its ascii value and add 1
        else : 
            encrypted+=char                      #keep the character in its original form
    return encrypted                  #return encrypted string
        
def decrypt(data):                        #decrypt function to encrypt all usernames and passwords
    decrypted=""
    
    for i in range(len(data)):
        
        char=data[i]
        if char.isalpha():
            decrypted+=chr(ord(char)-1)   #convert character into its ascii value and subtract 1
        elif char.isdigit():
            decrypted+=chr(ord(char)-1)  #convert character into its ascii value and subtract 1
        else : 
            decrypted+=char
    return decrypted       #return decrypted value

with sqlite3.connect("temporary.db") as db:   #Connect database
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(   
    ID INTEGER PRIMARY KEY NOT NULL,
    password TEXT NOT NULL
    );            
""")   #masterpassword table to store all master passwords in database
#Initiate window
win = Tk()
win.title("Password Vault")

def firstTimeScreen():
    for widget in win.winfo_children():
        widget.destroy()
        
    win.geometry("700x700")
    win.configure(bg = bgColor)
    
    label = Label(win, text="Enter Username", anchor = CENTER , bg = bgColor, fg = fgColor, font = FONT_STYLE)
    label.config(anchor = CENTER)
    label.grid(row = 0, column = 0 ,  padx = (170, 20), pady=(70, 0))
    
    txt2 = Entry(win, width = 50, font = SMALL_FONT_STYLE)
    txt2.grid(row = 1, column = 0, ipady = 5, ipadx = 5, padx = (170, 20), pady=(30, 0))
    txt2.focus()
    
    label = Label(win, text="Create Master Password", anchor = CENTER , bg = bgColor, fg = fgColor, font = FONT_STYLE)
    label.config(anchor = CENTER)
    label.grid(row = 2, column = 0 ,  padx = (170, 20), pady=(70, 0))
    
    txt = Entry(win, width = 50, font = SMALL_FONT_STYLE, show="*")
    txt.grid(row = 3, column = 0, ipady = 5, ipadx = 5, padx = (170, 20), pady=(30, 0))
    txt.focus()
    
    label1 = Label(win, text="Re-enter Master Password", bg = bgColor, fg = fgColor,  font = FONT_STYLE)
    label1.config(anchor = CENTER)
    label1.grid(row = 4, column = 0, padx = (170, 20), pady=(50, 0))
    
    txt1 = Entry(win, width = 50, font = SMALL_FONT_STYLE,show="*")
    txt1.grid(row = 5, column = 0,ipady = 5, ipadx = 5, padx = (170, 20), pady=(30, 0))
    txt1.focus()
    
    def savePassword():
       global LoginId 
       if txt.get() == txt1.get() :  #if re-enetred password is matched with created password
           LoginId=txt2.get()
           hashed = txt.get()
           hashedPassword=encrypt(hashed)  #password is converted in encrypted form to store in our database
           insert_password = """ INSERT INTO masterpassword (password)
           VALUES(?) """                     
           #password is inserted into masterpassword table 
           cursor.execute(insert_password, ((hashedPassword,)))
           db.commit()    #commit all changes
           passwordVault()   #to open password vault window
          
       else :  #if re-enetred password is not matched with created password
           label2 = Label(win,  fg = fgColor)
           label2.grid(row = 5, column = 0, padx = (150, 20), pady=(20, 0))
           label2.config(text="Passwords do not match")  
    def checkIfUsernameExists():
        usrnm = txt2.get()
        try:
            cursor.execute("""SELECT * FROM {0}""".format(usrnm))
            array = cursor.fetchall()
            label3 = Label(win, fg = fgColor,  font = SMALL_FONT_STYLE)
            label3.config(text = "Account with this username already exists.\n Enter a different username or login instead.")
            label3.grid(row = 6, column = 0, padx = (170, 20), pady=(50, 0))
        except:
            savePassword()
    btn = Button(win, text = "Sign Up",command = checkIfUsernameExists, font = BUTTON_FONT_STYLE)
    btn.grid(row = 6, column = 0, ipadx = 13, ipady = 3,  padx = (170, 20), pady=(30, 0))
    
    label2 = Label(win, text="Already an existing user?",  bg = bgColor, fg = fgColor,  font =SMALL_FONT_STYLE)
    label2.config(anchor = CENTER)
    label2.grid(row = 7, column = 0, padx = (87,0), pady=(30, 0))
    
    btn1 = Button(win, text = "Sign in",command = loginScreen, bg = bgColor, fg = fgColor, borderwidth = 0, font = SMALL_FONT_STYLE)
    btn1.grid(row = 7, column = 0, padx = (415,0), pady=(30,0), sticky = NW)
    
def loginScreen():
    for widget in win.winfo_children():
        widget.destroy()
        
    win.geometry("700x500")
    win.configure(bg = bgColor)
    label = Label(win, text="Enter Username", anchor = CENTER , bg = bgColor, fg = fgColor, font = FONT_STYLE)
    label.config(anchor = CENTER)
    label.grid(row = 0, column = 0 ,  padx = (170, 20), pady=(70, 0))
    
    txt2 = Entry(win, width = 50, font = SMALL_FONT_STYLE)
    txt2.grid(row = 1, column = 0, ipady = 5, ipadx = 5, padx = (170, 20), pady=(30, 0))
    txt2.focus()
    
    label = Label(win, text="Enter Master Password", bg = bgColor, fg = fgColor,  font = FONT_STYLE)
    label.config(anchor = CENTER)
    label.config(anchor = CENTER)
    label.grid(row = 2, column = 0 ,  padx = (170, 20), pady=(70, 0))
    
    txt = Entry(win, width = 50, font = SMALL_FONT_STYLE, show="*")
    txt.grid(row = 3, column = 0, ipady = 5, ipadx = 5, padx = (170, 20), pady=(30, 0))
    txt.focus()
    
    def getMasterPassword():
        HashedPassword = txt.get()    #this will store the entered password
        checkHashedPassword=encrypt(HashedPassword) #to convert into encrypted form as passwords are stored in encrypted form in database
        cursor.execute("SELECT * FROM masterpassword WHERE password = ?", [(checkHashedPassword)]) #to select data where the entered password is present
        return cursor.fetchall()  #if the password is present in masterpassword , fetch all data of that row
    
    def checkPassword():    #to check if login password is correct or not 
        global LoginId
        match = getMasterPassword()  #match will store data of password(if present in masterpassword table)
       
        if match:    #if match is not null , i.e. password is matched with the entered password
            LoginId=txt2.get()
            passwordVault()   #password vault window will be opened
        else:                 #if password is not matched 
            txt.delete(0, 'end')
            label1 = Label(win)
            label1.config(text="Incorrect password")   #'incorrect password' message will be shown to user
            label1.grid(row = 3, column = 0, padx = (170, 20), pady=(50, 0))
    
    btn = Button(win, text = "Log in",command = checkPassword, font = BUTTON_FONT_STYLE)
    btn.grid(row = 5, column = 0, ipadx = 13, ipady = 3,  padx = (170, 20), pady=(30, 0))
    
def passwordVault():
    global LoginId    #LoginId will be the name of each table for each user
    for widget in win.winfo_children():
        widget.destroy()
    
    win.configure(bg = bgColor)
   
    def addEntry():
        for widget in win.winfo_children():  #to clear previous widgets of the window
            widget.destroy()
        win.geometry("700x500")
        win.configure(bg = bgColor)
        label = Label(win, text="Associated with", bg = bgColor, fg = fgColor,  font = FONT_STYLE)
       
       
        label.grid(row = 0, column = 0 ,  padx = (180, 10), pady=(50, 20))
        
        txt = Entry(win,width = 50,  font = SMALL_FONT_STYLE)
        txt.grid(row = 1, column = 0, ipady = 5, ipadx = 5, padx = (150, 10))
        txt.focus()   
        label2 = Label(win, text="Username", bg = bgColor, fg = fgColor,  font = FONT_STYLE)
       
       
        label2.grid(row = 2, column = 0, padx = (180, 10), pady=(30, 20))
        
        txt2 = Entry(win, width = 50, font = SMALL_FONT_STYLE)
        txt2.grid(row = 3, column = 0, ipady = 5, ipadx = 5, padx = (150, 10))
        txt2.focus()   
        
        label3 = Label(win, text="Password", bg = bgColor, fg = fgColor,  font = FONT_STYLE)
        label3.config(anchor = CENTER)
       
        label3.grid(row = 4, column = 0, padx = (180, 10), pady=(30, 20))
        
        txt3 = Entry(win,width = 50, font = SMALL_FONT_STYLE)
        txt3.grid(row = 5, column = 0, ipady = 5, ipadx = 5, padx = (150, 10))
        txt3.focus()   
         
        
        def insertEntry():
            associated_with = encrypt(txt.get())  #encrypt all details to store in database file
            username = encrypt(txt2.get())
            password = encrypt(txt3.get())
            cursor.execute("""  
    CREATE TABLE IF NOT EXISTS {0}(                                 
    ID INTEGER PRIMARY KEY,
    associated_with TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL);              
    """.format(LoginId))  #here we are creating a unique table for each user which will store 4 entries , i.e a unique ID
                          #app name  , Username  and  password 
                          # if table is already created , details will get inserted in the same table
            insert_fields = """INSERT INTO {0}(associated_with, username, password)   
            VALUES(?, ?, ?)""".format(LoginId)                       #command to insert data into table
            cursor.execute(insert_fields, (associated_with, username, password))
            db.commit()
            passwordVault()  #this function is called again to show all details of user after inserting data
        
        btn = Button(win, text = "Submit",command = insertEntry, font = BUTTON_FONT_STYLE)
        btn.grid(row = 6, column = 0, ipadx = 13, ipady = 3,  padx = (200, 20), pady=(30, 0))  
    def removeEntry(input):
        cursor.execute("DELETE FROM {0} WHERE ID = ?".format(LoginId), (input,))  #deletes the data of whole row , i.e. particular 
        db.commit()                                                                    #app details  
        passwordVault()        #this function is called again to show all details of user after deleting
        
    win.geometry("1200x1000")
    win.configure(bg = bgColor)
    win.resizable(height = None, width = None)   
    label = Label(win, text="Password Vault", bg = bgColor, fg = fgColor,  font = FONT_STYLE)
    label.grid(column = 1)
    
    btn1 = Button(win, text="Add", command = addEntry, font = BUTTON_FONT_STYLE)
    btn1.grid(column = 1, pady=10, ipadx = 13, ipady = 3)
    
    label = Label(win, text="Associated with", bg = bgColor, fg = fgColor,  font = FONT_STYLE) 
    label.grid(row = 2, column = 0, padx = 80)
    
    label = Label(win, text="Username", bg = bgColor, fg = fgColor,  font = FONT_STYLE) 
    label.grid(row = 2, column = 1, padx = 80)
    
    label = Label(win, text="Password", bg = bgColor, fg = fgColor,  font = FONT_STYLE) 
    label.grid(row = 2, column = 2, padx = 80)
    
    cursor.execute("""SELECT * FROM {0}""".format(LoginId))  #to select table of particular user
    if(cursor.fetchall() != None):      #if no data is present in table user
        i = 0
        while(True):
            cursor.execute("""SELECT * FROM {0}""".format(LoginId))
            array = cursor.fetchall()                #will fetch all data of that table(username table)
            if(len(array)==0):      #if no data is present
                break
            lbl1 = Label(win, text = (decrypt(array[i][1])),bg = bgColor, fg = fgColor,  font = FONT_STYLE) #decrypted string
            lbl1.grid(column = 0, row = i+3)                                                               #will appear as label
            lbl1 = Label(win, text = decrypt(array[i][2]), bg = bgColor, fg = fgColor,  font = FONT_STYLE)
            lbl1.grid(column = 1, row = i+3)               #here i=row number , [1]=app name ,[2]=username, [3]=password
            lbl1 = Label(win, text = decrypt(array[i][3]), bg = bgColor, fg = fgColor,  font = FONT_STYLE)
            lbl1.grid(column = 2, row = i+3)
            
            btn = Button(win, text="Delete", command =partial(removeEntry, array[i][0]) , font = BUTTON_FONT_STYLE)
            btn.grid(column = 3, row = i+3, pady = 10, ipadx = 13, ipady = 3) #partial calles the function and passes argument in it
            i+=1     #to move on to next row
            cursor.execute("""SELECT * FROM {0}""".format(LoginId))   #to check if more entries are present
            if len(cursor.fetchall()) <= i :    #by checking length of rows
                break
firstTimeScreen()
win.mainloop()