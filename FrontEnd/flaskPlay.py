#!/usr/bin/env python
# coding: utf-8

# In[267]:


import random
class Simulation:
    
    def createPlayer(self, num):
        p = Player()
        p.number=num
        #print("Enter Player "+str(num)+"'s name:")
        p.name=num
        return(p)
        
    def __init__(self, session=None):
        self.shop = Shop()
        self.p1=self.createPlayer(1)
        self.p2=self.createPlayer(2)
        self.p1.setHandler(ActionHandler(self.shop, self.p1, self.p2))
        self.p2.setHandler(ActionHandler(self.shop, self.p2, self.p1))
        self.p1.phase = 1
        self.p2.phase = 1
        if session:
            self.p1.treasure = session['treasure']
            self.p1.buys = session['buys']
            self.p1.actions = session['actions']
            cards = session['cards']
            self.shop.cards = cards['Shop']
            self.p1.hand = cards['Your Hand']
            self.p1.deck = cards['Your Deck']
            self.p1.discard = cards['Your Discard']
            self.p2.hand = cards['ch']
            self.p2.deck = cards['cde']
            self.p2.discard = cards['cdi']
            
            
        else:

            '''
            self.shop = Shop()
            self.p1=self.createPlayer(1)
            self.p2=self.createPlayer(2)
            self.p1.setHandler(ActionHandler(self.shop, self.p1, self.p2))
            self.p2.setHandler(ActionHandler(self.shop, self.p2, self.p1))
            '''
            self.shop.reset()
            self.shop.setup([self.p1,self.p2])
            #print(self.getBuyState(self.p1))
            self.setupTurn(self.p1)
            self.setupTurn(self.p2)
            #!! done in model?
        '''
        while True:
            self.takeTurn(self.p1)
            if self.shop.checkEnd():
                break
            self.takeTurn(self.p2)
            if self.shop.checkEnd():
                break  
        if self.p1.getVP() > self.p2.getVP():
            print(str(self.p1)+" wins!")
        else:
            print(str(self.p2)+" wins!")
        '''
        #self.shop.reset()
        #self.p1.reset()
        #self.p2.reset()
            
    def setupTurn(self, player):
        #print('setup turn is run')
        player.actionPhase()
        #!!stop buy phase
        player.buyPhase(self.shop)
        #return self.getBuyState(player)
        
        #!! not needed yet 
        #player.cleanupPhase()
        
    
    def makeDecision(self, player, buy):
        self.setupTurn(player)
        player.updateTreasure()
        if buy==1:
            player.treasure -= player.makePurchase(self.shop)
            player.buys -= 1
        else: 
            player.buys = 0
        if player.buys == 0:
            player.treasure = 0
            player.cleanupPhase()
            return True
        return False
    
    def getBuyState(self, player):
        return [self.shop.cards, self.p1.hand, self.p1.deck, self.p1.discard, self.p2.hand, self.p2.deck, self.p2.discard]
        '''
        output = []
        for card in Card.options:
            total = 0
            for spot in [player.deck, player.hand, player.discard]:
                amount = spot.get(card)
                if amount != None:
                    total+=amount
            output.append(total)
        output.append(player.buys)
        output.append(player.treasure)
        return [output]
        '''
    
    def takeTurn(self):
        done = False
        while not done:
            #AI HERE?
            done = self.makeDecision(self.p2, 1)
        
        

# In[268]:


class Player:
    def __init__(self):
        self.reset()
        self.turn=0
    
    def __repr__(self):
        return "Player "+str(self.name)
    
    def setHandler(self, ah):
        self.actionHandler = ah
        
    def draw(self, quantity=1):
        
        #if you don't have enough cards, put discard into deck
        cardsLeft = sum(self.deck.values())
        if cardsLeft < quantity: 
            if cardsLeft > 0:
                self.takeCard(cardsLeft)
            for card in self.discard:
                self.deck[card] = self.discard[card]
            if quantity-cardsLeft > 0:
                self.takeCard(quantity-cardsLeft)
            self.discard = {}
        else:      
            #draw what you need from your deck into your hand
            self.takeCard(quantity)
            
    def takeCard(self, quantity):
        for i in range(quantity):
            drawnCard = random.choice(list(self.deck))
            self.deck[drawnCard] -= 1
            if self.deck[drawnCard] == 0:
                del self.deck[drawnCard]
            if drawnCard in self.hand:
                self.hand[drawnCard] += 1
            else:
                self.hand[drawnCard] = 1
    
    def actionPhase(self):
        self.actions = 1
        while self.actions > 0:
            actionCards = []
            for cardName in self.hand:
                if Card(cardName).type=="Kingdom":
                    actionCards.append(cardName)
            if len(actionCards)>0:
                self.takeAction(actionCards)
                self.actions -= 1
            else:
                break
        self.actions = 0
        self.phase = 2
        
    
    '''
    def takeAction(self, actionCards):
            print("\tYou have "+str(self.actions)+" actions left")
            print("\tEnter the index of your desired action:")
            print("\t"+str(actionCards))
            decision = int(input())
            if decision != -1:
                chosenAction = actionCards[decision]
                self.actionHandler.use(chosenAction)
                self.discardCard(chosenAction)
    '''
    
    def takeAction(self, actionCards):
            chosenAction = random.choice(actionCards)
            #print("random action choice of "+chosenAction)
            self.actionHandler.computerUse(chosenAction)
            self.discardCard(chosenAction)
            
            
    def updateTreasure(self):
        #count the treasure and add to player
        self.treasure = 0
        for cardName in self.hand:
            card = Card(cardName)
            if card.type == "Treasure":
                self.treasure += card.value * self.hand[cardName]
            
    def buyPhase(self, shop):
        self.buys += 1
        #find all money in hand
        for cardName in self.hand:
            card = Card(cardName)
            if card.type == "Treasure":
                self.treasure += card.value * self.hand[cardName]
        #buy things with treasure
        #!!output the state now and take input for makePurchase
        print('total treasure for buys')
        print(self.treasure)
        '''
        while self.buys > 0:
            self.treasure -= self.makePurchase(shop)
            self.buys -= 1
        self.treasure = 0
        self.buys = 0
        '''
    
    '''
    def makePurchase(self, shop):        
        #find all cards you can afford and are available
        buyable = []
        for cardName in shop.cards:
            if Card(cardName).cost <= self.treasure and shop.cards[cardName] > 0:
                buyable.append(cardName)
        print("\tYou have "+str(self.buys)+" buys remaining with "+str(self.treasure)+" to spend")
        print("\tEnter the index of the card you wish to buy:")
        print("\t"+str(buyable))
        decision = int(input())
        if decision != -1:
            bought = buyable[decision]
            shop.deal(bought, self, self.discard)
            return Card(bought).cost
        else:
            self.buys = 0
            return 0
    '''
    def playerPurchase(self, card, shop):
        shop.deal(card, self, self.discard)
        self.buys -= 1
        self.treasure -= Card(card).cost
        if self.buys <= 0:
            self.cleanupPhase()
            
            if len(self.getActions()) == 0:
                self.phase = 2
            else: 
                self.phase = 1
                #self.actions = 1
            return True
        return False
        
    def buyOptions(self, shop):
        buyable = []
        for cardName in shop.cards:
            if Card(cardName).cost <= self.treasure and shop.cards[cardName] > 0:
                buyable.append(cardName)
        return buyable
    
    def getActions(self):
        actionCards = []
        for cardName in self.hand:
            if Card(cardName).type=="Kingdom":
                actionCards.append(cardName)
        return actionCards
    
    def makePurchase(self, shop):
        buyable = []
        for cardName in shop.cards:
            if Card(cardName).cost <= self.treasure and shop.cards[cardName] > 0 and (self.buys > 1 or Card(cardName).cost >= self.treasure-1 or Card(cardName).cost>=6 or self.treasure==7):
                buyable.append(cardName)
        #print(self.treasure)
        #print(self.buys)
        #print(shop.cards)
        #print(shop.checkEnd())
        bought = random.choice(buyable) # random choice card being bought within reason
        shop.deal(bought, self, self.discard)
        return Card(bought).cost
        
    
    def cleanupPhase(self):
        #print('cleanupPhase')
       
        self.discardCard()
        self.draw(5)
        #print(self.hand)
        self.turn += 1
        self.phase = 1
        self.updateTreasure()
        self.buys = 1
        self.actions = 1
    
    def discardCard(self, card=None):
        #print('discarding..')
        if not card:
            for card in self.hand:
                print(card)
                if card in self.discard:
                    self.discard[card] += self.hand[card]
                else:
                    self.discard[card] = self.hand[card]
            self.hand = {}
        else:
            if card in self.discard:
                self.discard[card] += 1
            else:
                self.discard[card] = 1
            self.hand[card] -= 1
            if self.hand[card] == 0:
                del self.hand[card]
    
    def getVP(self):
        total = 0
        for card in self.hand:
            if Card(card).type == "VP":
                total += self.hand[card] * Card(card).value
        for card in self.deck:
            if Card(card).type == "VP":
                total += self.deck[card] * Card(card).value
        for card in self.discard:
            if Card(card).type == "VP":
                total += self.discard[card] * Card(card).value
        return total
    
    def reset(self):
        self.name=""
        self.number=0
        self.deck={}
        self.discard={}
        self.hand={}
        self.actions=0
        self.buys=0
        self.treasure=0
    
    


# In[269]:


#entirely redone
class ActionHandler:
    def __init__(self, shop, user, opponent):
        self.shop = shop
        self.user = user
        self.opp = opponent
        
    def playerUse(self, card, stage=0, arg=None):
        print(stage)
        print(card)
        print(arg)
        if card == "Cellar":
            if stage == 0:
                inHand = self.user.hand.copy()
                del inHand["Cellar"]
                if len(inHand) > 0:
                    self.user.phase = 3
                    return {"message":"Do you want to discard a card?", "options": ["Yes", "No"], "stage": stage+1, "card": card}
                else:
                    self.user.actions += 1
                    return None
            if stage == 1:
                #print(arg=="Yes")
                if arg == "Yes":
                    self.user.phase = 3
                    return {"message":"Which card?", "options": list(filter(lambda x: x != "Cellar", self.user.hand)), "stage": stage+1, "card": card}
                else:
                    self.user.actions += 1
                    return None
            if stage == 2:
                self.user.discardCard(arg)
                self.user.draw()
                self.user.phase = 3
                return self.playerUse(card)
                
            
        if card == "Market":
            self.user.draw(1)
            self.user.actions += 1
            self.user.buys += 1
            self.user.treasure += 1
        
        if card == "Militia":
            if "Moat" not in self.opp.hand:
                if len(self.opp.hand)>1:
                    discards = 2
                else: 
                    discards = len(self.opp.hand)
                for i in range(discards):
                    hand = list(self.opp.hand)
                    self.opp.discardCard(hand[random.randint(0,len(hand)-1)]) #which to discard
            self.user.treasure += 2
        
        if card == "Mine":
            if stage==0:
                treasure = ["Copper", "Silver"]
                inHand = list(filter(lambda x: x in treasure, self.user.hand)) #! maybe just check if the card value has a treasure type?
                if len(inHand) > 0:
                    self.user.phase = 3
                    return {"message":"Which treasure will you mine?", "options": inHand, "stage": stage+1, "card": card}
            else: 
                if arg == "Copper":
                    self.user.hand["Copper"] -= 1
                    if self.user.hand["Copper"] == 0:
                        del self.user.hand["Copper"]
                    if "Silver" in self.user.hand:
                        self.user.hand["Silver"] += 1
                    else: 
                        self.user.hand["Silver"] = 1
                if arg == "Silver":
                    self.user.hand["Silver"] -= 1
                    if self.user.hand["Silver"] == 0:
                        del self.user.hand["Silver"]
                    if "Gold" in self.user.hand:
                        self.user.hand["Gold"] += 1
                    else: 
                        self.user.hand["Gold"] = 1
        
        if card == "Moat":
            self.user.draw(2)
            
        if card == "Remodel":
            if stage == 0:
                if len(self.user.hand) > 0:
                    inHand = list(self.user.hand)
                    inHand.remove("Remodel")
                    self.user.phase = 3
                    return {"message":"What will you remodel?", "options": inHand, "stage": stage+1, "card": card}
            if stage == 1:
                if arg:
                    spending = Card(arg).cost + 2
                    buyable = []
                    for cardName in self.shop.cards:
                        if Card(cardName).cost <= spending and self.shop.cards[cardName] > 0:
                            buyable.append(cardName)
                    if len(buyable) > 0:
                        self.user.phase = 3
                        return {"message":"What will you buy?", "options": buyable, "stage": stage+1, "card": card}
                        
            if stage == 2:
                self.shop.deal(arg, self.user, self.user.discard)
        
        if card == "Smithy":
            self.user.draw(3)
            
        if card == "Village":
            self.user.draw(1)
            self.user.actions += 2
        
        if card == "Woodcutter":
            self.user.buys += 1
            self.user.treasure += 2
        
        if card == "Workshop":
            if stage == 0:
                buyable = []
                for cardName in self.shop.cards:
                    if Card(cardName).cost <= 4 and self.shop.cards[cardName] > 0:
                        buyable.append(cardName)
                if len(buyable) > 0:
                    self.user.phase = 3
                    return {"message":"What will you buy?", "options": buyable, "stage": stage+1, "card": card}
            else:
                self.shop.deal(arg, self.user, self.user.discard)
        self.user.actions -= 1
        if self.user.actions <= 0:
            self.user.phase = 2
            self.user.buys = 1
        
    def computerUse(self, card):
        #print(card+" played by "+str(self.user))
        if card == "Cellar":
            inHand = self.user.hand.copy()
            del inHand["Cellar"]
            if len(inHand) > 0:
                n = random.randint(0,len(inHand)-1) #how many to discard
                if n > 0:
                    for i in range(n):
                        inHand = list(filter(lambda x: x != "Cellar", self.user.hand))
                        self.user.discardCard(inHand[random.randint(0,len(inHand)-1)])
                    self.user.draw(n)
            self.user.actions += 1
            
        if card == "Market":
            self.user.draw(1)
            self.user.actions += 1
            self.user.buys += 1
            self.user.treasure += 1
        
        if card == "Militia":
            if "Moat" not in self.opp.hand:
                if len(self.opp.hand)>1:
                    discards = 2
                else: 
                    discards = len(self.opp.hand)
                for i in range(discards):
                    hand = list(self.opp.hand)
                    self.opp.discardCard(hand[random.randint(0,len(hand)-1)]) #which to discard
            self.user.treasure += 2
        
        if card == "Mine":
            treasure = ["Copper", "Silver"]
            inHand = list(filter(lambda x: x in treasure, self.user.hand)) #! maybe just check if the card value has a treasure type?
            if len(inHand) > 0:
                choice = random.randint(0,len(inHand)-1)
                if inHand[choice] == "Copper":
                    self.user.hand["Copper"] -= 1
                    if self.user.hand["Copper"] == 0:
                        del self.user.hand["Copper"]
                    if "Silver" in self.user.hand:
                        self.user.hand["Silver"] += 1
                    else: 
                        self.user.hand["Silver"] = 1
                if inHand[choice] == "Silver":
                    self.user.hand["Silver"] -= 1
                    if self.user.hand["Silver"] == 0:
                        del self.user.hand["Silver"]
                    if "Gold" in self.user.hand:
                        self.user.hand["Gold"] += 1
                    else: 
                        self.user.hand["Gold"] = 1
        
        if card == "Moat":
            self.user.draw(2)
            
        if card == "Remodel":
            if len(self.user.hand) > 0:
                inHand = list(self.user.hand)
                inHand.remove("Remodel")
                choice = random.randint(-1,len(inHand)-1) 
                if choice > -1:
                    spending = Card(inHand[choice]).cost + 2
                    buyable = []
                    for cardName in self.shop.cards:
                        if Card(cardName).cost <= spending and self.shop.cards[cardName] > 0:
                            buyable.append(cardName)
                    if len(buyable) > 0:
                        self.shop.deal(buyable[random.randint(0,len(buyable)-1)], self.user, self.user.discard)
        
        if card == "Smithy":
            self.user.draw(3)
            
        if card == "Village":
            self.user.draw(1)
            self.user.actions += 2
        
        if card == "Woodcutter":
            self.user.buys += 1
            self.user.treasure += 2
        
        if card == "Workshop":
            buyable = []
            for cardName in self.shop.cards:
                if Card(cardName).cost <= 4 and self.shop.cards[cardName] > 0:
                    buyable.append(cardName)
            if len(buyable) > 0:
                self.shop.deal(buyable[random.randint(0,len(buyable)-1)], self.user, self.user.discard)    
            


# In[270]:


class Card:
    #all possible cards
    options = {
        "Cellar": ["Cellar",2,"Kingdom"],
        "Market": ["Market",5,"Kingdom"],
        "Militia": ["Militia",4,"Kingdom"],
        "Mine": ["Mine",5,"Kingdom"],
        "Moat": ["Moat",2,"Kingdom"],
        "Remodel": ["Remodel",4,"Kingdom"],
        "Smithy": ["Smithy",4,"Kingdom"],
        "Village": ["Village",3,"Kingdom"],
        "Woodcutter": ["Woodcutter",3,"Kingdom"],
        "Workshop": ["Workshop",3,"Kingdom"],
        "Copper": ["Copper",0,"Treasure",1],
        "Silver": ["Silver",3,"Treasure",2],
        "Gold": ["Gold",6,"Treasure",3],
        "Estate": ["Estate",2,"VP",1],
        "Dutchy": ["Dutchy",5,"VP",3],
        "Province": ["Province",8,"VP",6]
    }
    
    def __init__(self, name):
        self.name = name
        card = self.options[name]
        self.cost = card[1]
        self.type = card[2]
        if len(card) == 4:
            self.value = card[3]
    
    def __repr__(self):
        return self.name
    
    


# In[271]:


class Shop:
    def reset(self):
        #initialize all cards
        self.cards = {
            "Cellar":10,
            "Market":10,
            "Militia":10,
            "Mine":10,
            "Moat":10,
            "Remodel":10,
            "Smithy":10,
            "Village":10,
            "Woodcutter":10,
            "Workshop":10,
            "Copper":60,
            "Silver":40,
            "Gold":30,
            "Estate":14,
            "Dutchy":8,
            "Province":8
        }
    
    def setup(self, players):
        for player in players:
            #deal out the starting decks to each player
            self.deal("Copper", player, player.deck, 7)
            self.deal("Estate", player, player.deck, 3)
            #each player draws 5
            player.draw(5)
    
    def deal(self, card, player, destination, quantity=1):
        #give the player a card from the shop
        self.cards[card] = self.cards[card]-quantity #CHECK IF WE RUN OUT? 
        if card in destination:
            destination[card] += quantity
        else:
            destination[card] = quantity
        #print(card+" purchased by "+str(player))
            
    def checkEnd(self):
        return len(list(filter(lambda x: self.cards[x]==0 , self.cards)))>=3 or self.cards["Province"]==0          
        
        
        


# In[272]:


'''
x=Simulation()
wins = [0]*10
for i in range(len(wins)):
    j=0
    while True:
        j+=1
        print("iteration: "+str(j))
        print("\tp1 turn: "+str(x.p1.turn))
        print("\tp2 turn: "+str(x.p2.turn))
        if x.p1.turn == x.p2.turn:
            player = x.p1
        else: 
            player = x.p2
        new_s, reward, end = x.makeDecision(player,1)
        if end:
            break
        
    print(x.p1.getVP())
    print(x.p2.getVP())
    if x.p1.getVP() > x.p2.getVP():
        print(str(x.p1)+" wins!")
        wins[i]=1
    else:
        print(str(x.p2)+" wins!")
        wins[i]=2
    x=Simulation()
print(str(wins))
'''

