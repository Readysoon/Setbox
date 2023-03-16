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

5. Create empty database in PostgreSQL

`psql`

`CREATE DATABASE setbox;`

6. Back outside of psql terminal, import pg_dump into database

`psql setbox < ./database/setbox_database.sql`

7. Run the app to see if it is working

`python app.py`


### Troubleshooting

If `psql` is not working, try using it with path. For me, the path is:
`/Application/Postgres.app/Contents/Versions/15/bin/psql`

Any more problems? Contact @edvardsmazprecnieks .