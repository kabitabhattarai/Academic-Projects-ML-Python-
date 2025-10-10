#Author: Kabita Bhattarai
#Project Four
#July 31, 2025
#This program stores data for each player, their name, position and stats.
#The command menu offers 7 options in which you can display or edit.
#This program uses classes and objects to store and update player information.
#This program includes exceptions to help users navigate errors
#This program connects to a sql database for data entry and storage

import objects
import db
from datetime import date, datetime

#Shows todays date, asks for game date and shows days until game.
#Includes exception if date format is wrong.
def dates_for_games():
    today = date.today()
    print("CURRENT DATE: ", today.strftime("%Y-%m-%d"))

    while True:
        get_game_date= input("GAME DATE: ").strip()


        if get_game_date == "":
           return

        try:
            game_date= datetime.strptime(get_game_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Game date must be entered in YYYY-MM-DD")



    days_until_game = (game_date - today).days
    if days_until_game >0:
        print("DAYS UNTIL GAME: ", days_until_game)
        return

#Displays menu options
def display_menu():
    print()
    print("MENU OPTIONS")
    print("1 - Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Move player")
    print("5 - Edit player position")
    print("6 - Edit player stats")
    print("7 - Exit program")
    print("\nPOSITIONS")
    print(" C, 1B, 2B, 3B, SS, LF, CF, RF, P ")
    print("="*60)


def display_lineup(lineup):
    print(f"{'':<3}{'Player':<31}{'POS':>6}{'AB':>6}{'H':>6}{'AVG':>8}")
    #print(f"{'Player':>10} {'POS':>25} {'AB':>6} {'H':>5} {'AVG':>7}")
    print("-"*60)

#Count the rows, then print the values by grabbing player attributes from the Player class
    for i, player in enumerate(lineup, start=1):
        full_name=player.get_full_name()
        position=player.position
        at_bats=player.at_bats
        hits=player.hits
        average=player.get_batting_average()

        print(f"{i:<3}{full_name:<31}{position:>6}{at_bats:>6}{hits:>6}{average:>8.3f}")

#Adds player by storing inputs into a player object
def add_player(lineup):
    positions = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")
    try:

        first_name= input("First name: ").strip()
        last_name= input("Last name: ").strip()
        position=input("Position: ").strip().upper()


        if position in positions:
            at_bats=int(input("At Bats: "))
            hits=int(input("Hits: "))
            if hits > at_bats:
                print("Hits cannot be greater than At Bats")
                return
            if at_bats < 0:
                print("At Bats must be 0 or greater")
                return
            if hits < 0:
                print("Hits must be between zero and at bats.")
                return
        else:
            print("Please enter a valid position")
            return
        #Calls add player method and passes in the player object, calls database add player function
        player=objects.Player(None, 0,first_name, last_name, position, at_bats, hits)
        lineup.add_player(player)
        db.add_player(player)


        print(f"{player.get_full_name()} was added.")

    except ValueError as e:
        print(type(e), e)
        print("Please enter a valid integer. \n")
        return


#Removes player by calling the remove player method, updates database by calling delete player function
def remove_player(lineup):
    try:
        lineup_removal=int(input("Enter a lineup number to remove: "))
        if 1 <= lineup_removal <= lineup.player_list_length():
            index=lineup_removal - 1
            removed_player=lineup.remove_player(index)
            db.delete_player(removed_player)

            print(f"{removed_player.get_full_name()} was removed.")
        else:
            print("Invalid lineup number. \n")
    except ValueError as e:
        print(type(e), e)
        print("Please enter a valid integer. \n")

#Moves player by calling move player method, updates database by calling update bat order function
def move_player(lineup):
    try:
        old_player_number=int(input("Enter a lineup number to move: "))
        if 1 <= old_player_number <= lineup.player_list_length():
            player=lineup.get_player(old_player_number-1)
            print(f"{player.get_full_name()} was selected.")

            new_player_number= int(input("Enter a new lineup number:  "))
            if 1 <= new_player_number <= lineup.player_list_length()+1:
                lineup.move_player(old_player_number-1, new_player_number-1)
                db.update_bat_order(lineup)

                print(f"{player.get_full_name()} was moved.")
            else:
                print("Invalid lineup number. \n")
        else:
            print("Invalid lineup number. \n")
    except ValueError as e:
        print(type(e), e)
        print("Please enter a valid integer. \n")

#Changes position of the player by reassigning an attribute, updates database by calling update function
def edit_position(lineup):
    positions = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")
    try:

        lineup_change = int(input("Enter a lineup number to edit: "))

        if 1 <= lineup_change <= lineup.player_list_length():
            player=lineup.get_player(lineup_change-1)
            print(f"You selected: {player.get_full_name()} Position: {player.position}")

            new_position = input("Enter new position: ").upper()
            if new_position in positions:
                player.position=new_position
                db.update_player(player)
                print (f"{player.get_full_name()} was updated.")
            else:
                 print("Invalid position.\n")
        else:
            print("Invalid lineup number. \n")

    except ValueError as e:
        print(type(e), e)
        print("Please enter a valid integer. \n")

#Changes stats by reassigning attributes,intakes integers, updated database by calling update player function
def edit_stats(lineup):
    try:
        stat_change_player=int(input("Enter a player number to edit: "))
        if 1 <= stat_change_player <= lineup.player_list_length():
            player=lineup.get_player(stat_change_player-1)
            print(f"You selected {player.get_full_name()} At Bats: {player.at_bats} Hits: {player.hits}")

            new_at_bats=int(input("Enter new At Bats: "))
            new_hits = int(input("Enter new Hits: "))

            if new_hits > new_at_bats:
                print("Hits cannot be greater than At Bats")
                return
            if new_at_bats < 0:
                print("At Bats must be 0 or greater")
                return
            if new_hits < 0:
                print("Hits must be between zero and at bats.")
                return
            player.at_bats = new_at_bats
            player.hits=new_hits
            db.update_player(player)
            print(f"{player.get_full_name()} was updated.")
        else:
            print("Invalid player number. \n")
    except ValueError as e:
        print(type(e), e)
        print("Please enter a valid integer. \n")



def main():
    print("="*60)
    print("Baseball Team Manager")
    #import text file by reading it and check that a file exits
    lineup=db.get_players()
    if lineup is None:
        print("File could not be found. Lineup is empty ")
        lineup=objects.Lineup()


    dates_for_games()
    display_menu()

    #lineup_list=[['Trevor','SS','588','173'],
                 #['Garrett','2B','299','74'],
                 #['Tony','C','535','176'],
                 #['Hunter','RF','580', '182'],
                 #['Ian','CF','443','113'],
                 #['Nolan','3B','588','185'],
                 #['Daniel','1B','430','129'],
                 #['David','LF','374','113'],
                 #['Phillip','P','102','12']
                 #]


    # Command menu selection if statement
    while True:
        command = input("Menu option: ")
        if command == "1":
            display_lineup(lineup)
        elif command == "2":
            add_player(lineup)
        elif command == "3":
            remove_player(lineup)
        elif command == "4":
            move_player(lineup)
        elif command == "5":
            edit_position(lineup)
        elif command == "6":
            edit_stats(lineup)
        elif command == "7":
            print("Bye!")
            break
        else:
            print("Invalid menu option. Please enter 1-7. \n")
            display_menu()


if __name__ == "__main__":
    main()
