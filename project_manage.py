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
    person_info = person.filter(lambda x: x['ID'] == to_member_id)
    print(person_info)
    if person_info.table:
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
                   'Status': 'Unfinished'
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

    create_csv('project_evaluate.csv', ['ProjectID', 'Leader', 'Advisor', 'Score', 'Advice'],
               my_DB.search('project_evaluate'))


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
            self.create_project_student()

        if choice == 2:
            self.student_check_message()

        if choice == 0:
            exit()

    def create_project_student(self):
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
            leader_pending.update('Response', 'y')
            append_member(self.lead_id, self.id, project_id)
            person = my_DB.search('persons')
            _login = my_DB.search('login')
            __login = _login.filter(lambda x: x['ID'] == self.id)
            __login.update('role', 'member')
            mem_request.filter(lambda x: x['to_be_member'] == self.id).filter(lambda x: x['Response'] == 'None')\
                .update('Response', 'n')
            project_name = project_table.filter(lambda x: x["Leader"] == self.lead_id).table[0]["Title"]
            print(f'You are member of {self.lead_id}: {project_name} project!')
            print('------------')
            Student(self.id).choice_student()

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
        print(f'Welcome! \n'
              f'Your role now is Leader. \n'
              f'What do you want to do? \n'
              f'1. Project \n'
              f'2. Create Project \n'
              f'3. Message \n'
              f'4. See score and advice from advisor \n'
              f'0. exit')
        choice = int(input('Select: '))
        project_table = my_DB.search('project_table')
        # project_table.filter(lambda x: x['Leader'] == self.id)

        if choice == 1:
            self.leader_check_project()
        elif choice == 2:
            create_project(self.id)
            Leader(self.id).leader_choice()
        elif choice == 3:
            for i in project_table.filter(lambda x: x['Leader'] == self.id).table:
                print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
            _project_id = int(input('Select project ID you want to send a member request: '))
            member_send_request(self.id, _project_id)
            Leader(self.id).leader_choice()
        elif choice == 4:
            self.see_evaluate()
        elif choice == 0:
            exit()

    def see_evaluate(self):
        project_evaluate = my_DB.search('project_evaluate')
        project_evaluate = project_evaluate.filter(lambda x: x['Leader'] == self.id).table
        if not project_evaluate:
            print("You haven't send project to advisor, please go to choice[1]: Project to send your project.")
            print('------------')
            Leader(self.id).leader_choice()
        project = my_DB.search('project_table')
        project_table = project.filter(lambda x: x['Leader'] == self.id).table
        print(project_evaluate)
        if project_evaluate['Score'] == 10:
            print('You have full score for your project! This project is finished')
        print(f"---Score and Advice--- \n"
              f"ProjectID: {project_evaluate[0]['ProjectID']} \n"
              f"Title: {project_table[0]['Title']} \n"
              f"Score: {project_evaluate[0]['Score']} \n"
              f"Advice from advisor: {project_evaluate[0]['Advice']}")
        choice = input('Do you want to rectify this project? [y/n]: ')
        if choice == 'y':
            self.leader_check_project()
        elif choice == 'n':
            print('------------')
            self.leader_choice()

    def leader_check_project(self):
        project_table = my_DB.search('project_table')
        for i in project_table.filter(lambda x: x['Leader'] == self.id).table:
            print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")
        _project_id = int(input('Select project id you want to modify:'))

        print('What do you want to do with this project? \n'
              '1. Rename Title \n'
              '2. Modify Content \n'
              '3. Finished this Project \n'
              '0. Return to menu')
        choice = int(input('Select: '))
        if choice == 1:
            new_title = input('New title name: ')
            for project in project_table.filter(lambda x: x['ProjectID'] == str(_project_id)).table:
                project.update('Title', new_title)
            print('Your title update successfully.')
            print('------------')
            Leader(self.id).leader_choice()
        if choice == 2:
            new_content = input('New Content: ')
            for project in project_table.filter(lambda x: x['ProjectID'] == str(_project_id)).table:
                project.update('Content', new_content)
            print('Your content update successfully.')
            print('------------')
            Leader(self.id).leader_choice()
        if choice == 3:
            for project in project_table.filter(lambda x: x['ProjectID'] == str(_project_id)).table:
                project.update('Status', 'Pending')
            print('Your project is finished! this project will automatically pending for advisor evaluation.')
            print('------------')
            Leader(self.id).leader_choice()
        if choice == 0:
            Leader(self.id).leader_choice()


class Member:
    def __init__(self, id, lead_id):
        self.id = id
        self.lead_id = lead_id

    def member_choice(self):
        print(f'Welcome! \n'
              f'Your role now is Member. \n'
              f'What do you want to do? \n'
              f'1. Project \n'
              f'2. See score and advice for your project\n'
              f'0. Exit')
        choice = int(input('Select: '))
        while 0 < choice > 2:
            print('Invalid choice, Please select again.')
            choice = int(input('Select: '))
        if choice == 1:
            self.member_check_project()
        elif choice == 2:
            self.see_evaluate()
        elif choice == 0:
            exit()

    def member_check_project(self):
        project_table = my_DB.search('project_table')
        print(type(project_table))
        project = project_table.filter(lambda x: x['Member1'] == self.id or x['Member2'] == self.id)
        for i in project.table:
            print(f"Project ID: {i['ProjectID']} Title: {i['Title']:2>}")

        _project_id = int(input('Select project id you want to modify:'))
        new_content = input('New Content: ')
        print(type(project.filter(lambda x: x['ProjectID'] == str(_project_id))))
        print(project.filter(lambda x: x['ProjectID'] == str(_project_id)))
        project.filter(lambda x: x['ProjectID'] == str(_project_id)).update('Content', new_content)
        print(f'You finished update content!')
        self.member_choice()

    def see_evaluate(self):
        project_evaluate = my_DB.search('project_evaluate')
        project_evaluate = project_evaluate.filter(lambda x: x['Leader'] == self.lead_id).table
        project = my_DB.search('project_table')
        project_table = project.filter(lambda x: x['Leader'] == self.lead_id).table
        if project_evaluate[0]['Score'] == 10:
            print('You have full score for your project! This project is finished')
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
                print(search_project(lead_id))
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
              f'0. Exit')
        choice = int(input('Select: '))
        if choice == 1:
            self.advisor_check_project()
        if choice == 0:
            exit()

    def advisor_check_project(self):
        project_table = my_DB.search('project_table')
        advisor_project = project_table.filter(lambda x: x['Advisor'] == self.id)\
            .filter(lambda x: x['Status'] == 'Pending')
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
            self.advisor_check_project()

        # copy from leader_check_project

    def find_project_advisor(self):
        project_table = my_DB.search('project_table')
        advisor_project = project_table.filter(lambda x: x['Advisor'] == self.id) \
            .filter(lambda x: x['Status'] == 'Pending')
        advisor_project = advisor_project.filter(lambda x: x['ProjectID'] == self.project_id).table
        return advisor_project

    def project_info(self):
        advisor_project = self.find_project_advisor()
        print(advisor_project)
        print(f"[Project Detail] \n"
              f"Project ID: {advisor_project.table[0]['ProjectID']} \n"
              f"Title: {advisor_project.table[0]['Title']}\n"
              f"Lead: {advisor_project.table[0]['Leader']}\n"
              f"Member1: {advisor_project.table[0]['Member1']}\n"
              f"Member2: {advisor_project.table[0]['Member2']}\n"
              f"Status: {advisor_project.table[0]['Status']}\n"
              f"Content: {advisor_project.table[0]['Content']}")
        return advisor_project

    def evaluate_project(self):
        project = my_DB.search('project_table')
        project.filter(lambda x: x['status'] == 'Pending').select(['ProjectID'])
        print('----Evaluation----')
        score = input(f'From 1 to 10, what score you think this project should have? '
                      f'(if this project is perfect, please score it 10): ')
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
        lead_id = search_project(val[0])['Leader']
        Member(val[0], lead_id).member_choice()
    elif val[1] == 'leader':
        Leader(val[0]).leader_choice()
    elif val[1] == 'faculty':
        Faculty(val[0]).faculty_choice()
    elif val[1] == 'advisor':
        Advisor(val[0]).advisor_choice()



