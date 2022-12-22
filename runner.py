import pygame 
import sys
import time
import os
import tictactoe as ttt
# untuk memanggil beberapa library yang akan digunakan

pygame.init()
size = width, height = 1080, 720  
#untuk mengatur ukuran layar




# untuk mengatur warna yang akan digunakan
dark = (45, 3, 59)          
purple = (193, 71, 233)                                                         

# untuk memangil size layar
screen = pygame.display.set_mode(size)

# untuk mengatur font yang akan digunakan dengan library pygame
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None                                                                     # user is none in the beginning
board = ttt.initial_state()                                                     # board is empty in the beginning                                            
ai_turn = False                                                                 # ai_turn is false in the beginning

while True:

    for event in pygame.event.get():                                            # Check for events
        if event.type == pygame.QUIT:                                           # If user clicks close
            sys.exit()                                                          # Exit the program

    screen.fill(dark)

    # Let user choose a player.
    if user is None:                                                            # If user is not chosen yet

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, purple)               # Text of title
        titleRect = title.get_rect()                                            # Get the rectangle of the text                 
        titleRect.center = ((width / 2), 50)                                    # Center the text in the screen
        screen.blit(title, titleRect)                                           # Draw the text

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)     # Width of button is 1/4 of the screen width
        playX = mediumFont.render("Play as X", True, dark)                     # Text of button
        playXRect = playX.get_rect()                                            # Get the rectangle of the text
        playXRect.center = playXButton.center                                   # Center the text in the button
        pygame.draw.rect(screen, purple, playXButton)                            # Draw the button
        screen.blit(playX, playXRect)                                           # Draw the text

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50) # Width of button is 1/4 of the screen width
        playO = mediumFont.render("Play as O", True, dark)                      # Text of button
        playORect = playO.get_rect()                                            # Get the rectangle of the text                                 
        playORect.center = playOButton.center                                   # Center the text in the button
        pygame.draw.rect(screen, purple, playOButton)                           # Draw the button
        screen.blit(playO, playORect)                                           # Draw the text

        # Check if button is clicked    
        click, _, _ = pygame.mouse.get_pressed()                        # Get the mouse state
        if click == 1:                                                  # If left mouse button is clicked             
            mouse = pygame.mouse.get_pos()                              # Get the mouse position
            if playXButton.collidepoint(mouse):                         # If mouse is inside the button
                time.sleep(0.2)                                         # Wait for 0.2 seconds
                user = ttt.X                                            # Set user to X
            elif playOButton.collidepoint(mouse):                       # If mouse is inside the button
                time.sleep(0.2)                                         # Wait for 0.2 seconds
                user = ttt.O                                            # Set user to O

    else:

        # Draw game board
        tile_size = 80                                              # Size of each tile
        tile_origin = (width / 2 - (1.5 * tile_size),               # Top left corner of the board
                       height / 2 - (1.5 * tile_size))              # Top left corner of the board
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, purple, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, purple)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        
        
        


        # Draw Return button
        returnbutton = pygame.Rect(0, 0, 100, 50)
        returnb = mediumFont.render("Back", True, dark)
        returnrect = returnb.get_rect()
        returnrect.center = returnbutton.center
        pygame.draw.rect(screen, purple, returnbutton)
        screen.blit(returnb, returnrect)

        # Check if Return button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if returnbutton.collidepoint(mouse):
                time.sleep(0.2)
                user = None
                board = ttt.initial_state()
                ai_turn = False

        # Draw Exit button
        exitbutton = pygame.Rect(width - 100, 0, 100, 50)
        exitb = mediumFont.render("Exit", True, dark)
        exitrect = exitb.get_rect()
        exitrect.center = exitbutton.center
        pygame.draw.rect(screen, purple, exitbutton)
        screen.blit(exitb, exitrect)

        # Check if Exit button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if exitbutton.collidepoint(mouse):
                time.sleep(0.2)
                sys.exit()
                

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, purple)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, dark)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, purple, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False


    # Update display
    pygame.display.flip()


