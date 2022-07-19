import roblox

client = roblox.Client(email="email@example.com", username="Example", password="Example")

@client.listen()
def on_ready(bot: roblox.User):
     print(f"{bot.username} is online!")

client.login("roblosecurity")
