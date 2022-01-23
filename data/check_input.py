import pygame

def check(event, left, right, up, down):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            left = True
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            right = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            up = True                
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            down = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            left = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            right = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            up = False               
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            down = False
    return left, right, down, up