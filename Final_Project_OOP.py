import json

class Employee:
    def __init__(self, name, emp_id, salary):
        self.name = name
        self.id = emp_id

        try:
            salary= float(salary)
            if salary >= 0:
                self.__salary = salary
            else:
                print("Invalid initial salary, setting to 0")
                self.__salary = 0
        except ValueError:
            print(f"Error: Salary for {name} must be a number! Setting to 0.")
            self.__salary = 0


    def set_salary(self,new_sal):
        if new_sal >= 0:
            self.__salary = new_sal
            print("✅ Salary updated successfully.")
        else:
            print("❌ Error: Salary cannot be negative!")

    def get_salary(self):

        return self.__salary


    def describe(self):
        print(f"ID: {self.id} | Name: {self.name} | Salary: {self.__salary}")

    def to_dict(self):
        return{
             'type':'Employee',
             'name':self.name,
             'emp_id':self.id,
             'salary':self.get_salary()

        }

class Manager(Employee):
    def __init__(self,name, emp_id, salary,bonus):

        super().__init__(name, emp_id, salary)
        self.bonus=bonus

    def get_total_salary(self):
        basic_salary=self.get_salary()
        total=basic_salary + self.bonus
        print(f"Total Income for Manager: {total}")

    def describe(self):
        print(f"💼 Manager: {self.name} | ID: {self.id} | Salary: {self.get_salary()} | Bonus: {self.bonus}")

    def to_dict(self):
        return {
            'type': 'Manager',
            'name': self.name,
            'emp_id': self.id,
            'salary': self.get_salary(),
            'bonus': self.bonus
        }




class Company:
    def __init__(self):

        self.employee = {}
        self.load_data()


    def add_employee(self, new_emp):
        if new_emp.id in self.employee:
            print('❌ Employee already exists!')
        else:
            self.employee[new_emp.id] = new_emp
            print(f'✅ Employee {new_emp.name} added.')
            self.save_data()


    def remove_employee(self, emp_id):
        if emp_id in self.employee:
            del self.employee[emp_id]
            print(f'🗑️ Employee {emp_id} deleted.')
        else:
            print('⚠️ Employee not found.')
            self.save_data()

    def show_all_employees(self):
        print('\n--- Company Staff ---')

        if not self.employee:
            print("No employees yet.")
        else:

            for emp_id, emp_object in self.employee.items():
                emp_object.describe()

        print('---------------------\n')

    def update_sal(self,emp_id,new_sal):
        if emp_id in self.employee:
            emp=self.employee[emp_id]
            emp.set_salary(new_sal)
            print('we updated ur salary')
            self.save_data()
            return new_sal

        else:
            print('we did not find he employee')
        print('---------------------\n')

    def save_data(self):
        data_list=[]
        for x in self.employee.values():
            emp_list=x.to_dict()
            data_list.append(emp_list)
        with open('emp_dict.json','w') as f:
            json.dump(data_list,f,indent=4)

    def load_data(self):
        try:
            with open('emp_dict.json','r') as f:
                data_read=json.load(f)
                for x in data_read:
                    if x['type']=='Employee':
                        emp= Employee(x['name'],x['emp_id'] ,x['salary'],)
                        self.employee[emp.id]= emp
                    #because we don't have other than manager and employee
                    else:
                        mgr = Manager(x['name'], x['emp_id'], x['salary'],x['bonus'])
                        self.employee[mgr.id]=mgr

        except FileNotFoundError:
            return





my_company = Company()

mgr2=Manager('talal',202,990,10)
my_company.add_employee(mgr2)
my_company.show_all_employees()
