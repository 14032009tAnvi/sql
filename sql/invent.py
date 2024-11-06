import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from PIL import Image, ImageTk
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sneha25',
    'database': 'management'
}

# Function to create a connection to the database
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)
def execute_query(query, data=None):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(query, data) if data else cursor.execute(query)
        connection.commit()
        return cursor
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
 
# Main application window
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1000x700")
root.config(bg="lightgray")

# Header
header = tk.Frame(root, bg="navy", height=70)
header.pack(side="top", fill="x")

title = tk.Label(header, text="Inventory Management System", font=("Arial", 18), fg="white", bg="navy")
title.pack(side="left", padx=10, pady=10)

# Date and Time - Displaying on separate lines within the header
date_time_frame = tk.Frame(header, bg="navy")
date_time_frame.pack(side="right", padx=20)

date_label = tk.Label(date_time_frame, text=f"Date: {datetime.now().strftime('%d/%m/%Y')}", fg="white", bg="navy", font=("Arial", 10))
date_label.pack()  # Date on first line

time_label = tk.Label(date_time_frame, text=f"Time: {datetime.now().strftime('%H:%M:%S %p')}", fg="white", bg="navy", font=("Arial", 10))
time_label.pack()  # Time on second line

# Sidebar
sidebar = tk.Frame(root, width=200, bg="teal")
sidebar.pack(side="left", fill="y")

# Content Frame
content_frame = tk.Frame(root, bg="white")
content_frame.pack(side="right", expand=True, fill="both")

# Sidebar Menu
# menu_title = tk.Label(sidebar, text="Menu", font=("Arial", 16, "bold"), bg="teal", fg="white")
# menu_title.pack(pady=10)

# menu_buttons = ["Employee", "Supplier", "Category", "Product", "Sales", "Exit"]
# for label in menu_buttons:
#     btn = tk.Button(sidebar, text=label, font=("Arial", 14), bg="black", fg="white", relief="flat",
#                     command=lambda l=label: switch_tab(l))
#     btn.pack(fill="x", pady=5)

menu_title = tk.Label(sidebar, text="Menu", font=("Arial", 16, "bold"), bg="teal", fg="white")
menu_title.pack(pady=10)

# Define the desired width for the buttons
button_width = 20  # You can adjust this value as needed

menu_buttons = ["Employee", "Supplier", "Category", "Product", "Sales", "Exit"]
for label in menu_buttons:
    btn = tk.Button(sidebar, text=label, font=("Arial", 14), bg="black", fg="white", relief="flat",
                    width=button_width,  # Set the button width
                    command=lambda l=label: switch_tab(l))
    btn.pack(fill="x", pady=5)


# Function to switch between tabs
def switch_tab(tab_name):
    # Clear current content
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    if tab_name == "Employee":
        create_employee_tab()
    elif tab_name == "Supplier":
        create_supplier_tab()
    elif tab_name == "Category":
        create_category_tab()
    elif tab_name == "Product":
        create_product_tab()
    elif tab_name == "Sales":
        create_sales_tab()
    elif tab_name == "Exit":
        root.quit()

def get_totals():
    totals = {}
    try:
        connection = connect_db()
        cursor = connection.cursor()
        
        # Query to get the count of records from each table
        queries = {
            "Total Employees": "SELECT COUNT(*) FROM employees",
            "Total Suppliers": "SELECT COUNT(*) FROM suppliers",
            "Total Categories": "SELECT COUNT(*) FROM categories",
            "Total Products": "SELECT COUNT(*) FROM products",
            "Total Sales": "SELECT COUNT(*) FROM sales"
        }
        for label, query in queries.items():
            cursor.execute(query)
            count = cursor.fetchone()[0]  # Fetch the first result
            totals[label] = count  # Store the count in the totals dictionary

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        connection.close()
    
    return totals 

def create_dashboard_tab():
    # Frame for dashboard items centered within content_frame
    dashboard_frame = tk.Frame(content_frame, bg="white")
    dashboard_frame.pack(pady=20, fill="both", expand=True)
    
    # Fetch totals from the database
    totals = get_totals()  # Ensure this returns a dictionary of totals

    # Load images for each total and keep references
    image_size = (100, 100)  # New size for the images (width, height)
    images = {
        "Total Employees": ImageTk.PhotoImage(Image.open("total_emp.png").resize(image_size)),
        "Total Suppliers": ImageTk.PhotoImage(Image.open("total_sup.png").resize(image_size)),
        "Total Categories": ImageTk.PhotoImage(Image.open("total_cat.png").resize(image_size)),
        "Total Products": ImageTk.PhotoImage(Image.open("total_prod.png").resize(image_size)),
        "Total Sales": ImageTk.PhotoImage(Image.open("total_sales.png").resize(image_size))
    }

    colors = ["#3b5998", "#8e44ad", "#27ae60", "#2980b9", "#e74c3c"]
    
    for index, label in enumerate(totals.keys()):  # Use keys from the totals dictionary
        frame = tk.Frame(dashboard_frame, bg=colors[index], width=200, height=200)  # Increased frame size
        frame.grid(row=index // 3, column=index % 3, padx=20, pady=20)
        frame.pack_propagate(False)
        
        # Display the image
        lbl_img = tk.Label(frame, image=images[label], bg=colors[index])
        lbl_img.image = images[label]  # Keep a reference to the image
        lbl_img.pack(pady=5)
        
        # Display the total
        lbl_total = tk.Label(frame, text=str(totals[label]), font=("Arial", 24, "bold"), bg=colors[index], fg="white")  # Increased font size
        lbl_total.pack()
        
        # Display the label
        lbl_text = tk.Label(frame, text=label, font=("Arial", 14), bg=colors[index], fg="white")  # Increased font size
        lbl_text.pack()

# Example of how to call this function
# switch_tab("Dashboard")  # Ensure this is called within the correct context


# Example Employee Tab
def create_employee_tab():
    # Clear current content
    for widget in content_frame.winfo_children():
        widget.destroy()

    title = tk.Label(content_frame, text="Employee Management", font=("Arial", 16), bg="white", fg="navy")
    title.grid(row=0, column=0, columnspan=2, pady=10)


    # Employee form fields
    fields = {
        "Employee Name": tk.Entry(content_frame, font=("Arial", 12)),
        "Email": tk.Entry(content_frame, font=("Arial", 12)),
        "Employee ID": tk.Entry(content_frame, font=("Arial", 12)),
        "Address": tk.Entry(content_frame, font=("Arial", 12)),
        "Contact": tk.Entry(content_frame, font=("Arial", 12)),
        "Password": tk.Entry(content_frame, font=("Arial", 12), show="*")
    }
    
    
    options = {
        "Gender": ["Male", "Female", "Other"],
        "Employee Type": ["Full-time", "Part-time", "Contract"],
        "Date of Birth": tk.Entry(content_frame, font=("Arial", 12)),  # Date as string for simplicity
        "Date of Joining": tk.Entry(content_frame, font=("Arial", 12)),  # Date as string for simplicity
        "Work Shift": ["Morning", "Evening", "Night"],
        "User Type": ["Admin", "Employee", "Manager"]
    }
    
    # Create labels and input fields for employee details
    for idx, (label, field) in enumerate(fields.items()):
        lbl = tk.Label(content_frame, text=label, font=("Arial", 12), bg="white")
        lbl.grid(row=idx + 1, column=0, padx=10, pady=5, sticky="w")
        field.grid(row=idx + 1, column=1, padx=10, pady=5, sticky="w")

    row_offset = len(fields)
    for idx, (label, values) in enumerate(options.items()):
        lbl = tk.Label(content_frame, text=label, font=("Arial", 12), bg="white")
        lbl.grid(row=row_offset + idx + 1, column=0, padx=10, pady=5, sticky="w")
        if isinstance(values, list):
            combobox = ttk.Combobox(content_frame, values=values, font=("Arial", 12))
            combobox.grid(row=row_offset + idx + 1, column=1, padx=10, pady=5, sticky="w")
            options[label] = combobox
        else:
            values.grid(row=row_offset + idx + 1, column=1, padx=10, pady=5, sticky="w")

    def save_employee():
        emp_data = {
            "name": fields["Employee Name"].get(),
            "email": fields["Email"].get(),
            "emp_id": fields["Employee ID"].get(),
            "address": fields["Address"].get(),
            "contact": fields["Contact"].get(),
            "password": fields["Password"].get(),
            "gender": options["Gender"].get(),
            "emp_type": options["Employee Type"].get(),
            "dob": options["Date of Birth"].get(),
            "date_joined": options["Date of Joining"].get(),
            "work_shift": options["Work Shift"].get(),
            "user_type": options["User Type"].get()
        }
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO employees (name, email, emp_id, address, contact, password, gender, emp_type, dob, date_joined, work_shift, user_type)
                VALUES (%(name)s, %(email)s, %(emp_id)s, %(address)s, %(contact)s, %(password)s, %(gender)s, %(emp_type)s, %(dob)s, %(date_joined)s, %(work_shift)s, %(user_type)s)
                """,
                emp_data
            )
            connection.commit()
            messagebox.showinfo("Success", "Employee details saved successfully.")
            display_all_employees()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()

    
    def update_employee():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Select Record", "Please select an employee record to update.")
            return

        emp_data = {
            "name": fields["Employee Name"].get(),
            "email": fields["Email"].get(),
            "emp_id": fields["Employee ID"].get(),
            "address": fields["Address"].get(),
            "contact": fields["Contact"].get(),
            "password": fields["Password"].get(),
            "gender": options["Gender"].get(),
            "emp_type": options["Employee Type"].get(),
            "dob": options["Date of Birth"].get(),
            "date_joined": options["Date of Joining"].get(),
            "work_shift": options["Work Shift"].get(),
            "user_type": options["User Type"].get(),
            "empid": tree.item(selected_item)["values"][0]  # Assuming ID is the first column
        }
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE employees 
                SET name = %(name)s, email = %(email)s, address = %(address)s, contact = %(contact)s,
                password = %(password)s, gender = %(gender)s, emp_type = %(emp_type)s, dob = %(dob)s,
                date_joined = %(date_joined)s, work_shift = %(work_shift)s, user_type = %(user_type)s 
                WHERE emp_id = %(emp_id)s
                """,
                emp_data
            )
            cursor.connection.commit()
            messagebox.showinfo("Success", "Employee details updated successfully.")
            display_employee_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()

    def delete_employee():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Select Record", "Please select an employee record to delete.")
            return

        emp_id = tree.item(selected_item)["values"][0]  # Assuming ID is the first column
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete employee ID: {emp_id}?"):
            try:
                connection = connect_db()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM employees WHERE empid = %s", (emp_id,))
                cursor.connection.commit()
                messagebox.showinfo("Success", "Employee deleted successfully.")
                display_employee_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()

    def clear_fields():
        for field in fields.values():
            field.delete(0, tk.END)
        for combobox in options.values():
            if isinstance(combobox, ttk.Combobox):
                combobox.set('')

    def display_employee_data():
        # Clear existing data in the tree
        for item in tree.get_children():
            tree.delete(item)

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT emp_id, name, email, contact, address, emp_type, dob, date_joined FROM employees")
            for row in cursor.fetchall():
                tree.insert('', 'end', values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()

    # Create Buttons
    button_frame = tk.Frame(content_frame, bg="white")
    button_frame.grid(row=row_offset + len(options) + 1, column=0, columnspan=2, pady=10)

    save_button = tk.Button(button_frame, text="Save Employee", command=save_employee, font=("Arial", 12), bg="green", fg="white")
    save_button.grid(row=0, column=0, padx=5)

    update_button = tk.Button(button_frame, text="Update Employee", command=update_employee, font=("Arial", 12), bg="orange", fg="white")
    update_button.grid(row=0, column=1, padx=5)

    delete_button = tk.Button(button_frame, text="Delete Employee", command=delete_employee, font=("Arial", 12), bg="red", fg="white")
    delete_button.grid(row=0, column=2, padx=5)

    clear_button = tk.Button(button_frame, text="Clear Fields", command=clear_fields, font=("Arial", 12), bg="blue", fg="white")
    clear_button.grid(row=0, column=3, padx=5)

    # Create display area for employee data
    display_frame = tk.Frame(content_frame, bg="white")
    display_frame.grid(row=row_offset + len(options) + 2, column=0, columnspan=2, pady=10)

    # Create Treeview to display employee data
    columns = ("ID", "Name", "Email", "Contact", "Address", "Type", "DOB", "DOJ")
    tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=10)
    tree.pack(side="top", fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    vsb = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview) 
    vsb.grid(row=0, column=1, sticky="ns") 
    tree.configure(yscrollcommand=vsb.set) 

    # Create horizontal scrollbar 
    hsb = ttk.Scrollbar(display_frame, orient="horizontal", command=tree.xview) 
    hsb.grid(row=1, column=0, sticky="ew") 
    tree.configure(xscrollcommand=hsb.set) 
        
    # Display employee data
    display_employee_data(tree)

# Define other tab functions (similar structure to Employee Tab)
def load_suppliers():
    for row in supplier_table.get_children():
        supplier_table.delete(row)
        
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM suppliers")
        rows = cursor.fetchall()
        for row in rows:
            supplier_table.insert("", tk.END, values=row)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        cursor.close()
        connection.close()

# The main function to create the Supplier tab
def create_supplier_tab():
    # Title for the Supplier Tab
    title = tk.Label(content_frame, text="Manage Supplier Details", font=("Arial", 16), bg="white", fg="navy")
    title.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

    # Search Section at the Top
    search_label = tk.Label(content_frame, text="Search by Invoice No.:", font=("Arial", 12), bg="white")
    search_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    search_entry = tk.Entry(content_frame, font=("Arial", 12))
    search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    search_button = tk.Button(content_frame, text="Search", font=("Arial", 12), command=lambda: search_supplier(search_entry.get()))
    search_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

    # Form for Supplier Details on the Left Side
    fields = {
        "Invoice No.": tk.Entry(content_frame, font=("Arial", 12)),
        "Supplier Name": tk.Entry(content_frame, font=("Arial", 12)),
        "Contact": tk.Entry(content_frame, font=("Arial", 12)),
        "Description": tk.Entry(content_frame, font=("Arial", 12))
    }

    for idx, (label, entry) in enumerate(fields.items()):
        lbl = tk.Label(content_frame, text=label, font=("Arial", 12), bg="white")
        lbl.grid(row=idx + 2, column=0, padx=10, pady=5, sticky="w")
        entry.grid(row=idx + 2, column=1, padx=10, pady=5, sticky="w")

    # CRUD Functions for Supplier Tab
    def save_supplier():
        invoice_no = fields["Invoice No."].get()
        supplier_name = fields["Supplier Name"].get()
        contact = fields["Contact"].get()
        description = fields["Description"].get()

        if not invoice_no or not supplier_name or not contact:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO suppliers (invoice_no, supplier_name, contact, description) VALUES (%s, %s, %s, %s)",
                           (invoice_no, supplier_name, contact, description))
            connection.commit()
            messagebox.showinfo("Success", "Supplier saved successfully.")
            clear_supplier()
            load_suppliers()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    def update_supplier():
        selected_item = supplier_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a supplier to update.")
            return
        
        invoice_no = fields["Invoice No."].get()
        supplier_name = fields["Supplier Name"].get()
        contact = fields["Contact"].get()
        description = fields["Description"].get()

        if not invoice_no or not supplier_name or not contact:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("UPDATE suppliers SET supplier_name=%s, contact=%s, description=%s WHERE invoice_no=%s",
                           (supplier_name, contact, description, invoice_no))
            connection.commit()
            messagebox.showinfo("Success", "Supplier updated successfully.")
            clear_supplier()
            load_suppliers()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    def delete_supplier():
        selected_item = supplier_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a supplier to delete.")
            return
        
        invoice_no = supplier_table.item(selected_item)['values'][0]  # Get the Invoice No. of the selected item
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM suppliers WHERE invoice_no=%s", (invoice_no,))
            connection.commit()
            messagebox.showinfo("Success", "Supplier deleted successfully.")
            clear_supplier()
            load_suppliers()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    def clear_supplier():
        for field in fields.values():
            field.delete(0, tk.END)

    def search_supplier(invoice_no):
        if not invoice_no:
            messagebox.showwarning("Input Error", "Please enter an Invoice No. to search.")
            return
        
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM suppliers WHERE invoice_no=%s", (invoice_no,))
            result = cursor.fetchone()
            if result:
                fields["Invoice No."].delete(0, tk.END)
                fields["Invoice No."].insert(0, result[0])
                fields["Supplier Name"].delete(0, tk.END)
                fields["Supplier Name"].insert(0, result[1])
                fields["Contact"].delete(0, tk.END)
                fields["Contact"].insert(0, result[2])
                fields["Description"].delete(0, tk.END)
                fields["Description"].insert(0, result[3])
            else:
                messagebox.showinfo("Not Found", "Supplier not found.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    # Buttons for Supplier, arranged below the form
    button_frame = tk.Frame(content_frame, bg="white")
    button_frame.grid(row=len(fields) + 3, column=0, columnspan=2, pady=10, sticky="w")

    tk.Button(button_frame, text="Save", command=save_supplier, font=("Arial", 12), bg="green", fg="white").grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Update", command=update_supplier, font=("Arial", 12), bg="blue", fg="white").grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Delete", command=delete_supplier, font=("Arial", 12), bg="red", fg="white").grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Clear", command=clear_supplier, font=("Arial", 12), bg="orange", fg="white").grid(row=0, column=3, padx=5)

    # Table for Displaying Suppliers on the Right Side
    global supplier_table
    table_frame = tk.Frame(content_frame, bg="white")
    table_frame.grid(row=2, column=3, rowspan=len(fields) + 5, padx=10, pady=10, sticky="nsew")

    supplier_table = ttk.Treeview(table_frame, columns=("Invoice No", "Supplier Name", "Contact", "Description"), show="headings")
    supplier_table.heading("Invoice No", text="Invoice No")
    supplier_table.heading("Supplier Name", text="Supplier Name")
    supplier_table.heading("Contact", text="Contact")
    supplier_table.heading("Description", text="Description")
    supplier_table.pack(fill=tk.BOTH, expand=True)

    # Adding a Scrollbar to the Table
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=supplier_table.yview)
    supplier_table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Ensure the table fills the frame
    supplier_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Load all suppliers initially
    load_suppliers()

    # You can populate your supplier_table with data here using your database logic

def create_category_tab():
    fields = {
        "Category ID": tk.Entry(content_frame, font=("Arial", 12)),
        "Category Name": tk.Entry(content_frame, font=("Arial", 12)),
        "Description": tk.Entry(content_frame, font=("Arial", 12)),
        "Supplier ID": tk.Entry(content_frame, font=("Arial", 12)),
        "Price": tk.Entry(content_frame, font=("Arial", 12)),
        "Quantity": tk.Entry(content_frame, font=("Arial", 12)),
        "Status": ttk.Combobox(content_frame, values=["Active", "Inactive"], font=("Arial", 12)),
    }

    for idx, (label, entry) in enumerate(fields.items()):
        lbl = tk.Label(content_frame, text=label, font=("Arial", 12), bg="lightblue")
        lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

    # Function to load categories into the table
    def load_categories():
        # Clear the table before loading
        for item in category_table.get_children():
            category_table.delete(item)
        
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM categories")
            for row in cursor.fetchall():
                category_table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    # CRUD functions for Category tab
    def add_category():
        category_name = fields["Category Name"].get()
        description = fields["Description"].get()
        supplier_id = fields["Supplier ID"].get()
        price = fields["Price"].get()
        quantity = fields["Quantity"].get()
        status = fields["Status"].get()

        # Basic validation
        if not category_name or not price or not quantity or not status:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return
        
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO categories (category_name, description, supplier_id, price, quantity, status) VALUES (%s, %s, %s, %s, %s, %s)",
                           (category_name, description, supplier_id, price, quantity, status))
            connection.commit()
            messagebox.showinfo("Success", "Category added successfully.")
            load_categories()  # Refresh the category table
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

        # Clear the fields after adding
        for entry in fields.values():
            entry.delete(0, tk.END)

    def delete_category():
        selected_item = category_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a category to delete.")
            return
        
        # Get the selected category's ID
        category_id = category_table.item(selected_item)["values"][0]

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM categories WHERE category_id=%s", (category_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Category ID {category_id} has been deleted.")
            load_categories()  # Refresh the category table
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    # Buttons for Category
    tk.Button(content_frame, text="Add", command=add_category, font=("Arial", 12), bg="green", fg="white").grid(row=len(fields), column=0, pady=15)
    tk.Button(content_frame, text="Delete", command=delete_category, font=("Arial", 12), bg="red", fg="white").grid(row=len(fields), column=1, pady=15)

    # Table for displaying categories
    category_table = ttk.Treeview(content_frame, columns=("Category ID", "Category Name", "Description", "Supplier ID", "Price", "Quantity", "Status"), show="headings")
    category_table.heading("Category ID", text="Category ID")
    category_table.heading("Category Name", text="Category Name")
    category_table.heading("Description", text="Description")
    category_table.heading("Supplier ID", text="Supplier ID")
    category_table.heading("Price", text="Price")
    category_table.heading("Quantity", text="Quantity")
    category_table.heading("Status", text="Status")
    category_table.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=15)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=category_table.yview)
    category_table.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=len(fields)+1, column=2, sticky='ns')

    # Load categories when the tab is created
    load_categories()

def create_product_tab():
    fields = {
        "Product ID": tk.Entry(content_frame, font=("Arial", 12)),
        "Category ID": tk.Entry(content_frame, font=("Arial", 12)),
        "Category Name": tk.Entry(content_frame, font=("Arial", 12)),
        "Description": tk.Entry(content_frame, font=("Arial", 12)),
    }

    for idx, (label, entry) in enumerate(fields.items()):
        lbl = tk.Label(content_frame, text=label, font=("Arial", 12), bg="lightblue")
        lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

    # Function to load products into the table
    def load_products():
        # Clear the table before loading
        for item in product_table.get_children():
            product_table.delete(item)
        
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM products")
            for row in cursor.fetchall():
                product_table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    # CRUD functions for Product tab
    def add_product():
        product_id = fields["Product ID"].get()
        category_id = fields["Category ID"].get()
        category_name = fields["Category Name"].get()
        description = fields["Description"].get()

        # Basic validation
        if not product_id or not category_id or not category_name or not description:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        
        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO products (product_id, category_id, category_name, description) VALUES (%s, %s, %s, %s)",
                           (product_id, category_id, category_name, description))
            connection.commit()
            messagebox.showinfo("Success", "Product added successfully.")
            load_products()  # Refresh the product table
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

        # Clear the fields after adding
        for entry in fields.values():
            entry.delete(0, tk.END)

    def delete_product():
        selected_item = product_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")
            return
        
        # Get the selected product's ID
        product_id = product_table.item(selected_item)["values"][0]

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Product ID {product_id} has been deleted.")
            load_products()  # Refresh the product table
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    # Buttons for Product
    tk.Button(content_frame, text="Add", command=add_product, font=("Arial", 12), bg="green", fg="white").grid(row=len(fields), column=0, pady=15)
    tk.Button(content_frame, text="Delete", command=delete_product, font=("Arial", 12), bg="red", fg="white").grid(row=len(fields), column=1, pady=15)

    # Table for displaying products
    product_table = ttk.Treeview(content_frame, columns=("Product ID", "Category ID", "Category Name", "Description"), show="headings")
    product_table.heading("Product ID", text="Product ID")
    product_table.heading("Category ID", text="Category ID")
    product_table.heading("Category Name", text="Category Name")
    product_table.heading("Description", text="Description")
    product_table.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=15)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=product_table.yview)
    product_table.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=len(fields)+1, column=2, sticky='ns')

    # Load products when the tab is created
    load_products()

def create_sales_tab():
    fields = {
        "Sale ID": tk.Entry(content_frame, font=("Arial", 12)),
        "Product ID": tk.Entry(content_frame, font=("Arial", 12)),
        "Quantity Sold": tk.Entry(content_frame, font=("Arial", 12)),
        "Sale Date": tk.Entry(content_frame, font=("Arial", 12)),  # Format: YYYY-MM-DD
        "Total Amount": tk.Entry(content_frame, font=("Arial", 12)),
    }

    for idx, (label, entry) in enumerate(fields.items()):
        lbl = tk.Label(content_frame, text=label, font=("Arial", 12), bg="lightblue")
        lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

    # Function to load sales into the table
    def load_sales():
        # Clear the table before loading
        for item in sales_table.get_children():
            sales_table.delete(item)

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM sales")
            for row in cursor.fetchall():
                sales_table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    # CRUD functions for Sales tab
    def add_sale():
        product_id = fields["Product ID"].get()
        quantity_sold = fields["Quantity Sold"].get()
        sale_date = fields["Sale Date"].get()
        total_amount = fields["Total Amount"].get()

        # Basic validation
        if not product_id or not quantity_sold or not sale_date or not total_amount:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO sales (product_id, quantity_sold, sale_date, total_amount) VALUES (%s, %s, %s, %s)",
                           (product_id, quantity_sold, sale_date, total_amount))
            connection.commit()
            messagebox.showinfo("Success", "Sale added successfully.")
            load_sales()  # Refresh the sales table
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

        # Clear the fields after adding
        for entry in fields.values():
            entry.delete(0, tk.END)

    def delete_sale():
        selected_item = sales_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a sale to delete.")
            return

        # Get the selected sale's ID
        sale_id = sales_table.item(selected_item)["values"][0]

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM sales WHERE sale_id=%s", (sale_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Sale ID {sale_id} has been deleted.")
            load_sales()  # Refresh the sales table
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    # Buttons for Sales
    tk.Button(content_frame, text="Add", command=add_sale, font=("Arial", 12), bg="green", fg="white").grid(row=len(fields), column=0, pady=15)
    tk.Button(content_frame, text="Delete", command=delete_sale, font=("Arial", 12), bg="red", fg="white").grid(row=len(fields), column=1, pady=15)

    # Table for displaying sales
    sales_table = ttk.Treeview(content_frame, columns=("Sale ID", "Product ID", "Quantity Sold", "Sale Date", "Total Amount"), show="headings")
    sales_table.heading("Sale ID", text="Sale ID")
    sales_table.heading("Product ID", text="Product ID")
    sales_table.heading("Quantity Sold", text="Quantity Sold")
    sales_table.heading("Sale Date", text="Sale Date")
    sales_table.heading("Total Amount", text="Total Amount")
    sales_table.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=15)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=sales_table.yview)
    sales_table.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=len(fields)+1, column=2, sticky='ns')

    # Load sales when the tab is created
    load_sales()
create_dashboard_tab()
root.mainloop()