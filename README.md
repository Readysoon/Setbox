# SetBox - the website for learning

SetBox is a place to plan your schedule with the use of subjects and lessons. It is also a place to track your learning progress and prepare for exams.

## What can you do in SetBox?

1. Make a profile to store your data
2. Create a subject, specify when the lessons are happening
3. Create lessons that are outside of specified subject times
4. Add files to learn from
5. Share a subject with other students (work in progress, some features not working properly)
6. Add quizzes for lessons to test your knowledge (not yet implemented)


### Prerequisites

python 3.9.12, PostgreSQL 15.2

[Download Python here](https://www.python.org/downloads/)

[Download PostgreSQL here](https://www.postgresql.org/download/)


### How to install in your computer

1. Clone the repository to your computer

    [How to clone a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository?tool=webui)


2. Create a virtual environment

        python -m venv venv


3. Enable the virtual environment

    For macOS bash or zsh:

        source venv/bin/activate

    For Windows cmd:

        venv\Scripts\activate.bat

    [Learn more about virtual environments here](https://docs.python.org/3/library/venv.html)


4. Install requirements in virtual environment

        pip install -r requirements.txt


5. Create databases for setbox and setbox_test (Run these commands in your PostgreSQl terminal)
    
        CREATE DATABASE setbox;
        CREATE DATABASE setbox_test;


6. Create a copy of .env.template as .env and fill in the project environment variables

        FLASK_DEBUG=set to True or False
        DATABASE_URL=postgresql://username:password@localhost:5432/setbox (change username and password to your database data)
        TESTING_DATABASE_URL=postgresql://username:password@localhost:5432/setbox_test (change username and password to your database data)
        FLASK_APP=run.py
        SECRET_KEY=generate a random secret key
        
        
7. Run upgrade command to generate database tables

        flask db upgrade


8. Create empty directory for storing files

        mkdir files
        
        
9. Run the app to see if it is working

        python run.py


### Testing

To run tests, use this command:

        pytest -v

## Database

##### Entity Relationship Diagram

```mermaid
    erDiagram
        users }o--o{ subjects : "belongs to"
        subjects ||--o{ lessons : "has"
        lessons ||--o{ files : "contains"
```
users collection and subjects collection have a many-to-many relationship through a table users_in_subjects

##### Table Definitions

1. users collection has columns - "id", "email", "password", and "first_name"
2. subjects collection has columns - "id", "name", and "owner_user_id"
3. lessons collection has columns - "id", "subject_id", "date", "formatted_date", "start_time", "end_time", and "name"
4. diles collection has columns - "id", "name", "type", "filename", "lesson_id", and "reviewed"
5. users_in_subjects collection has columns - "user_id", "subject_id", and "editor"

##### Indexes
1. Primary Key Index on "id" column for all collections.
2. Unique Constraint Index on "email" column for users collection.
3. Unique Constraint Index on "name" and "owner_user_id" columns for subjects collection.

Something is not working? Contact @edvardsmazprecnieks .
