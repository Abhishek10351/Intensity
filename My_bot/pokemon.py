import pokepy
client = pokepy.V2Client()
client.get_pokemon(14)
print(type(client))