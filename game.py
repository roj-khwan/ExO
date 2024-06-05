import pygame
from Tools import exo
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
        '1070021537 0060051316 1150031506 1190061524 0030040637 0020080516 1111011138 0011051150 0031100185 0011091080 0020020576 1050031208 0050050430 0071111353 0070020051 0041061558 1190060320 0000080330 1031020331 1170031415 1000060488 1101060541 0051011490 1020070047 0030000260 1061031654 0040031526 0020070209 1141011625 0030041137 0000011592 0010001493 1070050175 1020040692 0001000409 1041000370 1180030241 1160031026 0010000020 1050030240 1050010214 0031000489 1140040571 0071031399 1141130516 0040030206 1171021437 1170080638 1010010175 0040000560 0001070224 1190021524 1050030276 0000031551 0061081132 1110061166 1030001659 0071011573 0000050225 1040030617 1110001004 0081011499 0060041122 1120080368 0031080133 0081150526 1070030026 0010000720 0030040415 0060040728 0010011578 0060030659 0051140488 0031051121 1010051438 0051071311 1150061220 0051031150 0001010473 1040050081 0040080345 1120021182 1150080352 1020011245 1170071445 1081020601 0050081677 1060071417 1151010023 0020061033 1011001337 1151011662 0071141243 0030051355 0070031214 1090060255 0070020296 1161131299 0070081327 0060061345',
        1)

    run = True
    win = 0
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and win == 0 and turn == 0:
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

                    turn = abs(turn - 1)
                    
                    # exo.PrintBoard(board)

                    # move = agent.FindBestMove(board)

                    # print(move)

                    # board[move // 3][move % 3] = str(abs(turn - 1))

                    # UpdateBoard(board)
                    # win = exo.CheckWin(board, abs(turn - 1))

                    # if win != 0:
                    #     print(win)
                    #     txt = FONT.render(f'{["Blue", "Red"][int(abs(turn - 1))]} Win!', True, WHITE, BLACK)
                    #     rect = txt.get_rect(center = (SCREEN_SIZE / 2 + OFFSET, SCREEN_SIZE / 2 + OFFSET))
                    #     SCREEN.blit(txt, rect)
                    # elif exo.CheckGameEnd(board):
                    #     print(win)
                    #     txt = FONT.render("It\'s a Tie", True, WHITE, BLACK)
                    #     rect = txt.get_rect(center = (SCREEN_SIZE / 2 + OFFSET, SCREEN_SIZE / 2 + OFFSET))
                    #     SCREEN.blit(txt, rect)

            if event.type == pygame.MOUSEBUTTONDOWN and win == 0 and turn == 1:
                exo.PrintBoard(board)

                move = agent.FindBestMove(board)

                print(move)

                board[move // 3][move % 3] = str(turn)

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

                turn = abs(turn - 1)

        pygame.display.update()

    pygame.quit()