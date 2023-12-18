# Final project for 2023's 219114/115 Programming I
## File
  1. project_manage.py : for manage this project
  2. Database.py: Manages database interactions
  3. all csv file: Contains the member_request.csv, advisor_request.csv, project_table.csv and project_evaluate.csv for collect information

## Class
  1. Admin : for people who login as admin, this class will make user can use specific function of admin.
  2. Student : for people who login as student, this class will make user can use specific function of student.
  3. Member : from student who accept the request to be member, they can use specific function of member.
  4. Leader : from student who create project and become leader, they can use specific function of leader.
  5. Faculty : for people  who login as faculty, this class will make user can use specific function of faculty.
  6. Advisor : from faculty who accept to be advisor for student's project, they can use specific function of advisor.

## How to use my program?
- clone this repository
- use command cd to guide you to my program
- try to run by input your username and password

## Detailed Table
 |     Role        |      Action     |      Method     |      Class      | Completion percentage  |
 | --------------- | --------------- | --------------- | --------------- | ---------------------- | 
 | Admin           |Manage account in database (update ID/username/password/role) | manage_account (update) | Admin | 100% |
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
