
WALL = "WALL"
PATH = "PATH"
STAR = "STAR"
BOMB = "BOMB"

WALL_SQ = (WALL, 0)
PATH_SQ = (PATH, -0.04)
STAR_SQ = (STAR, 1)
BOMB_SQ = (BOMB, -1)

ARENA = [
    [PATH_SQ, PATH_SQ, PATH_SQ, STAR_SQ],
    [PATH_SQ, WALL_SQ, PATH_SQ, BOMB_SQ],
    [PATH_SQ, PATH_SQ, PATH_SQ, PATH_SQ],
]

DOWN = 0
LEFT = 1
UP = 2
RIGHT = 3

STARTING_POINT = (3, 0)

class Arena:

    def __init__(self, arena, starting_point):
        self.arena = arena
        self.starting_point = starting_point
        self.ACTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.MAX_ACTIONS = len(self.ACTIONS)
        self.MAX_COLS = len(arena[0])
        self.MAX_ROWS = len(arena)
        # columns are the states
        self.qtable = [[0 for _ in range(self.MAX_COLS * self.MAX_ROWS)] for _ in range(self.MAX_ACTIONS)]
        self.rtable = [[0 for _ in range(self.MAX_COLS * self.MAX_ROWS)] for _ in range(self.MAX_ACTIONS)]


    def state_to_col(self, state) -> int:
        mp = {
            (0, 0): 0,
            (0, 1): 1,
            (0, 2): 2,
            (0, 3): 3,
            (1, 0): 4,
            (1, 1): 5,
            (1, 2): 6,
            (1, 3): 7,
            (2, 0): 8,
            (2, 1): 9,
            (2, 2): 10,
            (2, 3): 11,
        }
        return mp[state]
    
    def col_to_state(self, col):
        mp = dict()
        s = 0
        for i in range(self.MAX_ROWS):
            for j in range(self.MAX_COLS):
                mp[s] = (i, j)
                s += 1
        return mp[col]

    # state is the current position
    def generate_actions(self, state):
        actions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        res_actions = []
        r, c = state
        for dr, dc in actions:
            hit_row_limit = (r + dr < 0) or (r + dr >= self.MAX_ROWS)
            hit_col_limit = (c + dc < 0) or (c + dc >= self.MAX_COLS)
            hit_wall = self.arena[r + dr][c + dc] == WALL_SQ
            if (not hit_row_limit) or (not hit_col_limit) or (not hit_wall):
                res_actions.append(actions)
        return res_actions

    def generate_reward_table(self):
        for scol in range(self.MAX_COLS * self.MAX_ROWS):
            row, col = self.col_to_state(scol)
            actions = self.generate_actions((row, col))
            for i, a in enumerate(actions):
                dr, dc = a
                next_row, next_col = (row + dr, col + dc)
                if (self.arena[next_row][next_col] == STAR_SQ):
                    pass
                    # self.rtable[self.state_to_col(scol)][i] = 


                

    # old state is represented by the row column position
    # new state is represented by the row colum position in the arena
    def eval_q(self, old_state, new_state):
        row_old, col_old = old_state
        row_new, col_new = new_state
    
    def fill_q_table():
        pass

