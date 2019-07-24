class GAME:
    def __init__(self):
        self.board = [['-' for x in range(4)],['-' for x in range(4)],['-' for x in range(4)],['-' for x in range(4)],['-' for x in range(4)],['-' for x in range(4)]]
        self.lastmoves = []
        self.winner = None
        self.print_board()

    def print_board(self):
        c = 0
        for i in range(3):
            print("|", end="")
            for j in range(4):
                c = c + 1
                if self.board[i][j] == '-':
                    st = str(i) + "," + str(j)
                    print("\t%s\t|" %st, end="")
                else:
                    print("\t%s\t|" %self.board[i][j], end="")
            print("\n", end="")
    
    def revert_last_move(self):
        (i,j) = self.lastmoves.pop()
        self.board[i][j] = '-'
        self.winner = None

    def is_game_over(self, i, j):
        isOver = False
        count = 0
        checkMarker = self.board[i][j]

        col_list = self.get_column_list(i, j)

        if self.check_four(col_list, checkMarker):
            self.winner = checkMarker
            return True

        #row
        row_list = self.get_row_list(i, j)
        

        if self.check_four(row_list, checkMarker):
            self.winner = checkMarker
            return True

        #leftdiagnol
        left_list = self.get_left_diagnol(i, j)

        if self.check_four(left_list, checkMarker):
            self.winner = checkMarker
            return True

        #rightdiagnol
        right_list = self.get_right_diagnol(i, j)

        if self.check_four(right_list, checkMarker):
            self.winner = checkMarker
            return True

        return False

    def get_column_list(self, i, j):
        row_list = []
        for x in range(3):
            row_list.append(self.board[x][j])
        return row_list

    def get_row_list(self, i, j):
        col_list = []
        for x in range(4):
            col_list.append(self.board[i][x])
        return col_list

    def get_left_diagnol(self, i, j):
        left_list = []
        a = i
        b = j
        while a > 0 and b > 0:
            left_list.append(self.board[a][b])
            a = a - 1
            b = b - 1

        a = a + 1
        b = b + 1
        while a < 3 and b < 4:
            left_list.append(self.board[a][b])
            a = a + 1
            b = b + 1
        return left_list

    def get_right_diagnol(self, i, j):
        right_list = []
        a = i
        b = j
        while a > 0 and b < 4:
            right_list.append(self.board[a][b])
            a = a - 1
            b = b + 1

        a = a + 1
        b = b - 1
        while a < 3 and b > 0:
            right_list.append(self.board[a][b])
            a = a + 1
            b = b - 1
        return right_list

    def get_possible_moves(self):
        moves = []
        for x in range(3):
            for y in range(4):
                if self.board[x][y] == '-':
                    if x == 2 or self.board[x + 1][y] != "-":
                        moves.append((x,y))
        return moves

    def mark(self, marker, i, j):
        self.board[i][j] = marker
        self.lastmoves.append((i,j))

    def check_four(self, lists, marker):
        for x in range(len(lists)):
            if lists[x] == marker:
                count = 0
                for y in range(x, len(lists)):
                    if lists[y] != marker:
                        break
                    count = count + 1
                if count == 3:
                    return True
                else:
                    count = 0
        return False

    def play(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        for i in range(42):
            self.print_board()
            if i%2 == 0:
                if self.p1.type == 'H':
                    print("\t\t[Human's Move]")
                else:
                    print("\t\t[Computer's Move]")
                mi, mj = self.p1.move(self)
            else:
                if self.p2.type == 'H':
                    print("\t\t[Human's Move]")
                else:
                    print("\t\t[Computer's Move]")
                mi, mj = self.p2.move(self)

            if self.is_game_over(mi, mj):
                self.print_board()
                if self.winner == '-':
                    print("Tie Game!")
                else:
                    print("\nWinner : %s" %self.winner)
                return

class Human:
    def __init__(self, marker):
        self.marker = marker
        self.type = 'H'

    def move(self, gameinstance):

        while True:
            mi = input("Input position I:")
            mj = input("Input position J:")
            try:
                mi =  int(mi)
                mj = int(mj)
            except:
                print("Input Number")

            if (mi,mj) not in gameinstance.get_possible_moves():
                print("Inavlid Move")
            else:
                break
        gameinstance.mark(self.marker, mi, mj)
        return mi, mj

class AI:
    def __init__(self, marker):
        self.marker = marker
        self.type = 'C'
        if self.marker == 'R':
            self.opponentmarker = 'B'
        else:
            self.opponentmarker = 'R'

    def move(self, gameinstance):
        mi, mj, score = self.maximized_move(gameinstance)
        gameinstance.mark(self.marker, mi, mj)
        return mi, mj

    def maximized_move(self, gameinstance):
        bestscore = None
        bestMovei = None
        bestMovej = None

        for mi, mj in gameinstance.get_possible_moves():
            gameinstance.mark(self.marker, mi, mj)

            if gameinstance.is_game_over(mi, mj):
                score = self.get_score(gameinstance, mi, mj)
            else:
                move_positioni, move_positionj, score = self.minimized_move(gameinstance)

            gameinstance.revert_last_move()

            if bestscore == None or bestscore < score:
                bestscore = score
                bestMovei = mi
                bestMovej = mj
        return bestMovei, bestMovej, bestscore
    def minimized_move(self, gameinstance):
        bestscore = None
        bestMovei = None
        bestMovej = None
        for mi, mj in gameinstance.get_possible_moves():
            gameinstance.mark(self.opponentmarker, mi, mj)

            if gameinstance.is_game_over(mi, mj):
                score = self.get_score(gameinstance, mi, mj)
                print("Score Here From Max " + str(score))
            else:
                move_positioni, move_positionj, score = self.maximized_move(gameinstance)

            gameinstance.revert_last_move()

            if bestscore == None or bestscore > score:
                bestscore = score
                bestMovei = mi
                bestMovej = mj
        return bestMovei, bestMovej, bestscore

    def get_score(self, gameinstance, i, j):
        if gameinstance.is_game_over(i, j):
            if gameinstance.winner == self.marker:
                return 1

            elif gameinstance.winner == self.opponentmarker:
                return -1

        return 0

if __name__ == '__main__':
    game = GAME()
    player1 = Human("R")
    player2 = AI("B")
    # n = random.randint(0,2)
    # if n == 1:    
    #     game.play(player2, player1)
    # else:
    game.play(player1, player2)
    # print(game.get_possible_moves())
    # list123 = ['A', '-', '-', '-', '-']
    # print(game.check_four(list123, 'A'))