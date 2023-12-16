# import database module
from database import DB, read_csv, Table, create_csv
import csv, random, datetime

# define a funcion called initializing

my_DB = DB()


def initializing():
    persons = read_csv('persons.csv')
    login = read_csv('login.csv')
    project_table = read_csv('project_table.csv')
    advisor_request = read_csv('advisor_request.csv')
    member_request = read_csv('member_request.csv')

    persons_table = Table('persons', persons)
    login_table = Table('login', login)
    project_table = Table('project_table', project_table)
    advisor_request_table = Table('advisor_request', advisor_request)
    member_request_table = Table('member_request', member_request)

    my_DB.insert(persons_table)
    my_DB.insert(login_table)
    my_DB.insert(project_table)
    my_DB.insert(advisor_request_table)
    my_DB.insert(member_request_table)

    return my_DB


# here are things to do in this function:

# create an object to read all csv files that will serve as a persistent state for this program

# create all the corresponding tables for those csv files

# see the guide how many tables are needed

# add all these tables to the database

# data = {'ProjectID': 12345,
#         'Title': 'title',
#         'Lead': 5662557,
#         'Member1': 3557832,
#         'Member2': None,
#         'Advisor': 2472659,
#         'Status': 'Unfinished'
#         }
# project_table = my_DB.search('project_table')
# print(type(project_table))
# project_table.insert(data)
# print(project_table)


# define a funcion called login

def login():
    username = input('Username: ')
    password = input('Password: ')
    _login = my_DB.search('login')
    users = _login.filter(lambda x: x['username'] == username).filter(lambda x: x['password'] == password)
    if len(users.table) != 0:
        return [users.table[0]['ID'], users.table[0]['role']]
    return None


# here are things to do in this function:
# add code that performs a login task
# ask a user for a username and password
# returns [ID, role] if valid, otherwise returning None

# define a function called exit
# def exit():

# here are things to do in this function:
# write out all the tables that have been modified to the corresponding csv files
# By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:

# https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above


def find_project(lead_id):
    project_table = my_DB.search('project_table')
    project_table_filter = project_table.filter(lambda x: x['Lead'] == lead_id)
    return project_table_filter.table


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
    member_request = my_DB.search('member_request')
    member_request.filter(lambda x: x[''])
    person = my_DB.search('persons')
    to_member_id = int(input("Member's ID you want to send a request: "))
    current_time = datetime.time()
    if person.filter(lambda x: x['ID'] == to_member_id):
        new_message = {'ProjectID': project_id,
                       'to_be_member': to_member_id,
                       'From': _id,
                       'Response': 'None',
                       'Response_date': current_time,

                       }
        member_request.insert(new_message)


def advisor_request(_id, project_id):
    to_advisor_id = int(input("Advisor's ID you want to send a request: "))
    current_time = datetime.time()
    new_message = {'ProjectID': project_id,
                   'to_be_member': to_advisor_id,
                   'From': _id,
                   'Response': 'None',
                   'Response_date': current_time,
                   }
    advisor_request = my_DB.search('advisor_request')
    advisor_request.insert(new_message)


def append_member(lead_id, _id):
    project = my_DB.search('project_table')
    lead_project = project.filter(lambda x: x['Lead'] == lead_id).select('Member1', 'Member2')
    for member in lead_project:
        if lead_project[member].isspace():
            lead_project[member] = _id
        print("This project's member is already full! Please select another project")


def create_project(_id):
    title = input('Project Title: ')
    # description = input('Description: ')
    project_id = random.randint(0000, 9999)
    new_project = {'ProjectID': project_id,
                   'Title': title,
                   'Lead': _id,
                   'Member1': 'None',
                   'Member2': 'None',
                   'Advisor': 'None',
                   'Status': 'Pending'
                   }
    my_DB.search('project_table').insert(new_project)
    _login = my_DB.search('login')
    person = my_DB.search('persons')
    person.filter(lambda x: x['ID'] == _id).update('role', 'leader')

    mem_choice = input('Do you want to send pending message to any student? [y/n]: ')
    if mem_choice == 'y':
        member_send_request(_id, project_id)

    adv_choice = input('Do you want to send pending message to any advisor? [y/n]: ')
    if adv_choice == 'y':
        advisor_request(_id, project_id)

    print('Your project is successful!')
    print('------------')


def check_choice(choice, error):
    if not isinstance(choice, str):
        print(error)


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
        self.project_id = 0
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

        if choice == 1:
            if is_member_in_group(val[0]):
                print("You alredy become a member! you can't create project")
                Student.choice_student(val[0])
            member_request = my_DB.search('member_request')
            tobe_member = member_request.filter(lambda x: x['to_be_member'] == self.id)
            for member in tobe_member.table:
                print(member['to_be_member'])
                if self.id == member['to_be_member']:
                    print("You haven't deny all member pending request.")
                    Student.choice_student(val[0])
            create_project(val[0])
            Student.choice_student(val[0])

        if choice == 2:
            project_table = my_DB.search('project_table')
            member = project_table.select(['Member1', 'Member2'])

            person = my_DB.search('persons')
            mem_request = my_DB.search('member_request')
            request = mem_request.filter(lambda x: x['to_be_member'] == self.id)
            if not request.table:
                print('You have no message from leader.')
                print('------------')
                Student.choice_student(val[0])
            for row in request.table:
                print(f"message from: {row['From']}")
            self.lead_id = input("Input leader's ID you want to respond: ")
            leader_pending = mem_request.filter(lambda x: x['From'] == self.lead_id)
            choice = input('deny or accept to be member [y/n]: ')
            while choice is True:
                if choice != 'y' or 'n':
                    print('Invalid choice, Please try again.')
                    choice = input('deny or accept to be member [y/n]: ')

            print(find_project(self.lead_id))
            if choice == 'y':
                print(f'You are member of {self.lead_id}: {find_project(self.lead_id).table.select("Title")} project!')
                leader_pending.update('Response', 'y')
                append_member(self.lead_id, self.id)
                _login = my_DB.search('login')
                _login.find_person(lambda x: x['id'] == self.id).update('role', 'member')
            elif choice == 'n':
                leader_pending.update('Response', 'n')
                print(find_project(self.lead_id))
                print(f'you deny {self.lead_id}: {find_project(self.lead_id).select("Title")} project!')
                Student.choice_student(val[0])

        if choice == 0:
            exit()


class Leader:

    def __init__(self, id, project):
        self.id = id
        self.project = project

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
        if choice == 1:
            project_title = find_project(self.id).select("Title")
            project_id = find_project(self.id).select("ProjectID")
            for _id in project_id:
                for title in project_title:
                    print(f'{_id}: {title}')
            project_id = int(input('Select project id you want to modify:'))


        elif choice == 2:
            create_project(self.id)

        elif choice == 3:
            project_table = my_DB.search('project_table')
            all_project = project_table.filter(lambda x: x['Lead'] == self.id)
            all_project.select(['Title', 'ProjectID'])
            for project in all_project:
                print(f"{project['ProjectID']}: {project['Title']}")
            project_id = input('What project you want student to be member of?: ')
            member_send_request(self.id, project_id)
            print('Message sent!')


        elif choice == 0:
            exit()


class Member:
    def __init__(self, id):
        self.id = id

    def member_choice(self):
        pass


class Faculty:
    pass


class Advisor:
    pass


initializing()
val = login()

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] == 'admin':
#         #  see and do admin related activities
if val[1] == 'student':
    Student(val[0]).choice_student()
    exit()
elif val[1] == 'member':
    Member(val[0]).member_choice()
    exit()
elif val[1] == 'lead':
    Leader.leader_choice(val[0])
    exit()
# elif val[1] == 'faculty':
#         #  see and do faculty related activities
# elif val[1] == 'advisor':
        #  see and do advisor related activities

# once everyhthing is done, make a call to the exit function


def exit():
    create_csv('project_table.csv', ['ProjectID', 'Title', 'Lead', 'Member1', 'Member2', 'Advisor', 'Status'],
               my_DB.search('project_table'))

    create_csv('persons.csv', ['ID', 'first', 'last', 'type'], my_DB.search('persons'))

    create_csv('login_csv', ['ID', 'username', 'password', 'role'], my_DB.search('login'))

    create_csv('member_request.csv', ['ProjectID', 'to_be_member', 'from', 'response', 'Response_date'],
               my_DB.search('member_request_table'))

    create_csv('advisor_request.csv', ['ProjectID', 'to_be_advisor', 'from', 'response', 'Response_date'],
               my_DB.search('advisor_request_table'))
