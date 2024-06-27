import csv
import random

class Employee:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.secret_child = None

    def __str__(self):
        return f"{self.name} ({self.email})"

class SecretSanta:
    def __init__(self, employees, previous_assignments=None):
        self.employees = employees
        self.previous_assignments = previous_assignments or {}

    def assign(self):
        available_children = self.employees[:]
        random.shuffle(available_children)
        
        for employee in self.employees:
            for potential_child in available_children:
                if (employee.name != potential_child.name and 
                    self.previous_assignments.get(employee.email) != potential_child.email):
                    employee.secret_child = potential_child
                    available_children.remove(potential_child)
                    break

    def export_assignments(self, output_file):
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for employee in self.employees:
                writer.writerow({
                    'Employee_Name': employee.name,
                    'Employee_EmailID': employee.email,
                    'Secret_Child_Name': employee.secret_child.name,
                    'Secret_Child_EmailID': employee.secret_child.email
                })

def read_employees(file_path):
    employees = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            employees.append(Employee(row['Employee_Name'], row['Employee_EmailID']))
    return employees

def read_previous_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            assignments[row['Employee_EmailID']] = row['Secret_Child_EmailID']
    return assignments

def main():
    employees_file = 'employees.csv'
    previous_assignments_file = 'previous_assignments.csv'
    output_file = 'new_assignments.csv'
    
    employees = read_employees(employees_file)
    previous_assignments = read_previous_assignments(previous_assignments_file)
    
    secret_santa = SecretSanta(employees, previous_assignments)
    secret_santa.assign()
    secret_santa.export_assignments(output_file)

if __name__ == '__main__':
    main()
