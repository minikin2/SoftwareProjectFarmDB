
'''
Program name: Farm database
Author: Samantha Kolb
Date last updated: 7/19/2022
Synopsis: a createCon function that creates a connection with a database, 
        a closeConAndCur function that closes a connection and cursor,
        a getItemID function to get an item's number based off the item's number,
        a delete function to delete one single record from the database,
        an add function to add a single record to the database,
        an update function to update a single record in the database

'''
import sqlite3 
from sqlite3 import Error

#this function creates a connection with the database file passed to it
def createCon(dbFile):
    con = None
    try:
        con = sqlite3.connect(dbFile)
    except Error as error:
        print('There was an error opening the database: ' +  error)
        return -1
     
    return con    

#this function closes the connection and the cursor passed to it
def closeConAndCur(con, cursor):
    #close the cursor
    cursor.close()
    #close the connection
    con.close()
    return


#this function gets an item's id from the name
def getItemID(dbFile, name):
    con = createCon(dbFile)
    if con == -1:
        return -1

    try:
        #create a cursor
        cursor = con.cursor()
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
        return id  
    #if there is an error, rollback and return -1
    except Error as error:
        print("Error: ", error)
        print("Item not found")   
        return -1   

    finally:
        closeConAndCur(con, cursor)

    

   


#this function takes a db connection and an item name and deletes them
def delete(dbFile, num):
    con = createCon(dbFile)
     #create a cursor
    cursor = con.cursor()
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

def add(dbFile, name, qnt, desc, cate, unit, price):

    try:
        con = createCon(dbFile)
        #create a cursor
        cursor = con.cursor()
        #an insert into statement to insert the function parameters into the item table
        sql = "INSERT INTO Item (item_name, item_qnt, item_desc, item_cate, item_unit, item_price) VALUES ( '" + str(name) + "', " + str(qnt) + ", '" + str(desc) + "', '" + str(cate) + "', '" + str(unit) + "', " + str(price) + ");"
        #execute the statement 
        cursor.execute(sql)
         #commit the changes, SUCCESS!
        con.commit()
        print("Item successfully added")
    
    except Error as error:
        print("Error: ", error)
        print("Item not added")   
        con.rollback()

    closeConAndCur(con, cursor)
 
#function to update a record in the database 
def update(dbFile, num, name, qnt, desc, cate, unit, price):
    con = createCon(dbFile)
     #create a cursor
    cursor = con.cursor()
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
        if name != None or name != "":
            updateName = True
        if qnt != None or qnt != "":  
            updateQnt = True
        if desc != None or desc != "":    
            updateDesc = True
        if cate != None or desc != "":
            updateCate = True
        if unit != None or unit != "":
            updateUnit = True
        if price != None or price != "":
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


        #an update statement to update a row in the item table
        sql += " WHERE item_num = " + str(num) + ";"   
    #if there is an error, print the error and rollback
    except Error as error:
        print("Error: ", error)
        print("Item not updated")   
        con.rollback()
    #commit
    con.commit()
    print("Item " + str(num) + " successfully updated")
    #close the cursor
    closeConAndCur(con, cursor)
    return  

#this function returns a list of the items
def view(dbFile):
    con = createCon(dbFile)

    cursor = con.cursor()

    try:
        cursor.execute("SELECT * FROM Item;")
        items = cursor.fetchall()

    except Error as error:
        print("Error: ", error)
        print("Items cannot be viewed")
        items = []

    closeConAndCur(con, cursor)

    return items
            

#def checkNum(num):
    
#this just is a variable so that I don't have to type the database name over and over
dbFile = 'Becker Farms Inventory.db'

