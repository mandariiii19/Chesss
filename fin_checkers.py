class CheckersPiece:
    """Базовый класс для фишек в шашках.

    Атрибуты:
        color (str): Цвет фишки ('white' или 'black').
        is_king (bool): Флаг, указывающий, является ли фишка дамкой (по умолчанию False).
        symbol (str): Символ фишки для отображения ('K' для дамки, 'W' для белой, 'B' для черной).
    """

    def __init__(self, color, is_king=False):
        """Инициализирует шашку с указанным цветом и статусом дамки.

        Аргументы:
            color (str): Цвет фишки ('white' или 'black').
            is_king (bool, optional): Статус дамки, по умолчанию False.
        """
        self.color = color
        self.is_king = is_king
        self.symbol = 'K' if is_king else ('W' if color == 'white' else 'B')

    def can_move(self, board, start, end):
        """Проверяет, может ли фишка переместиться с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий доску шашек.
            start (tuple): Кортеж (x, y) с начальной позицией фишки.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Примечания:
            Обычная фишка движется вперед по диагонали на одну клетку.
            Дамка может двигаться в любом направлении на одну клетку.
        """
        start_x, start_y = start
        end_x, end_y = end
        direction = 1 if self.color == 'black' else -1
        
        if (end_x + end_y) % 2 != 1:
            return False

        if abs(start_x - end_x) == 1:
            if self.is_king and abs(start_y - end_y) == 1:
                return True
            elif end_y == start_y + direction:
                return True
    
        return False

    def can_capture(self, board, start, end):
        """Проверяет, может ли фишка захватить другую с позиции start на позицию end.

        Аргументы:
            board (list): Двумерный список (8x8), представляющий доску шашек.
            start (tuple): Кортеж (x, y) с начальной позицией фишки.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Возвращает:
            bool: True, если захват возможен, иначе False.

        Примечания:
            Захват возможен, если фишка прыгает через фигуру противника на расстояние двух клеток
            по диагонали, и конечная клетка пуста.
        """
        start_x, start_y = start
        end_x, end_y = end
        direction = 1 if self.color == 'black' else -1

        if (end_x + end_y) % 2 != 1: 
            return False

        if abs(start_x - end_x) == 2 and abs(start_y - end_y) == 2:
            mid_x, mid_y = (start_x + end_x) // 2, (start_y + end_y) // 2
            if board[mid_y][mid_x] is not None and board[mid_y][mid_x].color != self.color and board[end_y][end_x] is None:
                return True
        
        return False


class CheckersBoard:
    """Класс, представляющий доску для игры в шашки.

    Атрибуты:
        board (list): Двумерный список (8x8), содержащий фишки или None.
    """

    def __init__(self):
        """Инициализирует доску с начальной расстановкой шашек."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        """Настраивает начальную позицию шашек на доске.

        Расставляет черные фишки на первых трех рядах (0-2) и белые на последних трех (5-7),
        только на черных клетках (где x + y нечетно).
        """
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 == 1:
                    self.board[y][x] = CheckersPiece('black')
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 == 1:
                    self.board[y][x] = CheckersPiece('white')

    def display_board(self):
        """Отображает текущую доску в консоли.

        Использует нотацию с буквами (a-h) для столбцов и цифрами (1-8) для строк.
        Пустые клетки обозначаются точкой ('.'), фишки — их символами (W, B, K).
        """
        print("  a b c d e f g h")
        for y in range(8):
            print(f"{8 - y}", end="")
            for x in range(8):
                piece = self.board[y][x]
                print(piece.symbol if piece else '.', end=" ")
            print(f"{8 - y}")
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        """Выполняет ход фишки с позиции start на позицию end.

        Аргументы:
            start (tuple): Кортеж (x, y) с начальной позицией.
            end (tuple): Кортеж (x, y) с конечной позицией.

        Примечания:
            Превращает фишку в дамку, если она достигла конца доски.
            Удаляет захваченную фигуру, если ход был прыжком.
        """
        start_x, start_y = start
        end_x, end_y = end
        piece = self.board[start_y][start_x]
        self.board[end_y][end_x] = piece
        self.board[start_y][start_x] = None

        if (piece.color == 'white' and end_y == 0) or (piece.color == 'black' and end_y == 7):
            piece.is_king = True
            piece.symbol = 'K'

        if abs(start_x - end_x) == 2:
            mid_x, mid_y = (start_x + end_x) // 2, (start_y + end_y) // 2
            self.board[mid_y][mid_x] = None


class CheckersGame:
    """Класс, управляющий игрой в шашки.

    Атрибуты:
        board (CheckersBoard): Объект доски.
        current_turn (str): Цвет текущего игрока ('white' или 'black').
    """

    def __init__(self):
        """Инициализирует игру с начальной доской и ходом белых."""
        self.board = CheckersBoard()
        self.current_turn = 'white'

    def play(self):
        """Запускает игровой цикл.

        Игроки по очереди вводят начальную и конечную позиции.
        Проверяет обязательные прыжки, шах и выполняет ходы.
        Завершает игру при мате или пате (не реализовано).
        """
        counter = 0
        while True:
            print(f"Ход {'белых' if self.current_turn == 'white' else 'черных'}")
            self.board.display_board()

            mandatory_captures = self.get_mandatory_captures()
            if mandatory_captures:
                print("Обязательные прыжки:")
                for start, end in mandatory_captures:
                    print(f"{self.indices_to_notation(start)} -> {self.indices_to_notation(end)}")
            
            start = input("Введите начальную позицию (например, 'c3'): ")
            end = input("Введите конечную позицию (например, 'd4'): ")
            
            start = self.notation_to_indices(start)
            end = self.notation_to_indices(end)
            
            if start is None or end is None:
                print("Некорректный ввод, попробуйте снова.")
                continue
            
            piece = self.board.board[start[1]][start[0]]
            if not piece or piece.color != self.current_turn:
                print("Некорректный ход, попробуйте снова.")
                continue
 
            if mandatory_captures and (start, end) not in mandatory_captures:
                print("Вы должны выполнить обязательный прыжок.")
                continue
            
            if piece.can_capture(self.board.board, start, end):
                self.board.move_piece(start, end)
                if self.has_additional_jump(end):
                    print("Вы можете продолжить прыжок.")
                else:
                    self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                print("Ход выполнен")
                counter += 1
                print(f'Количество ходов: {counter}')
            elif piece.can_move(self.board.board, start, end) and not mandatory_captures:
                self.board.move_piece(start, end)
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                print("Ход выполнен")
                counter += 1
                print(f'Количество ходов: {counter}')
            else:
                print("Некорректный ход, попробуйте снова.")

    def notation_to_indices(self, notation):
        """Преобразует нотацию (например, 'c3') в индексы (x, y).

        Аргументы:
            notation (str): Строка вида 'c3', где 'c' — столбец, '3' — строка.

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
        """Преобразует индексы (x, y) в нотацию (например, 'c3').

        Аргументы:
            indices (tuple): Кортеж (x, y) с координатами.

        Возвращает:
            str: Строка в нотации шашек.
        """
        x, y = indices
        return f"{chr(ord('a') + x)}{8 - y}"

    def has_additional_jump(self, position):
        """Проверяет, есть ли у фишки дополнительные прыжки с позиции position.

        Аргументы:
            position (tuple): Кортеж (x, y) с текущей позицией фишки.

        Возвращает:
            bool: True, если есть дополнительные прыжки, иначе False.
        """
        x, y = position
        piece = self.board.board[y][x]
        if not piece:
            return False
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            mid_x, mid_y = x + dx // 2, y + dy // 2
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                if self.board.board[new_y][new_x] is None and self.board.board[mid_y][mid_x] is not None and self.board.board[mid_y][mid_x].color != piece.color:
                    return True
        return False

    def get_mandatory_captures(self):
        """Возвращает список обязательных прыжков для текущего игрока.

        Возвращает:
            list: Список кортежей ((start_x, start_y), (end_x, end_y)) с возможными захватами.

        Примечания:
            В шашках обязательны прыжки, если они возможны.
        """
        captures = []
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece.color == self.current_turn:
                    for dx, dy in [(2, 2), (2, -2), (-2, 2), (-2, -2)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8:
                            if piece.can_capture(self.board.board, (x, y), (new_x, new_y)):
                                captures.append(((x, y), (new_x, new_y)))
        return captures

if __name__ == "__main__":
    """Запускает игру в шашки."""
    game = CheckersGame()
    game.play()