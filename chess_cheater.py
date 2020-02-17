import requests
import re

def get_current_games(username, password_hash):
    create_url = 'http://www.jeffcole.org/chessbymail/methods/getusergames.php'
    params = {
        'user':username,
        'pass':password_hash,
        'cache':'‭1580005118682‬',
        'year':'2020',
        'month':'2',
        'day':'17',
    }
    user_games = requests.get(create_url,params=params)
    pattern = r'Game id=\'(\d+)\' playerwhite=\'(\S+)\' playerblack=\'(\S+)\''
    games = re.findall(pattern, user_games.text)

    return games


def get_chess_params(username, password_hash):
    games = get_current_games(username, password_hash)
    game_id=0
    while game_id == 0:
        opponent = input("opponent name? ")
        for game in games:
            if game[1] == opponent or game[2] == opponent:
                game_id = game[0]
                print("got the game ID")        
    
    print("white moves go 0,2,4...")
    print("black moves go 1,3,5...")

    move_id = input("what move are you up to? ")
    if int(move_id) % 2 == 0:
        print("white pieces")
        isBlack = "false"
    else:
        print("black pieces")
        isBlack = "true"

    print('''
        p = pawn
        b = bishop
        r = rook
        n = knight
        q = queen
        k = king
    ''')
    piece = input("what piece are you moving?")

    print("if you get these positions wrong, you will corrupt the game and it will rollback to a previous move")
    print("positions are from 0-7: left-right, bottom-top if you are playing the white pieces")
    print("right-left, top-bottom if you are playing the black pieces")
    startRow = input("startRow: ")
    startCol = input("startCol: ")
    endRow = input("endRow: ")
    endCol = input("endCol: ")
    isCapturing="false"
    isCheckmate="false"
    isStalemate="false"
    drawAccepted="false"
    isPromoted="false"
    capturedPieceRow='-1'
    capturedPieceCol='-1'
    capturedPiece=""
    castleKingSide = "false"
    castleQueenSide ="false"
    isCheck = "false"
    promotedType="p"

    if (input("are you taking a piece?") == 'y'):
        isCapturing = "true"
        capturedPiece = input("what piece are you capturing?")
        capturedPieceRow = endRow
        capturedPieceCol = endCol

    if (input("are you promoting a piece?") == 'y'):
        isPromoted = "true"
        print('''
        p = pawn
        b = bishop
        r = rook
        n = knight
        q = queen
        k = king
        ''')
        promotedType=input("what piece do you want to promote into?")

    if (input("do you want to end the game this turn?") == 'y'):
        if(input("win by checkmate?") == 'y'):
            isCheckmate = "true"
        elif(input("win by stalemate?") == 'y'):
            isStalemate = "true"
        elif(input("win by enforced draw?") == 'y'):
            drawAccepted = "true"

    if (input("do you want to put them in check this turn?") == 'y'):
        isCheck = "true"

    params = {
        'user':username,
        'pass':password_hash,
        'gameID':'%s'%game_id,
        'moveID':'%s'%move_id,
        'piece':'%s'%piece,
        'isBlack':'%s'%isBlack,
        'startRow':'%s'%startRow,
        'startCol':'%s'%startCol,
        'endRow':'%s'%endRow,
        'endCol':'%s'%endCol,
        'isCapturing':'%s'%isCapturing,
        'capturedPiece':'%s'%capturedPiece,
        'capturedPieceRow':'%s'%capturedPieceRow,
        'capturedPieceCol':'%s'%capturedPieceCol,
        'isPromoting':'%s'%isPromoted,
        'promotedType':'%s'%promotedType,
        'enPassant':'false',
        'castleKingside':'%s'%castleKingSide,
        'castleQueenside':'%s'%castleQueenSide,
        'isCheck':'%s'%isCheck,
        'isCheckmate':'%s'%isCheckmate,
        'isStalemate':'%s'%isStalemate,
        'offerDraw':'false',
        'drawDenied':'false',
        'drawAccepted':'%s'%drawAccepted,
        'isResign':'false',
        'cache':'‭1580005118682‬'
    }
    return params


def create_game(username):
    create_url = 'http://www.jeffcole.org/chessbymail/methods/createrandomopponentgame.php'
    create_params = {
        'user':username,
        'cache':'1580021825117'
    }
    get_game = requests.get(create_url,params=create_params)
    print("created game")
    return(get_game.text)


def play_game(username, password_hash):
    params = get_chess_params(username, password_hash)
    url = 'http://www.jeffcole.org/chessbymail/methods/submitmove.php'
    r = requests.get(url, params=params)
    print(r.text)

    while(True):
        if (r.text != '<Success />'):
            if input("want to redo the move id?") == 'y':
                params['moveID'] = input("what move are you up to?")
                r = requests.get(url, params=params)
                print(r.text)
            else:
                break
        else:
            break

username = 'username here'
password_hash = 'md5 hash of your password here'

play_game(username, password_hash)
