
'''
Program name: Farm database
Author: Samantha Kolb
Date last updated: 7/21/2022
Synopsis: a createCon function that creates a connection with a database, 
        a closeConAndCur function that closes a connection and cursor,
        an isInt function to check if a variable is an int
        an isPriceValid function to check if a variable is a valid price
        an isSQL function to check for if a variable is a string of sql statements
        a getItemID function to get an item's number based off the item's number,
        a delete function to delete one single record from the database,
        an add function to add a single record to the database,
        an update function to update a single record in the database

'''
from ast import match_case
import decimal
from decimal import Decimal
import re
import sqlite3 
from sqlite3 import Error

ctx = decimal.getcontext()

ctx.prec = 2
ctx.rounding = decimal.ROUND_UP

#this function checks if the parameter is an integer or not, returns True or False
def isInt(num):
    if type(num) == int:
        return True
    else:
        return False 

#this function checks for if the parameter is a valid price, returns true if the parameter is a valid price, still needs a bit of work
def isPriceValid(num):
    if isInt(num) and num >= 0:
        return True
    pattern = re.compile(r"""^[0-9]+(\.[0-9]{1,2})?$""")
    result = pattern.search(str(num))
    return bool(result)


#this funtion checks a string for if it contains SQL which could cause problems, I'm working on it
def isSQL(s):
    str(s)
    pattern = re.compile(r"^")
    match = re.search("select", s)
    return


#this function creates a connection with the database file passed to it, returns -1 if there's an error
def createCon(dbFile):
    con = -1
    try:
        con = sqlite3.connect(dbFile)
    except Error as error:
        print('There was an error opening the database: ' +  error)
        return -1
     
    return con    

#this function creates a cursor from the connection given to it, returns -1 if there's an error
def createCur(con):
    cursor = -1
    try:
        cursor = con.cursor()
    except Error:
        print("Error")
        return -1
    return cursor

#this function closes the connection and the cursor passed to it, returns -1 if there's an error
def closeConAndCur(con, cursor):
    try:
        #close the cursor
        cursor.close()
        #close the connection
        con.close()
        return
    except Error:
        print("Error")
        return -1

#this function gets an item's id from the name
def getItemID(dbFile, name):
    con = createCon(dbFile)
    if con == -1:
        return -1

    try:
        #create a cursor
        cursor = createCur(con)
        #select statement to get the item id where the item name is the parameter
        sql = "SELECT item_num "
        sql += "FROM item "
        sql += "WHERE item_name LIKE '" + name + "';"
        cursor.execute(sql)

        l =  cursor.fetchall()

        if len(l) == 0:
            print("Item not found")
            return -1
        elif len(l) > 1:
            print("Warning: mulitple items discovered, only the first one will be altered")      
        id = l[0]
        num = id[0]
        return num  
    #if there is an error, rollback and return -1
    except Error as error:
        print("Error: ", error)
        print("Item not found")   
        return -1   

    finally:
        closeConAndCur(con, cursor)

#this function takes a db connection and an item name and deletes them
def deleteItem(dbFile, num):

    con = createCon(dbFile)
    if con == -1:
        return
     #create a cursor
    cursor = createCur(con)

    try:
        
        #delete statement 
        sql = "DELETE FROM item WHERE item_num = " + str(num) + ";"

        #execute the statement 
        cursor.execute(sql)
         #commit the changes, SUCCESS!
        con.commit()
        print("Item successfully deleted")
    #if there is an error let the user know and rollback    
    except Error as error:
        print("Error: ", error)
        print("Item not deleted")   
        con.rollback()

    closeConAndCur(con, cursor)

#this funtion takes a db connection and all of the attributes of the item table and adds a record with those attributes, returns 0 if all goes well, -1 if there is an error
def addItem(dbFile, name, qnt, desc, cate, unit, price):

    try:
        con = createCon(dbFile)
        if con == -1:
            return
        #create a cursor
        cursor = createCur(con)
        if not isInt(qnt):
            raise Error("Quantity must be a positive integer")
        if qnt < 0:
            raise Error("Quantity must be a positive integer")
        if not isPriceValid(price):
            raise Error("Price must be a positive number")
        else:
            #an insert into statement to insert the function parameters into the item table
            sql = "INSERT INTO Item (item_name, item_qnt, item_desc, item_cate, item_unit, item_price) VALUES ( '" + str(name) + "', " + str(qnt) + ", '" + str(desc) + "', '" + str(cate) + "', '" + str(unit) + "', " + str(price) + ");"
            #execute the statement 
            cursor.execute(sql)
            #commit the changes, SUCCESS!
            con.commit()
            print("Item successfully added")
            return 0
    
    except Error as error:
        print("Error: ", error)
        print("Item not added")   
        con.rollback()
        return -1

    finally:
        closeConAndCur(con, cursor)

 
#function to update a record in the database, returns 0 if it works, -1 if an error occurs
def updateItem(dbFile, num, name, qnt, desc, cate, unit, price):
    if int(num) == -1:
        return -1
    con = createCon(dbFile)
    if con == -1:
        return
     #create a cursor
    cursor = createCur(con)
    updateName = False
    updateQnt = False
    updateDesc = False
    updateCate = False
    updateUnit = False
    updatePrice = False     

    try:
       
        '''
        UPDATE item
SET item_qnt = 0, item_unit = 'single pkg'
WHERE item_name = 'Raw 3L';'''
        #start the sql statement
        sql = "UPDATE item Set "
        #if the variable is not null or "", we will update it, these variables will be used to create the update statement properly
        if name != None and name != "":
            updateName = True
        if qnt != None and qnt != "":  
            qnt = int(qnt)
            if not isInt(qnt):
                raise Error("Quantity must be a positive integer")
            if qnt < 0:
                raise Error("Quantity must be a positive integer")
            updateQnt = True
        if desc != None and desc != "":    
            updateDesc = True
        if cate != None and desc != "":
            updateCate = True
        if unit != None and unit != "":
            updateUnit = True
        if price != None and price != "":
            if not isPriceValid(price):
                raise Error("Price must be a positive number with no more than 2 decimal places")
            updatePrice = True            

        #these if statements go through and add the sql based on if there is another variable to be updated or not (if there is another variable then a comma is needed)
        if updateName and (updateQnt or updateDesc or updateCate or updateUnit or updatePrice):
            sql += "item_name = '" + str(name) + "', "
        else:
            sql += "item_name = '" + str(name) + "' "

        if updateQnt and (updateDesc or updateCate or updateUnit or updatePrice):
            sql += "item_qnt = " + str(qnt) + ", "
        else:
            sql += "item_qnt = " + str(qnt) + " "

        if updateDesc and (updateCate or updateUnit or updatePrice):
            sql += "item_desc = '" + str(desc) + "', "
        else:
            sql += "item_desc = '" + str(desc) + "' "

        if updateCate and (updateUnit or updatePrice):
            sql += "item_cate = '" + str(cate) + "', "
        else:
            sql += "item_cate = '" + str(cate) + "' "
        
        if updateUnit and updatePrice:
            sql += "item_unit = '" + str(unit) + "', "
        else:
            sql += "item_unit = '" + str(unit) + "' "

        if updatePrice:
            sql += "item_price = " + str(price) + " "

        #commit
        con.commit()
        print("Item " + str(num) + " successfully updated")
        #an update statement to update a row in the item table
        sql += " WHERE item_num = " + str(num) + ";"   
        return 0
    #if there is an error, print the error and rollback
    except Error as error:
        print("Error: ", error)
        print("Item not updated")   
        con.rollback()
        return -1
    except ValueError as e:
        print("Error: ", e)
        print("Item not updated")   
        con.rollback()
    finally:
        #close the cursor
        closeConAndCur(con, cursor)


#this function returns a list of all the items in the item table, if there is an issue or if there are no items, an empty list is returned
def view(dbFile):
    con = createCon(dbFile)

    cursor = createCur(con)

    try:
        cursor.execute("SELECT * FROM Item;")
        items = cursor.fetchall()

    except Error as error:
        print("Error: ", error)
        print("Items cannot be viewed")
        items = []

    closeConAndCur(con, cursor)

    return items
            
  
#this just is a variable so that I don't have to type the database name over and over
dbFile = 'Becker Farms Inventory.db'


