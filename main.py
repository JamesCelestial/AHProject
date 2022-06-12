# James McCaffery 2022 | Advanced Higher Computing Project



from cProfile import label
from cgitb import text
from operator import length_hint
from pydoc import doc
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.font import BOLD
from turtle import width
import pyodbc
import time
import warnings
from PIL import Image, ImageTk
import os

folder = os.getcwd()
path = (folder + '\QuestionDatabase.accdb') # Allows me to locate the question database as long as the .py file is in the same folder


# Let's connect to the Microsoft Access database and initalise our cursor.
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % path)
crsr = conn.cursor()


class AccountObject(): # Building account object, which will be able to be written into accounts.txt 
    def __init__(self):
        self.username = ""
        self.password = ""
        self.highscore = 0

CurrentAccount = AccountObject()

class QuestionObject(): # Building Question object
    def __init__(self):
        self.qNo = 0
        self.Level = ""
        self.Question = ""
        self.Difficulty = ""
        self.Answer = ""
        self.Explanation = ""

# Getting amount of questions
crsr.execute("SELECT * FROM Questions")
tempvar = crsr.fetchall()
count = len(tempvar)

QuestionsArray = []


# Re-executing query to go back to the start of the table and getting questions from database
for i in range(0, count):
    crsr.execute("SELECT * FROM Questions WHERE QuestionNo = " + str(i+1))
    result = crsr.fetchone()

    qNoResult = str(result[0])
    levelResult = int(result[1])
    questionResult = str(result[2]) 
    answerResult = str(result[3])
    explanationResult = str(result[4])  


    tempQuestion = QuestionObject() # Creating the object 
    tempQuestion.qNo = qNoResult
    tempQuestion.Level = levelResult
    tempQuestion.Question = questionResult
    tempQuestion.Answer = answerResult
    tempQuestion.Explanation = explanationResult

    QuestionsArray.append(tempQuestion) # Adding objects to array!

# I'm going to sort the Questions from easiest - hardest. To do this, I'm using a bubble sort on my array of objects by Question.Level
def bubbleSort(arr):
    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j].Level > arr[j+1].Level:
                tempval = arr[j].Level
                arr[j].Level = arr[j+1].Level
                arr[j+1].Level = tempval
    return arr

sortedQuestionArray = bubbleSort(QuestionsArray)

############# -- CODING USER INTERFACE -- #############
## FIRST PAGE SET UP ##
# firstPage window
firstPage = tk.Tk()
firstPage.geometry("240x100")
firstPage.title('Welcome')
firstPage.resizable(0, 0)

# configure the grid
firstPage.columnconfigure(0, weight=1)
firstPage.columnconfigure(1, weight=1)
firstPage.columnconfigure(2, weight=1)





## LOGIN PAGE SET UP ##
# loginPage window
loginPage = tk.Toplevel()
loginPage.geometry("450x150")
loginPage.title("Login")
loginPage.resizable (0,0)
loginPage.withdraw() # hide this page initially


# configure the grid
loginPage.columnconfigure(0, weight=1)
loginPage.columnconfigure(1, weight=3)
loginPage.columnconfigure(2, weight=1)





## REGISTER PAGE SET UP ##
# registerPage window
registerPage = tk.Toplevel()
registerPage.geometry("700x150")
registerPage.title("Register")
registerPage.resizable (0,0)
registerPage.withdraw() # hide this page initially


# configure the grid
registerPage.columnconfigure(0, weight=1)
registerPage.columnconfigure(1, weight=1)
registerPage.columnconfigure(2, weight=1)





## HOME PAGE SET UP ##
# homePage window
homePage = tk.Toplevel()
homePage.geometry("700x400")
homePage.title("Home")
homePage.resizable (0,0)
homePage.withdraw() # hide this page initially

# configure the grid
homePage.columnconfigure(0, weight=1)
homePage.columnconfigure(1, weight=1)
homePage.columnconfigure(2, weight=1)
homePage.columnconfigure(3, weight=1)
homePage.columnconfigure(4, weight=1)

homePage.rowconfigure(1, weight=0)
homePage.rowconfigure(2, weight=1)
homePage.rowconfigure(3, weight=1)
homePage.rowconfigure(4, weight=1)
homePage.rowconfigure(5, weight=1)
homePage.rowconfigure(6, weight=1)
homePage.rowconfigure(7, weight=1)
homePage.rowconfigure(8, weight=1)
homePage.rowconfigure(9, weight=1)






## QUIZ PAGE SET UP ##
# registerPage window
quizPage = tk.Toplevel()
quizPage.geometry("500x500")
quizPage.title("Quiz")
quizPage.resizable (0,0)
quizPage.withdraw() # hide this page initially

# configure the grid
quizPage.columnconfigure(0, weight=1)
quizPage.columnconfigure(1, weight=1)
quizPage.columnconfigure(2, weight=1)
quizPage.columnconfigure(3, weight=1)
quizPage.columnconfigure(4, weight=1)

quizPage.rowconfigure(1, weight=0)
quizPage.rowconfigure(2, weight=1)
quizPage.rowconfigure(3, weight=1)
quizPage.rowconfigure(4, weight=1)
quizPage.rowconfigure(5, weight=1)

## LOGIN / REGISTER SYSTEM FUNCTIONS ##
def clickLogin():
    firstPage.withdraw()
    loginPage.deiconify()

def clickRegister():
    firstPage.withdraw()
    registerPage.deiconify()

def backToFirstFromLogin():
    loginPage.withdraw()
    firstPage.deiconify()

def backToFirstFromRegister():
    registerPage.withdraw()
    firstPage.deiconify()

def readAccountsIntoPArrays():
    accountFile = open("accounts.txt", "r")
    uA = []
    pA = []
    sA = []

    for line in accountFile.readlines():
        lineStrip = line.strip()
        splitLine = lineStrip.split(",")
        username = splitLine[0]
        password = splitLine[1]
        score = splitLine[2]

        uA.append(username)
        pA.append(password)
        sA.append(score)

    for i in range(len(sA)): # Removing the /n from the end of each score, which existed due to the nature of the text file
        sA[i].strip("/n")

    return uA, pA, sA

def saveData(account): # Takes an "account" parameter and saves it's data
    pass

def enterHomePage():
    loginPage.withdraw()
    homePage.deiconify()

    highScoreMessage = ("Hello " + str(CurrentAccount.username) + " , your highscore is: " + str(CurrentAccount.highscore))
    highScoreLabel = ttk.Label(homePage, text=highScoreMessage, font="Helvetica")
    highScoreLabel.grid(column=2, row=1, padx=5, pady=0)
    # Here, I configure the message at the top of the homepage. I do it here because if I do it outside of a function, it runs at the start of the program
    # When CurrentAccount's details are empty, but at this point in the program it should be accurate.

def login():
    usernameArray, passwordArray, scoreArray = readAccountsIntoPArrays()

    enteredUser = str(usernameEntry.get())
    enteredPass = str(passwordEntry.get())

    accountFound = False

    for i in range(len(usernameArray)):
        if usernameArray[i] == enteredUser:
            if enteredPass == passwordArray[i]:
                # Validated login
                print("HERE")
                accountFound = True
                message = "Success"
                loginResultMessage.config(text=message)

                # Set CurrentAccount variable

                global CurrentAccount
                CurrentAccount.username = enteredUser
                CurrentAccount.password = enteredPass
                CurrentAccount.highscore = scoreArray[i]

                print(CurrentAccount.username)
                enterHomePage()

            else:
                # Correct username, incorrect password
                message = "Incorrect password!"
                loginResultMessage.config(text=message)

    if not accountFound:
        message = "User not found!"
        loginResultMessage.config(text=message)
        print("this")


def register():
    usernameArray, passwordArray, scoreArray = readAccountsIntoPArrays()


    enteredNewUser = str(newUsernameEntry.get())
    enteredNewPass = str(newPasswordEntry.get())
    enteredConfirmation = str(confirmPasswordEntry.get())

    # First, check that the entered password/username meets conditions
    condition1 = False # CONDITION 1 = Contains capital letter
    condition2 = False # CONDITION 2 = 8+ letters
    condition3 = False # CONDITION 3 = Confirmation field = entry field
    condition4 = False # CONDITION 4 = Username is original


    for i in range(0, len(enteredNewPass)):
        if enteredNewPass[i].isupper():
            condition1 = True

    if len(enteredNewPass) >= 8:
        condition2 = True

    if enteredConfirmation == enteredNewPass:
        condition3 = True
    
    if enteredNewUser not in usernameArray:
        condition4 = True

    # All conditions true, assign fields to Account object and write to file
    if condition1 and condition2 and condition3 and condition4:
        newAccount = AccountObject()
        newAccount.username = enteredNewUser
        newAccount.password = enteredNewPass

        with open("accounts.txt","w") as writefile:
            for i in range(len(usernameArray)): # Write the existing account data back into the file before addng the new one in
                writefile.write(usernameArray[i] + "," + passwordArray[i] + "," + str(scoreArray[i]) + '\n')
            writefile.write(newAccount.username + "," + newAccount.password + "," + "0")

        message = "Success!"
        registerResultMessage.config(text=message)

    # Username already taken
    elif condition4 == False:
        message = "Username already taken!"
        registerResultMessage.config(text=message) 


    # Username available but password invalid
    elif condition4 and condition1 == False or condition2 == False or condition3 == False:
        message = "ERROR: Please ensure your password is 8 or more characters \n and includes a capital, and is the same in both fields."
        registerResultMessage.config(text=message) 


def standardQuiz():
    homePage.withdraw()
    quizPage.deiconify()

    global num # Will keep track of what question we're on and use it to display the according question details
    num = 0
    
    global score # Keep track of score
    score = 0

    def exit():
        firstPage.destroy()

    def clickTrue():
        global num
        global score
        if sortedQuestionArray[num].Answer == "True":
            score += 1
        num += 1

        if num+1 > count: # Finished questions
            qNumber.config(text="Finished!")
            questionLabel.config(text="YOU REACHED THE END! You got " + str(score) + "/" + str(count))

            trueButton.destroy()
            falseButton.destroy()

            exitButton = ttk.Button(quizPage, text="Back to home", command=exit) # Close the app
            exitButton.grid(column=2,row=4)

            if score > int(CurrentAccount.highscore): # Save high score
                usernameArray, passwordArray, scoreArray = readAccountsIntoPArrays()
                for i in range(len(usernameArray)): # Linear search through username array, locate player and update corresponding score
                    if usernameArray[i] == CurrentAccount.username:
                        scoreArray[i] = score

                with open("accounts.txt","w") as writefile:
                    for i in range(len(usernameArray)): # Write the new account data back into the file
                        writefile.write(usernameArray[i] + "," + passwordArray[i] + "," + str(scoreArray[i]) + '\n')

        else:
            questionLabel.config(text=sortedQuestionArray[num].Question)
            qNumber.config(text=(str(num+1) + "/" + str(count))) # Display the new question and question number
        
    def clickFalse():
        global num
        global score
        if sortedQuestionArray[num].Answer == "False":
            score += 1
        num += 1

        if num+1 > count: # Finished questions
            qNumber.config(text="Finished!")
            questionLabel.config(text="YOU REACHED THE END! You got " + str(score) + "/" + str(count))

            trueButton.destroy()
            falseButton.destroy()

            exitButton = ttk.Button(quizPage, text="Back to home", command=exit) # Close the app
            exitButton.grid(column=2,row=4)

            if score > int(CurrentAccount.highscore): # Save high score
                usernameArray, passwordArray, scoreArray = readAccountsIntoPArrays()
                for i in range(len(usernameArray)): # Linear search through username array, locate player and update corresponding score
                    if usernameArray[i] == CurrentAccount.username:
                        scoreArray[i] = score
                        
                with open("accounts.txt","w") as writefile:
                    for i in range(len(usernameArray)): # Write the new account data back into the file
                        writefile.write(usernameArray[i] + "," + passwordArray[i] + "," + str(scoreArray[i]) + '\n')

        else:
            questionLabel.config(text=sortedQuestionArray[num].Question)
            qNumber.config(text=(str(num+1) + "/" + str(count))) # Display the new question and question number

    qNumber = ttk.Label(quizPage,text=("1" + "/" + str(count)))
    qNumber.grid(column=2,row=1)

    questionLabel = ttk.Label(quizPage,text=sortedQuestionArray[0].Question)
    questionLabel.grid(column=2,row=2)

    trueButton = ttk.Button(quizPage,text="TRUE",command=clickTrue)
    trueButton.grid(column=1,row=4)

    falseButton = ttk.Button(quizPage,text="FALSE",command=clickFalse)
    falseButton.grid(column=3,row=4)


    

## DECORATING PAGES - Adding all labels and buttons, except the quiz which is decorated in the standardQuiz function.
# First page
# welcome
welcomeText = ttk.Label(firstPage, text="Welcome to James' Quiz!")
welcomeText.grid(column=1, row=0, padx=3,pady=3)

# login
loginOption = ttk.Button(firstPage, text="LOGIN", command=clickLogin)
loginOption.grid(column=1, row=1, padx=3, pady=3)

# register
registerOption = ttk.Button(firstPage, text="REGISTER", command=clickRegister)
registerOption.grid(column=1, row=2, padx=3, pady=3)





# Login page
# username
usernameLabel = ttk.Label(loginPage, text="Username:")
usernameLabel.grid(column=0, row=0, padx=5, pady=5)

usernameEntry = ttk.Entry(loginPage)
usernameEntry.grid(column=1, row=0, padx=5, pady=5)

# password
passwordLabel = ttk.Label(loginPage, text="Password:")
passwordLabel.grid(column=0, row=1, padx=5, pady=5)

passwordEntry = ttk.Entry(loginPage, show="*")
passwordEntry.grid(column=1, row=1, padx=5, pady=5)

# login button
loginButton = ttk.Button(loginPage, text="Login",command=login)
loginButton.grid(column=1, row=2, padx=5, pady=5)

# back button
backButton = ttk.Button(loginPage, text="Back", command=backToFirstFromLogin)
backButton.grid(column=0, row=2, padx=5, pady=5)

# Error/success message template - will be edited depending on error's occuring in registration, initially empty
loginResultMessage = ttk.Label(loginPage, text="") 
loginResultMessage.grid(column=2, row=1,padx=5, pady=5)





# Register page
# username
newUsernameLabel = ttk.Label(registerPage, text="Choose a username:")
newUsernameLabel.grid(column=0, row=0, padx=5, pady=5)

newUsernameEntry = ttk.Entry(registerPage)
newUsernameEntry.grid(column=1, row=0, padx=5, pady=5)

# password
newPasswordLabel = ttk.Label(registerPage, text="Enter new password:")
newPasswordLabel.grid(column=0, row=1, padx=5, pady=5)

newPasswordEntry = ttk.Entry(registerPage,  show="*")
newPasswordEntry.grid(column=1, row=1, padx=5, pady=5)

# confirm password
confirmPasswordLabel = ttk.Label(registerPage, text="Confirm password:")
confirmPasswordLabel.grid(column=0, row=2, padx=5, pady=5)

confirmPasswordEntry = ttk.Entry(registerPage, show="*")
confirmPasswordEntry.grid(column=1, row=2, padx=5, pady=5)

# register button
registerButton = ttk.Button(registerPage, text="Register",command=register)
registerButton.grid(column=1, row=3, padx=5, pady=5)

# back button
backButton = ttk.Button(registerPage, text="Back", command=backToFirstFromRegister)
backButton.grid(column=0, row=3, padx=5, pady=5)

# Error/success message template - will be edited depending on error's occuring in registration, initially empty
registerResultMessage = ttk.Label(registerPage, text="") 
registerResultMessage.grid(column=2, row=1,padx=5, pady=5)





# Home page
# High score display
standardQuizButton = ttk.Button(homePage, text="Standard Quiz",command=standardQuiz)
standardQuizButton.grid(column=2,row=4)

homeWelcome = ttk.Label(homePage, text=("Welcome to James' ADVANCED HIGHER COMPUTING PROJECT? Can you complete the quiz?"), font="Helvetica 11 bold")
homeWelcome.grid(column=2,row=3)

img = ImageTk.PhotoImage(Image.open('compsci.png').resize((125, 125))) 
image_label = ttk.Label(
    homePage,
    image=img,
    padding=5
)

image_label.grid(column=2,row=2)



firstPage.mainloop()
loginPage.mainloop()
registerPage.mainloop()
homePage.mainloop()
quizPage.mainloop()