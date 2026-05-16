import tkinter as tk
import solver
import time

cells = [[None]*9 for _ in range(9)]
root = tk.Tk()
root.title("Sudoku Solver")

for r in range(9):
    for c in range(9):
        cells[r][c] = tk.Entry(root, width=2, font=("Arial", 18, "bold"), justify="center",
                               state="disabled", disabledforeground="white", disabledbackground="black")
        cells[r][c].grid(row=r, column=c)

prefilled = [[False]*9 for _ in range(9)]
status = tk.Label(root, text="Generate a Board!")
status.grid(row=14, column=0, columnspan=9)

def set_cell(row, col, val, bg):
    e = cells[row][col]
    e.config(state="normal")
    e.delete(0, tk.END)
    if val != 0:
        e.insert(0, val)
    e.config(state="disabled", disabledbackground=bg, disabledforeground="white")

def loadBoard():
    board = solver.BOARD
    for row in range(9):
        for col in range(9):
            val = board[row][col]
            if val != 0:
                set_cell(row, col, val, "gray")
                prefilled[row][col] = True
            else:
                set_cell(row, col, 0, "black")
                prefilled[row][col] = False

def clearBoard():
    for row in range(9):
        for col in range(9):
            if not prefilled[row][col]:
                set_cell(row, col, 0, "black")
                solver.BOARD[row][col] = 0

def generateBoard():
    clearBoard()
    solver.generate_board(str(diff_var.get()))
    loadBoard()
    status.config(text="Board generated!")
    root.update()
    time.sleep(0.5)
    status.config(text="")

def updatecell(r, c, val, backtrack):
    if backtrack:
        set_cell(r, c, 0, "red")
        root.update()
        time.sleep(0.05)
        set_cell(r, c, 0, "black")
    else:
        set_cell(r, c, val, "green")
    root.update()
    time.sleep(0.1)

def solveBoard():
    for w in [btn_solve, btn_generate, btn_clear, chk_mrv, chk_fc]:
        w.config(state="disabled")
    status.config(text="Solving...")
    solver.solve(updatecell,fc_var.get(),mrv_var.get())
    for w in [btn_solve, btn_generate, btn_clear, chk_mrv, chk_fc]:
        w.config(state="normal")
    status.config(text="Solved!")

mrv_var  = tk.BooleanVar(value=True)
fc_var   = tk.BooleanVar(value=True)
diff_var = tk.StringVar(value="Medium")
tk.OptionMenu(root, diff_var, "Easy", "Medium", "Hard").grid(row=13, column=0, columnspan=9)

btn_solve    = tk.Button(root, text="Solve",    command=solveBoard)
btn_generate = tk.Button(root, text="Generate", command=generateBoard)
btn_clear    = tk.Button(root, text="Clear",    command=clearBoard)
btn_solve.grid(   row=9,  column=0, columnspan=3)
btn_generate.grid(row=9,  column=3, columnspan=3)
btn_clear.grid(   row=9,  column=6, columnspan=3)
chk_mrv = tk.Checkbutton(root, text="MRV",              variable=mrv_var)
chk_fc  = tk.Checkbutton(root, text="Forward Checking", variable=fc_var)
chk_mrv.grid(row=11, column=0, columnspan=9)
chk_fc.grid( row=12, column=0, columnspan=9)

loadBoard()
root.mainloop()
