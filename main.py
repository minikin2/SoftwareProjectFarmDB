'''A Farm Market  web app that keep record of produce 
    and inventory
    Author: Ndubuisi, Jennifer, Samantha and Rajinder
    Date: 07/25/2022
    Synopsis: An inventory control application, which will allow the user to enter in information to add, delete, or update a database, the user can also view the items in the database.
'''
from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import csv
import os

from DBaccess import addItem, deleteItem, getItemID, updateItem, viewItems, viewByCate


root = Tk()
root.title("Becker Farms Inventory Management")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 1530
height = 1000
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(1, 1)

# It getting data from clients and adding them to csv file 
def additem():

    # the values of items are being fetched
    e1=entry1.get()
    e2=entry2.get()
    e3=entry3.get()
    e4=entry4.get()
    e5=entry5.get()
    e6=entry6.get()
   
    if entry1.get()=="" or entry2.get()=="" or entry4.get()=="" or entry5.get()=="":

        #print("Error")
        tkMessageBox.showerror("Error","there is an issue with some information")

    else:
        result=tkMessageBox.askquestion("Submit","You are about to enter following details\n" + e1 + "\n" + e2 + "\n" + e3 + "\n" + e4 + "\n" + e5 + "\n" + e6)
        clearitem()
        
        if(result =="yes"):
            r = addItem('Becker Farms Inventory.db', e1, e2, e3, e4, e5, e6)
            if r == 0:
                tkMessageBox.showinfo("Success!", "Item successfully added")
            else:
                tkMessageBox.showerror("Error", r)

    
def deleteitem():
##    tree.delete(*tree.get_children())
    e1=entry1.get()
   
    if entry1.get()=="":
        #print("Error")
        tkMessageBox.showerror("Error","there is an issue with some information")
    else:
        result=tkMessageBox.askquestion("Submit","You are about to delete the item\n" + e1)


        if(result =="yes"):
            r = deleteItem('Becker Farms Inventory.db', getItemID('Becker Farms Inventory.db', e1))
            if r == 0:
                tkMessageBox.showinfo("Success!", "Item successfully deleted")
            else:
                tkMessageBox.showerror("Error", r)
    
            entry1.delete(0, END)

def updateitem():
    # items are being updated
    name=entry1.get()

    if entry1.get()=="":

        #print("Error")
        tkMessageBox.showerror("Error","there is issue with some information")
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
          
            r = updateItem("Becker Farms Inventory.db", getItemID("Becker Farms Inventory.db", name), e1, e2, e3, e4, e5, e6)
            if r == 0:
                tkMessageBox.showinfo("Success!", "Item successfully updated")
            else:
                tkMessageBox.showerror("Error", r)

            clearitem()
                                      
# To the view all the items in the datbase
def viewitem():
    tree.delete(*tree.get_children())
    l = viewItems('Becker Farms Inventory.db')
    if type(l) == str:
       tkMessageBox.showerror("Error", l)
    else:
        i = 0
        for item in l:
            i += 1
            tree.insert(parent = "", index = END, iid = i, text = "", values = (item[1], item[2], item[3], item[4], item[5], item[6]))
        
    txt_result.config(text="Successfully read the data from database", fg="black")

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


# A deletion button to delete the item selected
def clearitem():
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)
   

 

# string variables
ItemName = StringVar()
Quantity = StringVar()
Description = StringVar()
Category = StringVar()
Unit=StringVar()
Price=StringVar()


# each widget created are appended to the window frame
Top = Frame(root, width=900, height=50 ,bd=8, relief="raise")
Top.pack(side=TOP)
Left = Frame(root, width=200, height=500, bd=8, relief="raise")
Left.pack(side=LEFT)
Right = Frame(root, width=600, height=500,bd=8, relief="raise")
Right.pack(side=RIGHT)
Forms = Frame(Left, width=300, height=450)
Forms.pack(side=TOP)
Buttons = Frame(Left, width=300, height=250, bd=8, relief="raise")
Buttons.pack(side=BOTTOM)

# adding widget for all the entry data
txt_title = Label(Top, width=900, font=('arial', 24),fg='green',text = "Becker Farms Inventory Management")
txt_title.pack()
label0 = Label(Forms, text="Item Name:", fg='green',font=('arial', 16), bd=15)
label0.grid(row=0, stick="e")
label1 = Label(Forms, text="Quantity:",fg='green', font=('arial', 16), bd=15)
label1.grid(row=1, stick="e")
label2 = Label(Forms, text="Description:",fg='green', font=('arial', 16), bd=15)
label2.grid(row=2, stick="e")
label3 = Label(Forms, text="Category:",fg='green', font=('arial', 16), bd=15)
label3.grid(row=3, stick="e")
label4 = Label(Forms, text="Unit:",fg='green', font=('arial', 16), bd=15)
label4.grid(row=4, stick="e")
label5 = Label(Forms, text="Price:",fg='green', font=('arial', 16), bd=15)
label5.grid(row=5, stick="e")


txt_result = Label(Buttons)
txt_result.pack(side=TOP)

entry1 = Entry(Forms, textvariable=ItemName, width=30)
entry1.grid(row=0, column=1) 
entry2 = Entry(Forms, textvariable=Quantity, width=30)
entry2.grid(row=1, column=1)
entry3 = Entry(Forms, textvariable=Description, width=30)
entry3.grid(row=2, column=1)
entry4 = Entry(Forms, textvariable=Category, width=30)
entry4.grid(row=3, column=1)
entry5 = Entry(Forms, textvariable=Unit, width=30)
entry5.grid(row=4, column=1)
entry6 = Entry(Forms, textvariable=Price, width=30)
entry6.grid(row=5, column=1)

ent1 = Entry(Forms, textvariable=ItemName, width=30)
ent1.grid(row = 0, column = 1)

btn_add = Button(Buttons, width=10, text="ADD", command=additem)
btn_add.pack(side=LEFT)
btn_delete = Button(Buttons, width=10, text="Delete", command=deleteitem)
btn_delete.pack(side=LEFT)
btn_update = Button(Buttons, width=10, text="UPDATE", command=updateitem )
btn_update.pack(side=LEFT)
btn_view = Button(Buttons, width=10, text="View", command=viewitem)
btn_view.pack(side=LEFT)
btn_clear = Button(Buttons, width=10, text="CLEAR", command=clearitem)
btn_clear.pack(side=LEFT)
btn_viewbycate = Button(Buttons, width=20, text="View By Category", command=viewbycategory)
btn_viewbycate.pack(side=LEFT)

scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=( "ItemName", "Quantity", "Description", "Category", "Unit", "Price"),
                    selectmode="extended", height=700, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

tree.heading('ItemName', text="Item Name", anchor=W)
tree.heading('Quantity', text="Quantity", anchor=W)
tree.heading('Description', text="Description", anchor=W)
tree.heading('Category', text="Category", anchor=W)
tree.heading('Unit', text="Unit", anchor=W)
tree.heading('Price', text="Price", anchor=W)


tree.column('#0', stretch=NO, minwidth=20, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=200)
tree.column('#2', stretch=NO, minwidth=0, width=70)
tree.column('#3', stretch=NO, minwidth=0, width=300)
tree.column('#4', stretch=NO, minwidth=0, width=140)
tree.column('#5', stretch=NO, minwidth=0, width=120)
tree.column('#6', stretch=NO, minwidth=0, width=100)



tree.pack()


if __name__ == '__main__':
    root.mainloop()
