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
Clone the repository and install [pipenv](https://pypi.org/project/pipenv/):
```bash
pip3 install pipenv
```

Navigate to the `applicazione` folder and install the dependencies:
```bash
cd applicazione
pipenv install
```

Activate the virtual environement:
```bash
pipenv shell
```

If you want a clean databese:
- Delete the existing `db.sqlite3` file.
- Remove the `dish_pics` and `profile_pics` folders.inside the `cook_and_share/media/` directory.
- Then apply the migrations:
```bash
rm db.sqlite3
rm -r cook_and_share/media/dish_pics/ cook_and_share/media/profile_pics/
python3 manage.py migrate
```

Start the project with:
```bash
python3 manage.py runserver
```