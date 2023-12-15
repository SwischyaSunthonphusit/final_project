# import database module
from database import DB, read_csv, Table, create_csv
import csv, random

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

    print(member_request_table.filter(lambda x: x['to_be_member']))

    return my_DB

# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed

    # add all these tables to the database


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

class Setup:
    def __init__(self, id, mem1_id, project_id):
        self.id = id
        self.mem1_id = mem1_id
        self.project_id = project_id
        self.lead_id = 0

    def find_project(self):
        project_table = my_DB.search('project_table')
        project_table.filter(lambda x:  x['Lead'] == self.lead_id)
        return project_table['title']

    def find_person(self):
        person = my_DB.search('persons')
        person_info = person.filter(lambda x: x['ID'] == self.id)
        return person_info

    def is_member_in_group(self):
        project_table = my_DB.search('project_table')
        project = project_table.select(['Member1'])
        project2 = project_table.select(['Member2'])
        for member in project:
            if self.id == member:
                return True
        return False



    def create_project(self):
        project_table = my_DB.search('project_table')
        member_request = my_DB.search('member_request')
        print(type(project_table))
        print(my_DB.__dict__)
        print(type(member_request))
        tobe_member = member_request.filter(lambda x: ['to_be_member'])

        if Setup.is_member_in_group(val[0]):
            Student.choice_student(val[0])

        for member in tobe_member:
            if self.id == member:
                print("You haven't deny all member pending request.")
                Student.choice_student(val[0])
        title = input('Project Title: ')
        # description = input('Description: ')
        project_table.append('Title', title)
        project_id = random.randint(0000, 9999)
        project_table.append('ProjectID', project_id)
        person = my_DB.search('person')
        person.find_person(lambda x: x['id'] == self.id).update('type', 'leader')

    def member_send_request(self):
        member_request = my_DB.search('member_request_table')
        member_request.append('from', self.id)
        person = my_DB.search('person')
        to_member_id = int(input("Member's ID you want to send a request: "))
        if person.filter(lambda x: x['ID'] == to_member_id):
            member_request.append('to_be_member', to_member_id)

    def advisor_request(self):
        advisor_request = my_DB.search('advisor pending request')
        advisor_request.append('from', self.id)
        person = my_DB.search('person')
        to_advisor_id = int(input("Member's ID you want to send a request: "))
        if person.filter(lambda x: x['ID'] == to_advisor_id):
            advisor_request.append('to_be_member', to_advisor_id)

    def append_member(self):
        project = my_DB.search('project_table')
        lead_project = project.filter(lambda x: x['Lead'] == self.lead_id).select('Member1', 'Member2', 'Member3', 'Member4', 'Member5')
        for member in lead_project:
            if lead_project[member].isspace():
                lead_project[member] = self.id
            print("This project's member is already full! Please select another project" )


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
#         presons = my_DB.search('persons')
#         Setup.find_person()


class Student:

    def __init__(self, id):
        self.id = id
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
        if choice == 1:
            Setup.create_project(val[0])
        if choice == 2:
            Student.choice_message(val[0])
        if choice == 0:
            exit()

    def choice_message(self):
        project_table = my_DB.search('project_table')
        # member = project_table.select('Member1', 'Member2')
        member_request = my_DB.search('member_request_table')
        # mem_request = member_request.filter(lambda x: ['to_be_member'])

        person = my_DB.search('person')
        mem_request = my_DB.search('member_request_table')
        request = mem_request.filter(lambda x: ['to_be_member'] == self.id)
        for i in range(len(request)):
            print(f"{i + 1}{request[i]['from']}")
        self.lead_id = input("Input leader's ID you want to respond: ")
        leader_id = mem_request.filter(lambda x: x['from'] == self.lead_id)
        choice = input('deny or accept to be member [y/n]: ')

        if choice == 'y':
            print(f'You are member of {project_table.find_project(self.lead_id)} project!')
            leader_id.append('Response', 'y')
            Setup.append_member(self.id)
            person.find_person(lambda x: x['id'] == self.id).update('type', 'member')
        elif choice == 'n':
            leader_id.append('Response', 'n')
            print(f'you deny {project_table.find_project(self.lead_id)} project!')

    def __repr__(self):
        f"""{Student.choice_student(self.id)}"""


initializing()
val = login()


# class Leader:
#
#     def __init__(self, id, project):
#         self.id = id
#         self.project = project
#
#     def leader_choice(self):
#         print(f'Welcome {Setup.find_person(self.id).select()}'
#               f'1. Project:'
#               f'2. Create Project'
#               f'3. Message'
#               f'input the name of project you want to modify')
#         choice = int(input('Select: '))
#         project_table = my_DB.search('project_table')
#         if choice == 1:
#             print(f'{project_table["title"]}')
#
#         elif choice == 2:
#             Setup.create_project()
#
#         elif choice == 3:
#             print('1. Check your message'
#                   '2. Sent a message')
#             message_choice = int(input('Select: '))
#             if message_choice == 1:
#                 member_request = my_DB.search('member_request_table')
#                 member_request.select()
#                 print(member_request['to_be_member'])
#                 response = input('Do you want to accept or deny the pending? (y/n): ')
#                 if response == 'y':
#                     member_request['Response'] = 'y'
#                 else:
#                     member_request['Response'] = 'n'
#             elif message_choice == 2:
#                 Setup.member_send_request(self.id)
#                 print('Message sent!')







# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] == 'admin':
#         #  see and do admin related activities
if val[1] == 'student':
     stu = Student(val[0])
     print(stu.choice_student())
# elif val[1] == 'member':
#         #  see and do member related activities
# elif val[1] == 'lead':
#
# elif val[1] == 'faculty':
#         #  see and do faculty related activities
# elif val[1] == 'advisor':
#         #  see and do advisor related activities

# once everyhthing is done, make a call to the exit function



def exit():
    project_table = my_DB.search('project_table')
    create_csv('project_table.csv', ['ProjectID', 'Title', 'Lead', 'Member1',
                                     'Member2', 'Advisor', 'Status'], project_table)

    persons = my_DB.search('persons')
    create_csv('persons.csv', ['ID', 'first', 'last', 'type'], persons)

    _login = my_DB.search('login')
    create_csv('login_csv', ['ID', 'username', 'password', 'role'], _login)

    mem_request = my_DB.search('member_request_table')
    create_csv('member_request.csv', ['ProjectID', 'to_be_member', 'from', 'response', 'Response_date'], mem_request)

    advisor_request = my_DB.search('advisor_request_table')
    create_csv('advisor_request.csv', ['ProjectID', 'to_be_advisor', 'from', 'response',
                                       'Response_date'], advisor_request)


