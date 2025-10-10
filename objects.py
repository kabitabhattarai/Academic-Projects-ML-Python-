#This module includes two classes Player and Lineup
#Lineup is used in the main function for UI and Player is used to store attributes

class Player:
    def __init__(self,playerID,batOrder, first_name, last_name, position, at_bats, hits):
        self.playerID = playerID
        self.batOrder = batOrder
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.at_bats = at_bats
        self.hits = hits


    #Full name method
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    #Calculate batting average
    def get_batting_average(self):
        if self.at_bats == 0:
            return 0
        average = round(self.hits / self.at_bats, 3)
        return average


class Lineup:
    def __init__(self):
        self.__player_list = []
        self.__index=0

        #Adds player by appending player object into the list
    def add_player(self, player):
        self.__player_list.append(player)

    #Removes player by removing the specific index in the private list
    def remove_player(self, index):
        return self.__player_list.pop(index)


    #Returns the player at specific index
    def get_player(self, index):
        return self.__player_list[index]

    #Moves player from old index to new index
    def move_player(self, old_index, new_index):
        player= self.__player_list.pop(old_index)
        self.__player_list.insert(new_index, player)

  #Added a method to get list length since list is private
    def player_list_length(self):
        return len(self.__player_list)

    #Initializes iterator
    def __iter__(self):
        self.__index=0
        return self

    #Returns players in iteration
    def __next__(self):
        if self.__index >= len(self.__player_list):
            raise StopIteration
        player = self.__player_list[self.__index]
        self.__index += 1
        return player





