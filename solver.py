import random

BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

def dummy(r,c,val,b):
    pass

def generate_board(diff):
    for r in range(9):
        for c in range(9):
            BOARD[r][c] = 0
    solve(dummy,True,True)
    d = {"Easy": (15,25), "Medium": (35, 50), "Hard":(55,70)}
    num = d[diff]
    for i in range(random.randint(num[0],num[1])):
       index = random.randint(0,80)
       BOARD[index//9][index%9] = 0



def get_peers_cords(r,c):
    peers = set()
    for i in range(9):
        if i != c:
            peers.add((r, i))
        if i != r:
            peers.add((i, c))

    box_r = (r // 3) * 3
    box_c = (c // 3) * 3
    for i in range(box_r,box_r+3):
        for j in range(box_c,box_c+3):
            if i == r and j == c: continue
            peers.add((i,j))
    return peers

def get_peers_values(peers:set[(int,int)]):
    vals = set()
    while peers:
        r,c = peers.pop()
        vals.add(BOARD[r][c])
    return vals

def print_board():
    for row in BOARD:
        print(row)

def get_domains():
    domains = [[set() for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            if BOARD[row][col] != 0:
                domains[row][col] = {BOARD[row][col]}
            else:
                domains[row][col] = {1,2,3,4,5,6,7,8,9}.difference(get_peers_values(get_peers_cords(row,col)))
    return domains

def find_MRV(domains:list[list[set]]):
    minIndex = [-1,-1]
    minVal = 10
    for row in range(9):
        for col in range(9):
            if BOARD[row][col] == 0 and minVal > len(domains[row][col]):
                minIndex = [row,col]
                minVal = len(domains[row][col])
    return minIndex

def find_next(domains:list[list[set]]):
    for row in range(9):
        for col in range(9):
            if BOARD[row][col] == 0:
                return row,col
    return [-1,-1]

def forward_check(domains:list[list[set]], r, c, val):
    domains = [[col.copy() for col in row] for row in domains]
    peers = get_peers_cords(r,c)
    for cell in peers:
        pr, pc = cell
        if BOARD[pr][pc] == 0:
            domains[pr][pc].discard(val)
            if len(domains[pr][pc]) == 0:
                return None
    return domains

def backtrack(domains,updatecell:callable,mrv):
    if mrv:
        row, col = find_MRV(domains)
    else:
        row, col = find_next(domains)
    if row == -1:
        return True
    
    for val in {1,2,3,4,5,6,7,8,9}.difference(get_peers_values(get_peers_cords(row, col))):
        BOARD[row][col] = val
        updatecell(row, col, val, False)
        new_domains = get_domains()
        if backtrack(new_domains, updatecell, mrv):
            return True
        BOARD[row][col] = 0
        updatecell(row, col, 0, True)
    return None
    

    

def fcbacktrack(domains,updatecell:callable,mrv):
    if mrv:
        row, col = find_MRV(domains)
    else:
        row, col = find_next(domains)
    if row == -1:
        return True

    for val in domains[row][col]:
        BOARD[row][col] = val
        updatecell(row,col,val,False)

        new_domains = forward_check(domains, row, col, val)
        if new_domains is not None:
            if fcbacktrack(new_domains, updatecell,mrv):
               return True
        BOARD[row][col] = 0
        updatecell(row,col,0,True)
    return None


def solve(updatecell:callable,fc,mrv):
    domains = get_domains()
    if fc:
        return fcbacktrack(domains,updatecell,mrv)
    else:
        return backtrack(domains,updatecell,mrv)
        

if __name__ == "__main__":
    generate_board()
    print_board()
    print("---------------------------------------------")
    solve(dummy)
    print("---------------------------------------------")
    print_board()