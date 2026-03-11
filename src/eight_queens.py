"""八皇后问题求解器（回溯法）"""
from typing import List, Set

def solve_n_queens(n: int) -> List[List[str]]:
    solutions = []
    board = [-1] * n  # 记录每行皇后的列位置

    def is_safe(row: int, col: int, diag1: Set[int], diag2: Set[int]) -> bool:
        """判断 (row, col) 能否放皇后"""
        return (row - col not in diag1 and
                row + col not in diag2 and
                col not in [board[i] for i in range(row)])

    def backtrack(row: int, diag1: Set[int], diag2: Set[int]) -> None:
        if row == n:
            # 生成棋盘字符串
            result = []
            for col in board:
                line = ["."] * n
                line[col] = "Q"
                result.append("".join(line))
            solutions.append(result)
            return

        for col in range(n):
            if is_safe(row, col, diag1, diag2):
                board[row] = col
                diag1.add(row - col)
                diag2.add(row + col)
                backtrack(row + 1, diag1, diag2)
                # 回溯
                diag1.remove(row - col)
                diag2.remove(row + col)
                board[row] = -1

    backtrack(0, set(), set())
    return solutions

if __name__ == "__main__":
    solutions = solve_n_queens(8)
    print(f"8皇后共有 {len(solutions)} 组解")