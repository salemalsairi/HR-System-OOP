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
                print('---------------------\n')
                self.__salary = 0
        except ValueError:
            print(f"Error: Salary for {name} must be a number! Setting to 0.")
            self.__salary = 0



    def set_salary(self,new_sal):
        if new_sal >= 0:
            self.__salary = new_sal
            print("✅ Salary updated successfully.")
            print('---------------------\n')
        else:
            print("❌ Error: Salary cannot be negative!")
            print('---------------------\n')

    def get_salary(self):

        return self.__salary


    def describe(self):
        print(f"Employee:{self.name} | ID: {self.id} | Salary: {self.__salary}")

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
        self.__bonus=bonus

    def get_total_salary(self):

            basic_salary=self.get_salary()
            total=basic_salary + self.__bonus
            print(f"Total Income for Manager: {total}")
            print('---------------------\n')


    def get_bonus(self):
        return self.__bonus


    def set_bonus(self,new_bonus):
        if new_bonus >= 0:
            self.__bonus = new_bonus
            print("✅ Bonus updated successfully.")
            print('---------------------\n')
        else:
            print("❌ Error: Salary cannot be negative!")
            print('---------------------\n')

    def describe(self):
        print(f"💼 Manager: {self.name} | ID: {self.id} | Salary: {self.get_salary()} | Bonus: {self.get_bonus()}")


    def to_dict(self):
        return {
            'type': 'Manager',
            'name': self.name,
            'emp_id': self.id,
            'salary': self.get_salary(),
            'bonus': self.__bonus
        }




class Company:
    def __init__(self):

        self.employee = {}
        self.load_data()


    def add_employee(self, new_emp):
        if new_emp.id in self.employee:
            print('❌ Employee already exists!,try another id number')
            print('---------------------\n')
        else:

            self.employee[new_emp.id] = new_emp
            print(f'✅ Employee {new_emp.name} added.')
            print('---------------------\n')
            self.save_data()


    def remove_employee(self, emp_id):
        if emp_id in self.employee:
            del self.employee[emp_id]
            print(f'🗑️ Employee {emp_id} has been deleted.')
            print('---------------------\n')
        else:
            print('⚠️ Employee not found.')
            print('---------------------\n')
            self.save_data()

    def show_all_employees(self):
        print('\n--- Company Staff ---')

        if not self.employee:
            print("No employees yet.")
        else:
            sort=sorted(self.employee.values(),key=lambda x:x.__class__.__name__)
            for emp_object in sort:
                emp_object.describe()

        print('---------------------\n')


    def update_sal(self,emp_id,new_sal):
        if emp_id in self.employee:
            emp=self.employee[emp_id]
            emp.set_salary(new_sal)
            self.save_data()
            return new_sal

        else:
            print('we did not find the employee')
        print('---------------------\n')


    def update_bonus(self,emp_idd,new_bonus):
        if emp_idd in self.employee:
            emp=self.employee[emp_idd]
            emp.set_bonus(new_bonus)
            self.save_data()
            print('---------------------\n')
            return new_bonus
        else:
            print('we did not find the employee')
        print('---------------------\n')

    def promote_employee(self):
        print("\n--- Promote Employee to Manager ---")
        try:

            p_id = int(input('Enter the ID of the Employee to promote: '))

            if p_id in self.employee:
                current_emp = self.employee[p_id]
                if not isinstance(current_emp,Manager):
                    print(f"Found Employee: {current_emp.name}")

                    old_name=current_emp.name
                    old_salary=current_emp.get_salary()
                    try:
                        new_bonus=float(input('Enter the Bonus for the new Manager:'))
                    except ValueError:
                        print("Invalid bonus amount.")
                        return
                    new_manager=Manager(old_name,p_id,old_salary,new_bonus)
                    self.employee[p_id]=new_manager
                    self.save_data()
                    print(f"✅ Success! {old_name} is promoted to Manager .")
                else:
                    print("⚠This person is already a Manager")
            else:
                print('ID not found.')
        except ValueError:
            print("❌ Error: Please enter a valid ID.")
            print('-----------------------------------\n')


    def calculate_total_budget(self):
        total_money = 0
        for emp in self.employee.values():
            total_money += emp.get_salary()


            if isinstance(emp, Manager):
                total_money += emp.get_bonus()

        print(f"\n Total Monthly Cost for the Company: {total_money} USD\n")

    def save_data(self):
        data_list=[]
        for x in self.employee.values():
            emp_list=x.to_dict()
            data_list.append(emp_list)
        with open('emp_dict.json','w') as f:
            json.dump(data_list,f,indent=4)

    def search_employee(self):
        search_name = input("Enter the name to search for: ").lower()
        found = False
        print("\n--- Search Results ---")
        for emp in self.employee.values():
            if search_name in emp.name.lower():
                emp.describe()
                found=True
        if not found:
            print("❌ No employee found with this name.")
            print('---------------------\n')

    def load_data(self):
        try:
            with open('emp_dict.json','r') as f:
                data_read=json.load(f)
                for x in data_read:
                    if x['type']=='Employee':
                        emp= Employee(x['name'],x['emp_id'] ,x['salary'])
                        self.employee[emp.id]= emp
                    #because we don't have other than manager and employee
                    else:
                        mgr = Manager(x['name'], x['emp_id'], x['salary'],x['bonus'])
                        self.employee[mgr.id]=mgr

        except FileNotFoundError:
            return


    def interface(self):
        while True:
            print('1.add a new Employee or Manager')
            print('2.update salary for any Employee or Manager')
            print('3.get total salary of any manager')
            print('4.show all employees')
            print('5.remove an Employee or Manager')
            print('6.Search by Name')
            print('7.calculate total budget for the Company')
            print('8.promote Employee')
            print('9.end the project')
            item = input('enter a number 1-6')
            if item == '1':
                typo = input('\ndo you want to add an Employee or Manager?')
                try:
                    try:
                        if typo.lower() == 'employee':

                            new_id=input('enter the new id')
                            if new_id not in self.employee:

                                new_emp = input('write here:name, salary. in order')
                                splito = new_emp.split(',')
                                name = splito[0].strip()
                                salary_int = int(splito[1].strip())
                                final_emp = Employee(name, new_id, salary_int)
                                my_company.add_employee(final_emp)
                                my_company.save_data()
                                print('we added the employee successfully✅')
                                print('---------------------\n')
                            else:
                                print('the id is already exist')
                        elif typo.lower() == 'manager':

                            new_mgr = input('\nwrite here:name, emp_id, salary, bonus. in order:')

                            splito = new_mgr.split(',')
                            name = splito[0].strip()
                            id_int = int(splito[1].strip())
                            salary_int = int(splito[2].strip())
                            bonus_int = int(splito[3].strip())
                            final_manager = Manager(name, id_int, salary_int, bonus_int)
                            self.add_employee(final_manager)
                            self.save_data()
                            print('we added the Manager successfully✅')

                    except ValueError:
                        print(f'error,make sure u added a valid number in salary bonus and a valid id number')
                except IndexError:
                    print('error happened,try again')

                else:
                    print('try to add either Employee or Manager')
            elif item == '2':
                try:
                    id_= int(input('enter the id number for the employee u want to update his salary or bonus'))
                    if id_ in self.employee:
                        current_emp = self.employee[id_]
                        change_money=input('do you want to change salary or bonus')

                        if change_money.lower()=='salary':

                            changed_salary=int(input('enter the new salary'))
                            self.update_sal(id_,changed_salary)

                        elif change_money.lower()=='bonus':

                            if isinstance(current_emp,Manager):

                                    changed_bonus = int(input('enter the new bonus'))
                                    self.update_bonus(id_,changed_bonus)

                            else:print('❌Error: Only Managers allow bonuses.')
                        else:print('sorry, choose between bonus or salary')

                    else:print('Employee ID not found.')

                except ValueError:
                    print("Please enter valid numbers.")

            elif item == '3':
                try:
                    the_mgr_id = int(input('enter the id number for the Manager: '))
                    if the_mgr_id in self.employee:
                        current_mgr = self.employee[the_mgr_id]
                        if isinstance(current_mgr, Manager):
                            current_mgr.get_total_salary()
                        else:
                            print("❌Error: Only Managers allow this.")
                    else:
                        print("❌the id is not exist.")

                except ValueError:
                    print("Please enter a valid number.")

            elif item=='4':
                self.show_all_employees()

            elif item=='5':
                removed=int(input('enter the id number for the employee u want to remove'))
                self.remove_employee(removed)

            elif item=='6':
                self.search_employee()

            elif item=='7':
                self.calculate_total_budget()
            elif item=='8':
                self.promote_employee()
            elif item=='9':
                print('\n---------------------')
                print('end...')
                break

            else:
                print('please,enter a valid number.')


my_company = Company()

my_company.interface()





















