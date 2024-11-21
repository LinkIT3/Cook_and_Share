# Cook & Share
Project for the Web Technologies exam (A.Y. 2023/2024)

## Summary
Cook & Share is a social network where users can post and share recipes.

Key features include:
- Searching for recipes by name or ingredients.
- Posting new recipes or creating variations of existing ones.
- Liking, saving, and downloading recipes.
- Following other users and viewing their recipes.


## How to run
After cloning the repository, install [pipenv](https://pypi.org/project/pipenv/):
```bash
pip3 install pipenv
```

Navigate to the `applicazione` folder and install the dependencies:
```bash
pipenv install
```

Activate the virtual environement:
```bash
pipenv shell
```

If you want a clean databese, delete the existing `db.sqlite3` file and create a new one:
```bash
rm db.sqlite3
python3 manage.py migrate
```

Start the project with:
```bash
python3 manage.py runserver
```