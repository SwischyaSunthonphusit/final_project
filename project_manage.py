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
    project_detail = read_csv('project_detail.csv')

    persons_table = Table('persons', persons)
    login_table = Table('login', login)
    project_table = Table('project_table', project_table)
    advisor_request_table = Table('advisor_request', advisor_request)
    member_request_table = Table('member_request', member_request)
    project_detail_table = Table('project_detail', project_detail)

    my_DB.insert(persons_table)
    my_DB.insert(login_table)
    my_DB.insert(project_table)
    my_DB.insert(advisor_request_table)
    my_DB.insert(member_request_table)
    my_DB.insert(project_detail_table)

    return my_DB


# define a funcion called login

def login():
    username = input('Username: ')
    password = input('Password: ')
    _login = my_DB.search('login')
    users = _login.filter(lambda x: x['username'] == username).filter(lambda x: x['password'] == password)
    if len(users.table) != 0:
        return [users.table[0]['ID'], users.table[0]['role']]
    return None


def search_project(_id):
    project_table = my_DB.search('project_table')
    project_table_filter = project_table.filter(lambda x: x['Lead'] == _id or x['Member1'] == _id or x['Member2'] == _id)
    return project_table_filter.table[0]


def find_person(_id):
    person = my_DB.search('persons')
    person_info = person.filter(lambda x: x['ID'] == _id)
    return person_info


def is_member_in_group(self):
    pass
    # project_table = my_DB.search('project_table')
    # project = project_table.select(['ProjectID', 'Title', 'Lead', 'Member1', 'Member2', 'Advisor', 'Status'])
    # print(project)
    # # for member in project:
    #     if self.id == member:
    #         for member2 in project2:
    #             if self.id == member2:
    #                 return True
    # return False


def member_send_request(_id, project_id):
    person = my_DB.search('persons')
    _login = my_DB.search('login')
    to_member_id = int(input("Member's ID you want to send a request: "))
    current_time = datetime.now()
    person_info = person.filter(lambda x: x['ID'] == str(to_member_id)).table
    if person_info:
        new_message = {'ProjectID': project_id,
                       'to_be_member': str(to_member_id),
                       'From': _id,
                       'Response': 'None',
                       'Response_date': current_time,

                       }
        member_request = my_DB.search('member_request')
        member_request.insert(new_message)
        print(f"Message send to {person_info[0]['first']} {person_info[0]['last']}.")
    else:
        print('Invalid ID')


def advisor_request(_id, project_id):
    to_advisor_id = int(input("Advisor's ID you want to send a request: "))
    current_time = datetime.now()
    _login = my_DB.search('login')
    if _login.filter(lambda x: x['ID'] == to_advisor_id).table:
        new_message = {'ProjectID': project_id,
                       'to_be_advisor': to_advisor_id,
                       'From': _id,
                       'Response': 'None',
                       'Response_date': current_time,
                       }
        advisor_request = my_DB.search('advisor_request')
        advisor_request.insert(new_message)
    else:
        print('Invalid ID')


def append_member(lead_id, _id, project_id):
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
    lead_project = project.filter(lambda x: x['Lead'] == lead_id).table[0]
    if lead_project['Advisor'] == 'None':
        lead_project['Advisor'] = _id
        return True
    print("This project's member is already full! Please select another project")
    return False


def create_project(_id):
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
                   'Status': 'Pending'
                   }
    my_DB.search('project_table').insert(new_project)
    _login = my_DB.search('login')
    _login.filter(lambda x: x['ID'] == _id).update('role', 'leader')

    mem_choice = input('Do you want to send pending message to any student? [y/n]: ')
    if mem_choice == 'y':
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


# class Admin:
#
#     def __init__(self):
#         self.project_id = 0
#         self.member1 = 0
#         self.member2 = 0
#         self.advisor = 0
#
#     def choice_admin(self):
#         print(f'Welcome!'
#               f'1. ')
#
#
#     def remove_person(self):
#         remove_id = int(input("Person's ID you want to remove: "))
#         persons = my_DB.search('persons')
#         Setup.find_person()


class Student:
    def __init__(self, _id):
        self.id = _id

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

        if choice == 1:
            self.create_project()

        if choice == 2:
            self.student_check_message()

        if choice == 0:
            exit()

    def create_project(self):
        member_request = my_DB.search('member_request')
        tobe_member = member_request.filter(lambda x: x['to_be_member'] == self.id)
        for member in tobe_member.table:
            print(member['to_be_member'])
            if self.id == member['to_be_member']:
                print("You haven't deny all member pending request.")
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
        for row in request.table:
            project = project_table.filter(lambda x: x['ProjectID'] == row['ProjectID']).table
            print(f"message from: {row['From']} \n"
                  f"Project: {project[0]['Title']}")

        self.lead_id = input("Input leader's ID you want to respond: ")
        project_id = project_table.filter(lambda x: x['Leader'] == self.lead_id).table[0]['ProjectID']
        leader_pending = mem_request.filter(lambda x: x['From'] == self.lead_id)
        choice = input('deny or accept to be member [y/n]: ')
        while choice is True:
            if choice != 'y' or 'n':
                print('Invalid choice, Please try again.')
                choice = input('deny or accept to be member [y/n]: ')

        if choice == 'y':

            print(f'You are member of {self.lead_id}: {project_table.filter(lambda x: x["Leader"] == self.lead_id).table[0]["Title"]} project!')
            leader_pending.update('Response', 'y')
            append_member(self.lead_id, self.id, project_id)
            person = my_DB.search('persons')
            person = person.filter(lambda x: x['ID'] == self.id)
            print(type(person.table))
            print(person.table)
            person.table.update('role', 'member')
            mem_request.filter(lambda x: x['to_be_member'] == self.id).filter(lambda x: x['Response'] == 'None').update('Response', 'n')

            Student(self.id).choice_student()
        elif choice == 'n':
            leader_pending.update('Response', 'n')
            print(f'you deny {self.lead_id}: {search_project(self.lead_id).select("Title")} project!')
            Student(self.id).choice_student()


class Leader:

    def __init__(self, id):
        self.id = id
        self.project_id = 0

    def leader_choice(self):
        print(f'Welcome! \n'
              f'Your role now is Leader. \n'
              f'What do you want to do? \n'
              f'1. Project \n'
              f'2. Create Project \n'
              f'3. Message \n'
              f'0. exit')
        choice = int(input('Select: '))
        project_table = my_DB.search('project_table')
        # project_table.filter(lambda x: x['Leader'] == self.id)

        if choice == 1:
            for i in project_table.filter(lambda x: x['Leader'] == self.id).table:
                print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
            _project_id = int(input('Select project id you want to modify:'))
            project = project_table.filter(lambda x: x['ProjectID'] == _project_id)
            print('What do you want to do with this project? \n'
                  '1. Rename Title \n'
                  '2. Modify Content \n'
                  '0. Return to menu')
            choice = int(input('Select: '))
            if choice == 1:
                new_title = input('New title name: ')
                project.update('Title', new_title)
                Leader(self.id).leader_choice()
            if choice == 2:
                print(project.select('Content'))
                new_content = input('New Content: ')
                project.update('Content', new_content)
                Leader(self.id).leader_choice()
            if choice == 3:
                Leader(self.id).leader_choice()

        elif choice == 2:
            create_project(self.id)
            Leader(self.id).leader_choice()

        elif choice == 3:
            for i in project_table.filter(lambda x: x['Leader'] == self.id).table:
                print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
            _project_id = int(input('Select project ID you want to send a member request: '))
            member_send_request(self.id, _project_id)
            Leader(self.id).leader_choice()

        elif choice == 0:
            exit()


class Member:
    def __init__(self, id, lead_id):
        self.id = id
        self.lead_id = lead_id

    def member_choice(self):
        print(f'Welcome! \n'
              f'Your role now is Member. \n'
              f'What do you want to do? \n'
              f'1. Project \n'
              f'0. Exit')
        choice = int(input('Select: '))
        while 0 < choice > 2:
            print('Invalid choice, Please select again.')
            choice = int(input('Select: '))
        if choice == 1:
            self.member_check_project()
        elif choice == 0:
            exit()
        self.member_choice()

    def member_check_project(self):
        project_table = my_DB.search('project_table')
        for i in project_table.filter(lambda x: x['Leader'] == self.id).table:
            print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
        _project_id = int(input('Select project id you want to modify:'))
        project = project_table.filter(lambda x: x['ProjectID'] == _project_id)
        print(project.select('Content'))
        new_content = input('New Content: ')
        project_table.update('Content', new_content)
        Leader(self.id).leader_choice()



class Faculty:
    def __init__(self, id):
        self.id = id

    def faculty_choice(self):
        print(f'Welcome!\n'
              f'Your role now is Faculty. \n'
              f'What do you want to do? \n'
              f'1. Message \n'
              f'0. Exit')
        choice = int(input('Select: '))
        if choice == 1:
            self.faculty_check_message()
        elif choice == 0:
            exit()

    def faculty_check_message(self):
        advisor_request = my_DB.search('advisor_request')
        request = advisor_request.filter(lambda x: x['to_be_advisor'] == self.id)
        if not request.table:
            print('You have no message from leader.')
            print('------------')
            self.faculty_choice()
        for row in request.table:
            print(f"message from: {row['From']}")
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
                    print(f'You are advisor of {lead_id}: {search_project(lead_id)["Title"]} project!')
                    leader_pending.update('Response', 'y')
                    other_lead_pending = request.filter(lambda x: x['From'] != lead_id)
                    other_lead_pending.update('Response', 'n')
                    _login = my_DB.search('login')
                    _login.filter(lambda x: x['ID'] == self.id).update('role', 'advisor')
                    Advisor(self.id).advisor_choice()
            elif choice == 'n':
                leader_pending.update('Response', 'n')
                print(search_project(lead_id))
                print(f'you deny {lead_id}: {search_project(lead_id)["Title"]} project!')
                self.faculty_choice()


class Advisor:
    def __init__(self, id):
        self.id = id

    def advisor_choice(self):
        print(f'Welcome!\n'
              f'Your role now is Advisor. \n'
              f'What do you want to do? \n'
              f'1. Check Project'
              f'0. Exit')
        choice = int(input('Select: '))
        if choice == 1:
            self.advisor_check_project()
        if choice == 0:
            exit()
        self.advisor_choice()

    def advisor_check_project(self):
        pass
        # copy from leader_check_project


initializing()
val = login()
if val is None:
    print('Invalid')
else:
    if val[1] == 'student':
        Student(val[0]).choice_student()
    elif val[1] == 'member':
        lead_id = search_project(val[0])['Lead']
        Member(val[0], lead_id).member_choice()
    elif val[1] == 'leader':
        Leader(val[0]).leader_choice()
    elif val[1] == 'faculty':
        Faculty(val[0]).faculty_choice()
    elif val[1] == 'advisor':
        Advisor(val[0]).advisor_choice()



