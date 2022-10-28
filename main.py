import random

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

STARTING_POINT = (2, 0)
GOAL_POINT = (0, 3)

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
    
    def action_to_number(self, action):
        mapper = {
            (-1, 0): UP, (0, -1): LEFT, (1, 0): DOWN, (0, 1): RIGHT
        };
        return mapper[action]

    def number_to_action(self, number):
        mapper = {
            UP: (-1, 0),
            LEFT: (0, -1),
            RIGHT: (0, 1),
            DOWN: (1, 0)
        }
        return mapper[number]

    # state is the current position
    def generate_actions(self, state):
        actions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        res_actions = []
        r, c = state
        if self.arena[r][c] == WALL_SQ:
            return []
        for dr, dc in actions:
            hit_row_limit = (r + dr < 0) or (r + dr >= self.MAX_ROWS)
            hit_col_limit = (c + dc < 0) or (c + dc >= self.MAX_COLS)
            hit_wall = (not hit_row_limit) and (not hit_col_limit) and (self.arena[r + dr][c + dc] == WALL_SQ)
            if (not hit_row_limit) and (not hit_col_limit) and (not hit_wall):
                res_actions.append((dr, dc))
        return res_actions

    def generate_reward_table(self):
        for scol in range(self.MAX_COLS * self.MAX_ROWS):
            row, col = self.col_to_state(scol)
            actions = self.generate_actions((row, col))
            print(f"scol: {scol}, row: {row}, col: {col}, actions: {actions}")
            for i, a in enumerate(actions):
                dr, dc = a
                next_row, next_col = (row + dr, col + dc)
                
                if (self.arena[next_row][next_col] == STAR_SQ):
                    self.rtable[self.action_to_number(a)][scol] = -0.04 + 1
                elif (self.arena[next_row][next_col] == PATH_SQ):
                    self.rtable[self.action_to_number(a)][scol] = -0.04
                elif (self.arena[next_row][next_col] == BOMB_SQ):
                    self.rtable[self.action_to_number(a)][scol] = -0.04 - 1
                else:
                    raise Exception("UKNOWN SQUARE")

    # when action is applied to old state it will create a new state
    # and modify the q-table
    # past_experience + old_state + action => experience + new_state
    def eval_q(self, old_state, action, discount_factor):
        old_state_number = self.state_to_col(old_state)
        action_number = self.action_to_number(action)
        r, c = old_state
        dr, dc = action
        new_state = (r + dr, c + dc)
        new_state_number = self.state_to_col(new_state)
        learning_rate = 1
        current_value = self.qtable[action_number][old_state_number]
        move_reward = self.rtable[action_number][old_state_number]
        # q learning equation
        self.qtable[action_number][old_state_number] = round(current_value + learning_rate * (move_reward + discount_factor * max([self.qtable[a][new_state_number] for a in [UP, DOWN, LEFT, RIGHT]]) - current_value), 2)
    
    def action_number_to_probability(self, action_number):
        mapper = {
            UP: 0.75,
            RIGHT: 0.1,
            LEFT: 0.1,
            DOWN: 0.05,
        }
        return mapper[action_number]
    
    def action_number_to_string(self, action_number):
        mapper = {
            UP: "UP",
            RIGHT: "RIGHT",
            LEFT: "LEFT",
            DOWN: "DOWN",
        }
        return mapper[action_number]
    
    def fill_q_table(self, start_state, end_state):
        journeys = 1000
        for _ in range(journeys):
            current_state = start_state
            iterations = 10
            for _ in range(iterations):
                if current_state == end_state:
                    break
                actions = self.generate_actions(current_state)
                action = random.choices(population=actions, weights=[self.action_number_to_probability(self.action_to_number(a)) for a in actions], k=1)[0]
                
                self.eval_q(current_state, action, 0.9)

                r, c = current_state
                dr, dc = action
                current_state = (r + dr, c + dc)
    
    def generate_soln(self, start_state, end_state):
        print("--- solution ---")
        current_state = start_state
        max_steps = 10
        for _ in range(max_steps):
            if current_state == end_state:
                return
            current_state_number = self.state_to_col(current_state)
            action_numbers = list(map(self.action_to_number, self.generate_actions(current_state)))
            preferred_action = max([(self.qtable[a][current_state_number], a) for a in action_numbers])[1]
            print(self.action_number_to_string(preferred_action))
            r, c = current_state
            dr, dc = self.number_to_action(preferred_action)
            next_state = (r + dr, c + dc)
            current_state = next_state
        print("GOAL NOT REACHED WITHIN MAX STEPS")

def main():
    arena = Arena(arena=ARENA, starting_point=STARTING_POINT)
    arena.generate_reward_table()
    print("--- reward table ---")
    for row in arena.rtable:
        print(row)
    
    print("--- qtable before ---")
    for row in arena.qtable:
        print(row)
    
    arena.fill_q_table(STARTING_POINT, GOAL_POINT)
    print("--- qtable after ---")
    for row in arena.qtable:
        print(row)
    
    arena.generate_soln(STARTING_POINT, GOAL_POINT)
    pass

if __name__ == '__main__':
    main()