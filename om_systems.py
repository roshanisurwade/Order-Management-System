from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from pymongo import *

def f1():
    mw.withdraw()
    lw.deiconify()

def f2():
    lw.withdraw()
    mw.deiconify()

def f3():
    mw.withdraw()
    vw.deiconify()
    view_orders()

def f4():
    vw.withdraw()
    mw.deiconify()

def view_orders():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["orders"]
		coll = db["customer"]
		data = coll.find()
		vw_st_data.delete(1.0, END)
		for d in data:
			vw_st_data.insert(END, f"ordno = {d["_id"]}, name =  {d["name"]}, phone =  {d["phone"]}, email = {d["email"]}, address = {d["address"]}, items = {d["items"]}\n")
	except Exception as e:
		showerror("Issue", str(e))
	finally:
		if con is not None:
			con.close()

mw = Tk()
mw.title("Order Management System")
mw.geometry("1000x700+50+50")
f = ("Simsun", 24, "bold")
mw.configure(bg="magenta2")
mw.iconbitmap("cafeadmin.ico")

mw_lab_title = Label(mw, text="Order Management System", font=f,bg="magenta2")
mw_lab_title.place(x=200, y=10)
mw_lab_id = Label(mw, text="Enter ID ", font=f, bg="magenta2")
mw_ent_id = Entry(mw, font=f, width=12, bg="floral white")
mw_lab_name = Label(mw, text="Enter Name", font=f,bg="magenta2")
mw_ent_name = Entry(mw, font=f,  width=12, bg="floral white")
mw_lab_phone = Label(mw, text="Enter Phone", font=f,bg="magenta2")
mw_ent_phone = Entry(mw, font=f,  width=12, bg="floral white")
mw_lab_email = Label(mw, text="Enter Email", font=f,bg="magenta2")
mw_ent_email = Entry(mw, font=f,  width=12, bg="floral white")
mw_lab_address = Label(mw, text="Enter Address ", font=f,bg="magenta2")
mw_ent_address = Entry(mw, font=f,  width=12, bg="floral white")

mw_lab_id.place(x=80, y=80)
mw_ent_id.place(x=320, y=80)
mw_lab_name.place(x=80, y=130)
mw_ent_name.place(x=320, y=130)
mw_lab_phone.place(x=80, y=180)
mw_ent_phone.place(x=320, y=180)
mw_lab_email.place(x=80, y=230)
mw_ent_email.place(x=320, y=230)
mw_lab_address.place(x=80, y=280)
mw_ent_address.place(x=320, y=280)

t, c, d, j, p, b = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
mw_lab_items = Label(mw, text="Select Items:", font=f,bg="magenta2")
mw_cb_tea = Checkbutton(mw, text="Tea", font=f, variable=t,bg="magenta2")
mw_cb_coffee = Checkbutton(mw, text="Coffee", font=f, variable=c,bg="magenta2")
mw_cb_dosa = Checkbutton(mw, text="dosa", font=f, variable=d,bg="magenta2")
mw_cb_juice = Checkbutton(mw, text="Juice", font=f, variable=j,bg="magenta2")
mw_cb_pizza = Checkbutton(mw, text="Pizza", font=f, variable=p,bg="magenta2")
mw_cb_burger = Checkbutton(mw, text="Burger", font=f, variable=b,bg="magenta2")

mw_lab_items.place(x=80, y=350)
mw_cb_tea.place(x=320, y =350)
mw_cb_coffee.place(x=440, y=350)
mw_cb_dosa.place(x=320, y=400)
mw_cb_juice.place(x=440, y=400)
mw_cb_pizza.place(x=320, y=450)
mw_cb_burger.place(x=440, y=450)

def order():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["orders"]
		coll = db["customer"]
		ordno = int(mw_ent_id.get())
		name = mw_ent_name.get()
		phone = int(mw_ent_phone.get())
		email = mw_ent_email.get()
		address = mw_ent_address.get()
		if name == "" or email == "" or address == "":
			showerror("issue", "inputs cannot be empty")
			return

		if name.strip() == "" or email.strip() == "" or address.strip() == "":
			showerror("issue", "inputs cannot contain spaces")
			return

		if name.isdigit():
			showerror("Issue", "name inputs cannot be a number")
			return

		if len(name) < 1 or len(name) > 10:
			showerror("issue", "name length shud be  betn 2 and 10 char.")
			return

		if email.isdigit():
			showerror("issue", "email cannot be all numbers")
			return
		if email.isalpha():
			showerror("issue", "email cannot be all text")
			return

		if address.isdigit():
			showerror("Issue", "address inputs cannot be a number")
			return

		if len(address) <1 or len(address) > 12:
			showerror("issue", "address length shud be between 1 and 12 char")
			return

		try:

			if phone < 0:
				showerror("Issue", "Phone number cannot be negative")
				return
		except Exception:
			showerror("Issue", "Invalid phone number")
		try:
			phone = int(mw_ent_phone.get())
			if len(str(phone)) == 0 or len(str(phone)) > 10:
				showerror("issue", "phone number should be between 1 and 10 digits")
				return

		except Exception as e:
			showerror("issue", e)

		items = ""	
		items = ""	
		if t.get() == 1:
			items += "Tea, "
		if c.get() == 1:
			items += "Coffee, "
		if d.get() == 1:
			items += "Dosa, "
		if j.get() == 1:
			items += "Juice, "
		if p.get() == 1:
			items += "Pizza, "
		if b.get() == 1:
			items += "Burger, "

		if not items:
			showerror("issue", "please select atleast one item")
			return
		items = items[:-2]

		info = {"_id": ordno, "name":name, "phone":phone, "email":email, "address":address, "items":items}
		coll.insert_one(info)
		showinfo("Success", "order will be delivered in 30 mins")

		mw_ent_id.delete(0, END)
		mw_ent_name.delete(0, END)
		mw_ent_phone.delete(0, END)
		mw_ent_email.delete(0, END)
		mw_ent_address.delete(0, END)
		t.set(0)
		c.set(0)
		d.set(0)
		j.set(0)
		p.set(0)
		b.set(0)
		mw_ent_id.focus()

	except Exception:
		showerror("Issue", "order cannot be empty")
	finally:
		if con is not None:
			con.close()

def clear():
		mw_ent_id.delete(0, END)
		mw_ent_name.delete(0, END)
		mw_ent_phone.delete(0, END)
		mw_ent_email.delete(0, END)
		mw_ent_address.delete(0, END)
		mw_ent_id.focus()
	
 
mw_btn_order = Button(mw, text="Order",width=12, font=f, command=order, bg="wheat1")
mw_btn_order.place(x=330, y=500)

mw_btn_view = Button(mw, text="View Order",width=12, font=f, bg="wheat1", command=f3)
mw_btn_view.place(x=330, y=570)

mw_btn_login = Button(mw, text="Admin Login",width=12, font=f,bg="wheat1", command=f1)
mw_btn_login.place(x=330, y=640)

mw_btn_clear = Button(mw, text="Clear", width=12, font=f, bg="wheat1", command=clear)
mw_btn_clear.place(x=330, y=710)

 
lw = Toplevel(mw)
lw.title("Cafe Admin Login")
lw.geometry("1000x600+50+10")
lw.configure(bg="magenta2")

lw_lab_title = Label(lw, text="Admin Login", font=f, bg="magenta2")
lw_lab_title.pack(pady=10)
lw_lab_un = Label(lw, text="Username ", font=f,bg="magenta2")
lw_ent_un = Entry(lw, font=f, width=15, bg="floral white")
lw_lab_pw = Label(lw, text="Password ", font=f,bg="magenta2")
lw_ent_pw = Entry(lw, font=f,width=15, bg="floral white")
lw_lab_un.pack(pady=5)
lw_ent_un.pack(pady=5)
lw_lab_pw.pack(pady=5)
lw_ent_pw.pack(pady=20)


def login():
	con = None
	try:
		username = lw_ent_un.get()
		password = lw_ent_pw.get()
		if (username == "admin") and (password == "password"):
			showinfo("success", "login successful")
		else:
			showerror("issue","invalid username and  password")

		info = {"username":username, "password":password}
		lw_ent_un.delete(0, END)
		lw_ent_pw.delete(0, END)
		lw_ent_un.focus()

	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()
		
		
lw_btn_login = Button(lw, text="Login",width=12, font=f, bg="wheat1", command=login)
lw_btn_login.pack(pady=15)

lw_btn_back = Button(lw, text="Back To Main", width=12, font=f,bg="wheat1", command=f2)
lw_btn_back.pack(pady=15)
lw.withdraw()

vw = Toplevel(mw)
vw.title("View Order")
vw.geometry("1000x600+50+10")
vw.configure(bg="magenta2")


def delete_order():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["orders"]
		coll = db["customer"]

		ordno_str = mw_ent_id.get()
		if ordno_str == "":
			showerror("error", "please enter order id")
			return

		if not ordno_str.isdigit():
			showerror("issue", "invalid order id")
			return

		ordno = int(ordno_str)
		if coll.find_one({"_id": ordno}):
			coll.delete_one({"_id": ordno})
			showinfo("success", "order deleted successfully")
		else:
			showinfo("error", "order does not exist")
	except Exception as e:
			showerror("issue", e)
	finally:
		if con is not None:
			con.close()
	
vw_st_data = ScrolledText(vw, font=f, width=50, height=10, bg="floral white")
vw_btn_delete = Button(vw, text="Delete Order", width=12, bg="wheat1", font=f, command=delete_order)
vw_btn_back = Button(vw, text="Back To Main", width=12, font=f, bg="wheat1", command=f4)
vw_st_data.place(x=50, y=50)
vw_btn_delete.place(x=400, y=400)
vw_btn_back.place(x=400, y=470)

vw.withdraw()

mw.mainloop()