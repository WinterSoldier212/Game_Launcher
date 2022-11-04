import pygame
import random
from random import randrange as rnd
import sys
import time

game_fast_click_score = 0

# Игра "Арканоид"
def game_arcanoid():
   try:
      pygame.font.init()
      WIDTH, HEIGHT = 1200, 800
      fps = 60

      bg_game = pygame.image.load("background\\bg_arcanoid.jpg").convert()

      font = pygame.font.SysFont('arial', 120, bold=True)

      paddle_w = 330
      paddle_h = 35
      paddle_speed = 15
      paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

      ball_radius = 20
      ball_speed = 6
      ball_rect = int(ball_radius * 2 ** 0.5)
      ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
      dx, dy = 1, -1

      block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
      color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

      pygame.init()
      sc = pygame.display.set_mode((WIDTH, HEIGHT))
      clock = pygame.time.Clock()

      def detect_collision(dx,dy, ball, rect):
         if dx > 0:
            delta_x = ball.right - rect.left
         else:
            delta_x = rect.right- ball.left
         if dy > 0:
            delta_y = ball.bottom - rect.top
         else:
            delta_y = rect.bottom - ball.top

         if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
         elif delta_x > delta_y:
            dy = -dy
         elif delta_y > delta_x:
            dx = -dx
         return dx, dy   

      while True:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               menu()

         sc.blit(bg_game, (0,0))

         [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
         pygame.draw.rect(sc, pygame.Color("darkorange"), paddle)
         pygame.draw.circle(sc, pygame.Color("white"), ball.center, ball_radius)

         ball.x += ball_speed * dx
         ball.y += ball_speed * dy

         if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
            dx = -dx
         
         if ball.centery < ball_radius:
            dy = -dy

         if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)

         hit_index = ball.collidelist(block_list)
         if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)

            hit_rect.inflate_ip(ball.width * 0.5, ball.height * 0.5)
            pygame.draw.rect(sc, hit_color, hit_rect)
            fps += 3
            if paddle_speed % 3 == 0 and paddle_speed <= 24:
               paddle_speed += 1

         if ball.bottom > HEIGHT:
            while True:
               render_win = font.render("GAME OVER", True, pygame.Color("darkorange"))
               sc.blit(render_win, (WIDTH // 3 - 110, HEIGHT // 3 + 20))
               pygame.display.flip()
               for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        menu()
               key = pygame.key.get_pressed()
               if key[pygame.K_r]:
                  game_arcanoid()
      
         elif not len(block_list):
            while True:
               render_win = font.render("GAME WIN", True, pygame.Color("orange"))
               sc.blit(render_win, (WIDTH // 3 - 120, HEIGHT // 3 + 20))
               pygame.display.flip()
               for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        menu()
               key = pygame.key.get_pressed()
               if key[pygame.K_r]:
                  game_arcanoid()

         key = pygame.key.get_pressed() 
         if (key[pygame.K_LEFT] or key[pygame.K_a]) and paddle.left > 0:
            paddle.left -= paddle_speed

         if (key[pygame.K_RIGHT] or key[pygame.K_d]) and paddle.right < WIDTH:
            paddle.left += paddle_speed

         pygame.display.flip()
         clock.tick(fps)
   except:
      pass

# Игра "Змейка"
def game_snake():
   try:
      pygame.font.init()

      WIDTH = 1200
      HEIGHT = 800
      SIZE = 50

      score = 0

      bg_game = pygame.image.load("background\\bg_snake.jpg").convert()

      font_score = pygame.font.SysFont('arial', 50, bold=True)
      font = pygame.font.SysFont('arial', 120, bold=True)

      x, y = rnd(50, WIDTH - 50, SIZE), rnd(50, HEIGHT - 50, SIZE)
      apple = rnd(50, WIDTH - 50, SIZE), rnd(50, HEIGHT - 50, SIZE)
      
      dirs = {
         "W": True,
         "S": True,
         "A": True,
         "D": True,
      }
      
      length = 2
      snake = [(x, y)]
      snake.append((x, y))
      dx, dy = 0, 0
      fps = 7.5

      pygame.init()
      sc = pygame.display.set_mode([WIDTH, HEIGHT])
      clock = pygame.time.Clock()

      while True:

         sc.blit(bg_game,(0, 0))
         [(pygame.draw.rect(sc, pygame.Color("blue"), (i, j, SIZE - 2, SIZE - 2))) for i, j in snake]
         pygame.draw.rect(sc, pygame.Color("darkred"), (*apple, SIZE, SIZE))

         render_score = font_score.render(f"Score: {score}", True, pygame.Color("orange"))

         sc.blit(render_score, (13, 5))

         x += dx * SIZE
         y += dy * SIZE

         snake.append((x, y))
         snake = snake[-length:]

         # Поедания яблок змейкой
         if snake[-1] == apple:
            apple = rnd(0, WIDTH, SIZE), rnd(0, HEIGHT, SIZE)
            length += 1
            fps += 0.5
            score += 1
         
         # Игра окончена
         if x < 0 or x > WIDTH - SIZE or y < 0 or y > HEIGHT - SIZE or ((len(snake) != len(set(snake))) and (len(snake) > 2)):
            while True:
               render_win = font.render("GAME OVER", True, pygame.Color("darkorange"))
               sc.blit(render_win, (WIDTH // 3 - 110, HEIGHT // 3 + 20))
               pygame.display.flip()
               for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                     menu()
               key = pygame.key.get_pressed()
               if key[pygame.K_r]:
                  game_snake()
            
         pygame.display.flip()
         clock.tick(fps)

         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               menu()
         
         key = pygame.key.get_pressed()

         if ((key[pygame.K_w]) or (key[pygame.K_UP])) and dirs["W"]:
            dx, dy = 0, -1
            dirs = {"W": True, "S": False, "A": True, "D": True}

         if ((key[pygame.K_s]) or (key[pygame.K_DOWN])) and dirs["S"]:
            dx, dy = 0, 1
            dirs = {"W": False, "S": True, "A": True, "D": True}

         if ((key[pygame.K_d]) or (key[pygame.K_RIGHT])) and dirs["D"]:
            dx, dy = 1, 0
            dirs = {"W": True, "S": True, "A": False, "D": True}

         if ((key[pygame.K_a]) or (key[pygame.K_LEFT])) and dirs["A"]:
            dx, dy = -1, 0
            dirs = {"W": True, "S": True, "A": True, "D": False}
   except:
      pass

# Игра "Быстрый клик"
def game_FastClick():
   global game_fast_click_score
   game_fast_click_score = 0

   pygame.init()
   WIDTH, HEIGHT = 1200, 800
   fps = 60

   timetick = 0
   font_END = pygame.font.SysFont('arial', 125, bold=True)
   font_time_cel = pygame.font.SysFont('arial', 90, bold= True)
   fontbat = pygame.font.SysFont('arial', 120, bold=True)
   font_but = pygame.font.SysFont('arial', 70, bold=True)

   sc = pygame.display.set_mode((WIDTH, HEIGHT))
   clock = pygame.time.Clock()
   bg_game = pygame.image.load("background\\bg_fast_click.jpg").convert()

   game_fast_click_time = 0
   timetimetick = 0

   clik_up = False
   
   objects = []

   class Button():
      def __init__(self, x, y, width, height, buttonText="Button", oneclickFunction = None, onePress = False):
         self.x = x
         self.y = y
         self.width = width
         self.height = height
         self.oneclickFunction = oneclickFunction
         self.onePress = onePress
         self.alreadyPressed = False

         self.fillColors = {
            "normal": "#7022cc",
            "hover": "#6622cc",
            "pressed": "#000066"
         }
         
         self.buttonSurface = pygame.Surface((self.width, self.height))
         self.buttonRect = pygame.Rect(self.x, self.y, self.width,self.height)

         self.buttonSurf = font_but.render(buttonText, True, (20, 20, 20))

         objects.append(self)

      def process(self):
         global clik_up
         mousePos = pygame.mouse.get_pos()
         self.buttonSurface.fill(self.fillColors["normal"])
         if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors["hover"])
            if pygame.mouse.get_pressed(num_buttons=3)[0] and clik_up == False:
               self.buttonSurface.fill(self.fillColors["pressed"])
               if self.onePress:
                  clik_up = True
                  self.oneclickFunction
               elif not self.alreadyPressed:
                  self.oneclickFunction
                  self.alreadyPressed = True
            else:
               clik_up = False
               self.alreadyPressed = False

         self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2,
         ])
         sc.blit(self.buttonSurface, self.buttonRect)

   def plus_click():
      global game_fast_click_score
      game_fast_click_score += 1

   def minus_click():
      global game_fast_click_score
      game_fast_click_score -= 1

   x_285, x_435, x_585, x_735, y_480, y_635, y_325 = 285, 435, 585, 735, 480, 635, 325

   def button_asas():
      x = rnd(285, 885, 150)
      y = rnd(325, 790, 155)

      Button(x, y, 130, 130, '+', plus_click)
      if y == y_480:
         Button(285, 635, 130, 130, '-', minus_click)
         Button(435, 635, 130, 130, '-', minus_click)
         Button(585, 635, 130, 130, '-', minus_click)
         Button(735, 635, 130, 130, '-', minus_click)
         Button(285, 325, 130, 130, '-', minus_click)
         Button(435, 325, 130, 130, '-', minus_click)
         Button(585, 325, 130, 130, '-', minus_click)
         Button(735, 325, 130, 130, '-', minus_click)
         if x != x_285:
            Button(285, 480, 130, 130, '-', minus_click)
         if x != x_435:
            Button(435, 480, 130, 130, '-', minus_click)
         if x != x_585:
            Button(585, 480, 130, 130, '-', minus_click)
         if x != x_735:
            Button(735, 480, 130, 130, '-', minus_click)

      if y == y_635:
         Button(735, 480, 130, 130, '-', minus_click)
         Button(585, 480, 130, 130, '-', minus_click)
         Button(435, 480, 130, 130, '-', minus_click)
         Button(285, 480, 130, 130, '-', minus_click)
         Button(285, 325, 130, 130, '-', minus_click)
         Button(435, 325, 130, 130, '-', minus_click)
         Button(585, 325, 130, 130, '-', minus_click)
         Button(735, 325, 130, 130, '-', minus_click)
         if x != x_285:
            Button(285, 635, 130, 130, '-', minus_click)
         if x != x_435:
            Button(435, 635, 130, 130, '-', minus_click)
         if x != x_585:
            Button(585, 635, 130, 130, '-', minus_click)
         if x != x_735:
            Button(735, 635, 130, 130, '-', minus_click)
      
      if y == y_325:
         Button(735, 480, 130, 130, '-', minus_click)
         Button(585, 480, 130, 130, '-', minus_click)
         Button(435, 480, 130, 130, '-', minus_click)
         Button(285, 480, 130, 130, '-', minus_click)
         Button(285, 635, 130, 130, '-', minus_click)
         Button(435, 635, 130, 130, '-', minus_click)
         Button(585, 635, 130, 130, '-', minus_click)
         Button(735, 635, 130, 130, '-', minus_click)
         if x != x_285:
            Button(285, 325, 130, 130, '-', minus_click)
         if x != x_435:
            Button(435, 325, 130, 130, '-', minus_click)
         if x != x_585:
            Button(585, 325, 130, 130, '-', minus_click)
         if x != x_735:
            Button(735, 325, 130, 130, '-', minus_click)

   button_asas()

   while True:

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            menu()
      sc.blit(bg_game, (0,0))

      for object in objects:
         object.process()

      timetick += 1
      timetimetick += 0.99667

      if timetimetick >= 59.8:
         timetimetick = 0
         game_fast_click_time += 1
      
      # Выведем На экран счёт время и цель
      render_time = font_time_cel.render("Time:", True, pygame.Color("black"))
      sc.blit(render_time, (45, 15))
      render_time = font_time_cel.render(f"{game_fast_click_time}", True, pygame.Color("black"))
      sc.blit(render_time, (125, 105))
      render_score = fontbat.render(f"{game_fast_click_score}", True, pygame.Color("black"))
      sc.blit(render_score, (WIDTH / 2 - 50, 75))
      render_time = font_time_cel.render("Purpose:", True, pygame.Color("black"))
      sc.blit(render_time, (875, 10))
      render_time = font_time_cel.render("30", True, pygame.Color("black"))
      sc.blit(render_time, (1000, 100))

      if timetick == 35:
         objects = []
         timetick = 0
         button_asas()

      # Если счёт >= 30, то выводим надпись Игра выйграна
      if game_fast_click_score >=30:
         while True:
            render_win = font_END.render("GAME WIN", True, pygame.Color("#cc8800"))
            sc.blit(render_win, (WIDTH // 3 - 100, HEIGHT // 3 + 20))
            pygame.display.flip()
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  menu()
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
               game_FastClick()
            render_score = fontbat.render(f"{game_fast_click_score}", True, pygame.Color("black"))
            sc.blit(render_score, (WIDTH / 2 - 50, 75))

      if game_fast_click_score <= -10:
         while True:
            render_win = font_END.render("GAME OVER", True, pygame.Color("#cc8800"))
            sc.blit(render_win, (WIDTH // 3 - 125, HEIGHT // 3 + 20))
            pygame.display.flip()
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  menu()
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
               game_FastClick()
            render_score = fontbat.render(f"{game_fast_click_score}", True, pygame.Color("black"))
            sc.blit(render_score, (WIDTH / 2 - 50, 75))

      pygame.display.flip()
      clock.tick(fps)

# Игра 21 очко
def game_21o4ko():
   pygame.init()
   pygame.font.init()

   font_button = pygame.font.SysFont('Monospace', 30, bold=True)
   font = pygame.font.SysFont('Monospace', 50, bold=True)
   font_end = pygame.font.SysFont('Monospace', 120, bold=True)

   screen = pygame.display.set_mode((1200, 800))
   clock = pygame.time.Clock()
   fps = 80
   
   butt = pygame.Rect(10, 710, 220, 75)
   butt2 = pygame.Rect(250, 710, 220, 75)
   end_butt = pygame.Rect(10, 710, 440, 75)

   rubashka_karti = pygame.image.load("graphic_cart\\karta.png").convert()

   spisok_kart_znach = {
      "6_kresti": 6, "6_pic": 6,"6_chervi": 6,"6_bubi": 6,
      "7_kresti": 7,"7_pic": 7,"7_chervi": 7,"7_bubi": 7,
      "8_kresti": 8,"8_pic": 8,"8_chervi": 8,"8_bubi": 8,
      "9_kresti": 9,"9_pic": 9,"9_chervi": 9,"9_bubi": 9,
      "10_kresti": 10,"10_pic": 10,"10_chervi": 10,"10_bubi": 10,
      "B_kresti": 2,"B_pic": 2,"B_chervi": 2,"B_bubi": 2,
      "D_kresti": 3,"D_pic": 3,"D_chervi": 3,"D_bubi": 3,
      "K_kresti": 4,"K_pic": 4,"K_chervi": 4,"K_bubi": 4,
      "T_kresti": 11,"T_pic": 11,"T_chervi": 11,"T_bubi": 11,}

   spisok_kart_graphic = {
      "6_kresti": "graphic_cart\\6_kresti.png", "6_pic": "graphic_cart\\6_pic.png", "6_chervi": "graphic_cart\\6_chervi.png", "6_bubi": "graphic_cart\\6_bubi.png",
      "7_kresti": "graphic_cart\\7_kresti.png", "7_pic": "graphic_cart\\7_pic.png", "7_chervi": "graphic_cart\\7_chervi.png", "7_bubi": "graphic_cart\\7_bubi.png",
      "8_kresti": "graphic_cart\\8_kresti.png", "8_pic": "graphic_cart\\8_pic.png", "8_chervi": "graphic_cart\\8_chervi.png", "8_bubi": "graphic_cart\\8_bubi.png",
      "9_kresti": "graphic_cart\\9_kresti.png", "9_pic": "graphic_cart\\9_pic.png", "9_chervi": "graphic_cart\\9_chervi.png", "9_bubi": "graphic_cart\\9_bubi.png",
      "10_kresti": "graphic_cart\\10_kresti.png", "10_pic": "graphic_cart\\10_pic.png", "10_chervi": "graphic_cart\\10_chervi.png ","10_bubi": "graphic_cart\\10_bubi.png",
      "B_kresti": "graphic_cart\\B_kresti.png", "B_pic": "graphic_cart\\B_pic.png", "B_chervi": "graphic_cart\\B_chervi.png", "B_bubi": "graphic_cart\\B_bubi.png",
      "D_kresti": "graphic_cart\\D_kresti.png", "D_pic": "graphic_cart\\D_pic.png", "D_chervi": "graphic_cart\\D_chervi.png", "D_bubi": "graphic_cart\\D_bubi.png",
      "K_kresti": "graphic_cart\\K_kresti.png", "K_pic": "graphic_cart\\K_pic.png", "K_chervi": "graphic_cart\\K_chervi.png", "K_bubi": "graphic_cart\\K_bubi.png",
      "T_kresti": "graphic_cart\\T_kresti.png", "T_pic": "graphic_cart\\T_pic.png", "T_chervi": "graphic_cart\\T_chervi.png", "T_bubi": "graphic_cart\\T_bubi.png",}

   spisok_kart = [
      "6_kresti", "6_pic","6_chervi","6_bubi",
      "7_kresti","7_pic","7_chervi","7_bubi",
      "8_kresti","8_pic","8_chervi","8_bubi",
      "9_kresti","9_pic","9_chervi","9_bubi",
      "10_kresti","10_pic","10_chervi","10_bubi",
      "B_kresti","B_pic","B_chervi","B_bubi",
      "D_kresti","D_pic","D_chervi","D_bubi",
      "K_kresti","K_pic","K_chervi","K_bubi",
      "T_kresti","T_pic","T_chervi","T_bubi",]

   random.shuffle(spisok_kart)

   minus_coloda = 4

   player_koloda = [spisok_kart[0], spisok_kart[2]]
   computer_koloda = [spisok_kart[1], spisok_kart[3]]

   x_cart = 11.875
   y_cart = -2.6

   x2_cart = 16
   y2_cart = 10.4

   x_comp = 75
   y_comp = 154

   x_player = 75
   y_player = 154

   player_plus_kart = False
   comp_plus_cart = False
   process_player_plus = False
   process_comp_plus = False

   yyye = 0
   xxxe = 0

   process_end_game = 0

   karta_comp_blit = 2
   karta_player_blit = 2

   end_game = False

   while True:

      y_comp_cart = 50
      x_comp_cart = 500

      y_player_cart = 570
      x_player_cart = 715

      computer_schet = 0
      player_schet = 0

      screen.fill((00, 66, 00))

      # Счёт значений карт
      for k, v in spisok_kart_znach.items():
         for kp in player_koloda:
            if k == kp:
               player_schet += v
         for kp in computer_koloda:
            if k == kp:
               computer_schet += v
      render_score = font.render(f"Ваш счёт: {player_schet}", True, pygame.Color("black"))
      screen.blit(render_score, (25, 645))

      # ИИ компьютера в 21
      if computer_schet <= 15 and process_comp_plus == False:
         computer_koloda.append(spisok_kart[minus_coloda])
         minus_coloda += 1
         comp_plus_cart = True
         process_comp_plus = True

      # When game over:
      if end_game == True:
         render_score = font.render(f"Cчёт бота: {computer_schet}", True, pygame.Color("black"))
         screen.blit(render_score, (17, 600))

         pygame.draw.rect(screen, pygame.Color("darkred"), end_butt)
         
         if process_end_game < 110:
            process_end_game += 2

         if process_end_game == 110:
            if player_schet == 21 != computer_schet or 21 >= player_schet > computer_schet or (player_koloda[0][0] == "T" and player_koloda[1][0] == "T") or (computer_schet >= 22 > player_schet and not (computer_koloda[0][0] == "T" and computer_koloda[1][0] == "T")):
               win_game = "Победа!"
               render_score = font_end.render(win_game, True, pygame.Color("darkorange"))
               screen.blit(render_score, (330, 305))

            elif 21 >= computer_schet > player_schet or computer_schet == 21 != player_schet or (computer_koloda[0][0] == "T" and computer_koloda[1][0] == "T") or (player_schet >= 22 > computer_schet and not (player_koloda[0][0] == "T" and player_koloda[1][0] == "T")):
               win_game = "Проигрыш"
               render_score = font_end.render(win_game, True, pygame.Color("darkorange"))
               screen.blit(render_score, (310, 310))

            else:
               win_game = "Ничья"
               render_score = font_end.render(win_game, True, pygame.Color("darkorange"))
               screen.blit(render_score, (330, 310))
            for j in computer_koloda:
               for k, v in spisok_kart_graphic.items():
                  if j == k:
                     blit_comp_kart = pygame.image.load(v).convert()
                     screen.blit(blit_comp_kart, (130 + x_comp_cart - 35*karta_comp_blit, y_comp_cart))
                     x_comp_cart += 30 + process_end_game

         else:
            for i in range(karta_comp_blit):
               screen.blit(rubashka_karti, (130 + x_comp_cart - 35*karta_comp_blit, y_comp_cart))
               x_comp_cart += 30 + process_end_game

         for j in player_koloda:
            for k, v in spisok_kart_graphic.items():
               if j == k:
                  blit_player_cart = pygame.image.load(v).convert()
                  screen.blit(blit_player_cart, (30 + x_player_cart - 50*karta_player_blit, y_player_cart))
                  x_player_cart += 65 + 0.7*process_end_game
         render_end = font.render("Играть снова", True, pygame.Color("black"))
         screen.blit(render_end, (48, 720))

      if end_game == False:
         if player_plus_kart == True and process_player_plus == True and yyye < 40:
            yyye += 1
            screen.blit(rubashka_karti, (x_player, y_player))
            x_player += x2_cart
            y_player += y2_cart

         elif player_plus_kart == True or process_player_plus == True and yyye >= 40:
            player_koloda.append(spisok_kart[minus_coloda])
            minus_coloda += 1
            karta_player_blit += 1
            player_plus_kart = False
            process_player_plus = False
            yyye = 0
            x_player = 75
            y_player = 154

         # Рисуем карты игрока
         for j in player_koloda:
            for k, v in spisok_kart_graphic.items():
               if j == k:
                  blit_player_cart = pygame.image.load(v).convert()
                  screen.blit(blit_player_cart, (x_player_cart, y_player_cart))
                  x_player_cart += 65

         # Рисуем карты компьютера
         for i in range(karta_comp_blit):
            screen.blit(rubashka_karti, (130 + x_comp_cart - 35*karta_comp_blit, y_comp_cart))
            x_comp_cart += 45
         
         if comp_plus_cart == True and process_comp_plus == True and xxxe < 40:
            xxxe += 1
            screen.blit(rubashka_karti, (x_comp, y_comp))
            x_comp += x_cart
            y_comp += y_cart

         elif comp_plus_cart == True or process_comp_plus == True and xxxe >= 40:
            karta_comp_blit += 1
            comp_plus_cart = False
            process_comp_plus = False
            xxxe = 0
            x_comp = 75
            y_comp = 154
         
      # Получаем данные о местонахождении мыши
      mouse = pygame.mouse.get_pos()
      for event in pygame.event.get():
         # Процесс выхода из вкладки
         if event.type == pygame.QUIT:
            menu()
            # pygame.quit()

         if event.type == pygame.MOUSEBUTTONDOWN:
            if end_game == True:
               if 10 <= mouse[0] <= 10 + 440 and 710 <= mouse[1] <= 710 + 75 and process_end_game == 110:
                  game_21o4ko()

            if 10 <= mouse[0] <= 10 + 220 and 710 <= mouse[1] <= 710 + 75 and player_schet < 21:
               player_plus_kart = True
               process_player_plus = True
            
            if 250 <= mouse[0] <= 250 + 220 and 710 <= mouse[1] <= 710 + 75 and process_comp_plus == False:
               end_game = True


      if end_game == False:
         pygame.draw.rect(screen, pygame.Color("darkred"), butt)
         pygame.draw.rect(screen, pygame.Color("darkred"), butt2)

         if player_schet == 21 or (player_koloda[0][0] == "T" and player_koloda[1][0] == "T"):
            render_perebor = font.render("У ваc!!", True, pygame.Color("darkred"))
            screen.blit(render_perebor, (10, 560))
            render_perebor = font.render("Победная комбинация!!", True, pygame.Color("darkred"))
            screen.blit(render_perebor, (10, 595))
         elif player_schet < 21 and not (player_koloda[0][0] == "T" and player_koloda[1][0] == "T"):
            pass
         else:
            render_perebor = font.render("У вас перебор!", True, pygame.Color("darkred"))
            screen.blit(render_perebor, (15, 595))

         render_score = font_button.render("Взять ещё", True, pygame.Color("black"))
         screen.blit(render_score, (33, 730))
         render_score = font_button.render("Вскрываемся", True, pygame.Color("black"))
         screen.blit(render_score, (260, 730))
      
      screen.blit(rubashka_karti, (75, 154))
      screen.blit(rubashka_karti, (65, 154))
      screen.blit(rubashka_karti, (55, 154))
      
      pygame.display.update()
      clock.tick(fps)

def game_ping_pong():
   pygame.init()

   # Размер экрана
   WIDTH, HEIGHT = 1200, 800

   y_paddle_1 = 275
   y_paddle_2 = 275

   ball_radius = 20
   ball_speed = 6
   ball_rect = int(ball_radius * 2 ** 0.5)
   ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_rect, ball_rect)
   dx, dy = rnd(-1,2,2), rnd(-1,2,2)

   x_2 = 1150
   x_1 = 15

   font = pygame.font.SysFont('Cosmic', 100, bold=True)
   font_2 = pygame.font.SysFont('Times new roman', 40, bold=True)
   font_win = pygame.font.SysFont('Times new roman', 120, bold=True)

   paddle_1 = pygame.Rect(x_1, y_paddle_1, 35, 250)
   paddle_2 = pygame.Rect(x_2, y_paddle_2, 35, 250)

   block_1 = pygame.Rect(0, 0, 1200, 50)
   block_2 = pygame.Rect(0, 750, 1200, 50)

   line = pygame.Rect(WIDTH // 2 - 10, 50, 20, 700)

   screen = pygame.display.set_mode((WIDTH, HEIGHT))

   paddle_speed = 10

   player_2_schet = 0
   player_1_schet = 0
   # Для фпс
   fps = 60
   clock = pygame.time.Clock()
   def detect_collision(dx,dy, ball, rect, ball_speed, paddle_speed):
      
      if dx > 0:
         delta_x = ball.right - rect.left
      else:
         delta_x = rect.right- ball.left
      if dy > 0:
         delta_y = ball.bottom - rect.top
      else:
         delta_y = rect.bottom - ball.top

      if abs(delta_x - delta_y) < 10:
         dx, dy = -dx, -dy
      elif delta_x > delta_y:
         dy = -dy
      elif delta_y > delta_x:
         dx = -dx
      ball_speed += 1 
      paddle_speed += 1
      return dx, dy, ball_speed, paddle_speed

   # Основной цикл
   while True:
      # Первым делом зальём экран цветом(Этот процесс не обязателен)
      screen.fill((00, 66, 00))

      pygame.draw.rect(screen, pygame.Color("darkorange"), paddle_1)
      pygame.draw.rect(screen, pygame.Color("darkorange"), paddle_2)

      render_schet = font.render(f"{player_1_schet}", True, pygame.Color("darkorange"))
      screen.blit(render_schet, (WIDTH // 2 - 105, 60))
      render_schet = font.render(f"{player_2_schet}", True, pygame.Color("darkorange"))
      screen.blit(render_schet, (WIDTH // 2 + 55, 60))

      if player_1_schet < 10 and player_2_schet < 10:
         ball.x += ball_speed * dx
         ball.y += ball_speed * dy

      if ball.colliderect(paddle_1) and dx < 0:
         dx, dy, ball_speed, paddle_speed = detect_collision(dx, dy, ball, paddle_1, ball_speed, paddle_speed)
         
      if ball.colliderect(paddle_2) and dx > 0:
         dx, dy, ball_speed, paddle_speed = detect_collision(dx, dy, ball, paddle_2, ball_speed, paddle_speed)

      if ball.centery < ball_radius + 50 or ball.centery > HEIGHT - ball_radius - 50:
         dy = -dy

      if ball.centerx < 0:
         player_2_schet += 1
         ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_rect, ball_rect)
         dx, dy = rnd(-1,2,2), rnd(-1,2,2)
         ball_speed = 6
         paddle_speed = 10

      if ball.centerx > 1200:
         player_1_schet += 1
         ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_rect, ball_rect)
         dx, dy = rnd(-1,2,2), rnd(-1,2,2)
         ball_speed = 6
         paddle_speed = 10

      pygame.draw.circle(screen, pygame.Color("white"), ball.center, ball_radius)

      pygame.draw.rect(screen, pygame.Color("white"), line)
      pygame.draw.rect(screen, pygame.Color("black"), block_1)
      pygame.draw.rect(screen, pygame.Color("black"), block_2)
      render_schet = font_2.render(f"""player 1                                                                                        player 2""", True, pygame.Color("darkorange"))
      screen.blit(render_schet, (15, 0)) 

      for event in pygame.event.get():
         # Если выключаем вкладку - программа выключается
         if event.type == pygame.QUIT:
            menu()

      key = pygame.key.get_pressed()

      # А это обрабатываем нажатия 
      if player_1_schet < 10 and player_2_schet < 10:
         if key[pygame.K_w] and paddle_1.y > 50:
            paddle_1.y -= paddle_speed
         if key[pygame.K_s] and paddle_1.y < HEIGHT - 300:
            paddle_1.y += paddle_speed
         if key[pygame.K_UP] and paddle_2.y > 50:
            paddle_2.y -= paddle_speed
         if key[pygame.K_DOWN] and paddle_2.y < HEIGHT - 300:
            paddle_2.y += paddle_speed

      else:
         if player_1_schet == 10:
            win_player = "Player 1"
         else:
            win_player = "Player 2"
         while True:
            render_win = font_win.render(win_player, True, pygame.Color("orange"))
            screen.blit(render_win, (WIDTH // 3 - 10, HEIGHT // 3 - 100))
            render_win = font_win.render("GAME WIN", True, pygame.Color("orange"))
            screen.blit(render_win, (WIDTH // 3 - 120, HEIGHT // 3 + 20))
            pygame.display.flip()
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                     menu()
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
               game_ping_pong()

      pygame.display.flip()
      clock.tick(fps)

# Главное меню
def menu():
   pygame.init()
   pygame.font.init()

   screen = pygame.display.set_mode((1200, 800))

   img_1 = pygame.image.load("icons_game\\game_arcanoid.jpg").convert()
   img_3 = pygame.image.load("icons_game\\game_fastclick.jpg").convert()
   img_2 = pygame.image.load("icons_game\\game_snake.jpg").convert()
   img_4 = pygame.image.load("icons_game\\game_21.jpg").convert()
   img_5 = pygame.image.load("icons_game\\game_ping_pong.jpg").convert()

   while True:
      for event in pygame.event.get():

         # Закрашиваем фон цветом 65 25 60
         screen.fill((60, 25, 60))

         # Получаем данные о местонахождении мыши
         mouse = pygame.mouse.get_pos()

         # Процесс выхода из вкладки
         if event.type == pygame.QUIT:
            pygame.quit()

         # Проверка клика мыши
         if event.type == pygame.MOUSEBUTTONDOWN:

            # Если нажимают на "картинку игры" арканоид, то включается игра
            if 75 <= mouse[0] <= 75 + 250 and 75 <= mouse[1] <= 75 + 250:
               game_arcanoid()

            if 475 <= mouse[0] <= 475 + 250 and 75 <= mouse[1] <= 75 + 250:
               game_snake()

            if 875 <= mouse[0] <= 875 + 250 and 75 <= mouse[1] <= 75 + 250:
               game_FastClick()

            if 75 <= mouse[0] <= 75 + 250 and 475 <= mouse[1] <= 475 + 250:
               game_21o4ko()

            if 475 <= mouse[0] <= 475 + 250 and 475 <= mouse[1] <= 475 + 250:
               game_ping_pong()

            if 875 <= mouse[0] <= 875 + 250 and 475 <= mouse[1] <= 475 + 250:
               pass

         screen.blit(img_1, (75, 75))
         screen.blit(img_2, (475, 75))
         screen.blit(img_3, (875, 75))
         screen.blit(img_4, (75, 475))
         screen.blit(img_5, (475, 475))
         # screen.blit(img_6, (875, 75))

         pygame.display.update()

menu()