
'''
Program name: Farm database
Author: Samantha Kolb
Date last updated: 7/17/2022
Synopsis: basic delete, add and update statements
'''
import sqlite3 
from sqlite3 import Error

def createCon(dbFile):
    con = None
    try:
        con = sqlite3.connect(dbFile)
    except Error as error:
        print('There was an error opening the database: ' +  error)
        return -1
     
    return con    

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
        sql += "WHERE item_name LIKE '" + str(name) + "';"
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
        #close the cursor
        cursor.close()
         #close the connection
        con.close()

    

   


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

    #close the cursor
    cursor.close()    

   #close the connection
    con.close()

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

     #close the cursor
    cursor.close()    
    #close the connection
    con.close()

    return  
 

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
        #if the variable is not null, we will update it, this needs work, I'm not sure that my idea here works great
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
    cursor.close()    
    #close the connection
    con.close()

    return  

def view(dbFile):
    con = createCon(dbFile)

    cursor = con.cursor()


    for item in items()

def checkNum(num):
    if num    


#this just is a variable so that I don't have to type the database name over and over
dbFile = 'Becker Farms Inventory.db'
'''add('Becker Farms Inventory.db', "name", 1, "desc", "c", "unit", 10.00)
add('Becker Farms Inventory.db', "name", 1, "desc", "c", "unit", 10.00)
add('Becker Farms Inventory.db', "name", 1, "desc", "c", "unit", 10.00)'''

if createCon(dbFile) == -1:

    print("Sorry you'll have to retry")

 #these are operations on dummy items that have no meaning but can be added, deleted and updated however I want so I can test the functions   
else:
    print('Successfully opened the database ' + dbFile)  

    update(dbFile, 147, "Name", None, "ds", "", None, 10)

    id = getItemID(dbFile, "name")

    if bool(id) == False:
        print("cant do operations on a nonexistent item")

    else:

        num = id[0]

        update(dbFile, num, "", 1, "", None, "unit", None)

        id = getItemID(dbFile, "name")
        print(num)

        if getItemID(dbFile, "name") == -1:
            print("Sorry, you'll have to retry")

        else:

            #name, qnt, desc, cate, unit, price
            update(dbFile, num, "name", 0, None, None, "", "")
            add('Becker Farms Inventory.db', "name", 1, "desc", "c", "unit", 10.00)
            delete('Becker Farms Inventory.db', num)