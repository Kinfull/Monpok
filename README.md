# Monpok
Monpok is a text-terminal based python game that connects to a website the website [keeraxm.rocks](https://www.keeraxm.rocks) which hosts a table of the results of all matches played. The website updates in realtime, no need to even refresh the site. Monpok is made as a school project and will not revice any updates once a grade has been set.

## Installation
Due to database authentication issues (I'm lazy), the full program is currently not available to anyone but the creator.

However, if I ever implement any sort of user authentication, then all you would need to do is: install the repo, open a terminal in that foler and type:

```bash
python -m venv venv
venv/scripts/actiavte
pip install -r requirements.txt
```

To launch the program simply type:
```bash
python main.py
```
Monpok uses [firebase/firestore](https://firebase.google.com/) to host all of its match data. If you want, you can create your own firebase/firetore project to host it yourself. 


## Usage
The main() fucntion  dictates the structure of the program. The main function initializes the Game class and calls the create_monpok() function, after that the play_round() function is called, this is where the actual game is played out. This function gets called until the game is over (when someone faints) at which point the program calls the push_to_database() function which writes the match results to the database.

## To do
- Implement user authentication and database sercurity rules, so it can actually be published.
- Exand the roaster, add new Monpoks, add more Moves etc.
- Find a way to package the program, which automatically make a virtual environment and downloads all prerequisites.

## Contributing
Don't. You can download and edit the code all you want, but all pull requests will be denied since the school project does not allow other contributors except myself.

## Licence
[MIT](https://choosealicense.com/licenses/mit/)