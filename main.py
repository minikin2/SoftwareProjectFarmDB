'''A Farm Market  web app that keep record of produce 
    and inventory
    Author: Ndubuisi, Jennifer, Samantha and Rajinder
    Date: 07/25/2022
    Synopsis: An inventory control application, which will allow the user to enter in information to add, delete, or update a database, the user can also view the items in the database.
'''
from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk


from DBaccess import addItem, deleteItem, getItemID, updateItem, view_an_item, viewItems, viewByCate, viewqnt, updateName


#main window
root = Tk()
root.title("Becker Farms Inventory Management")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 1650 
height = 1000
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(1, 1)
root.config(bg='teal')
#e7b771
#e7a971

dbFile = 'Becker Farms Inventory.db'

# It getting data from clients and adding them to csv file 
def additem():

#add listbox for category
    # the values of items are being fetched
    e2=entry2.get()
    e3=entry3.get()
    e4=entry4.get()
    e5=entry5.get()
    e6=entry6.get()
    e7=entry7.get()
   
    if entry2.get()=="" or entry3.get()=="" or entry5.get()=="" or entry6.get()=="":

        #print("Error")
        tkMessageBox.showerror("Error","Something went wrong, try again")

    else:
        result=tkMessageBox.askquestion("Submit","You are about to enter following details\n" + e2 + "\n" + e3 + "\n" + e4 + "\n" + e5 + "\n" + e6 + "\n" + e7)
        clearitem()
        
        if(result =="yes"):
            r = addItem('Becker Farms Inventory.db', e2, e3, e4, e5, e6, e7)
            if r == 0:
                tkMessageBox.showinfo("Success!", "Item successfully added")
            else:
                tkMessageBox.showerror("Error", r)
    viewitems()

#delete function     
def deleteitem():
##    tree.delete(*tree.get_children())
    e1=entry1.get()
   
    if entry1.get()=="":
        #print("Error")
        tkMessageBox.showerror("Error","Something went wrong, try again")
    else:
        result=tkMessageBox.askquestion("Submit","You are about to delete the item\n" + e1)

        if(result =="yes"):
            r = deleteItem(dbFile, e1)
            if r == 0:
                tkMessageBox.showinfo("Success!", "Item successfully deleted")
            else:
                tkMessageBox.showerror("Error", r)
    
            entry1.delete(0, END)
    viewitems()
    
#update function (can update anything but the name)
def updateitem():
    # items are being updated
    name=entry1.get()

    if name=="":

        #print("Error")
        tkMessageBox.showerror("Error","Something went wrong, try again")
    else:
        result=tkMessageBox.askquestion("Submit","You are about to update the item \n" + name)

        if(result =="yes"):

            ent1 = Entry(Forms, textvariable=ItemName, width=30)
            ent1.grid(row=0, column=1) 
            ent2 = Entry(Forms, textvariable=Quantity, width=30)
            ent2.grid(row=1, column=1)
            ent3 = Entry(Forms, textvariable=Description, width=30)
            ent3.grid(row=2, column=1)
            ent4 = Entry(Forms, textvariable=Category, width=30)
            ent4.grid(row=3, column=1)
            ent5 = Entry(Forms, textvariable=Unit, width=30)
            ent5.grid(row=4, column=1)
            ent6 = Entry(Forms, textvariable=Price, width=30)
            ent6.grid(row=5, column=1)
            e1 = ent1.get()
            e2=ent2.get()
            e3=ent3.get()
            e4=ent4.get()
            e5=ent5.get()
            e6=ent6.get()
          
            r = updateItem("Becker Farms Inventory.db", getItemID("Becker Farms Inventory.db", name), e2, e3, e4, e5, e6)
            if r == 0:
                tkMessageBox.showinfo("Success!", "Item successfully updated")
            else:
                tkMessageBox.showerror("Error", r)

            clearitem()
    viewitems()

#this pulls up another window to edit an item name
def editname():
    #window for editing an item name
    editwin = Toplevel()
    editwin.title("Edit name")

    editwin.geometry('345x155')
    editwin.resizable(0, 0)
    editwin.config(bg='#fef2da')

    global oldn
    global newn

    oldName = StringVar()
    newName = StringVar()
    labeln = Label(editwin, text="Current Name:", bg = "#fef2da", fg='teal',font=('arial', 16), bd=15)
    labeln.grid(row=0, stick="e")
    labelnn = Label(editwin, text="New Name:", bg = "#fef2da", fg='teal',font=('arial', 16), bd=15)
    labelnn.grid(row=1, stick="e")

    oldn = Entry(editwin, textvariable=oldName, width=25)
    oldn.grid(row=0, column=1) 
    newn = Entry(editwin, textvariable=newName, width=25)
    newn.grid(row=1, column=1)    

    enter_e = Button(editwin, bg = "tan", activebackground="teal", width = 8, text = "Enter", command = editname)
    enter_e.grid(row = 2, column= 0)
    clear_e = Button(editwin, bg = "tan", activebackground="teal", width = 8, text = "Clear", command = clearnames)
    clear_e.grid(row = 2, column = 1)
    editwin.mainloop()
    getNameInfo()
    viewitems()


def getNameInfo():

    o = oldn.get()
    n = newn.get()
    if(o == "" or n == ""):
        tkMessageBox.showerror("Error","there is missing info")
    else:
        result=tkMessageBox.askquestion("Submit","You are about to update the item name from '" + o + "' to '" + n + "'")

        if(result =="yes"):
            r = updateName("Becker Farms Inventory.db", getItemID("Becker Farms Inventory.db", o), n)
            if r == 0:
                tkMessageBox.showinfo("Success!", "Item successfully updated")
            else:
                tkMessageBox.showerror("Error", r)      


#this clears the names from the edit names window    
def clearnames():
    oldn.delete(0, END)
    newn.delete(0, END)


def viewitem():
    tree.delete(*tree.get_children())
    item = view_an_item('Becker Farms Inventory.db', entry1.get())
    if type(item) == str:
       tkMessageBox.showerror("Error", item)

    tree.insert(parent = "", index = END, iid = 1, text = "", values = (item[1], item[2], item[3], item[4], item[5], item[6]))

# To the view all the items in the datbase
def viewitems():
    tree.delete(*tree.get_children())
    l = viewItems('Becker Farms Inventory.db')
    if type(l) == str:
       tkMessageBox.showerror("Error", l)
    else:
        i = 0
        for item in l:
            i += 1
            tree.insert(parent = "", index = END, iid = i, text = "", values = (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
        

#to view the items by category            
def viewbycategory():
    e4 = entry4.get()  
    tree.delete(*tree.get_children())
    l = viewByCate('Becker Farms Inventory.db', e4)
    if type(l) == str:
       tkMessageBox.showerror("Error", "Something went wrong, try again")
    else:
        i = 0
        for item in l:
            i += 1
            tree.insert(parent = "", index = END, iid = i, text = "", values = (item[1], item[2], item[3], item[4], item[5], item[6]))

#to view only the quantities and names of items, the user may or may not specify a category
def viewQandN():
    e4 = entry4.get()
    tree.delete(*tree.get_children())
    l = viewqnt('Becker Farms Inventory.db', e4)
    if type(l) == str:
       tkMessageBox.showerror("Error", "Something went wrong, try again") 
    else:
        i = 0
        for item in l:
            i += 1
            tree.insert(parent = "", index = END, iid = i, text = "", values = (item[0], item[1]))

# A clear button to clear the data in the entries
def clearitem():
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)
    entry7.delete(0, END)

# string variables
ItemNum = IntVar()
ItemName = StringVar()
Quantity = StringVar()
Description = StringVar()
Category = StringVar()
Unit=StringVar()
Price=StringVar()


# each widget created are appended to the window frame
Top = Frame(root, width=900, height=50 ,bd=8, relief="raise")
Top.pack(side=TOP)
Left = Frame(root, width=200, bg="#fef2da",height=500, bd=4, relief="raise")
Left.pack(side=LEFT)
Right = Frame(root, width=700, bg="#fef2da", height=500,bd=4, relief="raise")
Right.pack(side=RIGHT)
Forms = Frame(Left, width=300, bg="#fef2da", height=450)
Forms.pack(side=TOP)
Buttons = Frame(Left, width=300, bg = "#fef2da", height=250, bd=8)
Buttons.pack(side=BOTTOM)

# adding widget for all the entry data
txt_title = Label(Top, width=900, font=('arial', 24), fg='teal', bg="#fef2da", text = "Becker Farms Inventory Management")
txt_title.pack()
label0 = Label(Forms, text="Item Number:", fg='teal',bg="#fef2da",font=('arial', 16), bd=15)
label0.grid(row=0, stick="e")
label1 = Label(Forms, text="Item Name:",fg='teal', bg="#fef2da",font=('arial', 16), bd=15)
label1.grid(row=1, stick="e")
label2 = Label(Forms, text="Quantity:",fg='teal', bg="#fef2da",font=('arial', 16), bd=15)
label2.grid(row=2, stick="e")
label3 = Label(Forms, text="Description:",fg='teal', bg="#fef2da",font=('arial', 16), bd=15)
label3.grid(row=3, stick="e")
label4 = Label(Forms, text="Category:",fg='teal', bg="#fef2da",font=('arial', 16), bd=15)
label4.grid(row=4, stick="e")
label5 = Label(Forms, text="Unit:",fg='teal', bg="#fef2da",font=('arial', 16), bd=15)
label5.grid(row=5, stick="e")
label5 = Label(Forms, text="Price:",fg='teal', bg="#fef2da",font=('arial', 16), bd=15)
label5.grid(row=6, stick="e")



entry1 = Entry(Forms, textvariable=ItemNum, width=30)
entry1.grid(row=0, column=1) 
entry2 = Entry(Forms, textvariable=ItemName, width=30)
entry2.grid(row=1, column=1)
entry3 = Entry(Forms, textvariable=Quantity, width=30)
entry3.grid(row=2, column=1)
entry4 = Entry(Forms, textvariable=Description, width=30)
entry4.grid(row=3, column=1)
entry5 = Entry(Forms, textvariable=Category, width=30)
entry5.grid(row=4, column=1)
entry6 = Entry(Forms, textvariable=Unit, width=30)
entry6.grid(row=5, column=1)
entry7 = Entry(Forms, textvariable=Price, width=30)
entry7.grid(row=6, column=1)


btn_add = Button(Buttons, activebackground='teal', bg= "tan", width=8, text="Add", command=additem).pack(side=LEFT)
btn_delete = Button(Buttons, activebackground='teal', bg= "tan", width=8, text="Delete", command=deleteitem).pack(side=LEFT)
btn_update = Button(Buttons, activebackground='teal', bg= "tan", width=8, text="Update", command=updateitem ).pack(side=LEFT)
btn_editname = Button(Buttons, activebackground='teal', bg= "tan", width=10, text="Edit name", command=editname).pack(side=LEFT)
btn_clear = Button(Buttons, activebackground='teal', bg= "tan", width=8, text="Clear", command=clearitem).pack(side=LEFT)
btn_view = Button(Buttons, activebackground='teal', bg= 'tan', width= 8, text= 'Refresh', command= viewitems).pack(side=LEFT)
btn_viewbycate = Button(Buttons, activebackground='teal', bg= "tan", width=15, text="View By Category", command=viewbycategory).pack(side=LEFT)
btn_viewqnt = Button(Buttons, activebackground='teal', bg= "tan", width = 13, text="View Quantities", command=viewQandN).pack(side=LEFT)
btn_viewitem = Button(Buttons, activebackground='teal', bg= "tan", width = 15, text="View An Item", command=viewitem).pack(side =LEFT)

scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=( 'ItemNum', "ItemName", "Quantity", "Description", "Category", "Unit", "Price"),
                    selectmode="extended", height=700, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

tree.heading('ItemNum', text= 'Item Number', anchor=W)
tree.heading('ItemName', text="Item Name", anchor=W)
tree.heading('Quantity', text="Quantity", anchor=W)
tree.heading('Description', text="Description", anchor=W)
tree.heading('Category', text="Category", anchor=W)
tree.heading('Unit', text="Unit", anchor=W)
tree.heading('Price', text="Price", anchor=W)


tree.column('#0', stretch=NO, minwidth=20, width=0)
tree.column('#1', stretch=YES, minwidth=0, width=90)
tree.column('#2', stretch=NO, minwidth=0, width=130)
tree.column('#3', stretch=NO, minwidth=0, width=60)
tree.column('#4', stretch=NO, minwidth=0, width=360)
tree.column('#5', stretch=NO, minwidth=0, width=75)
tree.column('#6', stretch=NO, minwidth=0, width=75)


#this is all for the edit name window, NOT the root window
'''ef = Frame(editwin, width = 100, height=100,  bd = 3, bg="#fef2da", relief="raised")
ef.pack(expand=True)
ef.

e_buttons = Frame(editwin, width = 100, height = 20, bg="#fef2da", relief="raised")
e_buttons.pack(expand=True)'''


tree.pack()

viewitems()

if __name__ == '__main__':
    root.mainloop()
