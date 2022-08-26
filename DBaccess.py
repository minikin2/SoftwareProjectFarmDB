'''
Program name: Farm database
Author: Samantha Kolb
Date last updated: 7/21/2022
Functions: a createCon function that creates a connection with a database, 
        a createCur function that creates a cursor with the connection given it
        a closeConAndCur function that closes a connection and cursor,
        an isInt function to check if a variable is an int
        an isPriceValid function to check if a variable is a valid price
        an isSQL function to check for if a variable is a string of sql statements
        a getItemID function to get an item's number based off the item's number,
        a deleteItem function to delete one single record from the database,
        an addItem function to add a single record to the database,
        an updateItem function to update a single record in the database
        a viewItems function to return a list of all the values in the item table

        the delete, add, and update functions will all return 0 if everything executes, and an error message if there is an error of some kind
        the view function will return a list if everything executes, and an error message if not
        the delete function parameters are: the database file, and the item_num to be deleted (2 parameters)
        the add function parameters are: the database file, the item name, quantity, description, category, unit, and price (7 parameters)
        the update function parameters are: the database file, the item number, name, quantity, description, category, unit, and price (8 parameters) 
            it is almost the same as the add fuction, just with the item number in between the database file and the name

'''
import re
import sqlite3 
from sqlite3 import Error


#this function checks if the parameter is an integer or not, returns True or False
def isInt(num):
    num = str(num)
    try:
        num = int(num)
        return True
    except ValueError:
        return False

#this function checks for if the parameter is a valid price, returns true if the parameter is a valid price
def isPriceValid(num):
    pattern = re.compile(r"""^[0-9]+(\.[0-9]{1,2})?$""")
    result = pattern.search(str(num))
    return bool(result)

#this funtion checks a string for if it contains SQL which could cause problems, if everything is ok, will return None
def isSQL(s):
    pattern = r"(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|JOIN|ALTER|GROUP BY|ORDER BY|;)"
    result = re.search(pattern, str(s), re.IGNORECASE)
    if result != None:
        raise ValueError("SQL found")
    return result

#this function creates a connection with the database file passed to it, returns -1 if there's an error
def createCon(dbFile):
    con = -1
    try:
        con = sqlite3.connect(dbFile)
    except Exception:
        raise Exception("Connection issue")
     
    return con    

#this function creates a cursor from the connection given to it, returns -1 if there's an error
def createCur(con):
    cursor = -1
    try:
        cursor = con.cursor()
    except Exception:
        raise Exception("Cursor issue")
    return cursor

#this function closes the connection and the cursor passed to it, returns -1 if there's an error
def closeConAndCur(con, cursor):
    try:
        #close the cursor
        cursor.close()
        #close the connection
        con.close()
        return
    except Exception:
        raise Exception("Closing issue")

#this function gets an item's id from the name
def getItemID(dbFile, name):

    try:
        con = createCon(dbFile)
         #create a cursor
        cursor = createCur(con)
        
        if type(name) != str:
            raise ValueError("Invalid name")
        isSQL(name)
        #select statement to get the item id where the item name is the parameter
        sql = "SELECT item_num "
        sql += "FROM item "
        sql += "WHERE item_name LIKE '" + name + "';"
        cursor.execute(sql)

        l = cursor.fetchall()

        if len(l) == 0:
            raise ("Item not found")
        #elif len(l) > 1:
            #print("Warning: mulitple items discovered, only the first one will be altered")      
        id = l[0]
        num = id[0]
        return num  

    except ValueError as error:
        e = "Error: " + str(error) + ". Incorrect value supplied."
        con.rollback()
        return e      
    #if there is an error, return the error and rollback
    except Exception as error:
        e = "Error: " + str(error) + ". Item not selected"
        con.rollback()
        return e  

    finally:
        closeConAndCur(con, cursor)

#this function takes a db connection and an item name and deletes them, returns 0 if all goes well, and an error message otherwise
def deleteItem(dbFile, num):

    try:
        #create a connection
        con = createCon(dbFile)

        #create a cursor
        cursor = createCur(con)
  #
        if not isInt(num) or int(num) <= 0:
            raise Error("Item number not valid")
#
        isSQL(num) 
        selectsql = "SELECT MAX(rowid) from item;"
        cursor.execute(selectsql)
        c = cursor.fetchone()
        id = c[0]
        if int(num) > id:
            raise Error("Item not in the database")
        #delete statement 
        sql = "DELETE FROM item WHERE item_num = " + str(num) + ";"

        #execute the statement 
        cursor.execute(sql)
         #commit the changes, SUCCESS!
        con.commit()
        #print("Item successfully deleted")
        return 0
    #if there is an error, return the error and rollback
    except Error as error:
        e = "Error: " + str(error) + ". Item not deleted"
        con.rollback()
        return e
    except ValueError:
        e = "Error: the value supplied is not a correct value. " + "Item not deleted"
        con.rollback()
        return e
    except NameError as error:
        e = "Error: " + str(error) + ". Item not deleted"
        con.rollback()
        return e
    finally:
        closeConAndCur(con, cursor)

#this funtion takes a db connection and all of the attributes of the item table and adds a record with those attributes, returns 0 if all goes well, and an error message otherwise
def addItem(dbFile, name, qnt, desc, cate, unit, price):

    try:
        con = createCon(dbFile)

        #create a cursor
        cursor = createCur(con)

        if not isInt(qnt):
            raise Error("Quantity must be a positive integer")
        if int(qnt) < 0:
            raise Error("Quantity must be a positive integer")
        if not isPriceValid(price):
            raise Error("Price must be a positive number, e.g. 14.20")
        isSQL(name)
        isSQL(desc)
        isSQL(cate)
        isSQL(unit) 
     
        #making sure there is an actual name
        if name == "":
            raise Error("No item name provided")
        if unit == "":
            raise Error("No item unit provided")
        #an insert into statement to insert the function parameters into the item table
        sql = "INSERT INTO Item (item_name, item_qnt, item_desc, item_cate, item_unit, item_price) VALUES ( '" + str(name) + "', " + str(qnt) + ", '" + str(desc) + "', '" + str(cate) + "', '" + str(unit) + "', " + str(price) + ");"
        #execute the statement 
        cursor.execute(sql)
        #commit the changes, SUCCESS!
        con.commit()
        #print("Item successfully added")
        return 0
    
    #if there is an error, return the error and rollback
    except Exception as error:
        e = "Error: " + str(error) + ". Item not added"
        con.rollback()
        return e

    finally:
        closeConAndCur(con, cursor)
 
def updateName(dbFile, num, name):
    try:
        con = createCon(dbFile)
        cursor = createCur(con)

        if type(num) != int:
            raise TypeError("Item number is not valid")
        if num < 0:
            raise ValueError("Item number is not valid")
        isSQL(name)    
        selectsql = "SELECT MAX(rowid) from item;"
        cursor.execute(selectsql)
        c = cursor.fetchone()
        id = c[0]
        if num > id:
            raise IndexError("Item not in the database")
        #start the sql statement
        sql = "UPDATE item Set item_name = '" + str(name) + "' WHERE item_num = "
        sql += str(num)
        sql += ";"
        cursor.execute(sql)
        #commit
        con.commit()
        return 0

    except Exception as error:
        e = "Error: " + str(error) + ". Item not updated"
        con.rollback()
        return e      
    finally:
        #close the cursor
        closeConAndCur(con, cursor)        

#function to update a record in the database, returns 0 if it works, and an error message otherwise
def updateItem(dbFile, num, qnt, desc, cate, unit, price):

    try:
        con = createCon(dbFile)
        if con == -1:
            raise Error("connection issue")
        #create a cursor
        cursor = createCur(con)
        if cursor == -1:
            raise Error("cursor issue")
        updateName = False
        updateQnt = False
        updateDesc = False
        updateCate = False
        updateUnit = False
        updatePrice = False     

        #start the sql statement
        sql = "UPDATE item Set "
        if type(num) != int:
            raise TypeError("Item number is not valid")
        if num < 0:
            raise ValueError("Item number is not valid")
        selectsql = "SELECT MAX(rowid) from item;"
        cursor.execute(selectsql)
        c = cursor.fetchone()
        id = c[0]
        if num > id:
            raise IndexError("Item not in the database")

        #if the variable is not null or "", we will update it, these variables will be used to create the update statement properly
        '''if name != "" and name != None:
            if isSQL(name) != None:
                raise Error("That is not a valid name")'''
        updateName = True
        if qnt != "" and qnt != None:  
            if not isInt(qnt):
                raise Error("Quantity must be a positive integer")
            if int(qnt) < 0:
                raise Error("Quantity must be a positive integer")
            updateQnt = True
        if desc != "" and desc != None:    
            if isSQL(desc) != None:
                raise Error("That is not a valid description")
            updateDesc = True
        if cate != "" and cate != None:
            if isSQL(cate) != None:
                raise Error("That is not a valid category")
            updateCate = True
        if unit != "" and unit != None:
            if isSQL(unit) != None:
                raise Error("That is not a valid unit")
            updateUnit = True
        if price != "" and price != None:
            if not isPriceValid(price):
                raise Error("Price must be a positive number with no more than 2 decimal places")
            updatePrice = True            
        if not updateName and not updateQnt and not updateDesc and not updateCate and not updateUnit and not updatePrice:
            raise Error("No information provided")

        #these if statements go through and add the sql based on if there is another variable to be updated or not (if there is another variable then a comma is needed)
        '''if updateName and (updateQnt or updateDesc or updateCate or updateUnit or updatePrice):
            sql += "item_name = '" + str(name) + "', "
        elif updateName and not (updateQnt or updateDesc or updateCate or updateUnit or updatePrice):
            sql += "item_name = '" + str(name) + "' "'''

        if updateQnt and (updateDesc or updateCate or updateUnit or updatePrice):
            sql += "item_qnt = " + str(qnt) + ", "
        elif updateQnt and not (updateDesc or updateCate or updateUnit or updatePrice):
            sql += "item_qnt = " + str(qnt) + " "

        if updateDesc and (updateCate or updateUnit or updatePrice):
            sql += "item_desc = '" + str(desc) + "', "
        elif updateDesc and not (updateCate or updateUnit or updatePrice):
            sql += "item_desc = '" + str(desc) + "' "

        if updateCate and (updateUnit or updatePrice):
            sql += "item_cate = '" + str(cate) + "', "
        elif updateCate and not (updateUnit or updatePrice):
            sql += "item_cate = '" + str(cate) + "' "
        
        if updateUnit and updatePrice:
            sql += "item_unit = '" + str(unit) + "', "
        elif updateUnit and not updatePrice:
            sql += "item_unit = '" + str(unit) + "' "

        if updatePrice:
            sql += "item_price = " + str(price) + " "

        sql += " WHERE item_num = " + str(num) + ";"   
        cursor.execute(sql)
        #commit
        con.commit()
        #print("Item " + str(num) + " successfully updated")
        return 0
    except Exception as error:
        e = "Error: " + str(error) + ". Item not updated"
        con.rollback()
        return e

    finally:
        #close the cursor
        closeConAndCur(con, cursor)

#this function returns a list of all the items in the item table, if there is an issue or if there are no items, an error message is returned
def viewItems(dbFile):
    con = createCon(dbFile)

    cursor = createCur(con)

    try:
        cursor.execute("SELECT * FROM Item;")
        items = cursor.fetchall()

    except Error as error:
        e = "Error: " + str(error) + ". Items not viewable"
        return e

    finally:
        #close the cursor
        closeConAndCur(con, cursor)

    return items

def viewByCate(dbFile, cate):

    try:
        con = createCon(dbFile)

        cursor = createCur(con)
        if isSQL(cate) != None:
            raise ValueError("That is not a valid name")
        sql ="SELECT * FROM Item WHERE Item.item_cate LIKE '" + cate + "';"
        cursor.execute(sql)   
        items = cursor.fetchall() 
        if len(items) == 0:
            raise IndexError("The category does not exist")
    except Exception as error:
        e = "Error: " + str(error) + ". Items not viewable"
        return e

    finally:
        #close the cursor
        closeConAndCur(con, cursor)

    return items

#this function selects all the item names and quantities or if a category is specified then only names and quantites from that category will be selected
def viewqnt(dbFile, cate):

    try:
        con = createCon(dbFile)

        cursor = createCur(con)
        if type(cate) != str:
            raise ValueError("That is not a valid name.")

        sql = "SELECT item_name, item_qnt FROM Item "
        if cate != "" and cate != None:
            if isSQL(cate) != None:
                raise ValueError("That is not a valid name.")
            sql += "WHERE item_cate LIKE '" + cate + "'"
        sql += ";"
        cursor.execute(sql)
        items = cursor.fetchall()
        if len(items) == 0:
            raise IndexError("The category does not exist.")

    except Exception as error:
        e = "Error: " + str(error) + " Error viewing quantities"
        return e

    finally:
        #close the cursor
        closeConAndCur(con, cursor)

    return items

def view_an_item(dbFile, num):

    try:
        con = createCon(dbFile)

        cursor = createCur(con)   
        if type(num) != int:
            raise TypeError("Item number is not valid.")
        if num < 0:
            raise ValueError("Item number is not valid.")
        selectsql = "SELECT MAX(rowid) from item;"
        cursor.execute(selectsql)
        c = cursor.fetchone()
        id = c[0]
        if num > id:
            raise IndexError("Item not in the database")

        sql = "SELECT * FROM Item WHERE Item_num = " + str(num)
        sql += ";"
        cursor.execute(sql)
        items = cursor.fetchone()

    except Exception as error:
        e = "Error: " + str(error) + " Item not viewable"
        return e

    finally:
        #close the cursor
        closeConAndCur(con, cursor)

    return items


dbFile = 'Becker Farms Inventory.db'


#print(updateItem(dbFile, getItemID(dbFile, 'Thick Hickory Bacon'), "Thickory", "", "", "", "", ""))
'''
print(updateName(dbFile, '5', 5))

print(updateName(dbFile, 4, 'Cube'))

print(updateName(dbFile, 100, 'k'))'''
'''
print(updateName(dbFile, 110, 'Whole Fresh Side'))
print(updateName(dbFile, 111, 'Whole Sm Belly'))
print(updateName(dbFile, 112, 'Bulk Jowl'))
print(updateName(dbFile, 113, 'Sm Ham'))
print(updateName(dbFile, 114, 'Fresh Ham'))
print(updateName(dbFile, 115, 'Bulk Wh Chicken'))
print(updateName(dbFile, 116, 'Bulk Ch Wings'))
print(updateName(dbFile, 117, 'Bulk LQ'))
print(updateName(dbFile, 118, 'Bulk B/S Thighs'))
print(updateName(dbFile, 119, 'Bulk B/S Breasts'))''''''
print(updateName(dbFile, 120, 'Bulk T Drums'))
print(updateName(dbFile, 121, 'Bulk Gr Turkey'))
print(updateName(dbFile, 122, '3L'))
print(updateName(dbFile, 126, 'Veal Chuck'))
print(updateName(dbFile, 128, 'Veal Sirloin Steak'))
print(updateName(dbFile, 129, 'Veal NY'))''''''
print(updateName(dbFile, 130, 'Veal Rib Chop'))
print(updateName(dbFile, 131, 'Veal Filet'))
print(updateName(dbFile, 132, 'Veal Gr Beef'))
print(updateName(dbFile, 133, 'Veal Ribs'))'''

#testing addItem
#def addItem(dbFile, name, qnt, desc, cate, unit, price):
#this should not add
print(addItem(dbFile, "test", "t", "t", "t", "t", "t"))
print(addItem(dbFile, "test", -3, "t", "t", "t", "t"))
print(addItem(dbFile, "test", 2, "t", "t", "t", "t"))
print(addItem(dbFile, "test", 2, "t", "t", "t", -3))
print(addItem(dbFile, "test", 2, "t", "t", "t", 1.222))
print(addItem(dbFile, "n", 5, "d", "c", "", 2.2))
print(addItem(dbFile, "", 5, "d", "c", "u", 2.2))
#this should add
addItem(dbFile, "test", 2, "t", "t", "t", 111.22)
addItem(dbFile, "test", 2, "t", "t", "t", 2.2)
addItem(dbFile, "test", 2, "t", "t", "t", 5)

print(addItem(dbFile, "test", 2, "", "t", "t", 5))