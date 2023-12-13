# import database module
from database import DB, read_csv, Table
import csv, random

# define a funcion called initializing


def initializing():

    persons = read_csv('persons.csv')
    login = read_csv('login.csv')
    persons_table = Table('persons', persons)
    login_table = Table('login', [login])
    project_table = Table('project', [])
    advisor_request_table = Table('Advisor pending request', [])
    member_request_table = Table('Member pending request', [])


    my_DB = DB()
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


# define a funcion called login

def login():
    username = input('Username: ')
    password = input('Password: ')
    _login = my_DB.search('login')
    users = _login.filter(lambda x: x['username'] == username).filter(lambda x: x['password'] == password)
    if len(users) != 0:
        return [users[0]['ID'], users[0]['role']]
    print('None')


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

my_DB = initializing()
val = login()
print(login())
#
#
# class Setup:
#     def __init__(self, id):
#         self.id = id
#
#     def find_project(self):
#         project_table = my_DB.search('project_table')
#         project_table.filter(lambda x: x[self.id] == project_table['Lead'])
#         return project_table['title']
#
#     def find_person(self):
#         person = my_DB.search('person')
#         person_info = person.filter(lambda x: x[self.id] == person['id'])
#         return person_info
#
#     @staticmethod
#     def create_project():
#         title = input('Project Title: ')
#         description = input('Description: ')
#         new_project = {'Title': {title, description}}
#         project_table = my_DB.search('project_table')
#         project_table.append(new_project)
#         project_id = random.randint(0000, 9999)
#         return project_id
#
#     def member_send_request(self):
#         member_request = my_DB.search('member_request_table')
#         member = Setup.find_person(self.id)
#         person = my_DB.search('person')
#         to_member_id = int(input("Member's ID you want to send a request: "))
#         if to_member_id == member['id']:
#             member_request.append('to_be_member', to_member_id)
#
#
#     def advisor_request(self):
#         advisor_request = my_DB.search('advisor pending request')
#
#
#
# class Student:
#     def __init__(self, id, project):
#         self.id = id
#         self.project = project
#
#     def student_choice(self):
#         print(f'Welcome {Setup.find_person(self.id).select(["first", "last"])}'
#               f'1. Project:'
#               f'2. Create Project'
#               f'3. Message')
#         choice = int(input('Select: '))
#         project_table = my_DB.search('project_table')
#         member = project_table.filter(lambda x: x['Member1'] and x['Member2'])
#         member_request = my_DB.search('member_request_table')
#         mem_request = member_request.filter(lambda x: ['to_be_member'])
#         if choice == 1:
#             print(f'{project_table["title"]}')
#
#         elif choice == 2:
#             if self.id in member:
#                 print('You already become member.')
#             elif self.id in mem_request:
#                 print("You haven't deny all member pending request.")
#             else:
#                 Setup.create_project()
#
#             person = my_DB.search('person')
#             person.find_person(lambda x: x['id'] == self.id).update('type', 'leader')  # update student role to leader
#
#         elif choice == 3:
#             mem_request = my_DB.search('member_request_table')
#             request = mem_request.filter(lambda x: x['to_be_member'] == mem_request)
#             for i in request:
#                 print(f"{i+1}{request[i]['to_be_member']}")
#                 message = int(input('Select message: '))
#                 choice = input('deny or accept to be member [y/n]: ')
#                 if choice == y:
#
#
#
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
#
#
#
#
#
#
#
# # based on the return value for login, activate the code that performs activities according to the role defined for that person_id
#
# # if val[1] == 'admin':
# #         #  see and do admin related activities
# # elif val[1] == 'student':
# #
# # elif val[1] == 'member':
# #         #  see and do member related activities
# # elif val[1] == 'lead':
# #
# # elif val[1] == 'faculty':
# #         #  see and do faculty related activities
# # elif val[1] == 'advisor':
# #         #  see and do advisor related activities
# #
# # # once everyhthing is done, make a call to the exit function
# exit()
#
# #
# #
