from datetime import datetime
from random import randint
from os import system
from time import sleep

# Stage modifires. Used to modify the stats of a Monpok.
stages = [1, 1.5, 2, 2.5, 3, 3.5, 4, 0.66, 0.5, 0.4, 0.33, 0.28, 0.25]

class Monpok:
    # General Monpok class.

    def __init__(self, name: str, stab: list) -> None:
        self.name = name
        self.stab = stab
        self.hp = (stab[0], 0)
        self.attack = (stab[1], 0)
        self.defense = (stab[2], 0)
        self.sp_attack = (stab[3], 0)
        self.sp_defense = (stab[4], 0)
        self.speed = (stab[5], 0)
        self.moves = ["Basic"]
        self.basic = AtkMove("Basic", self)
        
    def show_moves(self, indent: str="") -> None:
        # Print all available moves.
        print(f"{indent}{self.name}'s Moves:")
        for idx, val in enumerate(self.moves):
            print(f"  {indent}{idx+1}: {val}")
 
    def get_hp(self) -> int:
        return self.hp
    
    def take_dmg(self, dmg: int) -> None:
        if self.hp[0] >= dmg:
            self.hp = (self.hp[0] * self.hp[1] - dmg, self.hp[1])
        else:
            self.hp = (0, self.hp[1])

    def use_basic(self, target) -> None:
        """Use basic attack move. 

        Args:
            target (Monpok): Target of the attack.
        """

        dmg = self.basic.use_move(target, "attack")
        if dmg > 0:
            target.take_dmg(dmg)
            print(f"{self.name} hits {target.name} for {dmg} damage!")
        else:
            print(f"{self.name} missed!", end=" ")
            sleep(1)
            print(f"{target.name} Defense stat is too high!")


class FireMonpok(Monpok):
    # Fire-themed monpok.

    def __init__(self, name: str, stab: list) -> None:
        super().__init__(name, stab)
        self.type = "Fire"
        self.fireball = AtkMove("Fireball", self)
        self.combustion = BuffMove("Combustion", "sp_attack", 1)
        self.moves.extend([self.fireball.name, self.combustion.name])

    def use_fireball(self, target: Monpok) -> None:
        dmg = self.fireball.use_move(target, "sp_attack")
        if dmg > 0:
            target.take_dmg(dmg)
            print(f"{self.name} burnes {target.name} for {dmg} damage!")
        else:
            print(f"{self.name} missed:", end=" ")
            sleep(1)
            print("{target.name}'s Sp_Defense stat is too high!")
    
    def use_combustion(self) -> None:
        self.combustion.apply_buff(self)
        print(f"{self.name} is on fire:", end=" ")
        sleep(1)
        print(f"sp_attack increased by {self.combustion.delta_stage} stages!")
        
    def use_move(self, move: int, target: Monpok) -> None:
        # Manages what move to use.

        if move == 1:
            self.use_basic(target)
        elif move == 2:
            self.use_fireball(target)
        elif move == 3:
            self.use_combustion()


class DarkMonpok(Monpok):
    # Like fire, but dark.

    def __init__(self, name: str, stab: list) -> None:
        super().__init__(name, stab)
        self.type = "Dark"
        self.shadowbolt = AtkMove("Shadowbolt", self)
        self.curse = BuffMove("Curse", "sp_attack", -1, 0.75)
        self.moves.extend([self.shadowbolt.name, self.curse.name])

    def use_shadowbolt(self, target: Monpok) -> None:
        dmg = self.shadowbolt.use_move(target, "sp_attack")
        if dmg > 0:
            target.take_dmg(dmg)
            print(f"{self.name} hits {target.name} for {dmg} damage!")
        else:
            print(f"{self.name} missed:", end=" ")
            sleep(1)
            print(f"{target.name}'s Sp_Defense stat is too high!")

    def use_curse(self, target: Monpok) -> None:
        if get_hit(self.curse.accuracy):
            self.curse.apply_buff(target)
            print(f"{self.name} curses {target.name}:", end=" ")
            sleep(1)
            print(f"sp_defense stat decreased by {self.curse.delta_stage} stages!")
        else:
            print(f"{self.name} failed the curse!")

    def use_move(self, move: int, target: Monpok) -> None:
        # Manages what move to use.

        if move == 1:
            self.use_basic(target)
        elif move == 2:
            self.use_shadowbolt(target)
        elif move == 3:
            self.use_curse(target)


class RockMonpok(Monpok):
    # Rocksolid.

    def __init__(self, name: str, stab: list) -> None:
        super().__init__(name, stab)
        self.type = "Rock"
        self.rock_throw = AtkMove("Rock Throw", self)
        self.harden_skin = BuffMove("Harden Skin", "defense", 1)
        self.moves.extend([self.rock_throw.name, self.harden_skin.name])

    def use_rock_throw(self, target: Monpok) -> None:
        dmg = self.rock_throw.use_move(target, "sp_attack")
        if dmg > 0:
            target.take_dmg(dmg)
            print(f"{self.name} hurls a bolder at {target.name} for {dmg} damage!")
        else:
            print(f"{self.name} missed:", end=" ")
            sleep(1)
            print(f"{target.name}'s Sp_Defense stat is too high!")
    
    def use_harden_skin(self) -> None:
        self.harden_skin.apply_buff(self)
        print(f"{self.name}'s skin hardens:", end=" ")
        sleep(1)
        print(f"defense stat increased by {self.harden_skin.delta_stage} stage!")
    
    def use_move(self, move: int, target: Monpok) -> None:
        # Manages what move to use.

        if move == 1:
            self.use_basic(target)
        elif move == 2:
            self.use_rock_throw(target)
        elif move == 3:
            self.use_harden_skin()


class Move:
    # Move class template.

    def __init__(self, name: str, accuracy: float=1) -> None:
        self.name = name
        self.accuracy = accuracy


class AtkMove(Move):
    # Attacking moves.

    def __init__(self, name: str, user: Monpok, accuracy: float=1) -> None:
        super().__init__(name, accuracy)
        self.user = user

    def use_move(self, target: Monpok, stat: str) -> int:
        """Determins the dmg of used move based on stats.

        Args:
            target (Monpok): Target object.
            stat (str): Stat used for attack.

        Returns:
            int: damage the target will take.
        """

        if stat == "attack":
            if target.defense <= self.user.attack:
                dmg = int(self.user.attack[0] * stages[self.user.attack[1]]) - int(target.defense[0] * stages[target.defense[1]])
                return dmg
            else:
                return 0
        elif stat == "sp_attack":
            if target.sp_defense <= self.user.sp_attack:
                dmg = int(self.user.sp_attack[0] * stages[self.user.sp_attack[1]]) - int(target.sp_defense[0] * stages[target.sp_defense[1]])
                return dmg
            else:
                return 0


class BuffMove(Move):
    # Handles buff moves.

    def __init__(self, name: str, stat: str, delta_stage: int, accuracy: float=1) -> None:
        super().__init__(name, accuracy)
        self.stat = stat
        self.delta_stage = delta_stage
    
    def apply_buff(self, target: Monpok) -> None:
        if self.stat == "hp":
            target.hp = (target.hp[0], target.hp[1] + self.delta_stage)
        elif self.stat == "attack":
            target.attack = (target.attack[0], target.attack[1] + self.delta_stage)
        elif self.stat == "defense":
            target.defense = (target.defense[0], target.defense[1] + self.delta_stage)
        elif self.stat == "sp_attack":
            target.sp_attack = (target.sp_attack[0], target.sp_attack[1] + self.delta_stage)
        elif self.stat == "sp_defense":
            target.sp_defense = (target.sp_defense[0], target.sp_defense[1] + self.delta_stage)
        elif self.stat == "speed":
            target.speed = (target.speed[0], target.speed[1] + self.delta_stage)

    def remove_buff(self, target: Monpok) -> None:
        if self.stat == "hp":
            target.hp = (target.hp[0], target.hp[1] - self.delta_stage)
        elif self.stat == "attack":
            target.attack = (target.attack[0], target.attack[1] - self.delta_stage)
        elif self.stat == "defense":
            target.defense = (target.defense[0], target.defense[1] - self.delta_stage)
        elif self.stat == "sp_attack":
            target.sp_attack = (target.sp_attack[0], target.sp_attack[1] - self.delta_stage)
        elif self.stat == "sp_defense":
            target.sp_defense = (target.sp_defense[0], target.sp_defense[1] - self.delta_stage)
        elif self.stat == "speed":
            target.speed = (target.speed[0], target.speed[1] - self.delta_stage)


class Game:
    # Manages the game.

    def __init__(self) -> None:
        self.player_list = []
        self.round = 0

    def init_game(self) -> None:
        # Initializes a game: chooses who starts and starts the round counter.

        self.turn = self.player_list[0]
        self.increment_round()
    
    def get_turn(self) -> Monpok:
        return self.turn

    def change_turn(self) -> None:
        if self.turn == self.player_list[0]:
            self.turn = self.player_list[1]
        else:
            self.turn = self.player_list[0]

    def get_round(self) -> int:
        return self.round
    
    def increment_round(self) -> None:
        self.round += 1

    def is_running(self) -> bool:
        # If game is running: Everyone is alive.

        if self.player_list[0].get_hp()[0] == 0 or self.player_list[1].get_hp()[0] == 0:
            return False
        else:
            return True


def main():
    # Manages structure of the game.

    game = Game()
    create_monpok(game)
    game.init_game()
    
    system("CLS")
    print("\t--Game Start--")

    while game.is_running():
        results = play_round(game)

    else:
        winner = results[0]
        loser = results[1]

        system("CLS")
        sleep(1)
        print("We have a winner!\n")
        sleep(1)
        print(f"{winner.name} wins!")

        sleep(1)
        push_to_database(winner, loser)
    input_handler("\n\nPress enter to exit.")

def play_round(game: Game) -> list:
    """Players take turns deciding an action for thire turn. After making a decition the round is played out, whoever has speed is greater goes first.

    Args:
        game (Game): Game object.

    Returns:
        list: If a Monpok faints: return [winner object, loser object]. Else: no return.
    """

    player_action = []
    player_one = game.player_list[0]
    player_two = game.player_list[1]

    system("CLS")
    print(f"Round: {game.get_round()}!")

    for player in game.player_list:
        print(f"\n{game.get_turn().name}'s Turn!")

        used_action = False
        while not used_action:
            action = input_handler("\nChoose your action!\n : ", ["Av", "Help", "Hp", "Move", "Sheet"], "Try: 'Av' or 'Help'") 
            system("CLS")
            if action == "Av" or action == "Help":
                print("Available actions:")
                print("    Av/Help: Show Available action.")
                print("    Hp: Get your Monpok's current Hp.")
                print("    Move: Use a move.")
                print("    Sheet: Get your Monpok's base stats and available moves.")

            elif action == "Hp":
                print(f"{player.name}'s Current hp: {player.get_hp()[0]}")    

            elif action == "Sheet":
                print(f"{player.name}'s Sheet:")
                print(f"    Type: {player.type}")
                print()
                print(f"    Hp: {player.hp[0] * stages[player.hp[1]]}")
                print(f"    Attack: {player.attack[0] * stages[player.attack[1]]}")
                print(f"    Defense: {player.defense[0] * stages[player.defense[1]]}")
                print(f"    Sp_Attack: {player.sp_attack[0] * stages[player.sp_attack[1]]}")
                print(f"    Sp_Defense: {player.sp_defense[0 ]* stages[player.sp_defense[1]]}")
                print(f"    Speed: {player.speed[0] * stages[player.speed[1]]}")
                print()
                player.show_moves("    ")                

            elif action == "Move":
                player.show_moves()
                move = input_handler(" : ", [i+1 for i in range(len(player.moves))], "", int)
                player_action.append(move)

                used_action = True

            print()

        game.change_turn()
        system("CLS")

    system("CLS")
    sleep(0.5)
    print(f"Round {game.get_round()} Start!\n")
    sleep(1)
    print()

    if player_one.speed > player_two.speed:
        player_one.use_move(player_action[0], player_two)
        print()
        sleep(1)
        # If monpok has fainted return winner, loser.
        if check_faint(player_two):
            return player_one, player_two

        player_two.use_move(player_action[1], player_one)
        
        if check_faint(player_one):
            return player_two, player_one
    else:
        player_two.use_move(player_action[1], player_one)
        print()
        sleep(1)
        if check_faint(player_one):
            return player_two, player_one
            
        player_one.use_move(player_action[0], player_two)
        if check_faint(player_two):
            return player_one, player_two

    sleep(1.5)
    input_handler("\n Press Enter button to continue.")
    game.increment_round()

def check_faint(player: Monpok) -> bool:
    """Check if Monpok object has fainted i.e hp is 0

    Args:
        player (Monpok): Monpok object to check.

    Returns:
        bool: True if Monpok has fainted.
    """

    if player.hp[0] * stages[player.hp[1]] == 0:
        print(f"\n {player.name} faints!")
        sleep(1)
        input_handler("\n  Press Enter button to continue.")
        return True
    else:
        return False
    
def create_monpok(game: Game) -> None:
    """Players take turns creating a Monpok object.

    Args:
        game (Game): Game object.
    """

    for i in range(2):
        system("CLS")
        print(f"Player {i+1}: Choose your Monpok!\n\t1. Fire\n\t2. Dark\n\t3. Rock")
        player_choice = input_handler(" : ", [1, 2, 3], "", int)
        player_name = input_handler("Name your Monpok: ")
        if player_choice == 1:
            game.player_list.append(FireMonpok(player_name, [85, 30, 50, 75, 40, 65]))
        elif player_choice == 2:
            game.player_list.append(DarkMonpok(player_name, [90, 40, 65, 70, 60, 50]))
        elif player_choice == 3:
            game.player_list.append(RockMonpok(player_name, [120, 80, 60, 0, 30, 30]))

def input_handler(input_message: str="", expected_values: list=[], error_message: str="", input_type: any=str, ) -> any:
    """Manage inputs, expands the functionanlity of python's built in input() function.

    Args:
        input_message (str, optional): String to display on input.
        expected_values (list, optional): Input must be one of the items in the list or the user will be promted again. Defaults to [].
        error_message (str, optional): If input is one of the expected_values display the string. Defaults to "".
        input_type (any, optional): Forced typing of input, user will be promted again on ValueError. Defaults to str.

    Returns:
        any: Returns the user input.
    """

    while True:
        try:
            user_input = input_type(input(input_message).capitalize().strip())
            
            if expected_values == []:
                break
            if user_input in expected_values:
                break
            else:
                print("Input exeeded expected values.", error_message)
    
        except ValueError:
            print("ValueError.")
    return user_input

def get_hit(accuracy: float) -> bool:
    """Generate hit within specified accuracy

    Args:
        accuracy (float): Hit chance.

    Returns:
        bool: True on hit, False on miss.
    """

    roll = randint(0,11)/10
    if roll <= accuracy:
        return True
    else:
        return False

def push_to_database(winner: Monpok, loser: Monpok) -> None:
    """Tries to upload to firestore database specified in service-account.json

    Args:
        winner (Monpok): Winner Monpok object
        loser (Monpok): Loser Monpok object
    """

    # Check if firebase is installed
    try:
        import firebase_admin
        from firebase_admin import credentials
        from firebase_admin import firestore

    except ImportError:
        print()
        print("ImportError.")
        sleep(1)
        print("Couldn't upload game-data to database.")
        sleep(1)
        print("Prerequisite firebase-admin not installed.")
        return

    # Upload to database if account-credentials are provided.
    try:
        cred = credentials.Certificate("service-account.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        db.collection(u"matches").document(datetime.now().strftime("%d:%m:%Y:%H:%M:%S")).set({
            u"winner_name": winner.name,
            u"winner_monpok": winner.type,
            u"loser_name": loser.name,
            u"loser_monpok": loser.type
        })
        print("\n Game-data saved.")

    except:
        print("\n Error: Couldn't upload game to database.\n No valid account-credentials")

if __name__ == "__main__":
    main()