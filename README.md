# Monpok
Monpok is a terminal text-based python game that connects to the website [keeraxm.rocks](https://www.keeraxm.rocks) which hosts a table which updates in realtime of the results of all matches played. Monpok is made as a school project and will most likely not revice any updates once a grade has been set.

## Installation
Due to database authentication issues (I'm lazy), the full program is currently not available to anyone but the creator.

However, the game itself can still be played by simply dowloading the main.py file and launching it.

If I ever implement any sort of user authentication, then what you would need to do is: install the repo, open a terminal in that foler and type:

```bash
python -m venv .venv
.venv\Scripts\actiavte
pip install -r requirements.txt
```

To launch the program simply type:
```bash
python main.py
```
Monpok uses [firebase/firestore](https://firebase.google.com/) to host all of its match data. If you want, you can create your own firebase/firetore project to upload game-data youself, modify any code as you see fit.

## Usage
The main() fucntion  dictates the structure of the program. The main function initializes the Game class and calls the create_monpok() function, after that the play_round() function is called, this is where the actual game is played out. This function gets called until the game is over (when someone faints) at which point the program calls the push_to_database() function which writes the match results to the database.

## To do
- Implement user authentication, so the full program can actually be published.
- Exand the roster, add new Monpoks, add more Moves etc.
- Find a way to package the program which automatically make a virtual environment and downloads all prerequisites.

## Contributing
Don't. You can download and edit the code all you want, but all pull requests will be denied since the school project does not allow any other contributors except myself.

## Licence
[MIT](https://choosealicense.com/licenses/mit/)