#!/usr/bin/python

import curses
import time
import random
import sys

class Screen(object):
	myscreen = None
	screen_lines = 20
	screen_cols = 40

	def __init__(self, screen):
		curses.curs_set(0)
		self.myscreen = screen.subwin(self.screen_lines, self.screen_cols, 0, 0)
		self.myscreen.border(0, 0, 0, 0, curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LLCORNER, curses.ACS_LRCORNER)

	def clear(self, snake):
		i = snake.length-1
		while i>=0:
			self.myscreen.addstr(snake.body[i][1], snake.body[i][0], " ")#(y,x,character)
			i -= 1

	def refresh(self):
		self.myscreen.refresh()

	def timeout(self, i):
		self.myscreen.timeout(i)

	def getch(self):
		return self.myscreen.getch()

	def close(self):
		self.myscreen.getch()
		curses.endwin()
		sys.exit(0)

#snake[tail, body, body, ..., body, head]
class Snake(object):
	alive = True
	screen = None
	body = []
	original_length = 8
	length = original_length
	directions = {"up":0, "right":1, "down":2, "left":3}
	direction = directions["right"]

	def __init__(self, screen):
		self.screen = screen
		i = 1
		while i<=self.original_length:
			i += 1
			self.body.append([i, 1])

	def draw(self):
		i = self.length-1
		while i>=0:
			self.screen.myscreen.addstr(self.body[i][1], self.body[i][0], "*")#(y,x,character)
			i -= 1

	def move(self, direction):
		i = 0
		if self.directions["up"] == direction and self.direction != self.directions["down"]:
			self.body.append([(self.body[-1][0]), (self.body[-1][1] - 1)])
			self.body.pop(0)
			self.direction = direction
		elif self.directions["right"] == direction and self.direction != self.directions["left"]:
			self.body.append([(self.body[-1][0] + 1), (self.body[-1][1])])
			self.body.pop(0)
			self.direction = direction
		elif self.directions["down"] == direction and self.direction != self.directions["up"]:
			self.body.append([(self.body[-1][0]), (self.body[-1][1] + 1)])
			self.body.pop(0)
			self.direction = direction
		elif self.directions["left"] == direction and self.direction != self.directions["right"]:
			self.body.append([(self.body[-1][0] - 1), (self.body[-1][1])])
			self.body.pop(0)
			self.direction = direction

	def get_dead_state(self):
		head = self.body[-1]
		if head[0] == 1 or head[0] == self.screen.screen_cols:
			self.alive = False
			return
		if head[1] == 0 or head[1] == self.screen.screen_lines-1:
			self.alive = False
			return
		for i in range(len(self.body)-2):
			if head == self.body[i]:
				self.alive = False
				return
		self.alive = True

class Barrier(object):
	screen = None
	def __init__(self, screen):
		self.screen = screen

	def draw(self, snake):
		while True:
			x = random.randint(1, self.screen.screen_cols-2)
			y = random.randint(1, self.screen.screen_lines-2)
			if [x, y] not in snake.body:
				character = chr(random.randint(65, 90))
				self.screen.myscreen.addstr(y, x, character)
				break
		return

def run_snake(stdscr):
	screen = Screen(stdscr)
	snake = Snake(screen)
	barrier = Barrier(screen)

	direction = snake.direction
	last_direction = direction

	screen.clear(snake)
	screen.refresh()
	snake.draw()
	barrier.draw(snake)
	screen.refresh()

	screen.timeout(0)

	while True:
		time.sleep(0.2)
		key = screen.getch()
		if key in (curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT):
			if key == curses.KEY_DOWN:
				direction = snake.directions["down"]
			elif key == curses.KEY_UP:
				direction = snake.directions["up"]
			elif key == curses.KEY_LEFT:
				direction = snake.directions["left"]
			elif key == curses.KEY_RIGHT:
				direction = snake.directions["right"]
		elif key == ord('q'):
			break

		screen.clear(snake)
		if snake.alive:
			if 2 != abs(direction - last_direction):
				snake.move(direction)
				last_direction = direction
			else:
				snake.move(last_direction)
			snake.draw()
			screen.refresh()
			snake.get_dead_state()
		else:
			screen.refresh()
			time.sleep(0.2)
			snake.draw()
			screen.refresh()

	screen.close()

def main(stdscr):
	run_snake(stdscr)

if __name__ == '__main__':
    try:
    	curses.wrapper(main)
    except:
    	sys.exit(0)