# Final project for 2023's 219114/115 Programming I
## File
  1. project_manage.py : 
           - project_manage.py is the main file, managing all project functions and roles through specific classes.
     
  2. Database.py:
           - Database.py will contain all fuction that necessary for the main program such as function to search, insert and update for table in csv files.
     
  3. all csv file:

     3.1 login.csv : Contains with all class.
           - login.csv file will store all username, password and role for person who login in this program.
     
     3.2 persons.csv : Contains with all class.
           - In persons.csv file, this file will store similar information with login.csv, but in this persons.csv, it will have first name, last name and instead of username and password.
     
     3.3 member_request.csv : Contains with class Student and Leader.
           - This CSV file will store member requests by leaders, containing the project ID for the students whom the leader has requested to join. Students can respond to these requests with either an acceptance or denial.
     
     3.4 advisor_request.csv : Contains with class Faculty and Leader.
           - This CSV file stores information similar to the "member_request.csv" file but is specifically for faculty. It store requests from leaders for faculty to join their projects, and faculty can respond with either acceptance or denial.
     
     3.5 project_table.csv : Contains with all class except Admin.
           - The "project_table.csv" file stores information about all projects created by leaders. It includes projectID, title, content, leader's ID, a list of member IDs, advisor's ID, and the project's status.
     
     3.6 project_evaluate.csv : Contains with class Advisor, Leader and Member.
           - This CSV file is meant for advisors to score and give some advice on leader and members projects. If the score is complete (10 out of 10), the project is done. Otherwise, leader and members must improve the project following the advisor's guidance.\

     
## Class
  1. class 'Admin' :
       - This class is specially for person who login as 'Admin', which can have only 1 person. Admin can manage database, change all account information, create or remove account.
         
  2. class 'Student' : 
       - Students can either create new projects and become leaders or accept/deny member requests from other leaders, turning them into members if they accepted.
         
  4. class 'Member' : from student who accept the request to be member, they can use specific function of member.
       - If students accept a leader's member request and become members, they can see project details, edit project content, and check advisor score and advice if the leader has finished and submitted the project for advisor's evaluation.
         
  6. class 'Leader' : from student who create project and become leader, they can use specific function of leader.
       - For student who choose to create their own project and become leader, what they can do in leader's role is view and edit project details, send the project for advisor evaluation, send requests to students and faculty. They can also check the score and advice provided by the advisor.
         
  8. class 'Faculty' : for people  who login as faculty, this class will make user can use specific function of faculty.
       - Faculty members can choose to become advisors by accepting or denying advisor requests from leaders.
         
  10. class 'Advisor' : from faculty who accept to be advisor for student's project, they can use specific function of advisor.
      - Faculty who choose to accept request and become advisor can check their student's project detail and evaluate it.

## How to use my program?
- clone this repository 
- use command cd to guide you to my program
- try to run by input your username and password

## Detailed Table
 |     Role        |      Action     |      Method     |      Class      | Completion percentage  |
 | --------------- | --------------- | --------------- | --------------- | ---------------------- | 
 | Admin|Manage account in database (update ID/username/password/role) | manage_account (update) | Admin | 100% |
 | Admin | Append new account in database | create_account (insert) | Admin | 100% |
 |Admin |Delete account in database|remove_account (del)|Admin|100%|
 |Student|Create new project and become leader|insert (create project), update(role)|Student|100% |
 |Student|Check message from leader and accept or deny it (if accept, student will became member)|update (update role, member_request table), append_member|Student|100% |
 |Leader|check project detail|project_info (search)|Leader|100% |
 |Leader|modify their project (rename title)|lead_check_project (update)|Leader|100%|
 |Leader|modify their project (modify content)|lead_check_project (update)|Leader|100%|
 |Leader|modify their project (finished this project (to wait for evaluation from advisor)|lead_check_project (update)|Leader|100%|
 |Leader|Send a message to student to be member|update (for member_request function)|Leader|100%|
 |Leader|Send a message to faculty to be advisor|update (for advisor_request function)|Leader|100%|
 |Leader|See score and advice from advisor|see_evaluate (search)|Leader|100%|
 |Member|Check project detail|project_info (search)|Member|100%|
 |Member|Modify project content|member_check_project|Member|100%|
 |Member|See score and advice from advisor|see_evaluate (search)|Member|100%|
 |Faculty|Check message from leader and accept or deny it (if accept, faculty will became advisor)|faculty_check_message (update)|Faculty|100%|
 |Advisor|Check project detail|project_info (search)|Advisor|100%|
 |Advisor|Evaluate project by giving score and some advice|advisor_check_project > evaluate_project (insert, update)|Advisor|100%|
