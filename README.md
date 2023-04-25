# SetBox - the website for learning



### Prerequisites

python 3.9.12, PostgreSQL 15.2

[Download Python here](https://www.python.org/downloads/)

[Download PostgreSQL here](https://www.postgresql.org/download/)


### How to install in your computer

1. Clone the repository to your computer

    [How to clone a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository?tool=webui)


2. Create a virtual environment

    `python -m venv venv`


3. Enable the virtual environment

    For macOS bash or zsh:

        `source venv/bin/activate`

    For Windows cmd:

        `venv\Scripts\activate.bat`

    [Learn more about virtual environments here](https://docs.python.org/3/library/venv.html)


4. Install requirements in virtual environment

        `pip install -r requirements.txt`


5. Create databases for setbox and setbox_test
    
        Run these commands in your PostgreSQl:
        `CREATE DATABASE setbox;
         CREATE DATABASE setbox_test;`


6. Create a copy of .env.template as .env and fill in the project environment variables

        `FLASK_DEBUG=set to True or False
        DATABASE_URL=postgresql://username:password@localhost:5432/setbox (change username and password to your database data)
        TESTING_DATABASE_URL=postgresql://username:password@localhost:5432/setbox_test (change username and password to your database data)
        FLASK_APP=run.py
        SECRET_KEY=generate a random secret key`
        
        
7. Run upgrade command to generate database tables

        `flask db upgrade`


8. Create empty directory for storing files

        `mkdir files`
        
        
9. Run the app to see if it is working

        `python run.py`



Something is not working? Contact @edvardsmazprecnieks .
