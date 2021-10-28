import random
import sys
from datetime import datetime
import pygame
import copy
import numpy as np


class LifeGame:
	def __init__(self, screen_width=800, screen_height=600, cell_size=10, alive_color=(0, 255, 255),
				 dead_color=(0, 0, 0), max_fps=10):

		pygame.init()
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.cell_size = cell_size
		self.alive_color = alive_color
		self.dead_color = dead_color

		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		self.clear_screen()
		pygame.display.flip()

		self.last_update_completed = 0
		self.desired_milliseconds_between_updates = (1.0 / max_fps) * 1000.0

		self.num_cols = int(self.screen_width / self.cell_size)
		self.num_rows = int(self.screen_height / self.cell_size)
		self.active_grid = 0
		self.grids = []

		self.init_grids()
		self.set_grid()

		self.paused = False
		self.game_over = False

	def init_grids(self):

		def create_grid():
			rows = []
			for row_num in range(self.num_rows):
				list_of_columns = [0] * self.num_cols
				rows.append(list_of_columns)
			return rows

		self.grids.append(create_grid())
		self.grids.append(create_grid())

	def set_grid(self, value=None, grid=0):
		for r in range(self.num_rows):
			for c in range(self.num_cols):
				if value is None:
					cell_value = np.random.choice([0, 255], p=[0.8, 0.2])
				else:
					cell_value = value
				self.grids[grid][r][c] = cell_value

	def draw_grid(self):
		self.clear_screen()
		for r in range(self.num_rows):
			for c in range(self.num_cols):
				if self.grids[self.active_grid][r][c] == 255:
					color = self.alive_color
				else:
					color = self.dead_color
				pygame.draw.circle(self.screen,
								   color,
								   (int(c * self.cell_size + (self.cell_size / 2)),
									int(r * self.cell_size + (self.cell_size / 2))),
								   int(self.cell_size / 2),
								   0)
		pygame.display.flip()

	def clear_screen(self):
		self.screen.fill(self.dead_color)

	def inactive_grid(self):
		inactive_grid = (self.active_grid + 1) % 2
		return inactive_grid

	def check_cell_neighbors(self, row_index, col_index, grid):
		# self.grids[self.active_grid][r][c] # current cell
		total = int((grid[row_index][(col_index - 1) % self.num_cols] + grid[row_index][(col_index + 1) % self.num_cols] +
					 grid[(row_index - 1) % self.num_rows][col_index] + grid[(row_index + 1) % self.num_rows][col_index] +
					 grid[(row_index - 1) % self.num_rows][(col_index - 1) % self.num_cols] +
					 grid[(row_index - 1) % self.num_rows][(col_index + 1) % self.num_cols] +
					 grid[(row_index + 1) % self.num_rows][(col_index - 1) % self.num_cols] +
					 grid[(row_index + 1) % self.num_rows][(col_index + 1) % self.num_cols])/255)

		# Apply rules
		val = int()
		if grid[row_index][col_index] == 255:
			if (total < 2) or (total > 3):
				val = 0
			else:
				val = grid[row_index][col_index]
		else:
			if total == 3:
				val = 255
		return val

	def update_generation(self):
		# TODO
		# Inspect the current active generation
		grid = copy.deepcopy(self.grids[self.active_grid])
		for r in range(self.num_rows):
			for c in range(self.num_cols):
				next_gen_state = self.check_cell_neighbors(r, c, grid)
				self.grids[self.inactive_grid()][r][c] = next_gen_state

		self.active_grid = self.inactive_grid()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				print("Key pressed")
				if event.unicode == 's':
					if self.paused:
						self.paused = False
					else:
						self.paused = True
				elif event.unicode == 'r':
					self.active_grid = 0
					self.set_grid(None, self.active_grid)
					self.draw_grid()
				elif event.unicode == 'q':
					self.game_over = True
			if event.type == pygame.QUIT:
				sys.exit()

	def cap_frame_rate(self):
		now = pygame.time.get_ticks()
		millieseconds_since_last_update = now - self.last_update_completed
		time_to_sleep = self.desired_milliseconds_between_updates - millieseconds_since_last_update
		if time_to_sleep > 0:
			pygame.time.delay(int(time_to_sleep))
		self.last_update_completed = now

	def run(self):
		while True:
			if self.game_over:
				return
			self.handle_events()

			if self.paused:
				continue

			self.update_generation()
			self.draw_grid()
			self.cap_frame_rate()


if __name__ == '__main__':
	game = LifeGame()
	game.run()
