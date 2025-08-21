import csv

data_file = "employees_details.txt"
csv_file = "employees_details_sheet.csv"

def extract_emp_id(line):
    try:
        return line.strip().split("Employee ID: ")[-1].strip()
    except IndexError:
        return ""
    
def parse_employee_line(line):
    """Extracts employee data from text line into dictionary."""
    try:
        parts = line.split(" | ")
        name = parts[0].split(": ")[1]
        role = parts[1].split(": ")[1]
        salary = parts[2].split(": ")[1].replace("Rs. ", "")
        emp_id = parts[3].split(": ")[1]
        return {
            "Name": name,
            "Role": role,
            "Salary": salary,
            "Employee ID": emp_id
        }
    except:
        return None
    
def export_to_csv():
    """Exports text file data to CSV."""
    try:
        with open(data_file, "r") as txtfile:
            lines = [line.strip() for line in txtfile if line.strip()]
        
        if not lines:
            print("⚠️ No data to export!")
            return
        
        employees = [parse_employee_line(line) for line in lines if parse_employee_line(line)]
        
        with open(csv_file, "w", newline="") as csvfile_obj:
            fieldnames = ["Name", "Role", "Salary", "Employee ID"]
            writer = csv.DictWriter(csvfile_obj, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(employees)
        
        print(f"✅ Data exported successfully to {csv_file}")
    
    except FileNotFoundError:
        print("⚠️ No text file found to export!")

def is_valid_text(text):
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'.")
    return all(c in allowed for c in text)

def id_exists(emp_id):
    try:
        with open(data_file, "r") as file:
            for line in file:
                if extract_emp_id(line) == str(emp_id):
                    return True
    except FileNotFoundError:
        return False
    return False


def add_employee():
    print("\n📝 Add New Employee")
    while True:
        name = input("👤 Enter employee name: ").title().strip()
        if is_valid_text(name):
            break
        else:
            print("❌ Name should not contain numbers or special characters.")

    while True:
        role = input("💼 Enter employee role: ").title().strip()
        if is_valid_text(role):
            break
        else:
            print("❌ Role should not contain numbers or special characters.")

    while True:
        salary = input("💰 Enter Employee salary: ")
        if salary.isdigit():
            salary = int(salary)
            break
        else:
            print("❌ Salary should be a valid number.")

    while True:
        emp_id = input("🆔 Enter employee ID: ")
        if emp_id.isdigit() and not id_exists(emp_id):
            emp_id = int(emp_id)
            break
        else:
            print("❌ Invalid or duplicate Employee ID.")

    with open(data_file, 'a+') as f:
        f.seek(0)
        if f.read().strip():
            f.write("\n")
        f.write(f"The Employee name is: {name} | His/Her Role: {role} | Salary: Rs. {salary} | Employee ID: {emp_id}")
        print(f"\n✅ {name} added successfully!")


def view_employees():
    print("\n🔍 View Employee Details")
    employee = input("🔎 Enter the name, role, or employee ID to search: ").strip()
    found = False
    results = []
    try:
        with open(data_file, "r") as file:
            for line in file:
                if employee.isdigit():
                    if extract_emp_id(line) == employee:
                        results.append(f"{line.strip()}")
                        found = True
                else:
                    if employee.lower() in line.lower():
                        results.append(f"{line.strip()}")
                        found = True
        if found:
            print("\n📋 Employee Details are:\n")
            for result in results:
                print(result)

        else:
            print(f"❌ No details found for {employee}.")

    except FileNotFoundError:
        print("⚠️ No data file found. Save something first!")

def update_employee():
    print("\n✏️  Update Employee Details")
    while True:
        emp_id = input("🆔 Enter the Employee ID to update: ").strip()
        updated_lines = []
        found = False
        try:
            with open(data_file, "r") as file:
                for line in file:
                    if extract_emp_id(line) == emp_id:
                        print(f"\n📄 Found: {line.strip()}\n")
                        while True:
                            name = input("👤 New name: ").title().strip()
                            if is_valid_text(name):
                                break
                            else:
                                print("❌ Name should not contain numbers or special characters.")

                        while True:
                            role = input("💼 New role: ").title().strip()
                            if is_valid_text(role):
                                break
                            else:
                                print("❌ Role should not contain numbers or special characters.")

                        try:
                            while True:
                                salary = input("💰 New salary: ").strip()
                                if salary.isdigit():
                                    break
                                else:
                                    print("❌ Salary should be a valid number.")

                        except ValueError:
                            print("⚠️ Please enter a valid number for salary.")
                            return
                        
                        updated_line = f"The Employee name is: {name} | His/Her Role: {role} | Salary: Rs. {salary} | Employee ID: {emp_id}\n"
                        updated_lines.append(updated_line)
                        found = True
                    else:
                        updated_lines.append(line)

            if found:
                with open(data_file, "w") as file:
                    file.writelines(updated_lines)
                print("\n✅ Employee details updated successfully!")
                break
            else:
                print("❌ No employee found with that ID.")

        except FileNotFoundError:
            print("⚠️ No data file found. Add some employees first!")
            break


def delete_employee():
    print("\n🗑️  Delete Employee")
    while True:
        emp_id = input("🆔 Enter the Employee ID to delete: ").strip()
        updated_lines = []
        found = False
        confirm = input("❓ Are you sure? Type 'yes' to proceed: ").lower()
        if confirm != "yes":
            print("❌ Action cancelled.")
            return
        else:
            with open(data_file, "r") as file:
                for line in file:
                    if extract_emp_id(line) == emp_id:
                        print(f"🧾 Deleting: {line.strip()}")
                        found = True
                        continue
                    if line.strip():
                        updated_lines.append(line.strip())

            if found:
                with open(data_file, "w") as file:
                    file.writelines("\n".join(updated_lines))
                print("\n✅ Employee deleted successfully!")
                break
            else:
                print("❌ No employee found with that ID.")


def run_employees_program():
    print("\n👋 Welcome to the Employee Management System!")
    while True:
      print("\n📌 ---- MENU ----\n1️⃣  Add Employee\n2️⃣  View All Employees\n3️⃣  View Employee\n4️⃣  Update Employee\n5️⃣  Delete Employee\n6️⃣  Export to CSV\n7️⃣  Exit")
      choice = input("👉 Choose an option: ").lower().strip()
      if "add" in choice or "1" in choice:
          add_employee()

      elif "all" in choice or "2" in choice:
        try:
            with open(data_file, "r") as file:
                print("\n📋 All Employees:\n")
                print(file.read())

        except FileNotFoundError:
            print("⚠️ No data file found. Add employees first!")

      elif "view" in choice or "3" in choice:
          view_employees()

      elif "update" in choice or "4" in choice:
        update_employee()

      elif "delete" in choice or "5" in choice:
        delete_employee()

      elif "export" in choice or "6" in choice:
            export_to_csv()

      elif "exit" in choice or "7" in choice:
          print("\n👋 Goodbye! Have a productive day!\n")
          break
      
      else:
          print("Invalid choice. Please say 'add', 'view all', 'view employee', 'update', 'delete' or 'exit'.\n")

run_employees_program()