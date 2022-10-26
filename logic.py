class User:
    def __init__(self, id, username:str, password:str):
        self.id = id
        self.username = username
        self.password = password

class LoginManager:

    def __init__(self):
        self.users = []
        self.session = []
        self.userNum = len(self.users)
    
    def getUser(self, username):
        if(self.users): 
            user = [user for user in self.users if user.username == username]
            if(user): return user[0]
            else: return None

    def getUserById(self, id):
        if(self.users): 
            user = [user for user in self.users if user.id == id]
            if(user): return user[0]
            else: return None
    
    def login(self, username, password):
        user = self.getUser(username)
        if(type(user) == User):
            if(user.password == password):
                self.session.append(user)
                return user
        return "Invalid login credentials"
    
    def logout(self, userId):
        user = self.getUserById(userId)
        self.session.remove(user)
        
    def register(self, username, password):
        if(not len(username) > 0 or not len(password) > 0): return "Invalid data"
        
        elif (type(self.getUser(username)) != User):
            user = User(self.userNum, username, password)
            self.userNum += 1
            self.users.append(user)
            return user
        return "User already registered!"

class Game:
    def __init__(self, id, ownerId):
        self.id = id
        self.owner = ownerId
        self.players = []
        self.active = False
        self.mode = "classic"
        self.board = self.generateBoard()
        self.last = None
        

    def generateBoard(self):
        if(self.mode == "classic"):
            board = []
            for i in range(9):
                board.append(-1)
            return board

    def winCheck(self):
        rows = self.checkRows()
        if(rows): return rows 
        cols = self.checkColumns()
        if(cols): return cols
        diags = self.checkDiagonals()
        if(diags): return diags
        return
    
    def checkRows(self):
        rows = 3
        for i in range(rows):
            p1 = True
            p2 = True
            for j in range(rows):
                if (not self.board[j + rows*i] == self.players[0].id): p1 = False
                if (not self.board[j + rows*i] == self.players[1].id): p2 = False
                if (not p1 and not p2): break
            if(p1) : return self.players[0].id
            if(p2) : return self.players[1].id
                
        return
    
    def checkColumns(self):
        cols = 3
        for i in range(cols):
            p1 = True
            p2 = True
            for j in range(cols):
                if(not self.board[j*cols + i] == self.players[0].id): p1 = False
                if(not self.board[j*cols + i] == self.players[1].id): p2 = False
                if(not p1 and not p2): break
            if(p1) : return self.players[0].id
            if(p2) : return self.players[1].id
                
        return
        
    def checkDiagonals(self):
        rows = 3
        p1 = True
        p2 = True
        for i in range(rows):
            if(not self.board[rows*(i+1)-i-1] == self.players[0].id): p1 = False
            if(not self.board[rows*(i+1)-i-1] == self.players[1].id): p2 = False
            if(not p1 and not p2): break
        if(p1) : return self.players[0].id
        if(p2) : return self.players[1].id
            
        p1 = True
        p2 = True
        for i in range(rows):
            if(not self.board[2*i*(rows-1)] == self.players[0].id): p1 = False
            if(not self.board[2*i*(rows-1)] == self.players[1].id): p2 = False
        
        if(p1) : return self.players[0].id
        if(p2) : return self.players[1].id 
          
        return

    def addPlayer(self, user):
        self.players.append(user)
        self.active = True

    def removePlayer(self, user):
        self.players.remove(user)
        if(len(self.players) == 0): self.active = False

    def checkTile(self, tile, user):
        if(self.last == None or self.last == self.players[1]):
            if(user == self.players[0]):
                self.board[int(tile)] = user.id
                winner = self.winCheck()
                self.last = user
                if(winner): return self.last
        elif(self.last == self.players[0]):
            if(user == self.players[1]):
                self.board[int(tile)] = user.id
                winner = self.winCheck()
                self.last = user
                if(winner): return self.last
        if(not any(e == -1 for e in self.board)): return "Draw"
                   

class GameManager:
    
    def __init__(self):
        self.games = []
        self.numGames = 0
        
    def createGame(self, ownerId):
        gameId = self.numGames
        self.numGames += 1
        self.games.append(Game(gameId, ownerId))

    def getGame(self, gameId):
        return [game for game in self.games if game.id == gameId][0]
        
    def deleteGame(self, userId, gameId):
        game = self.getGame(int(gameId))
        if(game.owner == userId and not game.active):
            self.games.remove(game)
            
    def joinGame(self, user, gameId):
        game = self.getGame(gameId)
        game.addPlayer(user)
        
    def leaveGame(self, user, gameId):
        game = self.getGame(gameId)
        game.removePlayer(user)
