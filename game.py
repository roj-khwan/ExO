import pygame
import Tools as exo
from Models.Genetic import Agent

SCREEN_SIZE = 450
GRID_SIZE = SCREEN_SIZE / 3
OFFSET = 25
LINE_WIDTH = 10
BORDER = SCREEN_SIZE

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (90, 202, 224)
RED = (245, 42, 85)

def UpdateBoard(board = exo.InitBoard()):
    
    for x in range(3):
        for y in range(3):
            coin = board[y][x]

            size = GRID_SIZE

            rect = lambda : pygame.Rect(
                OFFSET + GRID_SIZE * x + (GRID_SIZE - size) / 2, 
                OFFSET + GRID_SIZE * y + (GRID_SIZE - size) / 2, 
                size, size)
            
            if coin == '0':

                size = size * .8
                pygame.draw.rect(SCREEN, BLUE, rect(), LINE_WIDTH, int(size))

            elif coin == '1':

                size = size * .75
                pygame.draw.rect(SCREEN, RED, rect(), LINE_WIDTH)

if __name__ == "__main__":
    global SCREEN

    pygame.init()

    board = exo.InitBoard()
    turn = 0

    #region Screen
    SCREEN = pygame.display.set_mode((SCREEN_SIZE + OFFSET * 2, SCREEN_SIZE + OFFSET * 2))
    FONT = pygame.font.Font(pygame.font.get_default_font(), 25)
    SCREEN.fill(WHITE)

    pygame.draw.line(SCREEN, BLACK, 
                     (OFFSET, OFFSET + GRID_SIZE), 
                     (OFFSET + SCREEN_SIZE, OFFSET + GRID_SIZE), 
                     LINE_WIDTH)

    pygame.draw.line(SCREEN, BLACK, 
                     (OFFSET, OFFSET + GRID_SIZE * 2), 
                     (OFFSET + SCREEN_SIZE, OFFSET + GRID_SIZE * 2), 
                     LINE_WIDTH)

    pygame.draw.line(SCREEN, BLACK, 
                     (OFFSET + GRID_SIZE, OFFSET), 
                     (OFFSET + GRID_SIZE, OFFSET + SCREEN_SIZE), 
                     LINE_WIDTH)

    pygame.draw.line(SCREEN, BLACK, 
                     (OFFSET + GRID_SIZE * 2, OFFSET),
                     (OFFSET + GRID_SIZE * 2, OFFSET + SCREEN_SIZE), 
                     LINE_WIDTH)
    #endregion Screen

    agent = Agent(
        '14030186 19001187 18030673 02021661 14150485 12191321 17061728 01110658 13041223 08161315 04070232 03191107 13150172 12000723 14050369 06081660 03190690 13151559 03181396 05141064 17060332 14010492 06141287 06031029 11020365 03030166 19071673 03100446 07101282 14161126 15170432 11151713',
        1)

    run = True
    win = 0
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and win == 0:
                #get mouse pos turn into grid pos
                posx, posy = pygame.mouse.get_pos()
                pos = ((posx - OFFSET) // GRID_SIZE, (posy - OFFSET) // GRID_SIZE)

                pos = (int(max(min(pos[0], 2), 0)), int(max(min(pos[1], 2), 0)))

                #if grid not empty then allow play
                if exo.CheckEmptyByXY(board, pos[0], pos[1]):
                    board[pos[1]][pos[0]] = str(turn)

                    UpdateBoard(board)
                    win = exo.CheckWin(board, turn)

                    if win != 0:
                        print(win)
                        txt = FONT.render(f'{["Blue", "Red"][int(turn)]} Win!', True, WHITE, BLACK)
                        rect = txt.get_rect(center = (SCREEN_SIZE / 2 + OFFSET, SCREEN_SIZE / 2 + OFFSET))
                        SCREEN.blit(txt, rect)
                    elif exo.CheckGameEnd(board):
                        print(win)
                        txt = FONT.render("It\'s a Tie", True, WHITE, BLACK)
                        rect = txt.get_rect(center = (SCREEN_SIZE / 2 + OFFSET, SCREEN_SIZE / 2 + OFFSET))
                        SCREEN.blit(txt, rect)
                    

                    if agent.side == abs(turn - 1):
                        print(agent.FindBestMove(board))

                    turn = abs(turn - 1)

        pygame.display.update()

    pygame.quit()