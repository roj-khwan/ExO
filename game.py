import pygame
from Tools import exo
from Models.Genetic import Agent, workshop as ws
from Models.Minimax import BestMove

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

def RunGame(isHumanFirst, func):
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

    run = True
    win = 0
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            #Human Turn
            if event.type == pygame.MOUSEBUTTONDOWN and win == 0 and turn == 0:
                #get mouse pos turn into grid pos
                posx, posy = pygame.mouse.get_pos()
                pos = ((posx - OFFSET) // GRID_SIZE, (posy - OFFSET) // GRID_SIZE)

                pos = (int(max(min(pos[0], 2), 0)), int(max(min(pos[1], 2), 0)))

                if not exo.CheckEmpty(board, pos[0], pos[1]): continue

                board[pos[1]][pos[0]] = str(turn)

                UpdateBoard(board)

                win = exo.CheckWin(board, turn)
                if win != 0:
                    txt = FONT.render(f'{["Blue", "Red"][int(turn)]} Win!', True, WHITE, BLACK)
                    rect = txt.get_rect(center = (SCREEN_SIZE / 2 + OFFSET, SCREEN_SIZE / 2 + OFFSET))
                    SCREEN.blit(txt, rect)
                elif exo.CheckGameEnd(board):
                    txt = FONT.render("It\'s a Tie", True, WHITE, BLACK)
                    rect = txt.get_rect(center = (SCREEN_SIZE / 2 + OFFSET, SCREEN_SIZE / 2 + OFFSET))
                    SCREEN.blit(txt, rect)

                turn = abs(turn - 1)

            # #Bot Turn
            elif event.type == pygame.MOUSEBUTTONDOWN and win == 0 and turn == 1:

                move = func(board)

                if not exo.CheckEmpty(board, move): continue

                board[move // 3][move % 3] = str(turn)

                UpdateBoard(board)

                win = exo.CheckWin(board, turn)
                if win != 0:
                    txt = FONT.render(f'{["Blue", "Red"][int(turn)]} Win!', True, WHITE, BLACK)
                    rect = txt.get_rect(center = (SCREEN_SIZE / 2 + OFFSET, SCREEN_SIZE / 2 + OFFSET))
                    SCREEN.blit(txt, rect)
                elif exo.CheckGameEnd(board):
                    txt = FONT.render("It\'s a Tie", True, WHITE, BLACK)
                    rect = txt.get_rect(center = (SCREEN_SIZE / 2 + OFFSET, SCREEN_SIZE / 2 + OFFSET))
                    SCREEN.blit(txt, rect)

                turn = abs(turn - 1)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":

    agent = Agent(ws.ChromoCaller('D:\Code-Vault\Intelligence-Trailblazer\EXO\Models\Genetic\Gnomes\ID-4919_Gen-20.txt', 31), 1)

    func = lambda board : agent.FindBestMove(board)

    RunGame(True, func)