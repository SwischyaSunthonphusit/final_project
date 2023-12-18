# import database module
import sys

from database import DB, read_csv, Table, create_csv
import csv, random, datetime
from _datetime import datetime


my_DB = DB()


def initializing():
    persons = read_csv('persons.csv')
    login = read_csv('login.csv')
    project_table = read_csv('project_table.csv')
    advisor_request = read_csv('advisor_request.csv')
    member_request = read_csv('member_request.csv')
    project_evaluate = read_csv('project_evaluate.csv')

    persons_table = Table('persons', persons)
    login_table = Table('login', login)
    project_table = Table('project_table', project_table)
    advisor_request_table = Table('advisor_request', advisor_request)
    member_request_table = Table('member_request', member_request)
    project_evaluate_table = Table('project_evaluate', project_evaluate)

    my_DB.insert(persons_table)
    my_DB.insert(login_table)
    my_DB.insert(project_table)
    my_DB.insert(advisor_request_table)
    my_DB.insert(member_request_table)
    my_DB.insert(project_evaluate_table)

    return my_DB


# define a funcion called login

def login():
    username = input('Username: ')
    password = input('Password: ')
    _login = my_DB.search('login')
    users = _login.filter(lambda x: x['username'] == username).filter(lambda x: x['password'] == password)
    if len(users.table) != 0:
        return [users.table[0]['ID'], users.table[0]['role']]
    print('Invalid ID or Username, Please try again')
    login()
    return None


def search_project(_id):
    project_table = my_DB.search('project_table')
    project_table_filter = project_table.filter(lambda x: x['Leader'] == _id or x['Member1'] == _id or x['Member2'] == _id)
    print(project_table_filter.table)
    return project_table_filter.table


def find_person(_id):
    person = my_DB.search('persons')
    person_info = person.filter(lambda x: x['ID'] == _id)
    return person_info


def member_send_request(_id, project_id):
    persons = my_DB.search('persons')
    _login = my_DB.search('login')
    students_id = _login.filter(lambda x: x['role'] == 'student').select(['ID', 'username'])
    students_info = persons.filter(lambda x: x['ID'] == students_id)
    print("[----Students that still can be a member----]")
    print("---ID---     ---username---     ---role---")
    for student_id in students_id:
        print(f"{student_id['ID']} {student_id['username']:>15} {'Student':>17}")
    to_member_id = int(input("Member's ID you want to send a request: "))
    if to_member_id == _login.filter(lambda x: x['role'] == 'member').select(['ID']):
        print('This student is already became a member for other project! Please select new student ID')
        to_member_id = int(input("Member's ID you want to send a request: "))

    current_time = datetime.now()
    person_info = persons.filter(lambda x: x['ID'] == str(to_member_id))
    if person_info.table:
        new_message = {'ProjectID': project_id,
                       'to_be_member': str(to_member_id),
                       'From': _id,
                       'Response': 'None',
                       'Response_date': current_time,

                       }
        member_request = my_DB.search('member_request')
        member_request.insert(new_message)
        print(f"Message send successfully.")
        print('------------')
    else:
        print('Invalid ID')


def advisor_request(_id, project_id):
    person = my_DB.search('persons')
    persons = my_DB.search('persons')
    _login = my_DB.search('login')
    advisors_id = _login.filter(lambda x: x['role'] == 'faculty').select(['ID', 'username'])
    print("[----Faculty that still can be advisor----]")
    print("---ID---     ---username---     ---role---")
    for advisor_id in advisors_id:
        print(f"{advisor_id['ID']} {advisor_id['username']:>15} {'Faculty':>17}")

    to_advisor_id = input("Advisor's ID you want to send a request: ")
    if to_advisor_id == _login.filter(lambda x: x['role'] == 'advisor').select(['ID']):
        print('This faculty is already became an advisor for other project! Please select new faculty ID')
        to_advisor_id = int(input("Advisor's ID you want to send a request: "))

    person_info = person.filter(lambda x: x['ID'] == str(to_advisor_id))
    print(person_info.table)
    current_time = datetime.now()
    _login = my_DB.search('login')
    if person_info.table:
        new_message = {'ProjectID': project_id,
                       'to_be_advisor': to_advisor_id,
                       'From': _id,
                       'Response': 'None',
                       'Response_date': current_time,
                       }
        advisor_request = my_DB.search('advisor_request')
        advisor_request.insert(new_message)
        print(f"Message send successfully!.")
        print('------------')
    else:
        print('Invalid ID')


def append_member(lead_id, _id):
    project = my_DB.search('project_table')
    lead_project = project.filter(lambda x: x['Leader'] == lead_id).table[0]
    if lead_project['Member1'] == 'None':
        lead_project['Member1'] = _id
        return True
    if lead_project['Member2'] == 'None':
        lead_project['Member2'] = _id
        return True
    # if code come here means there all member is full
    print("This project's member is already full! Please select another project")
    return False


def append_advisor(lead_id, _id):
    project = my_DB.search('project_table')
    lead_project = project.filter(lambda x: x['Leader'] == lead_id).table[0]
    if lead_project['Advisor'] == 'None':
        lead_project['Advisor'] = _id
        return True
    return False


def create_project(_id):
    print('---Create Project---')
    title = input('Project Title: ')
    content = input('Project Content: ')
    project_id = random.randint(0000, 9999)
    new_project = {'ProjectID': project_id,
                   'Leader': _id,
                   'Title': title,
                   'Content': content,
                   'Member1': 'None',
                   'Member2': 'None',
                   'Advisor': 'None',
                   'Status': 'Unfinished'
                   }
    my_DB.search('project_table').insert(new_project)
    _login = my_DB.search('login')
    persons = my_DB.search('persons')
    _login.filter(lambda x: x['ID'] == _id).update('role', 'leader')

    mem_choice = input('Do you want to send pending message to any student? [y/n]: ')
    if mem_choice == 'y':
        students_id = _login.filter(lambda x: x['role'] == 'student')
        students_info = persons.filter(lambda x: x['ID'] == students_id)
        print("[----Students that still can be a member----]")
        print("---ID---  ---first name--- ---last name--- ---role---")
        for student_id in students_id.table:
            for student_info in students_info.table:
                print(f"{student_id['role']} {student_info['first']} {student_info['last']} Student")
        member_send_request(_id, project_id)

    adv_choice = input('Do you want to send pending message to any advisor? [y/n]: ')
    if adv_choice == 'y':
        advisor_request(_id, project_id)

    print('Your project is successful!')
    print('------------')
    return project_id


def exit():
    create_csv('project_table.csv', ['ProjectID', 'Title', 'Leader', 'Content', 'Member1', 'Member2', 'Advisor', 'Status'],
               my_DB.search('project_table'))

    create_csv('persons.csv', ['ID', 'first', 'last', 'type'], my_DB.search('persons'))

    create_csv('login.csv', ['ID', 'username', 'password', 'role'], my_DB.search('login'))

    create_csv('member_request.csv', ['ProjectID', 'to_be_member', 'From', 'Response', 'Response_date'],
               my_DB.search('member_request'))

    create_csv('advisor_request.csv', ['ProjectID', 'to_be_advisor', 'From', 'Response', 'Response_date'],
               my_DB.search('advisor_request'))

    create_csv('project_evaluate.csv', ['ProjectID', 'Leader', 'Advisor', 'Score', 'Advice'],
               my_DB.search('project_evaluate'))


class Admin:

    def __init__(self):
        self.id = 0
        self.username = str
        self.password = 0
        self.role = str

    def admin_choice(self):
        print(f'----MENU----\n'
              f'Welcome! \n'
              f'Your role is Admin \n'
              f'What do you want to do? \n'
              f'1. Database \n'
              f'0. Exit')
        choice = int(input('Select:'))
        while 0 < choice > 1:
            print('Invalid choice, Please select again.')
            choice = int(input('Select:'))

        if choice == 1:
            print('1. Manage account \n'
                  '2. Create new account \n'
                  '3. Remove account')
            choice = int(input('Select: '))
            if choice == 1:
                self.manage_account()
                self.admin_choice()
            if choice == 2:
                self.create_account()
                self.admin_choice()
            if choice == 3:
                self.remove_account()
                self.admin_choice()

        if choice == 0:
            exit()

    def manage_account(self):
        _login = my_DB.search('login')
        print("---ID---   ---username---  ---password---  ------role------")
        for person_login in _login.table:
            print(f"{person_login['ID']:<10} {person_login['username']:<10} {person_login['password']:>15} {person_login['role']:>15}")
        self.id = input('Select Person ID: ')
        persons = my_DB.search('persons')
        persons = persons.filter(lambda x: x['ID'] == self.id)
        login = _login.filter(lambda x: x['ID'] == self.id)
        for login_ in login.table:
            self.username = login_['username']
            self.password = login_['password']
            self.role = login_['role']
        for person in persons.table:
            first = person["first"]
            last = person["last"]
            print(f'What do you want to do with {first} {last} \n'
                  f'1. ID \n'
                  f'2. Username \n'
                  f'3. Password \n'
                  f'4. Role \n'
                  f'0. Reselect account ID')
            choice = int(input('Select number: '))
            while 0 < choice > 4:
                print('Invalid choice, Please select again.')
                choice = int(input('Select number: '))
            if choice == 1:
                print(f"{person['first']} ID: {self.id}")
                change_id = input(f'Input new ID for {person["first"]}: ')
                person.update('ID', change_id)
                login.update('ID', change_id)
                self.admin_choice()

            if choice == 2:
                print(f"{person['first']} username: {self.username}")
                change_user = input(f'Input new username for {person["first"]}: ')
                login.update('username', change_user)
                self.admin_choice()

            if choice == 3:
                print(f"{person['first']} password: {self.password}")
                change_pass = input(f'Input new password for {person["first"]}: ')
                login.update('password', change_pass)
                self.admin_choice()

            if choice == 4:
                print(f"{person['first']} role: {self.role}")
                change_role = input(f'Input new role for {person["first"]} [student/faculty]: ')
                login.update('role', change_role)
                self.admin_choice()

            if choice == 0:
                self.manage_account()

    def create_account(self):
        persons = my_DB.search('persons')
        _login = my_DB.search('login')
        print('---Create New Account---')
        self.username = input('New Username: ')
        self.password = input('New Password: ')
        if len(self.password) != 4:
            print('Invalid password, please create new password')
            self.password = input('New Password: ')
        self.role = input('New Role [Student/Faculty]: ')
        if self.role != 'Student' and 'Faculty':
            print('Invalid role, please enter role again')
            self.role = input('New Role: ')
        self.id = random.randint(1111111, 9999999)
        account_id = _login.filter(lambda x: x['ID'] == id)
        for _id in account_id.table:
            if _id == self.id:
                self.id = random.randint(1111111, 9999999)

        first = input('First name: ')
        last = input('Last name: ')

        new_person = {'ID': self.id,
                      'first': first,
                      'last': last,
                      'type': self.role
                      }
        print(type(persons))
        persons.insert(new_person)

        new_account = {'ID': self.id,
                       'username': self.username,
                       'password': self.password,
                       'role': self.role
                       }
        print(type(_login))
        _login.insert(new_account)

        print(f'Create new account Successful! \n'
              f'ID: {self.id} \n'
              f'username: {self.username} \n'
              f'password: {self.password} \n'
              f'role: {self.role}')

    def remove_account(self):
        _login = my_DB.search('login')
        print("---ID---   ---username---  ---password---  ------role------")
        for person_login in _login.table:
            print(f"{person_login['ID']:<10} {person_login['username']:<10} {person_login['password']:>15} "
                  f"{person_login['role']:>15}")
        self.id = input('Input user ID you want to remove: ')
        _login = my_DB.search('login')
        persons = my_DB.search('persons')
        project = my_DB.search('project_table')
        in_project_id_stu = project.filter(lambda x: x['Leader'] == self.id or x['Member1'] == self.id or x['Member2']
                                                     == self.id)
        if in_project_id_stu.table:
            print("Can't delete this account, student still modify their project")
        in_project_id_fac = project.filter(lambda x: x['Advisor'] == self.id)
        if in_project_id_fac.table:
            print("Can't delete this account, advisor still have to evaluate student's project")

        for i in range(len(_login.table)):
            if _login.table[i]['ID'] == self.id:
                if persons.table[i]['ID'] == self.id:
                    del _login.table[i]
                    del persons.table[i]
                    print(f'Remove {self.id} successfully!')
                    break


class Student:
    def __init__(self, _id):
        self.id = _id
        self.lead_id = 0

    def choice_student(self):
        print(f'Welcome!\n'
              f'Your role now is Student. \n'
              f'What do you want to do? \n'
              f'1. Create Project \n'
              f'2. Message \n'
              f'0. Exit')
        choice = int(input('Select: '))
        while 0 < choice > 2:
            print('Invalid choice, Please select again.')
            choice = int(input('Select: '))

        if choice == 0:
            exit()

        elif choice == 1:
            self.create_project_student()

        elif choice == 2:
            self.student_check_message()

    def create_project_student(self):
        member_request = my_DB.search('member_request')
        tobe_member = member_request.filter(lambda x: x['to_be_member'] == self.id)
        for member in tobe_member.table:
            if self.id == member['to_be_member']:
                print("You haven't deny all member pending request.")
                print('------------')
                self.choice_student()
        create_project(self.id)
        Leader(self.id).leader_choice()

    def find_person(self):
        person = my_DB.search('persons')
        person_info = person.filter(lambda x: x['ID'] == self.id)
        return person_info

    def student_check_message(self):
        project_table = my_DB.search('project_table')
        member = project_table.select(['Member1', 'Member2'])
        mem_request = my_DB.search('member_request')
        request = mem_request.filter(lambda x: x['to_be_member'] == self.id)
        if not request.table:
            print('You have no message from leader.')
            print('------------')
            Student.choice_student(val[0])
        else:
            for row in request.table:
                project = project_table.filter(lambda x: x['ProjectID'] == row['ProjectID']).table
                print(f"ProjectID: {row['ProjectID']} \n"
                      f"message from: {row['From']}")
            self.lead_id = input("Input leader's ID you want to respond: ")
            leader_pending = mem_request.filter(lambda x: x['From'] == self.lead_id)
            choice = input('deny or accept to be member [y/n]: ')
            while choice is True:
                if choice != 'y' or 'n':
                    print('Invalid choice, Please try again.')
                    choice = input('deny or accept to be member [y/n]: ')

            if choice == 'y':
                leader_pending.update('Response', 'y')
                append_member(self.lead_id, self.id)
                person = my_DB.search('persons')
                _login = my_DB.search('login')
                __login = _login.filter(lambda x: x['ID'] == self.id)
                __login.update('role', 'member')
                mem_request.filter(lambda x: x['to_be_member'] == self.id).filter(lambda x: x['Response'] == 'None')\
                    .update('Response', 'y')
                project_name = project_table.filter(lambda x: x["Leader"] == self.lead_id).table[0]["Title"]
                print(f'You are member of {self.lead_id}: {project_name} project!')
                print('------------')
                Member(self.id).member_choice()

            elif choice == 'n':
                leader_pending.update('Response', 'n')
                print(f'you deny {self.lead_id}: {search_project(self.lead_id).select("Title")} project!')
                print('------------')
                Student(self.id).choice_student()


class Leader:

    def __init__(self, id):
        self.id = id
        self.project_id = 0

    def leader_choice(self):
        print(f'----MENU----\n'
              f'Welcome! \n'
              f'Your role now is Leader. \n'
              f'What do you want to do? \n'
              f'1. Project \n'
              f'2. Message \n'
              f'3. See score and advice from advisor \n'
              f'0. exit')
        choice = int(input('Select: '))
        while 0 < choice > 3:
            print('Invalid choice, Please select again.')
            choice = int(input('Select: '))

        if choice == 0:
            exit()

        elif choice == 1:
            project_table = my_DB.search('project_table')
            for i in project_table.filter(lambda x: x['Leader'] == self.id).table:
                print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
                print('1. View your project detail \n'
                      '0. Return to menu')
                self.project_id = i['ProjectID']
            choice = int(input('Select your choice: '))
            while choice != 1 and choice != 0:
                print('Invalid choice, Please select again.')
                choice = int(input('Select your choice: '))
            if choice == 1:
                self.project_info()
                print('1. Modify this project \n'
                      '0. Return to menu')
                choice = int(input('Select your choice: '))
                while choice != 1 and choice != 0:
                    print('Invalid choice, Please select again.')
                    choice = int(input('Select your choice: '))

                if choice == 1:
                    self.leader_check_project()
                if choice == 0:
                    self.leader_choice()
            if choice == 0:
                self.leader_choice()

        elif choice == 2:
            print('1. Send message to student. \n'
                  '2. Send message to advisor \n'
                  '0. Return to menu')
            choice = int(input('Select your choice: '))
            while 0 < choice > 2:
                print('Invalid choice, Please select again.')
                choice = int(input('Select your choice: '))
            if choice == 1:
                project_table = my_DB.search('project_table')
                for i in project_table.filter(lambda x: x['Leader'] == self.id).table:
                    print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
                _project_id = int(input('Select project ID you want to send a member request: '))
                member_send_request(self.id, _project_id)
                Leader(self.id).leader_choice()
            elif choice == 2:
                project_table = my_DB.search('project_table')
                for i in project_table.filter(lambda x: x['Leader'] == self.id).table:
                    print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
                _project_id = int(input('Select project ID you want to send a advisor request: '))
                advisor_request(self.id, _project_id)
                Leader(self.id).leader_choice()

            elif choice == 0:
                self.leader_choice()

        elif choice == 3:
            self.see_evaluate()

    def see_evaluate(self):
        project_evaluate = my_DB.search('project_evaluate')
        project_evaluate = project_evaluate.filter(lambda x: x['Leader'] == self.id).table
        if not project_evaluate:
            print("You haven't send project to advisor, please go to choice[1]: Project to send your project.")
            print('------------')
            Leader(self.id).leader_choice()
        project = my_DB.search('project_table')
        project_table = project.filter(lambda x: x['Leader'] == self.id).table
        if project_evaluate[0]['Advice'] == "None":
            print('You have full score for your project! This project is finished')
            print('------------')
            Leader(self.id).leader_choice()
        print(f"---Score and Advice--- \n"
              f"ProjectID: {project_evaluate[0]['ProjectID']} \n"
              f"Title: {project_table[0]['Title']} \n"
              f"Score: {project_evaluate[0]['Score']} \n"
              f"Advice from advisor: {project_evaluate[0]['Advice']}")
        choice = input('Do you want to rectify this project? [y/n]: ')
        if choice == 'y':
            self.project_id = project_evaluate[0]['ProjectID']
            self.leader_check_project()
        elif choice == 'n':
            print('------------')
            self.leader_choice()

    def leader_check_project(self):
        project_table = my_DB.search('project_table')
        print('What do you want to do with this project? \n'
              '1. Rename Title \n'
              '2. Modify Content \n'
              '3. Finished this Project \n'
              '0. Return to menu')
        choice = int(input('Select your choice: '))
        if choice == 1:
            new_title = input('New title name: ')
            projects = project_table.filter(lambda x: x['ProjectID'] == str(self.project_id))
            projects.update('Title', new_title)
            print('Your title update successfully.')
            print('------------')
            Leader(self.id).leader_choice()
        if choice == 2:
            new_content = input('New Content: ')
            projects = project_table.filter(lambda x: x['ProjectID'] == str(self.project_id))
            print(self.project_id)
            projects.update('Content', new_content)
            print(projects.table)
            print('Your content update successfully.')
            print('------------')
            Leader(self.id).leader_choice()
        if choice == 3:
            projects = project_table.filter(lambda x: x['ProjectID'] == str(self.project_id))
            for project in projects.table:
                if project['Advisor'] == 'None':
                    print("You have no advisor! Please send a message to ask faculty to be your advisor first.")
                    print('-------')
                    self.leader_check_project()
                if project['Member1'] == 'None' or ['Member2'] == 'None':
                    print("You have not enough member! Please send a message to ask student to be your member first.")
                    print('-------')
                    self.leader_check_project()
                project['Status'] = 'Pending'
            print('Your project is finished! this project will automatically pending for advisor evaluation.')
            print('------------')
            Leader(self.id).leader_choice()
        if choice == 0:
            Leader(self.id).leader_choice()

    def project_info(self):
        project_table = my_DB.search('project_table')
        my_project = project_table.filter(lambda x: x['Leader'] == self.id).table
        print(f"----Project Detail---- \n"
              f"ProjectID: {my_project[0]['ProjectID']} \n"
              f"Title: {my_project[0]['Title']} \n"
              f"Content: {my_project[0]['Content']} \n"
              f"Leader: {my_project[0]['Leader']} \n"
              f"Member1: {my_project[0]['Member1']} \n"
              f"Member2: {my_project[0]['Member2']} \n"
              f"Advisor: {my_project[0]['Advisor']} \n"
              f"Status: {my_project[0]['Status']}")


class Member:
    def __init__(self, id):
        self.id = id
        self.lead_id = 0
        self.project_id = 0

    def member_choice(self):
        print(f'----MENU----\n'
              f'Welcome! \n'
              f'Your role now is Member. \n'
              f'What do you want to do? \n'
              f'1. Project \n'
              f'2. See score and advice for your project\n'
              f'0. Exit')
        choice = int(input('Select your choice: '))
        while 0 < choice > 2:
            print('Invalid choice, Please select again.')
            choice = int(input('Select your choice: '))
        if choice == 1:
            project_table = my_DB.search('project_table')
            project_table_filter = project_table.filter(lambda x: x['Member1'] == self.id or x['Member2'] == self.id)
            for i in project_table_filter.table:
                self.lead_id = i['Leader']
                print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
                self.project_id = i['ProjectID']

            print('1. View your project detail \n'
                  '0. Return to menu')
            choice = int(input('Select your choice: '))
            while choice != 0 and choice != 1:
                print('Invalid choice, Please select again.')
                choice = int(input('Select your choice: '))
            if choice == 1:
                self.project_info()
                print('1. Modify this project \n'
                      '0. Return to menu')
                choice = int(input('Select your choice: '))
                while choice != 0 and choice != 1:
                    print('Invalid choice, Please select again.')
                    choice = int(input('Select your choice: '))
                if choice == 1:
                    self.member_check_project()
                if choice == 0:
                    self.member_choice()
            if choice == 0:
                self.member_choice()

        if choice == 2:
            self.see_evaluate()
        if choice == 0:
            exit()

    def member_check_project(self):
        project_table = my_DB.search('project_table')
        project = project_table.filter(lambda x: x['Member1'] == self.id or x['Member2'] == self.id)
        for i in project.table:
            print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>} \n"
                  f"Content: {i['Content']}")
            _project_id = i['ProjectID']
        new_content = input('New Content: ')
        project.filter(lambda x: x['ProjectID'] == str(_project_id)).update('Content', new_content)
        print(f'You finished update content!')
        self.member_choice()

    def see_evaluate(self):
        project_evaluate = my_DB.search('project_evaluate')
        project_evaluate = project_evaluate.filter(lambda x: x['Leader'] == self.lead_id).table
        project = my_DB.search('project_table')
        project_table = project.filter(lambda x: x['Leader'] == self.lead_id).table
        if project_evaluate[0]['Advice'] == "None":
            print('You have full score for your project! This project is finished')
            print('------------')
        print(f"---Score and Advice--- \n"
              f"ProjectID: {project_evaluate[0]['ProjectID']} \n"
              f"Title: {project_table[0]['Title']} \n"
              f"Score: {project_evaluate[0]['Score']} \n"
              f"Advice from advisor: {project_evaluate[0]['Advice']}")
        choice = input('Do you want to rectify this project? [y/n]: ')
        if choice == 'y':
            self.member_check_project()
        elif choice == 'n':
            print('------------')
            self.member_choice()

    def project_info(self):
        project_table = my_DB.search('project_table')
        my_project = project_table.filter(lambda x: x['Member1'] == self.id or x['Member2'] == self.id).table
        print(f"----Project Detail---- \n"
              f"ProjectID: {my_project[0]['ProjectID']} \n"
              f"Title: {my_project[0]['Title']:<10} \n"
              f"Leader: {my_project[0]['Leader']:<10} \n"
              f"Content: {my_project[0]['Content']:<10} \n"
              f"Member1: {my_project[0]['Member1']:<10} \n"
              f"Member2: {my_project[0]['Member2']:<10} \n"
              f"Advisor: {my_project[0]['Advisor']:<10} \n"
              f"Status: {my_project[0]['Status']:<10}")


class Faculty:
    def __init__(self, id):
        self.id = id

    def faculty_choice(self):
        print(f'----MENU----\n'
              f'Welcome!\n'
              f'Your role now is Faculty. \n'
              f'What do you want to do? \n'
              f'1. Message \n'
              f'0. Exit')
        choice = int(input('Select your choice: '))
        while choice != 0 and choice != 1:
            print('Invalid choice, Please select again.')
            choice = int(input('Select your choice: '))
        if choice == 1:
            self.faculty_check_message()
        elif choice == 0:
            exit()

    def faculty_check_message(self):
        project = my_DB.search('project_table')
        advisor_request = my_DB.search('advisor_request')
        request = advisor_request.filter(lambda x: x['to_be_advisor'] == self.id)
        if not request.table:
            print('You have no message from leader.')
            print('------------')
            self.faculty_choice()
        for row in request.table:
            project_title = project.filter(lambda x: x['Leader'] == row['From']).table[0]['Title']
            print(f"message from: {row['From']} Project Title: {project_title}")
        lead_id = input("Input leader's ID you want to respond: ")
        leader_pending = request.filter(lambda x: x['From'] == lead_id)
        if not leader_pending.table:
            print('Invalid LeadID')
        else:
            choice = input('deny or accept to be advisor [y/n]: ')
            while choice != 'y' and choice != 'n':
                print('Invalid choice, Please try again.')
                choice = input('deny or accept to be advisor [y/n]: ')
            if choice == 'y':
                check = append_advisor(lead_id, self.id)
                if check:
                    print(f'You are advisor of {search_project(lead_id)["Title"]} project!')
                    leader_pending.update('Response', 'y')
                    other_lead_pending = request.filter(lambda x: x['From'] != lead_id)
                    other_lead_pending.update('Response', 'n')
                    _login = my_DB.search('login')
                    _login.filter(lambda x: x['ID'] == self.id).update('role', 'advisor')
                    Advisor(self.id).advisor_choice()
            elif choice == 'n':
                leader_pending.update('Response', 'n')
                print(f'you deny {lead_id}: {search_project(lead_id)["Title"]} project!')
                self.faculty_choice()


class Advisor:
    def __init__(self, id):
        self.id = id
        self.project_id = 0

    def advisor_choice(self):
        print(f'Welcome!\n'
              f'Your role now is Advisor. \n'
              f'What do you want to do? \n'
              f'1. Check Project\n'
              f'2. Evaluate Project \n'
              f'0. Exit')
        choice = int(input('Select your choice: '))
        while choice != 0 and choice != 1 and choice != 2:
            print('Invalid choice, Please select again.')
            choice = int(input('Select your choice: '))
        if choice == 1:
            self.advisor_check_project()
        if choice == 2:
            project_table = my_DB.search('project_table')
            advisor_project = project_table.filter(lambda x: x['Advisor'] == self.id) \
                .filter(lambda x: x['Status'] == 'Pending' and x['Member1'] != 'None' and x['Member2'] != 'None')
            for i in advisor_project.table:
                print(f"ProjectID: {i['ProjectID']} Title: {i['Title']}")
            self.project_id = input('Select project ID you want to evaluate (select 0 if you want to return to menu): ')
            if self.project_id == '0':
                print('------------')
                self.advisor_choice()
            self.evaluate_project()

        if choice == 0:
            exit()

    def advisor_check_project(self):
        project_table = my_DB.search('project_table')
        advisor_project = project_table.filter(lambda x: x['Advisor'] == self.id)\
            .filter(lambda x: x['Status'] == 'Pending' and x['Member1'] != 'None' and x['Member2'] != 'None')
        for i in advisor_project.table:
            print(f"ProjectID: {i['ProjectID']} Title: {i['Title']}")
        print('Select Project ID you want to check (select 0 if you want to return to menu)')
        self.project_id = input('Select:')
        if self.project_id == '0':
            print('------------')
            self.advisor_choice()
        self.project_info()
        choice = input('Do you want to evaluate this project? [y/n]: ')

        if choice == 'y':
            self.evaluate_project()
            self.advisor_check_project()

        if choice == 'n':
            print('This project will still wait for you to evaluate it!')
            print('------------')
            self.advisor_choice()

    def find_project_advisor(self):
        project_table = my_DB.search('project_table')
        advisor_project = project_table.filter(lambda x: x['Advisor'] == self.id) \
            .filter(lambda x: x['Status'] == 'Pending')
        advisor_project = advisor_project.filter(lambda x: x['ProjectID'] == self.project_id).table
        return advisor_project

    def project_info(self):
        project_table = my_DB.search('project_table')
        my_project = project_table.filter(lambda x: x['Advisor'] == self.id).table
        print(f"----Project Detail---- \n"
              f"ProjectID: {my_project[0]['ProjectID']} \n"
              f"Title: {my_project[0]['Title']} \n"
              f"Leader: {my_project[0]['Leader']} \n"
              f"Content: {my_project[0]['Content']} \n"
              f"Member1: {my_project[0]['Member1']} \n"
              f"Member2: {my_project[0]['Member2']} \n"
              f"Advisor: {my_project[0]['Advisor']} \n"
              f"Status: {my_project[0]['Status']}")

    def evaluate_project(self):
        project = my_DB.search('project_table')
        to_eval_project = project.filter(lambda x: x['Status'] == 'Pending').filter(lambda x: x['Advisor'] == self.id)
        print('----Evaluation----')
        score = int(input(f'From 1 to 10, what score you think this project should have? '
                      f'(if this project is perfect, please score it 10): '))
        evaluate = my_DB.search('project_evaluate')
        advisor_project = self.find_project_advisor()
        leader = advisor_project[0]['Leader']
        eval_project = {'ProjectID': self.project_id,
                        'Leader': leader,
                        'Advisor': self.id,
                        'Score': score,
                        'Advice': 'None',
                        }
        evaluate.insert(eval_project)
        if score != 10:
            advice = input('Do you have any advice for leader and member to rectify their project?: ')
            evaluate.update('Advice', advice)
            to_eval_project.update('Status', 'Unfinished')
        else:
            to_eval_project.update('Status', 'Finished')
        project_info = self. find_project_advisor()
        print(f"Your evaluation for {project_info[0]['Title']} is finished!")
        print('------------')


initializing()
val = login()
if val is None:
    print('Invalid')
else:
    if val[1] == 'student':
        Student(val[0]).choice_student()
    elif val[1] == 'member':
        Member(val[0]).member_choice()
    elif val[1] == 'leader':
        Leader(val[0]).leader_choice()
    elif val[1] == 'faculty':
        Faculty(val[0]).faculty_choice()
    elif val[1] == 'advisor':
        Advisor(val[0]).advisor_choice()
    elif val[1] == 'admin':
        Admin().admin_choice()