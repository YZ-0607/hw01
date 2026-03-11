"""八皇后问题单元测试"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # 把项目根目录加入搜索路径
import unittest
from src.eight_queens import solve_n_queens

class TestEightQueens(unittest.TestCase):
    def test_n_queens_basic(self):
        # 4皇后有 2 组解
        self.assertEqual(len(solve_n_queens(4)), 2)
        # 8皇后有 92 组解
        self.assertEqual(len(solve_n_queens(8)), 92)

    def test_n_queens_edge_cases(self):
        self.assertEqual(len(solve_n_queens(1)), 1)  # 1皇后
        self.assertEqual(len(solve_n_queens(2)), 0)  # 2皇后无解
        self.assertEqual(len(solve_n_queens(3)), 0)  # 3皇后无解

    def test_solution_validity(self):
        """验证解的合法性：无冲突"""
        solutions = solve_n_queens(8)
        for sol in solutions[:5]:
            cols = set()
            diag1 = set()
            diag2 = set()
            for i, row in enumerate(sol):
                j = row.index("Q")
                self.assertNotIn(j, cols)
                self.assertNotIn(i - j, diag1)
                self.assertNotIn(i + j, diag2)
                cols.add(j)
                diag1.add(i - j)
                diag2.add(i + j)

if __name__ == "__main__":
    unittest.main()