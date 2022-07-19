# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2022-present Artic

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio, functools, warnings

import aiohttp, requests

__all__ = (
    'LoginError',
    'UserNotFound',
    'GroupNotGroup',
    'GameNotFound',
    'Logout',
    'AsyncEvent',
    'Forbidden',
    'User',
    'Game',
    'Group',
    'Client'
)

__author__ = 'Artic'
__version__ = '1.0.0'
__description__ = 'A simple API wrapper for Roblox.'

class LoginError(Exception):
    pass

class UserNotFound(Exception):
    pass

class GroupNotFound(Exception):
    pass

class GameNotFound(Exception):
    pass

class Logout(Exception):
    pass

class AsyncEvent(Exception):
    pass

class Forbidden(Exception):
    pass

def deprecated(instead: str = None):
    def actual_decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            if instead:
                fmt = 'roblox.deprecated: {0.__name__} is deprecated, use {1} instead.'
            else:
                fmt = 'roblox.deprecated: {0.__name__} is deprecated.'

            warnings.warn(fmt.format(func, instead), stacklevel=3, category=DeprecationWarning)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)
        return decorated
    return actual_decorator

def unstable(message: str = None):
    def actual_decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            if message:
                fmt = 'roblox.unstable: {0.__name__}() is unstable, {1}.'
            else:
                fmt = 'roblox.unstable: {0.__name__} is unstable.'
            print(fmt.format(func, message))
            return func(*args, **kwargs)
        return decorated
    return actual_decorator

class User(object):
    r"""
    This object representing a user on Roblox.
    
    Attributes
    -----------
    id: <class 'int'>
        The id of the user.
    username: <class 'str'>
        The username of the user.
    avatarURL: <class 'str'>
        The url of the user's avatar.
    avatarFinal: <class 'str'>
        The url of the user's final avatar.
    is_online: <class 'bool'>
        Whether the user is online or not.
    friends: <class 'list'>
        A list of all the user's friends.
    games: <class 'list'>
        A list of all the user's games.
    favorite_games: <class 'list'>
        A list of all the user's favorite games.
    description: <class 'str'>
        The user's description.
    created: <class 'str'>
        The date the user was created.
    is_banned: <class 'bool'>
        Whether the user is banned or not.
    externalAppDisplayName: <class 'str'>
        The user's external app display name.
    has_badge: <class 'bool'>
        Whether the user has a badge or not.
    name: <class 'str'>
        The user's name.
    username_history: <class 'list'>
        A list of all the user's username history.
    """

    def __init__(self, json: dict, bot) -> None:
        self.json = json
        self.base_url = "https://api.roblox.com"
        self.requests = requests.Session()
        self.bot = bot
    
    id = property(lambda self: self.json['Id'])
    username = property(lambda self: self.json['Username'])
    avatarURL = property(lambda self: self.json['AvatarUri'])
    avatarFinal = property(lambda self: self.json['AvatarFinal'])
    is_online = property(lambda self: self.json['IsOnline'])

    def __str__(self):
        r"""
        This function is called when the user is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        # The user object is now available.
        user = client.fetch_user(id=1) 

        # This will print the user's info.
        print(user) 

        client.login("roblosecurity")
        -----------

        >>> User(id=1, username="Roblox", avatarURL=None, avatarFinal=None, is_online=False)

        """

        return f"User(id={self.id}, username={self.username}, avatarURL={self.avatarURL}, avatarFinal={self.avatarFinal}, is_online={self.is_online})"

    def get_friends(self):
        r"""
        This function returns a list of all the user's friends.

        It is not called directly, but is called by a variable in the user object, "friends".
        """

        __friends__ = []
        resp = self.requests.get(f"{self.base_url}/users/{self.id}/friends")
        for friend in resp.json():
            id = friend['Id']
            username = friend['Username']
            avatarURL = friend['AvatarUri']
            avatarFinal = friend['AvatarFinal']
            is_online = friend['IsOnline']
            user = {"Id": id, "Username": username, "AvatarUri": avatarURL, "AvatarFinal": avatarFinal, "IsOnline": is_online}
            __friends__.append(User(user, self.bot))
        self.requests.close()
        return __friends__
    
    def get_games(self):
        r"""
        This function returns a list of all the user's games.

        It is not called directly, but is called by a variable in the user object, "games".
        """

        __games__ = []
        resp = self.requests.get(f"https://games.roblox.com/v2/users/{self.id}/games")
        data = resp.json()
        for game in data['data']:
            id = game['id']
            name = game['name']
            description = game['description']
            creator = game['creator']
            rootPlace = game['rootPlace']
            created = game['created']
            updated = game['updated']
            visits = game['placeVisits']
            game = {"id":id,"name":name,"description":description,"creator":creator,"rootPlace":rootPlace,"created":created,"updated":updated,"placeVisits": visits}
            __games__.append(game)
        self.requests.close()
        return __games__
    
    def get_favorite_games(self):
        r"""
        This function returns a list of all user's favorite games.

        It is not called directly, but is called by a variable in the user object, "favorite_games".
        """

        __games__ = []
        resp = self.requests.get(f"https://games.roblox.com/v2/users/{self.id}/favorite/games")
        data = resp.json()
        for game in data['data']:
            id = game['id']
            name = game['name']
            description = game['description']
            creator = game['creator']
            rootPlace = game['rootPlace']
            created = game['created']
            updated = game['updated']
            visits = game['placeVisits']
            game = {"id":id,"name":name,"description":description,"creator":creator,"rootPlace":rootPlace,"created":created,"updated":updated,"placeVisits": visits}
            __games__.append(game)
        self.requests.close()
        return __games__
    
    def get_description(self):
        r"""
        This function returns the user's description.

        It is not called directly, but is called by a variable in the user object, "description".
        """

        resp = self.requests.get(f"https://users.roblox.com/v1/users/{self.id}")
        data = resp.json()
        return data['description']
    
    def get_created(self):
        r"""
        This function returns the user's creation date.

        It is not called directly, but is called by a variable in the user object, "created".
        """

        resp = self.requests.get(f"https://users.roblox.com/v1/users/{self.id}")
        data = resp.json()
        return data['created']
    
    def get_is_banned(self):
        r"""
        This function returns whether the user is banned or not.

        It is not called directly, but is called by a variable in the user object, "is_banned".
        """

        resp = self.requests.get(f"https://users.roblox.com/v1/users/{self.id}")
        data = resp.json()
        return data['isBanned']
    
    def get_externalAppDisplayName(self):
        r"""
        This function returns the user's external app display name.

        It is not called directly, but is called by a variable in the user object, "externalAppDisplayName".
        """

        resp = self.requests.get(f"https://users.roblox.com/v1/users/{self.id}")
        data = resp.json()
        return data['externalAppDisplayName']

    def get_hasVerifiedBadge(self):
        r"""
        This function returns whether the user has verified their badge or not.

        It is not called directly, but is called by a variable in the user object, "has_badge".
        """

        resp = self.requests.get(f"https://users.roblox.com/v1/users/{self.id}")
        data = resp.json()
        return data['hasVerifiedBadge']
    
    def get_displayName(self):
        r"""
        This function returns the user's display name.

        It is not called directly, but is called by a variable in the user object, "name".
        """

        resp = self.requests.get(f"https://users.roblox.com/v1/users/{self.id}")
        data = resp.json()
        return data['displayName']
    
    def get_username_history(self):
        r"""
        This function returns the user's username history.

        It is not called directly, but is called by a variable in the user object, "username_history".
        """

        __usernames__ = []
        resp = self.requests.get(f"https://users.roblox.com/v1/users/{self.id}/username-history")
        data = resp.json()
        for username in data['data']:
            __usernames__.append(username)
        self.requests.close()
        return __usernames__

    friends = property(get_friends)
    games = property(get_games)
    favorite_games = property(get_favorite_games)
    description = property(get_description)
    created = property(get_created)
    is_banned = property(get_is_banned)
    externalAppDisplayName = property(get_externalAppDisplayName)
    has_badge = property(get_hasVerifiedBadge)
    name = property(get_displayName)
    username_history = property(get_username_history)

    @unstable()
    def send(self, title: str, value: str, **kwargs):
        data = {
            "userId": self.bot.id,
            "subject": title,
            "body": value,
            "recipientId": self.id,
            "replyMessageId": kwargs.get('replyMessageId', None),
            "includePreviousMessage": kwargs.get('includePreviousMessage', False),
        }
        resp = self.requests.post(f"https://privatemessages.roblox.com/v1/messages/send", json=data)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Forbidden(resp.json()['errors'][0]['message'])

class Game:
    r"""
    This object representing a game on Roblox.
    
    Attributes:
    -----------
    id: <class 'int'>
        The game's id.
    name: <class 'str'>
        The game's name.
    description: <class 'str'>
        The game's description.
    sourceName:
        The game's source name.
    sourceDescription:
        The game's source description.
    creator: <class 'dict'>
        The game's creator.
    price: <class 'int'> or <class 'NoneType'>
        The game's price.
    allowedGearGenres: <class 'list'>
        The game's allowed gear genres.
    allowedGearCategories: <class 'list'>
        The game's allowed gear categories.
    isGenreEnforced: <class 'bool'>
        Whether the game's gear genre is enforced.
    copyingAllowed: <class 'bool'>
        Whether the game is allowed to be copied.
    playing: <class 'int'>
        The game's playing count.
    visits: <class 'int'>
        The game's visits.
    maxPlayers: <class 'int'>
        The game's max players.
    created: <class 'str'>
        The game's creation date.
    updated: <class 'str'>
        The game's update date.
    studioAccessToApisAllowed: <class 'bool'>
        Whether the game's studio is allowed to access the game's APIs.
    createVipServersAllowed: <class 'bool'>
        Whether the game's studio is allowed to create VIP servers.
    universeAvatarType: <class 'str'>
        The game's universe avatar type.
    genre: <class 'str'>
        The game's genre.
    isAllGenre: <class 'bool'>
        Whether the game's genre is all genre.
    isFavoriteByUser: <class 'bool'>
        Whether the game is favorited by the user.
    favoritedCount: <class 'int'>
        The game's favorited count.
    """

    def __init__(self, json: dict) -> None:
        self.json = json

    id = property(lambda self: self.json['id'])
    name = property(lambda self: self.json['name'])
    description = property(lambda self: self.json['description'])
    sourceName = property(lambda self: self.json['sourceName'])
    sourceDescription = property(lambda self: self.json['sourceDescription'])
    creator = property(lambda self: self.json['creator'])
    price = property(lambda self: self.json['price'])
    allowedGearGenres = property(lambda self: self.json['allowedGearGenres'])
    allowedGearCategories = property(lambda self: self.json['allowedGearCategories'])
    isGenreEnforced = property(lambda self: self.json['isGenreEnforced'])
    copyingAllowed = property(lambda self: self.json['copyingAllowed'])
    playing = property(lambda self: self.json['playing'])
    visits = property(lambda self: self.json['visits'])
    maxPlayers = property(lambda self: self.json['maxPlayers'])
    created = property(lambda self: self.json['created'])
    updated = property(lambda self: self.json['updated'])
    studioAccessToApisAllowed = property(lambda self: self.json['studioAccessToApisAllowed'])
    createVipServersAllowed = property(lambda self: self.json['createVipServersAllowed'])
    universeAvatarType = property(lambda self: self.json['universeAvatarType'])
    genre = property(lambda self: self.json['genre'])
    isAllGenre = property(lambda self: self.json['isAllGenre'])
    isFavoritedByUser = property(lambda self: self.json['isFavoritedByUser'])
    favoritedCount = property(lambda self: self.json['favoritedCount'])

    def __str__(self):
        r"""
        This function is called when the game is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        # The user object is now available.
        user = client.fetch_game(id=1) 

        # This will print the user's info.
        print(game) 

        client.login("roblosecurity")
        -----------

        >>> Game(id=1, name=test103120131046am's Place, description=, sourceName=test103120131046am's Place, sourceDescription=, creator={'id': 50655902, 'name': 'test103120131046am', 'type': 'User', 'isRNVAccount': False, 'hasVerifiedBadge': False}, price=None, allowedGearGenres=['All'], allowedGearCategories=[], isGenreEnforced=True, copyingAllowed=False, playing=0, visits=0, maxPlayers=10, created=2013-10-31T17:46:29.823Z, updated=2013-10-31T17:46:29.823Z, studioAccessToApisAllowed=False, createVipServersAllowed=False, universeAvatarType=MorphToR6, genre=All, isAllGenre=True, isFavoritedByUser=False, favoritedCount=31)

        """

        return f"Game(id={self.id}, name={self.name}, description={self.description}, sourceName={self.sourceName}, sourceDescription={self.sourceDescription}, creator={self.creator}, price={self.price}, allowedGearGenres={self.allowedGearGenres}, allowedGearCategories={self.allowedGearCategories}, isGenreEnforced={self.isGenreEnforced}, copyingAllowed={self.copyingAllowed}, playing={self.playing}, visits={self.visits}, maxPlayers={self.maxPlayers}, created={self.created}, updated={self.updated}, studioAccessToApisAllowed={self.studioAccessToApisAllowed}, createVipServersAllowed={self.createVipServersAllowed}, universeAvatarType={self.universeAvatarType}, genre={self.genre}, isAllGenre={self.isAllGenre}, isFavoritedByUser={self.isFavoritedByUser}, favoritedCount={self.favoritedCount})"

class Group:
    r"""
    This object represents a group on Roblox.

    Attributes:
    -----------
    id: <class 'int'>
        The group's id.
    name: <class 'str'>
        The group's name.
    description: <class 'str'>
        The group's description.
    owner: <class 'dict'>
        The group's owner.
    shout: <class 'str'> or <class 'NoneType'>
        The group's shout.
    member: <class 'int'>
        The group's member count.
    buildersClubOnly: <class 'bool'>
        Whether the group is builders club only.
    is_public: <class 'bool'>
        Whether the group is public.
    has_badge: <class 'bool'>
        Whether the group has a badge.
    games: <class 'list'>
        The group's games.
    wall_posts: <class 'list'>
        The group's wall posts.
    send: <class 'method'>
        Send a message in the group chat.
    get_roles: <class 'method'>
        Get someones roles in the group.
    """

    def __init__(self, json: dict) -> None:
        self.json = json
        self.requests = requests.Session()
    
    id = property(lambda self: self.json['id'])
    name = property(lambda self: self.json['name'])
    description = property(lambda self: self.json['description'])
    owner = property(lambda self: self.json['owner'])
    shout = property(lambda self: self.json['shout'])
    member = property(lambda self: self.json['memberCount'])
    buildersClubOnly = property(lambda self: self.json['isBuildersClubOnly'])
    is_public = property(lambda self: self.json['publicEntryAllowed'])
    has_badge = property(lambda self: self.json['hasVerifiedBadge'])

    def __str__(self):
        r"""
        This function is called when the group is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        # The user object is now available.
        user = client.fetch_group(id=1) 

        # This will print the user's info.
        print(group) 

        client.login("roblosecurity")
        -----------

        >>> Group(id=1, name=RobloHunks, description=, owner={'buildersClubMembershipType': 'None', 'hasVerifiedBadge': False, 'userId': 1179762, 'username': 'RobloTim', 'displayName': 'RobloTim'}, shout=None, member=42560, builderClubOnly=False, is_public=True, badge=False)

        """
        
        return f"Group(id={self.id}, name={self.name}, description={self.description}, owner={self.owner}, shout={self.shout}, member={self.member}, builderClubOnly={self.buildersClubOnly}, is_public={self.is_public}, badge={self.has_badge}, games={self.games}, wall_posts={self.wall_posts})"

    def get_games(self):
        __games__ = []
        resp = self.requests.get(f"https://games.roblox.com/v2/groups/{self.id}/games")
        data = resp.json()
        for game in data['data']:
            id = game['id']
            name = game['name']
            description = game['description']
            creator = game['creator']
            rootPlace = game['rootPlace']
            created = game['created']
            updated = game['updated']
            visits = game['placeVisits']
            game = {"id":id,"name":name,"description":description,"creator":creator,"rootPlace":rootPlace,"created":created,"updated":updated,"placeVisits": visits}
            __games__.append(game)
        self.requests.close()
        return __games__
    
    def get_wall_posts(self, limit: int = 10):
        __wall_posts__ = []
        try:
            resp = self.requests.get(f"https://groups.roblox.com/v2/groups/{self.id}/wall/posts?sortOrder=Desc&limit={limit}")
            if resp.status_code == 200:
                data = resp.json()
                for wall_post in data['data']:
                    post = wall_post
                    __wall_posts__.append(post)
                    self.requests.close()
                return __wall_posts__
            else:
                raise Forbidden(resp.json()['errors'][0]['message'])
        except KeyError:
            raise ValueError(f"Allowed values for the limit: 10, 25, 50, 100")

    def get_roles(self, _id: int):
        __roles__ = []
        resp = self.requests.get(f"https://groups.roblox.com/v2/users/{_id}/groups/roles")
        data = resp.json()
        for role in data['data']:
            group = role['group']
            role = {'data':group}
            __roles__.append(role)
        self.requests.close()
        return __roles__

    games = property(get_games)
    wall_posts = property(get_wall_posts)

    def send(self, message: str):
        data = {
            "body": message,
            "captchaId": "",
            "captchaToken": "None",
            "captchaProvider": "PROVIDER_ARKOSE_LABS"
        }
        resp = self.requests.post(f"https://groups.roblox.com/v2/groups/{self.id}/wall/posts", json=data)
        if resp.status_code == 200:
            self.requests.close()
            return resp.json()
        else:
            self.requests.close()
            raise Forbidden(resp.json()['errors'][0]['message'])

class Client(object):
    r"""
    This object will build the bot
    
    Attributes:
    -----------
    fetch_user: <class 'method'>
        Fetch a user from Roblox by id.
    fetch_game: <class 'method'>
        Fetch a game from Roblox by rootid.
    fetch_group: <class 'method'>
        Fetch a group from Roblox by id.
    get_user: <class 'method'>
        Get a user from Roblox by username.
    listen: <class 'method'>
        This method serves as an event on the bot.
    login: <class 'method'>
        Login to Roblox.
    """

    def __init__(self, email: str, username: str, password: str) -> None:
        self.email = email
        self.username = username
        self.password = password
        self.events = ["on_ready", "on_client_error"]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.requests = requests.Session()
        self.base_url = 'https://api.roblox.com'
        resp = self.requests.get(f'{self.base_url}/users/get-by-username?username={self.username}')
        data = resp.json()
        user = User(data, data)
        self.bot = user
    
    def __del__(self):
        asyncio.get_event_loop().run_until_complete(self.session.close())
    
    def fetch_user(self, id: int):
        r"""
        This function is called when the group is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        # The user object is now available.
        user = client.fetch_user(id=1)

        client.login("roblosecurity")
        """

        try:
            r = self.requests.get(f'{self.base_url}/users/{id}')
            return User(r.json(), self.bot)
        except KeyError:
            raise UserNotFound(f"User {id} does not exist.")
    
    def fetch_game(self, rootid: int):
        r"""
        This function is called when the group is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        # The user object is now available.
        user = client.fetch_game(id=1)

        client.login("roblosecurity")
        """

        try:
            r = self.requests.get(f'https://games.roblox.com/v1/games?universeIds={rootid}')
            data = r.json()
            return Game(data['data'][0])
        except KeyError:
            raise GameNotFound(f"Game {id} does not exist.")

    def fetch_group(self, id: int):
        r"""
        This function is called when the group is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        # The user object is now available.
        user = client.fetch_group(id=1)

        client.login("roblosecurity")
        """

        try:
            r = self.requests.get(f'https://groups.roblox.com/v1/groups/{id}')
            return Group(r.json())
        except KeyError:
            raise GroupNotFound(f"Group {id} does not exist.")
    
    def get_user(self, _name: str, limit: int = 10):
        r"""
        This function is called when the group is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        # The user object is now available.
        user = client.get_user(_name="Roblox", limit=10)

        client.login("roblosecurity")
        """

        try:
            _r = self.requests.get(f'https://users.roblox.com/v1/users/search?keyword={_name}&limit={limit}')
            __users__ = []
            data = _r.json()
            for user in data['data']:
                id = user['id']
                r = self.requests.get(f'{self.base_url}/users/{id}')
                user = User(r.json(), self.bot)
                __users__.append(user)
            self.requests.close()
            return __users__
        except KeyError:
            raise ValueError(f"Allowed values for the limit: 10, 25, 50, 100")

    def listen(self):
        r"""
        This function is called when the group is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        @client.listen()
        def on_ready(bot: roblox.User):
            print(f"{bot.username} is online!")

        client.login("roblosecurity")
        """

        def decorator(func):
            if asyncio.iscoroutinefunction(func):
                raise AsyncEvent(f'Unable to execute an asynchronous function. ({func.__name__})')
            for event in self.events:
                self.__setattr__(event, func)
            return func
        return decorator
    
    def login(self, roblosecurity: str):
        r"""
        This function is called when the group is printed.
        Like this:

        -----------
        import roblox

        client = roblox.Client(email="email@example.com", username="Example", password="Example")

        @client.listen()
        def on_ready(bot: roblox.User):
            print(f"{bot.username} is online!")

        client.login("roblosecurity")
        """

        async def login_async():
            cookies = {'.ROBLOSECURITY': roblosecurity}
            _session = requests.Session()
            _session.cookies[".ROBLOSECURITY"] = roblosecurity
            req = _session.post(url="https://auth.roblox.com/v2/logout")
            req.close()
            async with aiohttp.ClientSession(headers={"X-CSRF-TOKEN": req.headers["X-CSRF-Token"]}, cookies=cookies) as session:
                async with session.post('https://www.roblox.com/', data={"ctype": self.email, "cvalue": self.username, "password": self.password, "captchaToken": "None", "captchaProvider": "PROVIDER_ARKOSE_LABS"}) as resp:
                    if resp.status == 200:
                        for event in self.events:
                            if event == "on_ready":
                                try:
                                    self.__getattribute__(event)(self.bot)
                                except AttributeError:
                                    pass
                    else:
                        raise LoginError((await resp.json())['errors'][0]['message'])
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(login_async())
            loop.run_forever()
        except KeyboardInterrupt:
            loop.stop()
            loop.run_forever()
            loop.run_until_complete(self.session.close())
            raise Logout("Logged out.")

# made with ❤️ by @Artic#3065

# You can add the ArticBoat test robot to Roblox. (there may be surprises in the near future)