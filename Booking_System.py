import pandas as pd
from pandas import DataFrame
import os.path
import time

rooms = {}
days = []
schedule = {}

#takes a string of what is displayed to the user before the input, an array of expected inputs
def getStringChoice(text,expected):
    validInput = False
    while not validInput:
        print("\n" * 50)#clears screen
        choice = input(text)
        # makes the choice lowercase to handle any capitalisation errors
        if type(choice) == int or type(choice) == float:
            print("\nPlease do not input any numbers")
        else:
            choice = choice.lower()
        if choice in expected:
            validInput = True
        else:
            print("\nYour input was invalid")
        time.sleep(1)#adds wait time for the user to be able to read any error messages that appear
    return choice

#takes a string of what is displayed to the user before the input, and an array of expected inputs
def getIntChoice(text, expected):
    validInput = False
    while not validInput:
        print("\n" * 50)#clears screen
        choice = input(text)
        if " " in choice:
            print("\nPlease take care not to input a space")
        elif "." in choice:
            print("\nPlease input a whole number")
        elif choice.isnumeric():
            choice = int(choice)
            if choice in expected:
                validInput = True
            else:
                print("\nYour input was invalid")
        else:
            print("\nPlease input a number")
        time.sleep(1)  # adds wait time for the user to be able to read any error messages that appear
    return choice

#makes the default rooms for the program
def makeRooms():
    rooms = {}
    roomNames = ["endeavour", "galileo", "python", "voyager"]
    for roomName in roomNames:
        rooms[roomName] = []
        for i in range(1,4):
            rooms[roomName].append("e")
    return rooms

#creates default roomschedule, default resources, and days
def makeSchedule():
    rooms = makeRooms()
    days = ["monday", "tuesday"]
    for room in rooms:
        schedule[room] = {}
        for day in days:
            schedule[room][day] = {}
            for i in range(1,8):
                schedule[room][day][i] = "a"
    return days, schedule

#lets user create a booking
def createBooking(rooms, schedule):
    #this is a common header used by each text input for the text interface
    header = """
1.Create Booking
--------------------------"""

    #gets the day for the booking from the user
    text = header+"\nPlease input the day you want your booking to be on\n"
    i = 1
    for day in days:
        text = text + day
        if i != len(days):
            text = text + ", "#this gap is only added for days that are not at the end, for formatting
        i += 1

    text = text + "\n\nPlease enter your choice here: "
    day = getStringChoice(text, days)

    #gets the period for the booking from the user
    text = header+"\nPlease input the period you want your booking to be on\n1, 2, 3, 4, 5, 6, 7\n\nPlease enter your choice here: "
    period = getIntChoice(text, [1,2,3,4,5,6,7])

    #gets the room for the booking from the user
    text = header+"\nPlease input the room you want to book\nEach room has the resources available listed next to it\n"
    expected = []
    roomAvailable = False
    for room in rooms:
        roomAdded = False
        if schedule[room][day][period] == "a":#only adds the available rooms to the expected input from the user
            expected.append(room)
            roomAvailable = True
            for resource in rooms[room]:#firstly checks if there is a space available before adjusting the input
                if not roomAdded:
                    text = text + "\n" + room
                    roomAdded = True
                if resource != "e":
                    text = text + ":"
                    i = 1
                    for resource in rooms[room]:
                        if resource != "e":
                            text = text + " " + resource
                            if i != 3:
                                text = text + ","
                            i += 1
                    break

    if roomAvailable:
        text = text + "\n\nPlease enter your choice here: "
        room = getStringChoice(text, expected)

        #checks if a room is available
        if schedule[room][day][period] == "a":
            schedule[room][day][period] = "b"
            print(header + "\nYou have booked " + room + " for period " + str(period) + " on " + day + ".")
        else:
            print(header+"\n"+room+"is already booked for your requested time slot\n"+"Period:"+str(period)+" on " + day)

    else:
        print(header +"\n\nThere are no rooms available for " + period + " on " +day)
    time.sleep(3)
    return schedule

#lets user delete a booking
def deleteBooking(rooms, schedule):
    header = """
2.Delete Booking
--------------------------"""

    # gets the day of the booking to be deleted from the user
    text = header + "\nPlease input the day of the booking you want to delete\n"
    i = 1
    for day in days:
        text = text + day
        if i != len(days):
            text = text + ", "  # this gap is only added for days that are not at the end, for formatting
        i += 1

    text = text + "\n\nPlease enter your choice here: "
    day = getStringChoice(text, days)

    # gets the period of the booking to be deleted from the user
    text = header + "\nPlease input the period of the booking you want to delete\n1, 2, 3, 4, 5, 6, 7\n\nPlease enter your choice here: "
    period = getIntChoice(text, [1, 2, 3, 4, 5, 6, 7])

    # gets the room of the booking to be deleted from the user
    text = header + "\nPlease input the room of the booking you want to delete"
    expected = []
    for room in rooms:
        if schedule[room][day][period] == "b":  # only adds the booked rooms to the expected input from the user
            expected.append(room)
            text = text + "\n" + room

    # if there are no bookings to be deleted, the user does not need to input the day of the booking
    if len(expected) == 0:
            print(header+"\n\nThere are no bookings made for this room for period " + str(period) + " on " + day)
            time.sleep(5)
    else:
        text = text + "\n\nPlease enter your choice here: "
        room = getStringChoice(text, expected)

        # checks if a room is already booked
        if schedule[room][day][period] == "b":
            schedule[room][day][period] = "a"
            print(header + "\nYou have deleted the booking for " + room + " for period " + str(period) + " on " + day + ".")
        else:
            print(header + "\nThe booking for " + room + " for period " + str(period) + " on " + day + "\ndid not exist")
        time.sleep(3)

    return schedule

#enables the user to either add or remove a resource
def changeRoomDescription(rooms):
    header = """
4.Edit Room Description
-------------------------"""
    #either enables the user to proceed if they enter the correct password or lets them go back
    validPassword = False
    tries = 3
    while not validPassword:
        choice = input(header+"\nThis action requires a password, if you wish to go back enter 'back'\n\nPlease enter the password here:")
        if choice == "back":
            break #exits loop without enabling the user to change resources which is reserved for admin users
        elif choice == "admin":
            validPassword = True
        else:
            print("\nInvalid Password")
            time.sleep(5)
            tries -= 1
            if tries == 0:
                choice = "back"

    #only enables the user to change resources if they enter the admin password
    if validPassword:
        text = header+"\nPlease enter the name of the room you want to change the description of"
        expected = []
        #creates the choices available for the user
        for room in rooms:
            expected.append(room)
            text = text + "\n" + room
        text = text + "\n\nPlease Enter your choice here: "

        room = getStringChoice(text, expected)

        resources = rooms[room]#a list of all the resources is extracted from the rooms dictionary

        spaceForResources = False
        for item in resources:
            if item == "e":
                spaceForResources = True

        actionPerformed = False
        while not actionPerformed:
            text = header+"\nDo you wish to\n1.Add a resource\n2.Remove a resource\n\nPlease enter your choice here: "
            #choice is taken as an integer when both options are available
            choice = getIntChoice(text, [1,2])

            if choice == 1:
                if spaceForResources:
                    validResource = False
                    while not validResource:
                        text = header+"\nPlease enter the name of the resource you wish to add\n\nPlease enter your input here: "
                        resource = input(text)
                        if len(resource) > 30:
                            print("Please input a name for the resource that has no more than 30 characters")
                        elif len(resource) < 2:
                            print("Please input a resource with at least 2 characters")
                        elif resource in resources:
                            print("This resource already exists in this room, please input a different resource")
                        else:
                            validResource = True
                            actionPerformed = True
                        time.sleep(2)
                    for slot in rooms[room]:
                        if slot == "e":
                            pos = rooms[room].index(slot)
                            rooms[room][pos] = resource
                            print(header+ "\n" + resource +" has been added to the room " + room)
                            break #prevents every available slot from being taken up
                else:
                    print(header+ "\nThere are already 3 resources in this room, therefore no more can be added")

            elif choice == 2:
                counter = 1
                options = []
                text = header+"\nThe following resources are in this room: "
                # creates the text displayed to the user
                for resource in resources:
                    if resource != "e":
                        text = text + "\n"+ str(counter)+"." + str(resource)
                        options.append(resource)
                        counter += 1
                if len(options) == 0:
                    print(header+ "\nThere are no resources in this room to be removed")
                else:
                    text = text + "\n\nPlease enter the name of the resource you wish to remove"

                    resource = getStringChoice(text, options)#integer choice of the user is obtained
                    pos = rooms[room].index(resource)
                    rooms[room][pos] = "e"#removes the resource from the list
                    print(header+ "\n" + resource + " has been removed from the room " + room)
                actionPerformed = True
            time.sleep(5)
    return rooms

def viewBookings(schedule, days):
    gap = 10

    header = """
3.View Bookings
--------------------------"""
    text = header + "\nPlease enter the day you want to view"+"\n("
    for day in days:
        text = text + day
        if days.index(day) != (len(days)-1):#prevents the last item from having a comma
            text = text + ","

    text = text +")\n\nPlease enter your choice here: "
    day = getStringChoice(text, days)

    print(" "*(int(gap+0.5*gap)-1), end="")
    for i in range(1,8):
        print("P"+str(i) + " "*(gap-len(str(i))-1), end = "")
    print("")#prints a new line
    for room in schedule:
        print(room + " "*(10-len(room)),end = "")
        i = 1
        for period in schedule[room][day]:
            if schedule[room][day][period] == "a":#available rooms are shown as blank spaces
                displayVal = ""
            else:
                displayVal = "  booked"
            if i == 7:#makes sure the last item does not have a comma
                print(displayVal+" " * (gap - len(displayVal)-2))
            else:
                print(displayVal+" " * (gap - len(displayVal)-2), end =", ")
            i += 1
    temp = input("\nPress enter to exit")#let's the user to decide when to exit

#displays choices to user and handles the decisions for what is done after a choice is made
def menu(rooms, days, schedule):
    exit = False
    while not exit:
        text = """\nAda Room Booking System
--------------------
1.Create Booking
2.Delete Booking
3.View Bookings
4.Admin

0.Exit

Enter your choice here:"""
        choice = getIntChoice(text, [1,2,3,4,0])
        if choice == 1:
            schedule = createBooking(rooms, schedule)
            writeBookingsCSV(schedule)
        elif choice == 2:
            schedule = deleteBooking(rooms, schedule)
            writeBookingsCSV(schedule)
        elif choice == 3:
            viewBookings(schedule, days)
        elif choice == 4:
            rooms = changeRoomDescription(rooms)
            writeResourcesCSV(rooms)
        elif choice == 0:
            exit = True

#writes the schedule to the csv file
def writeBookingsCSV(schedule):
    columns=["P1","P2","P3","P4","P5","P6","P7"]
    data = pd.DataFrame()
    for room in rooms:
        for day in schedule[room]:
            for i in range(1,8):
                index = room+" "+day
                column = columns[i-1]
                value = schedule[room][day][i]
                data.set_value(index=index, col=column,value=value)
    data.to_csv("bookings.csv",mode="w+",index=True)

#reads schedule in the bookings.csv file
def readBookingsCSV(rooms):
    data = pd.read_csv("C:\\Users\Student\Documents\GitHub\python\\Unit_24_Booking_System\.idea\\bookings.csv",index_col=0)
    days = []
    rooms = []
    period = ["P1","P2","P3","P4","P5","P6","P7"]
    for index in data.index:
        if "monday" in index:
            index = index.replace(" monday", "")
            rooms.append(index)

    for index in data.index:
        if rooms[0] in index:
            day = index.replace(rooms[0] + " ", "")
            days.append(day)

    for room in rooms:
        schedule[room] = {}
        for day in days:
            schedule[room][day] = {}
            for i in range(1,8):
                index = room+" " + day
                column = period[i-1]
                schedule[room][day][i] = data.at[index, column]
    return days,schedule

#writes the resources each room has into the resources.csv file
def writeResourcesCSV(rooms):
    index = [1,2,3]
    data = pd.DataFrame(columns=rooms, index=index)
    for room in rooms:
        i = 1
        for resource in rooms[room]:
            data.set_value(index= i, col=room, value = resource)
            i += 1
    data.to_csv("resources.csv", mode="w+", index=True)

#reads the resources.csv file and creates the rooms dictionary which contains the resources each room holds
def readResourcesCSV():
    data = pd.read_csv("C:\\Users\Student\Documents\GitHub\python\\Unit_24_Booking_System\.idea\\resources.csv", index_col=0)
    rooms = {}
    roomNames = data.columns
    for roomName in roomNames:
        rooms[roomName] = []
        for i in range(1,4):
            value = data.at[i, roomName]
            rooms[roomName].append(value)
    return rooms

#checks if the resources file exists to initialise variables
if os.path.isfile("C:\\Users\Student\Documents\GitHub\python\\Unit_24_Booking_System\.idea\\resources.csv"):
    rooms = readResourcesCSV()
else:
    rooms = makeRooms()#creates a default template of the rooms

#checks if the bookings file exists to initialise variables
if os.path.isfile("C:\\Users\Student\Documents\GitHub\python\\Unit_24_Booking_System\.idea\\bookings.csv"):
    days, schedule = readBookingsCSV(rooms)
else:
    days, schedule = makeSchedule()#creates a default template for the rooms

menu(rooms, days, schedule)
