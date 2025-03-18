class ChessPiece:
    """Базовый класс для всех фигур в шахматах.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        symbol (str): Символ фигуры для отображения на доске (например, 'P' для белого пешки, 'p' для черного).
    """

    def __init__(self, color, symbol):
        """Инициализирует фигуру с указанным цветом и символом.

        Аргументы:
            color (str): Цвет фигуры ('white' или 'black').
            symbol (str): Символ фигуры для отображения.
        """
        self.color = color
        self.symbol = symbol

    def can_move(self, board, start, end):
        """Проверяет, может ли фигура переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией фигуры.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Raises:
            NotImplementedError: Этот метод должен быть реализован в подклассах.
        """
        raise NotImplementedError("Subclasses should implement this method")


class Pawn(ChessPiece):
    """Класс, представляющий пешку в шахматах.

    Атрибуты:
        color (str): Цвет пешки ('white' или 'black').
        symbol (str): Символ пешки ('P' для белой, 'p' для черной).
    """

    def __init__(self, color):
        """Инициализирует пешку с указанным цветом.

        Аргументы:
            color (str): Цвет пешки ('white' или 'black').
        """
        super().__init__(color, 'P' if color == 'white' else 'p')
        
    def can_move(self, board, start, end):
        """Проверяет, может ли пешка переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией пешки.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Пешка может двигаться вперед на одну клетку, на две клетки с начальной позиции,
            или атаковать по диагонали на одну клетку, если там фигура противника.
        """
        start_x, start_y = start
        end_x, end_y = end
        direction = 1 if self.color == 'white' else -1
        
        if start_x == end_x and end_y == start_y + direction and board[end_y][end_x] is None:
            return True
        
        if (start_x == end_x and 
            ((self.color == 'white' and start_y == 1) or (self.color == 'black' and start_y == 6)) and 
            end_y == start_y + 2 * direction and 
            board[end_y][end_x] is None and 
            board[start_y + direction][start_x] is None):  
            return True
        
        if abs(start_x - end_x) == 1 and end_y == start_y + direction and board[end_y][end_x] is not None and board[end_y][end_x].color != self.color:
            return True
        
        return False


class Rook(ChessPiece):
    """Класс, представляющий ладью в шахматах.

    Атрибуты:
        color (str): Цвет ладьи ('white' или 'black').
        symbol (str): Символ ладьи ('R' для белой, 'r' для черной).
    """

    def __init__(self, color):
        """Инициализирует ладью с указанным цветом.

        Аргументы:
            color (str): Цвет ладьи ('white' или 'black').
        """
        super().__init__(color, 'R' if color == 'white' else 'r')
    
    def can_move(self, board, start, end):
        """Проверяет, может ли ладья переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией ладьи.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Ладья может двигаться по вертикали или горизонтали, но путь должен быть свободен.
        """
        start_x, start_y = start
        end_x, end_y = end
        if start_x != end_x and start_y != end_y:
            return False
        if start_x == end_x:
            step = 1 if end_y > start_y else -1
            for y in range(start_y + step, end_y, step):
                if board[y][start_x] is not None:
                    return False
        else:
            step = 1 if end_x > start_x else -1
            for x in range(start_x + step, end_x, step):
                if board[start_y][x] is not None:
                    return False
        return True


class Knight(ChessPiece):
    """Класс, представляющий коня в шахматах.

    Атрибуты:
        color (str): Цвет коня ('white' или 'black').
        symbol (str): Символ коня ('N' для белого, 'n' для черного).
    """

    def __init__(self, color):
        """Инициализирует коня с указанным цветом.

        Аргументы:
            color (str): Цвет коня ('white' или 'black').
        """
        super().__init__(color, 'N' if color == 'white' else 'n')
    
    def can_move(self, board, start, end): 
        """Проверяет, может ли конь переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией коня.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Конь ходит буквой "L" (на 2 клетки в одном направлении и 1 в перпендикулярном).
        """
        dx, dy = abs(start[0] - end[0]), abs(start[1] - end[1])
        return (dx, dy) in [(2, 1), (1, 2)]


class Bishop(ChessPiece):
    """Класс, представляющий слона в шахматах.

    Атрибуты:
        color (str): Цвет слона ('white' или 'black').
        symbol (str): Символ слона ('B' для белого, 'b' для черного).
    """

    def __init__(self, color):
        """Инициализирует слона с указанным цветом.

        Аргументы:
            color (str): Цвет слона ('white' или 'black').
        """
        super().__init__(color, 'B' if color == 'white' else 'b')
    
    def can_move(self, board, start, end):
        """Проверяет, может ли слон переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией слона.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Слон движется по диагонали, путь должен быть свободен.
        """
        start_x, start_y = start
        end_x, end_y = end
        if abs(start_x - end_x) != abs(start_y - end_y):
            return False
        step_x = 1 if end_x > start_x else -1
        step_y = 1 if end_y > start_y else -1
        x, y = start_x + step_x, start_y + step_y
        while x != end_x and y != end_y:
            if board[y][x] is not None:
                return False
            x += step_x
            y += step_y
        return True


class Queen(ChessPiece):
    """Класс, представляющий ферзя в шахматах.

    Атрибуты:
        color (str): Цвет ферзя ('white' или 'black').
        symbol (str): Символ ферзя ('Q' для белого, 'q' для черного).
    """

    def __init__(self, color):
        """Инициализирует ферзя с указанным цветом.

        Аргументы:
            color (str): Цвет ферзя ('white' или 'black').
        """
        super().__init__(color, 'Q' if color == 'white' else 'q')
    
    def can_move(self, board, start, end):
        """Проверяет, может ли ферзь переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией ферзя.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Ферзь сочетает движения ладьи и слона (по вертикали, горизонтали и диагонали).
        """
        return Rook.can_move(self, board, start, end) or Bishop.can_move(self, board, start, end)


class King(ChessPiece):
    """Класс, представляющий короля в шахматах.

    Атрибуты:
        color (str): Цвет короля ('white' или 'black').
        symbol (str): Символ короля ('K' для белого, 'k' для черного).
    """

    def __init__(self, color):
        """Инициализирует короля с указанным цветом.

        Аргументы:
            color (str): Цвет короля ('white' или 'black').
        """
        super().__init__(color, 'K' if color == 'white' else 'k')
    
    def can_move(self, board, start, end):
        """Проверяет, может ли король переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией короля.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Король может двигаться на одну клетку в любом направлении.
        """
        dx, dy = abs(start[0] - end[0]), abs(start[1] - end[1])
        return max(dx, dy) == 1


class Whiterabbit(ChessPiece):
    """Класс, представляющий фигуру Белый Кролик в шахматах.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        symbol (str): Символ фигуры ('W' для белого, 'w' для черного).
    """

    def __init__(self, color):
        """Инициализирует Белого Кролика с указанным цветом.

        Аргументы:
            color (str): Цвет фигуры ('white' или 'black').
        """
        super().__init__(color, 'W' if color == 'white' else 'w')
    
    def can_move(self, board, start, end):
        """Проверяет, может ли Белый Кролик переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией фигуры.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Белый Кролик может двигаться ровно на 3 клетки по горизонтали, вертикали или диагонали,
            при условии, что путь свободен.
        """
        start_x, start_y = start
        end_x, end_y = end
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        
        # Может ходить только на 3 клетки по диагонали, вертикали или горизонтали
        if (dx == 3 and dy == 0) or (dx == 0 and dy == 3) or (dx == 3 and dy == 3):
            # Проверка, что на пути нет фигур
            step_x = (end_x - start_x) // 3
            step_y = (end_y - start_y) // 3
            x, y = start_x + step_x, start_y + step_y
            while x != end_x or y != end_y:
                if board[y][x] is not None:
                    return False
                x += step_x
                y += step_y
            return True
        return False


class KittyCheshire(ChessPiece):
    """Класс, представляющий фигуру Чеширский Кот в шахматах.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        symbol (str): Символ фигуры ('C' для белого, 'c' для черного, может измениться при захвате).
    """

    def __init__(self, color):
        """Инициализирует Чеширского Кота с указанным цветом.

        Аргументы:
            color (str): Цвет фигуры ('white' или 'black').
        """
        super().__init__(color, 'C' if color == 'white' else 'c')
    
    def can_move(self, board, start, end):
        """Проверяет, может ли Чеширский Кот переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией фигуры.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Чеширский Кот ходит как пешка, но при захвате фигуры противника принимает ее символ.
        """
        start_x, start_y = start
        end_x, end_y = end
        direction = 1 if self.color == 'white' else -1
        
        # Ходит как пешка
        if start_x == end_x and end_y == start_y + direction and board[end_y][end_x] is None:
            return True
        
        if (start_x == end_x and 
            ((self.color == 'white' and start_y == 1) or (self.color == 'black' and start_y == 6)) and 
            end_y == start_y + 2 * direction and 
            board[end_y][end_x] is None and 
            board[start_y + direction][start_x] is None):  
            return True
        
        if abs(start_x - end_x) == 1 and end_y == start_y + direction and board[end_y][end_x] is not None and board[end_y][end_x].color != self.color:
            # Превращается в фигуру, которую съела
            self.symbol = board[end_y][end_x].symbol
            return True
        
        return False


class AppleWhite(ChessPiece):
    """Класс, представляющий фигуру Белоснежка в шахматах.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
        symbol (str): Символ фигуры ('A' для белого, 'a' для черного).
        has_moved (bool): Флаг, указывающий, двигалась ли фигура.
    """

    def __init__(self, color):
        """Инициализирует Белоснежку с указанным цветом.

        Аргументы:
            color (str): Цвет фигуры ('white' или 'black').
        """
        super().__init__(color, 'A' if color == 'white' else 'a')
        self.has_moved = False
    
    def can_move(self, board, start, end):
        """Проверяет, может ли Белоснежка переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий шахматную доску.
            start (tuple): Кортеж (x, y) с начальной позицией фигуры.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Белоснежка может сделать только один ход за игру, на любую клетку,
            кроме той, где находится король.
        """
        if self.has_moved:
            return False
        
        start_x, start_y = start
        end_x, end_y = end
        
        # Может ходить на любое место, кроме клетки с королем
        target_piece = board[end_y][end_x]
        if isinstance(target_piece, King):
            return False
        
        self.has_moved = True
        return True


class ChessBoard:
    """Класс, представляющий шахматную доску.

    Атрибуты:
        board (list): Двумерный список (8x8), содержащий фигуры или None.
    """

    def __init__(self):
        """Инициализирует шахматную доску с начальной расстановкой фигур."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        """Настраивает начальную позицию фигур на доске.

        Расставляет стандартные шахматные фигуры и дополнительные фигуры (Белый Кролик, Чеширский кот, Белоснежка).
        """
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for x in range(8):
            self.board[1][x] = Pawn('white')
            self.board[6][x] = Pawn('black')
            self.board[0][x] = pieces[x]('white')
            self.board[7][x] = pieces[x]('black')
        
        # Здесь я расставляю доп фигуры.
        self.board[1][0] = Whiterabbit('white')  
        self.board[1][2] = KittyCheshire('white')  
        self.board[0][7] = AppleWhite('white')  
        self.board[6][7] = Whiterabbit('black')  
        self.board[6][5] = KittyCheshire('black')  
        self.board[7][0] = AppleWhite('black')  

    def display_board(self):
        """Отображает текущую доску в консоли.

        Использует нотацию с буквами (a-h) для столбцов и цифрами (1-8) для строк.
        Пустые клетки обозначаются точкой ('.'), фигуры — их символами.
        """
        print("  a b c d e f g h")
        for y in range(8):
            print(f"{8 - y} ", end="")
            for x in range(8):
                piece = self.board[y][x]
                if piece:
                    print(piece.symbol, end=" ")
                else:
                    print(".", end=" ")
            print(f"{8 - y}")
        print("  a b c d e f g h")

    def is_valid_move(self, start, end, current_turn):
        """Проверяет, является ли ход с позиции start на позицию end допустимым.

        Аргументы:
            start (tuple): Кортеж (x, y) с начальной позицией.
            end (tuple): Кортеж (x, y) с конечной позицией.
            current_turn (str): Цвет текущего игрока ('white' или 'black').

        Возвращает:
            bool: True, если ход допустим, иначе False.

        Примечания:
            Учитывает принадлежность фигуры текущему игроку, правила движения и шах после хода.
        """
        piece = self.board[start[1]][start[0]]
        if not piece or piece.color != current_turn:
            return False
        if not piece.can_move(self.board, start, end):
            return False
        # Проверка на шах после хода
        temp_board = [row[:] for row in self.board]
        temp_board[end[1]][end[0]] = temp_board[start[1]][start[0]]
        temp_board[start[1]][start[0]] = None
        if self.is_check(current_turn, temp_board):
            return False
        return True

    def is_check(self, color, board=None):
        """Проверяет, находится ли король указанного цвета под шахом.

        Аргументы:
            color (str): Цвет короля ('white' или 'black').
            board (list, optional): Двумерный список доски. Если None, используется текущая доска.

        Возвращает:
            bool: True, если король под шахом, иначе False.
        """
        if board is None:
            board = self.board
        king_pos = None
        for y in range(8):
            for x in range(8):
                piece = board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (x, y)
                    break
            if king_pos:
                break
        if not king_pos:
            return False
        for y in range(8):
            for x in range(8):
                piece = board[y][x]
                if piece and piece.color != color and piece.can_move(board, (x, y), king_pos):
                    return True
        return False

    def is_checkmate(self, color):
        """Проверяет, является ли положение мата для указанного цвета.

        Аргументы:
            color (str): Цвет короля ('white' или 'black').

        Возвращает:
            bool: True, если мат, иначе False.

        Примечания:
            Мат — это ситуация, когда король под шахом и нет возможных ходов для выхода из шаха.
        """
        if not self.is_check(color):
            return False
        # Проверка, есть ли ходы, чтобы уйти от шаха
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.color == color:
                    for dy in range(8):
                        for dx in range(8):
                            if self.is_valid_move((x, y), (dx, dy), color):
                                # Проверяем, уходит ли король из-под шаха
                                temp_board = [row[:] for row in self.board]
                                temp_board[dy][dx] = temp_board[y][x]
                                temp_board[y][x] = None
                                if not self.is_check(color, temp_board):
                                    return False
        return True

    def is_stalemate(self, color):
        """Проверяет, является ли положение пата для указанного цвета.

        Аргументы:
            color (str): Цвет игрока ('white' или 'black').

        Возвращает:
            bool: True, если пат, иначе False.

        Примечания:
            Пат — это ситуация, когда нет легальных ходов, но король не под шахом.
        """
        if self.is_check(color):
            return False
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.color == color:
                    for dy in range(8):
                        for dx in range(8):
                            if self.is_valid_move((x, y), (dx, dy), color):
                                return False
        return True

    def move_piece(self, start, end):
        """Выполняет ход фигуры с позиции start на позицию end.

        Аргументы:
            start (tuple): Кортеж (x, y) с начальной позицией.
            end (tuple): Кортеж (x, y) с конечной позицией.
        """
        start_x, start_y = start
        end_x, end_y = end
        piece = self.board[start_y][start_x]
        self.board[end_y][end_x] = piece
        self.board[start_y][start_x] = None


class ChessGame:
    """Класс, управляющий игрой в шахматы.

    Атрибуты:
        board (ChessBoard): Объект доски.
        current_turn (str): Цвет текущего игрока ('white' или 'black').
        move_history (list): Список ходов в формате нотации (например, 'a2 -> a4').
    """

    def __init__(self):
        """Инициализирует игру с начальной доской и ходом белых."""
        self.board = ChessBoard()
        self.current_turn = 'white'
        self.move_history = []

    def play(self):
        """Запускает игровой цикл.

        Игроки по очереди вводят начальную и конечную позиции.
        Проверяет шах, мат, пат и выполняет ходы.
        Завершает игру при мате или пате.
        """
        counter = 0
        while True:
            print(f"Ход {'белых' if self.current_turn == 'white' else 'черных'}")
            self.board.display_board()
            
            # Проверка на шах
            if self.board.is_check(self.current_turn):
                print(f"ШАХ! Король {'белых' if self.current_turn == 'white' else 'черных'} под угрозой.")
            
            # Проверка на мат
            if self.board.is_checkmate(self.current_turn):
                print(f"МАТ! {'Белые' if self.current_turn == 'white' else 'Черные'} проиграли.")
                break
            
            # Проверка на пат
            if self.board.is_stalemate(self.current_turn):
                print("Пат! Игра окончена вничью.")
                break
            
            start = input("Введите начальную позицию (например, 'a2'): ")
            end = input("Введите конечную позицию (например, 'a4'): ")
            
            start = self.notation_to_indices(start)
            end = self.notation_to_indices(end)
            
            if start is None or end is None:
                print("Некорректный ввод, попробуйте снова.")
                continue
            
            if self.board.is_valid_move(start, end, self.current_turn):
                self.board.move_piece(start, end)
                self.move_history.append(f"{self.indices_to_notation(start)} -> {self.indices_to_notation(end)}")
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                print("Ход выполнен")
                counter += 1
                print(f'Количество ходов: {counter}')
            else:
                print("Некорректный ход, попробуйте снова.")

    def notation_to_indices(self, notation):
        """Преобразует нотацию (например, 'a2') в индексы (x, y).

        Аргументы:
            notation (str): Строка вида 'a2', где 'a' — столбец, '2' — строка.

        Возвращает:
            tuple: Кортеж (x, y) или None, если нотация некорректна.
        """
        if len(notation) != 2:
            return None
        x = ord(notation[0]) - ord('a')
        y = 8 - int(notation[1])
        if 0 <= x < 8 and 0 <= y < 8:
            return (x, y)
        return None

    def indices_to_notation(self, indices):
        """Преобразует индексы (x, y) в нотацию (например, 'a2').

        Аргументы:
            indices (tuple): Кортеж (x, y) с координатами.

        Возвращает:
            str: Строка в нотации шахматной доски.
        """
        x, y = indices
        return f"{chr(ord('a') + x)}{8 - y}"


if __name__ == "__main__":
    """Запускает игру в шахматы с дополнительными фигурами."""
    game = ChessGame()
    game.play()
