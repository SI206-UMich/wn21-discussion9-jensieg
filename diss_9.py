from bs4 import BeautifulSoup
import re
import requests
import unittest

# Task 1: Get the URL that links to the Pokemon Charmander's webpage.
# HINT: You will have to add https://pokemondb.net to the URL retrieved using BeautifulSoup
def getCharmanderLink(soup):
    infocard = soup.find('div', class_ = 'infocard-list infocard-list-pkmn-lg')
    charmander = infocard.find_all('span', class_ = 'infocard-lg-img')[3]
    actual = charmander.find('a')['href']
    full = 'https://pokemondb.net' + actual
    return full

# Task 2: Get the details from the box below "Egg moves". Get all the move names and store
#         them into a list. The function should return that list of moves.
def getEggMoves(pokemon):
    url = 'https://pokemondb.net/pokedex/' + pokemon
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    lst = []
    egg_moves= soup.find_all('table', {'class': 'data-table'})[2]
    tags = egg_moves.find_all('tr')
    for tag in tags[1:]:
        stuff = tag.find('a', class_ = "ent-name").text
        move = stuff.strip()
        lst.append(move)
    return lst

# Task 3: Create a regex expression that will find all the times that have these formats: @2pm @5 pm @10am
# Return a list of these times without the '@' symbol. E.g. ['2pm', '5 pm', '10am']
def findLetters(sentences):
    lst = []
    regex = r'@(\d+ ?[ap]m)'
    for phrase in sentences:
        formats = re.findall(regex, phrase)
        for word in formats:
            lst.append(word)
    return lst
    #return the list of the last letter of all words that begin or end with a capital letter



def main():
    url = 'https://pokemondb.net/pokedex/national'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    getCharmanderLink(soup)
    getEggMoves('scizor')

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(requests.get('https://pokemondb.net/pokedex/national').text, 'html.parser')

    def test_link_Charmander(self):
        self.assertEqual(getCharmanderLink(self.soup), 'https://pokemondb.net/pokedex/charmander')

    def test_egg_moves(self):
        self.assertEqual(getEggMoves('scizor'), ['Counter', 'Defog', 'Feint', 'Night Slash', 'Quick Guard'])

    def test_findLetters(self):
        self.assertEqual(findLetters(['Come eat lunch at 12','there"s a party @2pm', 'practice @7am','nothing']), ['2pm', '7am'])
        self.assertEqual(findLetters(['There is show @12pm if you want to join','I will be there @ 2pm', 'come at @3 pm will be better']), ['12pm', '3 pm'])

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)