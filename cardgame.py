# AUTHOR: HAOCHEN GOU

import random

def main():
    filename = input('Enter name of file to read >  ')
    try:
        file = open(filename,'r')
        content = file.read().splitlines()
        assert (len(content)== 52),'the number of cards is wrong' # test number of card
        
        # transefer list of cards to set to check if there has duplicate cards
        set_content = set(content)        
        assert (len(set_content)== 52),'file has duplicate cards' 
       
        for card in content:
            card.upper()
            assert (card[0] in '023456789KQJA' and card[1] in 'DCHS' and len(card) == 2),'wrong card' # check format of the card    
    except IOError:
        print('file dose not exist or can not be read')
    except AssertionError as e:
        print(e.args[0])
    
    else:
        # distribute cards to two players 
        player1 = CircularQueue(52)
        player2 = CircularQueue(52)
        begin = random.choice(['player1','player2'])
        if begin == 'palyer1':
            for card in content[0:26]:
                player1.enqueue(card)
            for card in content[26:]:
                player2.enqueue(card)
        else:
            for card in content[26:]:
                player1.enqueue(card)
            for card in content[0:26]:
                player2.enqueue(card)
        
        # ask player for data
        war = input('Enter the number of cards down ?')
        while war not in ['1','2','3']:
            war = input('Enter the number of cards down ?')
        
        endgame = False
        player1_win = False
        player2_win = False
        table = OnTable()
       
        # get card from player1 and player2 to compare
        while not endgame:
            card_p1 = player1.dequeue()
            table.place('player1',card_p1,False)
            
            card_p2 = player2.dequeue()
            table.place('player2',card_p2,False)
        
            result = compare_cards(card_p1,card_p2)
            
            #display table
            print(table)
            print('player1 : ',player1.size(),' player2 : ',player2.size())
            
            # for different result clean table and append card to player
            if result == 1:
                for i in table.cleanTable():
                    player1.enqueue(i)
                print('Player1 takes all cards on table') 
            elif result == -1:
                for i in table.cleanTable():
                    player2.enqueue(i)
                print('Player2 takes all cards on table')
            else:
                print('WAR STARTS!!!')
                # check if each player have enough cards to start the war
                if player1.size() < int(war)+1:
                    print('Player1 does not have enough cards','\n','Player2 takes all cards on table and player1 cards','\n')
                    while not player1.isEmpty():
                        player2.enqueue(player1.dequeue()) # get all card from player1 to player2
                    player2_win = True
                    for i in table.cleanTable():# get card from table
                        player2.enqueue(i)                    
                    break
                elif player2.size() < int(war)+1:
                    print('Player2 does not have enough cards','\n','Player1 takes all cards on table and player2 cards','\n')
                    while not player2.isEmpty():
                        player1.enqueue(player2.dequeue()) # get all card from player2 to player1                   
                    player1_win = True
                    for i in table.cleanTable():# get card from table
                        player1.enqueue(i)                    
                    break
                    
                # start the war
                else:
                    # face_down cards
                    for num in range(int(war)):
                        card_p1 = player1.dequeue()
                        table.place('player1',card_p1,True)
                        card_p2 = player2.dequeue()
                        table.place('player2',card_p2,True)
            #desplay 60 dashes
            print('-'*60)
            action = input()
            if player1.size() == 0 or player2.size() == 0:
                endgame = True
        #display winner
        if player1.size() > 0 and player2.size() == 0 or player1_win :
            print('Player1 wins the game','\n','player1 : ', player1.size(),' Player2 : ',player2.size())
        elif player2.size() > 0 and player1.size() == 0 or player2_win :
            print('Player2 wins the game','\n','player1 : ', player1.size(),' Player2 : ',player2.size())
            


                
class OnTable:
    def __init__(self):
        self._cards = []
        self._faceUp = []
    
    def place(self,player,card,hidden):
        # get the card for the player and display on each player's table side
        player1_table = []
        player2_table = []
        if not hidden:
            self._faceUp.append(card)        
        if player == 'player1':
            player1_table.append(card)
        else:
            player2_table.append(card)
        self._cards += player1_table
        self._cards += player2_table
    
    def cleanTable(self):
        get_list = []
        get_list += self._cards
        random.shuffle(get_list)
        self._cards = []
        self._faceUp = []
        return get_list
    
    def __str__(self):
        card_list = []
        list_str = ''
        num = len(self._cards)//2
        for card in self._cards:
            if card not in self._faceUp:
                card_list .append('XX')
            else:
                card_list.append(card)
        p1 = ','.join(card_list[0::2])
        p2 =','.join(card_list[1::2])
        list_str = '[ '+p1+' | '+p2 + ' ]'
        return list_str

            

 
# use to compare cards
def compare_cards(card_p1,card_p2):
    # make dic for cards rank
    rank = {} 
    rank["A"] = 13
    rank["K"] = 12
    rank["Q"] = 11
    rank["J"] = 10
    rank["0"] = 9
    rank["9"] = 8
    rank["8"] = 7
    rank["7"] = 6
    rank["6"] = 5
    rank["5"] = 4
    rank["4"] = 3
    rank["3"] = 2
    rank["2"] = 1
    if rank[card_p1[0]] == rank[card_p2[0]]:
        return 0
    elif rank[card_p1[0]] > rank[card_p2[0]]:
        return 1    
    elif rank[card_p1[0]] < rank[card_p2[0]]:
        return -1    
    

class CircularQueue:
# Constructor, which creates a new empty queue:
    def __init__(self, capacity):
        if type(capacity) != int or capacity<=0:
            raise Exception ('Capacity Error')
        self.__items = []
        self.__capacity = capacity
        self.__count=0
        self.__head=0
        self.__tail=0
    def enqueue(self, item):
        if self.__count== self.__capacity:
            raise Exception('Error: Queue is full')
        if len(self.__items) < self.__capacity:
            self.__items.append(item)
        else:
            self.__items[self.__tail]=item
        self.__count +=1
        self.__tail=(self.__tail +1) % self.__capacity
        
    # Removes and returns the front-most item in the queue.
    # Returns nothing if the queue is empty.
    def dequeue(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty')
        item= self.__items[self.__head]
        self.__items[self.__head]=None
        self.__count -=1
        self.__head=(self.__head+1) % self.__capacity
        return item 
   
    # Returns the front-most item in the queue, and DOES NOT change the queue.
    def peek(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty')
        return self.__items[self.__head]    

    # Returns True if the queue is empty, and False otherwise:
    def isEmpty(self):
        return self.__count == 0
    
    # Returns True if the queue is full, and False otherwise:
    def isFull(self):
        return self.__count == self.__capacity
    
    # Returns the number of items in the queue:
    def size(self):
        return self.__count
    
    # Returns the capacity of the queue:
    def capacity(self):
        return self.__capacity

    # Removes all items from the queue, and sets the size to 0
    # clear() should not change the capacity
    def clear(self):
        self.__items = []
        self.__count=0
        self.__head=0
        self.__tail=0
    
    # Returns a string representation of the queue:
    def __str__(self):
        str_exp = "]"
        i=self.__head
        for j in range(self.__count):
            str_exp += str(self.__items[i]) + " "
            i=(i+1) % self.__capacity
        return str_exp + "]"
    
    # Returns a string representation of the object CircularQueue
    def __repr__(self):
        return str(self.__items) + " H="+ str(self.__head) + " T="+str(self.__tail) +" ("+str(self.__count)+"/"+str(self.__capacity)+")"

    
    
    
main()
