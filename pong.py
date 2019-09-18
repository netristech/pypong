#!/usr/bin/python

#import libraries
import curses
import time
import random

def main(win):
    class Player:
        def __init__(self, name, score):
            self.name = name
            self.score = score

        def increment_score(self):
            self.score += 1
        
    class Paddle:
        def __init__(self, pos_y):
            self.pos_y = pos_y

        def move_up(self):
            self.pos_y -= 1

        def move_down(self):
            self.pos_y += 1

    class Ball:
        def __init__(self, pos_y, pos_x, dir_y, dir_x):
            self.pos_y = pos_y
            self.pos_x = pos_x
            self.dir_x = dir_x
            self.dir_y = dir_y

        def move(self, skip):
            #compensate for screen aspect ratio
            if skip == int(width / (height * 2)):
                if self.dir_y == "up":
                    self.pos_y -= 1
                elif self.dir_y == "down":
                    self.pos_y += 1
                skip = 1 
            else:
                skip += 1
            if self.dir_x == "right":
                self.pos_x += 2 
            elif self.dir_x == "left":
                self.pos_x -= 2
            return skip

    def initialize():
        player_paddle = Paddle(1)
        computer_paddle = Paddle(1)
        ball = Ball(height / 2 - 1, width / 2 + (width / 2) / 2, "null", "left")
        return player_paddle, computer_paddle, ball

    def title_screen():
        title = [
            " _______  __   __  _______  _______  __    _  _______ ",
            "|       ||  | |  ||       ||       ||  |  | ||       |",
            "|    _  ||  |_|  ||    _  ||   _   ||   |_| ||    ___|",
            "|   |_| ||       ||   |_| ||  | |  ||       ||   | __ ",
            "|    ___||_     _||    ___||  |_|  ||  _    ||   ||  |",
            "|   |      |   |  |   |    |       || | |   ||   |_| |",
            "|___|      |___|  |___|    |_______||_|  |__||_______|"
        ]
        title_messages = [
            "Written by Netris",
            "Press ENTER to start ('q' to quit)",
            "Enter your name: ",
            "Please wait a moment "
        ]
        cursor_spin = ["|", "/", "-", "\\"]
        win.clear()
        for i in range(0, len(title)):
            win.addstr(
                height / 2 - len(title) / 2 + i,
                width / 2 - len(title[0]) / 2, title[i],
                curses.color_pair(1)
            )
        win.addstr(height - 3, width /2 - len(title_messages[0]) / 2, title_messages[0])
        win.addstr(height - 2, width / 2 - len(title_messages[1]) / 2, title_messages[1])
        win.refresh()
        in_key = 0 
        while in_key not in (curses.KEY_ENTER, 10, 13, "\n"):
            in_key = win.getch()
            if in_key == ord("q"):
                return False
        win.move(height - 3, 0)
        win.clrtobot()
        win.refresh()
        win.addstr(height - 3, width / 2 - len(title_messages[2]) / 2, title_messages[2])
        curses.echo()
        player = Player(win.getstr(8), 0)
        timeout = time.time() + 2
        while time.time() < timeout:
            for i in cursor_spin:
                win.addstr(
                    height - 2,
                    width / 2 - len(title_messages[3]) / 2,
                    title_messages[3] + i,
                    curses.color_pair(1)
                )
                time.sleep(.05)
                win.refresh()
        return player 

    def render_screen():
        win.nodelay(True)
        win.clear()
        for i in range(height):
            win.addstr(i, width / 2, "|")
        for i in range(0, len(paddle_gfx)):
            win.addstr(player_paddle.pos_y + i, 1, paddle_gfx[i])
            win.addstr(computer_paddle.pos_y + i, width - 4, paddle_gfx[i])
        for i in range(0, len(ball_gfx)):
            win.addstr(ball.pos_y + i, ball.pos_x, ball_gfx[i])
        win.addstr(
            0,
            width / 2 - (len(player.name) + 10) / 2,
            "{}'s Score: {}".format(player.name, player.score),
            curses.color_pair(1)
        )
        #render full height
        win.move(0, height)
        win.refresh()
        time.sleep(speed)

    def ball_hit():
        if (
            ball.pos_y >= player_paddle.pos_y and
            ball.pos_y < player_paddle.pos_y + 5
        ):
            if ball.pos_y > player_paddle.pos_y + 2:
                ball.dir_y = "down"
            elif ball.pos_y < player_paddle.pos_y + 2:
                ball.dir_y = "up"
            else:
                ball.dir_y = "none"
            return True
        else:
            return False

    def game_over():
        win.clear()
        go_text = [
            " _______  _______  __   __  _______    _______  __   __  _______  ______   ",
            "|       ||   _   ||  |_|  ||       |  |       ||  | |  ||       ||    _ |  ",
            "|    ___||  |_|  ||       ||    ___|  |   _   ||  |_|  ||    ___||   | ||  ",
            "|   | __ |       ||       ||   |___   |  | |  ||       ||   |___ |   |_||_ ",
            "|   ||  ||       ||       ||    ___|  |  |_|  ||       ||    ___||    __  |",
            "|   |_| ||   _   || ||_|| ||   |___   |       | |     | |   |___ |   |  | |",
            "|_______||__| |__||_|   |_||_______|  |_______|  |___|  |_______||___|  |_|"
        ]
        go_messages = [
            "Thanks for playing, {}!".format(player.name),
            "To continue press 'c' to quit press 'q'"
        ]
        win.addstr(
            0,
            width / 2 - (len(player.name) + 10) / 2,
            "{}'s Score: {}".format(player.name, player.score),
            curses.color_pair(1)
        )
        for i in range(0, len(go_text)):
            win.addstr(
                height / 2 - len(go_text) / 2 + i,
                width / 2 - len(go_text[0]) / 2,
                go_text[i],
                curses.color_pair(2)
            )
        win.addstr(height - 3, width / 2 - len(go_messages[0]) / 2, go_messages[0])
        win.addstr(height - 2, width / 2 - len(go_messages[1]) / 2, go_messages[1])
        win.refresh()
        in_key = 0
        while in_key not in (ord("c"), ord("q")):
            in_key = win.getch()
            if in_key == ord("q"):
                return True
            elif in_key == ord("c"):
                return False

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    height, width = win.getmaxyx()
    player_paddle, computer_paddle, ball = initialize()
    paddle_gfx = [" _ ", "| |", "| |", "| |", "| |", "|_|"]
    ball_gfx = [" _ ", "(_)"]
    skip = 1
    speed = .05
    player = title_screen()
    while player:
        render_screen()
        skip = ball.move(skip)
        if ball.dir_x == "right":
            dest = ball.pos_y - 2
            if (
                computer_paddle.pos_y < dest and
                computer_paddle.pos_y < height - 8
            ):
                computer_paddle.move_down()
            elif (
                computer_paddle.pos_y > dest and
                computer_paddle.pos_y > 1
            ):
                computer_paddle.move_up()
        if ball.pos_y < 1:
            ball.dir_y = "down"
        if ball.pos_y > height - 4:
            ball.dir_y = "up"
        if ball.pos_x > width - 5:
            ball.dir_x = "left"
            ball.dir_y = random.choice(["up", "down"])
        if ball.pos_x < 4:
            if ball_hit():
                ball.dir_x = "right"
                player.increment_score()
                if player.score % 10 == 0 and speed > .01:
                    speed -= .01
            else:
                if game_over():
                    break
                else:
                    speed = .05
                    player.score = 0
                    player_paddle, computer_paddle, ball = initialize()
                    
        in_key = win.getch()
        if (
            in_key == curses.KEY_UP and
            player_paddle.pos_y > 1
        ):
            player_paddle.move_up()
        elif (
            in_key == curses.KEY_DOWN and
            player_paddle.pos_y < height - 8
        ): 
            player_paddle.move_down()
        if in_key == ord("q"):
            break

curses.wrapper(main)
