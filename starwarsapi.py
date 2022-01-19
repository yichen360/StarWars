import pymongo
import requests

client = pymongo.MongoClient()
db = client['StarWars'] #Database Name

# Get starships info from swapi.dev website
def get_data():
    db.starships.drop()
    db.create_collection("starships")
    starships_list = []
    #Puts starships info into a list
    for x in range(4):
        url = "https://swapi.dev/api/starships/?page=" + str(x+1)
        star_wars_req = requests.get(url)
        for x in star_wars_req.json()["results"]:
            starships_list.append(x)

    return starships_list

def replace_pilot(starships_list):
    for ship in starships_list: #loop through each starship
        count = 0
        for x in ship["pilots"]: #find each pilot
            pilot_req = requests.get(x) # use the url to find get character info
            pilot = pilot_req.json()["name"]
            one_character_dict = db.characters.find_one({"name": pilot}, {"name": 1, "_id": 1}) #get the character objectID
            ship["pilots"][count] = one_character_dict["_id"] #replace the piloturl with the character objectID
            count += 1
    print(starships_list)
    return starships_list

def create_starships_collection(starships_list):
    db.starships.insert_many(starships_list)
    return True

starships_list = get_data()
starships_list = replace_pilot(starships_list)
create_starships_collection(starships_list)