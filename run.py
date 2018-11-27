from game import *
import pandas as pd

ORDER = "maxmin"
EPOCH = 500

result = []
N_range = range(1,22)
random.seed(1);

for i in range (0,EPOCH):
    print(i)
    result_i = []
    for N in N_range:
        UNROLL_DEPTH = N
        board = game_constructor(N)
        scoring_master(board, ORDER)
        result_i.append(board.root().score())
    result.append(result_i)
    df = pd.DataFrame(result)
    df.to_csv("game_result.csv")
