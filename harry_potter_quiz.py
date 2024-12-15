# QUiz Game
print("Welcome to the game!! ")

player = input("Would you like to play? ")

if player.lower() != "yes":
    quit()
print(" Awesome Let's play good luck!! ")
score = 0
answer = input("What is the name of Harry Potter's owl? ")
if answer == "Hedwig":
    print("on your way to being a Potter Head!! ")
    score += 1
else:
    print(" wrong you are not a potter head! ")
    
answer = input("Who is the author of the Harry Potter book series? ")
if answer == "J.K. Rowling":
    print("correct on your way to being a Potter head!! ")
    score += 1
else:
    print("Wrong your not a Potter head! ")    
    
answer = input("What house at Hogwarts does Harry belong to? ")
if answer == "Gryffindor":
    print("Keep going your getting closer to being a Potter head!! ")
    score += 1
else:
    print("wrong you should go read the books!! ")
    
answer = input("What is the name of the wizarding bank in Diagon Alley? ")
if answer == "Gringotts":
    print("WoW your showing your on your path to be a potter head!! ")
    score += 1
else:
    print("Wrong Go read the books are watch the movies!")
    
answer = input("What position does Harry play on the Quidditch team? ")
if answer == "Seeker":
    print("Great job halfway there to being a Potter Head!!! ")
    score += 1
else:
    print("keep trying one day you will get there! ")
    
answer = input("What is the name of the potion that grants luck to the drinker? ")
if answer == "Felix Felicis":
    print("Great Job you belong in the wizard world!!! ")
    score += 1
else:
    print("Questions are going to get even harder read a book! ")
    
answer = input("what is the name of Hagrids giant half brother? ")
if answer == "Grawp":
    print("Great you got it right now lets see if you really are a potter head!! ")
    score += 1
else:
    print("Wrong looks like you need to study harder!!")
    
answer = input("Who was the original owner of the Elder Wand? ")
if answer == "Antioch Peverell":
    print(" The Wizard world is buzzing about you getting that correct!! ")
    score += 1
else:
    print("Quite has fallen over the wizard world cause you were wrong")
    
answer = input("What is the incantation for conjuring the Dark Mark?")
if answer == "Morsmorde":
    print("WOW you know your Potter!!")
    score += 1
else:
    print("1 question left keep trying!")
    
answer = input("In what year in universe was the battle of hogwarts fought? ")
if answer == "1998":
    print("Potter Head? lets see")
    score += 1
else:
    print("Lets see if you got any of the others right!! ")
    
    print("You got " + str(score) + "questions correct ")
    print(" If your score is 7+ your a Potter Head if not go read a book!!! ")
    