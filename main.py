from flask import *
from logic import *

app = Flask(__name__)

loginManager = LoginManager()
gameManager = GameManager()



#LOGIN
@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def loginPage():
    if(request.cookies.get('id')):
        return redirect(url_for('home'))
  
    if(request.method == 'GET'):
        return(render_template('login.html', err = ''))

    elif(request.method == 'POST'):
        user = loginManager.login(request.form['name'], request.form['pass'])

        if(type(user) == User):
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('name', user.username)
            resp.set_cookie('id', str(user.id))
            return resp
        return render_template('login.html', err = user)


#REGISTER
@app.route('/register', methods = ['GET', 'POST'])
def registerPage():
    if(request.cookies.get('id')):
        return redirect(url_for('home'))

    if(request.method == 'GET'):
        return(render_template('register.html', err = ''))
        
    elif(request.method == 'POST'):
        user = loginManager.register(request.form['name'], request.form['pass'])
        if(type(user) == User):
            return redirect(url_for('loginPage'))
        return render_template('register.html', err = user)
    


@app.route('/home', methods=['GET', 'POST'])
def home():
    if(not request.cookies.get('id')):
        return redirect(url_for('loginPage'))
    
    if(request.method == "GET"):
        return render_template('home.html', name = request.cookies.get("name"), userId = int(request.cookies.get("id")), games = gameManager.games )
    
    elif(request.method == "POST"):
        logout = request.form.get('logout', 0)
        create = request.form.get('create', 0)
        delete = request.form.get('delete', -1)
        join = request.form.get('join', -1)
        userId = int(request.cookies.get('id'))
        if(logout):
            loginManager.logout(userId)
            resp = make_response(redirect(url_for('loginPage')))
            resp.delete_cookie("id")
            resp.delete_cookie("name")
            return resp
        
        elif(create):
            if(int(create) == 1): gameManager.createGame(userId)
            return redirect('home')

        elif(delete != -1):
            gameManager.deleteGame(userId, int(delete))
            return redirect('home')

        elif(join != -1):
            gameManager.joinGame(loginManager.getUserById(userId), int(join))
            return redirect('classic/%d' %(int(join)))

@app.route('/classic/<int:gameId>', methods=['GET', 'POST'])
def play(gameId):
    
    if(not request.cookies.get('id')):
        return redirect(url_for('loginPage'))
    if(request.method == 'GET'):
        game = gameManager.getGame(int(gameId))
        return render_template('classic.html', winner = None, board = game.board, players = game.players, name = request.cookies.get('name'))

    elif(request.method == 'POST'):
        logout = request.form.get('logout', 0)
        leave = request.form.get('leave', 0)
        tile = request.form.get('tile', -1)

        userId = int(request.cookies.get('id'))
        game = gameManager.getGame(int(gameId))
        if(logout):
            loginManager.logout(userId)
            resp = make_response(redirect(url_for('loginPage')))
            resp.delete_cookie("id")
            resp.delete_cookie("name")
            return resp
        if(leave):
            gameManager.leaveGame(loginManager.getUserById(userId), gameId)
            return redirect(url_for('home'))
        if(tile):
            game.checkTile(int(tile), loginManager.getUserById(userId))
            return redirect(url_for('play', gameId=gameId))
        
if(__name__ == '__main__'):
    app.run(debug=True, host='localhost', port=5000)