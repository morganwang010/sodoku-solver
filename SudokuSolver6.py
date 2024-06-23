import numpy as np


# 检验数字 n 是否能填在(y,x)位置
def is_valid(board, row, col, num):
    # 检查行
    for i in range(6):
        if board[row][i] == num:
            return False

    # 检查列
    for i in range(6):
        if board[i][col] == num:
            return False

    # 检查2x3子网格
    start_row, start_col = 2 * (row // 2), 3 * (col // 3)
    for i in range(2):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve6(board):
    for row in range(6):
        for col in range(6):
            if board[row][col] == 0:
                for num in range(1, 7):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve6(board):
                            return True
                        board[row][col] = 0
                return False
    return True


# # 测试
# grid = [[0, 6, 0, 7, 0, 9, 0, 4, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0],
#         [0, 0, 7, 4, 0, 0, 9, 0, 8],
#         [3, 0, 0, 0, 0, 0, 5, 0, 4],
#         [0, 4, 0, 0, 0, 0, 0, 9, 0],
#         [1, 0, 9, 0, 0, 0, 0, 0, 2],
#         [8, 0, 1, 0, 0, 4, 7, 0, 0],
#         [0, 0, 0, 0, 2, 0, 0, 0, 0],
#         [0, 2, 0, 9, 0, 6, 0, 5, 0]]

# grid = [[6, 2, 0, 5, 0, 3],
#         [0, 0, 0, 0, 0, 0],
#         [5, 0, 0, 0, 3, 0],
#         [0, 6, 0, 0, 2, 0],
#         [0, 0, 0, 3, 4, 6],
#         [3, 0, 6, 0, 0, 0]]
# print(np.matrix(solve6(grid)))
