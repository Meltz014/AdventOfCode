from y2021.day11.solve import Solver as Base
import tkinter as tk
from tkinter import ttk

class SquareButton(tk.Frame):
    def __init__(self, root, **kwargs):
        bg = kwargs.pop('background', None)
        super().__init__(root, **kwargs)
        self.btn = tk.Button(self)
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.grid_propagate(0)
        self.btn.grid(sticky = "NWSE")
        self.btn.configure(background=bg)

    def set_energy(self, energy):
        # energy is 0 to 9 in intensity, or 10 will be "flash"
        if energy == 0:
            self.btn.configure(background='#00FF00')
        else:
            i = int(25.5*energy)
            self.btn.configure(background=f'#{i:02X}{i:02X}{i:02X}')


class GridFrame(tk.Frame):
    def __init__(self, root, grid):
        super().__init__(root)
        options = {'padx': 1, 'pady': 1}
        self.btn_grid = []
        self.fishgrid = grid

        row_num = 0
        for g_row in self.fishgrid:
            col_num = 0
            btn_row = []
            for energy in g_row:
                btn = SquareButton(self, width=10, height=10)
                btn.grid(row=row_num, column=col_num, **options)
                btn.set_energy(energy)
                btn_row.append(btn)
                col_num += 1
            self.btn_grid.append(btn_row)
            row_num += 1

        self.pack(padx=5, pady=5)

    def update_energy(self):
        for (r,g_row) in enumerate(self.fishgrid):
            for (c,energy) in enumerate(g_row):
                self.btn_grid[r][c].set_energy(energy)


class VisUI(ttk.Frame):
    def __init__(self, root, solver):
        super().__init__(root)
        self.root = root
        self.p1_flashers = 0
        self.n = 0
        self.p2_done = False
        self.solver = solver

        options = {'padx': 5, 'pady': 5}
        self.label = ttk.Label(self, text='Day 11 Visualizer')
        self.label.pack(**options)

        self.gf = GridFrame(self, solver.grid)
        self.gf.pack(**options)
        
        self.p1_text = tk.StringVar()
        self.p1_text.set("Part 1 flashes after 100 iter:")
        p1_label = tk.Label(self.root, textvariable=self.p1_text)
        p1_label.pack(**options)

        self.p2_text = tk.StringVar()
        self.p2_text.set("Part 2 steps for sync:")
        p2_label = tk.Label(self.root, textvariable=self.p2_text)
        p2_label.pack(**options)

        self.pack(**options)

    def update(self):
        if self.n == 0:
            input()
        n_flash = self.solver.step()
        self.n += 1
        if self.n <= 100:
            self.p1_flashers += n_flash
        if self.n == 100:
            self.p1_text.set(f'Part 1 flashes after 100 iter: {self.p1_flashers}')
        if not self.p2_done and n_flash == self.gf.fishgrid.size:
            self.p2_done = True
            self.p2_text.set(f"Part 2 steps for sync: {self.n}")
        self.gf.update_energy()
        self.root.after(30, self.update)

class Solver(Base):

    def visualize(self):
        self.parse()

        root = tk.Tk()
        ui = VisUI(root, self)
        root.after(10, ui.update)
        root.mainloop()

