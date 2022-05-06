# Monpok
Monpok is a text-terminal based python game that connects to a website the website [keeraxm.rocks](https://www.keeraxm.rocks) which hosts a table of the results of all matches played. The website updates in realtime, no need to even refresh the site. Monpok is made as a school project and will not revice any updates once a grade has been set. There is also a wiki on [keeraxm.rocks/wiki](https://www.keeraxm.rocks/wiki) for any information about the game itself, how to play and Monpoks (type, stats etc.)

## Installation
Due to database authentication issues (I'm lazy), the program is currently not available to anyone but the creator.

However, if I ever to implement it or you would create your own database this is how you would do it:

Monpok uses [firebase/firestore](https://firebase.google.com/) to host all of its match data.<br>To be able to use the program, create a [virtual environment](https://docs.python.org/3/library/venv.html) in python.
```bash
pip install google-cloud-firestore
```
After that you would need to log in and, done :) (Incase you want to use your own database you would need to create a service account and create an environment variable to the path of the service account file, refer to the [firebase documentation](https://firebase.google.com/docs) )

ps. If you only want to play the game, just remove line 2, 292, 445-456. Then you will be able to launch the game as you would any python file, no prerequisites needed, not even a virtual environment.

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