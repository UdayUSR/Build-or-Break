import pygame
import random

pygame.init()
width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Build or Break')
clock = pygame.time.Clock()
#Fonts
myfont = pygame.font.Font(None, 24)
mymediumfont = pygame.font.Font(None, 30)
myfontLarge = pygame.font.Font(None, 48)
#Variables
humanScore = 0
aiScore = 0
bgSky_width = 0
humanTurn = True
gotNumber = False
increse = "Increase?"
decrease = "Decrease?"

# Define number button properties
num_button_radius = 50
num_button_pos = (width // 2, height // 2)
numberButtonText = "Tap"
numberButtonColor = "Purple"
numberButtonTextColor = "White"

# Human/AI increase/decrease buttons properties
id_button_width = 100
id_button_height = 30
id_button_margin = 5
humanbuttonrect = pygame.Rect(width // 4 - id_button_width // 2, height * 3 // 4 - id_button_height // 2+90, id_button_width, id_button_height)
aibuttonrect = pygame.Rect(width*3 // 4 - id_button_width // 2, height * 3 // 4 - id_button_height // 2+90, id_button_width, id_button_height)



# Define function to check if a point is inside the button
def is_inside_num_button(pos):
    button_x, button_y = num_button_pos
    x, y = pos
    distance = ((x - button_x) ** 2 + (y - button_y) ** 2) ** 0.5
    return distance <= num_button_radius



#Block Building
#Block Properties
block_width = 70
block_height = 20
block_margin = 2
# Define the class for a block
class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([block_width, block_height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#Surfaces
bgSky  = pygame.image.load("photo/longsky.png").convert_alpha()
bgSky_rect = bgSky.get_rect(topleft = (0,0))

turntexthu = myfontLarge.render("Human's Turn", False, "Brown")
turntextai = myfontLarge.render("AI's Turn", False, "Brown")
aiupdatetext1 = myfontLarge.render("", False, "Brown")
aiupdatetext2 = myfontLarge.render("", False, "Brown")
# Render labels
human_label = myfont.render("Human - "+str(humanScore), True, "Brown")
ai_label = myfont.render("AI - "+str(aiScore), True, "Brown")

# Win Declaration
# human_win = myfontLarge.render("Human Wins!", False, "White")
# ai_win = myfontLarge.render("AI Wins!", False, "White")
playagainrect = pygame.Rect(width // 2 - id_button_width // 2-200, height * 3 // 4 - id_button_height // 2, id_button_width+100, id_button_height+20)
Quitrect = pygame.Rect(width // 2 - id_button_width // 2+120, height * 3 // 4 - id_button_height // 2, id_button_width+100, id_button_height+20)




# check if the game is over
def is_game_over(hum, ai):
    if hum == 20 or ai == 20:
        return True
    else:
        return False

# result evaluation
def eval_result(hum, ai):
    print("eval_result hum: ", hum, "ai: ", ai)
    if hum > ai:
        return -1
    elif ai > hum:
        return 1
    else:
        return 0

# Minimax algorithm
def minimax(hum, ai, depth, alpha, beta, maximizing_player):
    if is_game_over(hum, ai) or depth == 2:
        return eval_result(hum, ai)

    if maximizing_player:
        max_eval = float("-inf")
        for i in range(-8,9):
            if i <= 0:
                prev = hum
                hum += i
                if hum < 0:
                    hum = 0

                eval = minimax(hum, ai, depth + 1, alpha, beta, False)
                hum = prev
            else:
                prev = ai
                ai += i
                if ai > 20:
                    ai = 20
            
                eval = minimax(hum, ai, depth + 1, alpha, beta, False)
                ai = prev
            max_eval = max(max_eval, eval)
            alpha = max(alpha, max_eval)

        return max_eval
    


    else:
        min_eval = float("inf")
        for i in range(-8,9):
            if i > 0:
                prev = hum
                hum += i
                if hum < 0:
                    hum = 0

                eval = minimax(hum, ai, depth + 1, alpha, beta, True)
                hum = prev
            else:
                prev = ai
                ai += i
                if ai > 20:
                    ai = 20
            
                eval = minimax(hum, ai, depth + 1, alpha, beta, True)
                ai = prev

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

          
        return min_eval
    

#calculate the best move for AI
def make_ai_move(hum, ai, pnt):
    best_move = float("-inf")
    
    prev = hum
    hum -= pnt
    if hum < 0:
        hum = 0

    dec_val = minimax(hum, ai, 0, float("-inf"), float("inf"), False)
    hum = prev

    prev = ai
    ai += pnt
    if ai > 20:
        ai = 20
        
    inc_val = minimax(hum, ai, 0, float("-inf"), float("inf"), False)
    ai = prev

    
    if inc_val== -1 and dec_val== -1 and (hum-ai)>2 and hum>12:
        best_move =0

    elif dec_val > inc_val:
        best_move = 0

    else:
        best_move = 1
    
    print("inc_val: ", inc_val, "dec_val: ", dec_val)
    return best_move









while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 
    
    if aiScore >= 20 or humanScore >= 20:
        screen.fill("Brown")
        if aiScore > humanScore:
            ai_win = myfontLarge.render("AI incresed "+str(random_number)+" and Won!", False, "White")
            screen.blit(ai_win, (width // 2 - ai_win.get_width() // 2, height // 2 - ai_win.get_height() // 2-50-50))
            print("AI wins")
        if humanScore > aiScore:
            human_win = myfontLarge.render("Human Won!", False, "White")
            screen.blit(human_win, (width // 2 - human_win.get_width() // 2, height // 2 - human_win.get_height() // 2))
            print("Human wins")
        pygame.draw.rect(screen, "Purple", playagainrect)
        pygame.draw.rect(screen, "White", playagainrect, 3)
        playagain = myfontLarge.render("Play Again", False, "Black")
        screen.blit(playagain, (playagainrect.centerx - playagain.get_width() // 2, playagainrect.centery - playagain.get_height() // 2))
        pygame.draw.rect(screen, "Purple", Quitrect)
        pygame.draw.rect(screen, "White", Quitrect, 3)
        Quit = myfontLarge.render("Quit", False, "Black")
        screen.blit(Quit, (Quitrect.centerx - Quit.get_width() // 2, Quitrect.centery - Quit.get_height() // 2))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if playagainrect.collidepoint(pos):
                    humanScore = 0
                    aiScore = 0
                    humanTurn = True
                    aiupdatetext1 = myfont.render("", False, "White")
                    aiupdatetext2 = myfont.render("", False, "White")
                    continue
                if Quitrect.collidepoint(pos):
                    pygame.quit()
                    exit()
        # pygame.quit()
        # exit()
        pygame.display.flip()
        clock.tick(60)
        continue
    #Block Printing
    # Create a list for all blocks
    all_blocks = pygame.sprite.Group()
    # Create blocks for the human player
    for i in range(humanScore):
        if i > 19:
            break
        x = width // 4 - block_width // 2
        y = (block_height + block_margin) * (19-i) + block_margin
        block = Block("Black", x, y+50)
        all_blocks.add(block)

    # Create blocks for the computer player
    for i in range(aiScore):
        if i > 19:
            break
        x = width * 3 // 4 - block_width // 2
        y = (block_height + block_margin) *(19-i) + block_margin
        block = Block("Black", x, y+50)
        all_blocks.add(block)
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button clicked
            mouse_pos = pygame.mouse.get_pos()
            if is_inside_num_button(mouse_pos) and gotNumber == False:
                # Generate random number and update the text
                random_number1 = random.randint(0, 4)
                random_number2 = random.randint(0, 4)
                random_number = (random_number1 + random_number2)%10
                numberButtonText = str(random_number)
                print(random_number)
                event.button = 0
                gotNumber = True
            if humanbuttonrect.collidepoint(mouse_pos) and gotNumber == True and humanTurn == True:
                humanScore += random_number
                humanTurn = False
                gotNumber = False
                numberButtonText = "Tap"
            if aibuttonrect.collidepoint(mouse_pos) and gotNumber == True and humanTurn == True:
                aiScore -= random_number
                if aiScore < 0:
                    aiScore = 0
                humanTurn = False
                gotNumber = False
                numberButtonText = "Tap"
            """if humanbuttonrect.collidepoint(mouse_pos) and gotNumber == True and humanTurn == False:
                humanScore -= random_number
                if humanScore < 0:
                    humanScore = 0
                humanTurn = True
                gotNumber = False
                numberButtonText = "Tap"
            if aibuttonrect.collidepoint(mouse_pos) and gotNumber == True and humanTurn == False:
                aiScore += random_number
                humanTurn = True
                gotNumber = False
                numberButtonText = "Tap" """
            if humanTurn == False and gotNumber == True:
                random_number1 = random.randint(0, 4)
                random_number2 = random.randint(0, 4)
                random_number = (random_number1 + random_number2)%10
                numberButtonText = str(random_number)
                print(random_number)
                event.button = 0
                gotNumber = True
                #asyncio.sleep(1)
                move = make_ai_move(humanScore, aiScore, random_number)
                print("move", move)
                if move == 1:
                    aiScore += random_number
                    humanTurn = True
                    gotNumber = False
                    numberButtonText = "Tap"
                    print("aiScore increased by", random_number)
                    aiupdatetext1 = mymediumfont.render("AI's Random number was "+str(random_number), False, "Brown")
                    aiupdatetext2 = mymediumfont.render("AI increased own score", False, "Brown")

                else:
                    humanScore -= random_number
                    if aiScore < 0:
                        aiScore = 0
                    humanTurn = True
                    gotNumber = False
                    numberButtonText = "Tap"
                    print("humanScore decreased by", random_number)
                    aiupdatetext1 = mymediumfont.render("AI's Random number was "+str(random_number), False, "Brown")
                    aiupdatetext2 = mymediumfont.render("AI decreased human's score", False, "Brown")
            

    # Blits
    #screen.fill("White")
    bgSky_rect.x -= 4
    if bgSky_rect.right <= 700:
        bgSky_rect.left = 0
    screen.blit(bgSky, bgSky_rect)
    if humanTurn == True:
        screen.blit(turntexthu, (width//2-100, height//2-280))
    if humanTurn == False:
        screen.blit(turntextai, (width//2-70, height//2-280))
    # Draw all blocks
    all_blocks.draw(screen)
    # Draw labels
    # Render labels
    human_label = myfont.render("Human - "+str(humanScore), True, "Brown")
    ai_label = myfont.render("AI - "+str(aiScore), True, "Brown")
    screen.blit(human_label, (width // 4 - human_label.get_width() // 2, height - 100))
    screen.blit(ai_label, (width * 3 // 4 - ai_label.get_width() // 2, height - 100))

    # Draw the numberbutton
    pygame.draw.circle(screen, "Purple", num_button_pos, num_button_radius)
    pygame.draw.circle(screen, "BLACK", num_button_pos, num_button_radius, 3)

    #draw the increase/decrease buttons
    
    if humanTurn == True and gotNumber == True:
        pygame.draw.rect(screen, "Brown", humanbuttonrect)
        hum_button_text = myfont.render("Increse "+str(numberButtonText)+"?", True, "White")
        screen.blit(hum_button_text, (humanbuttonrect.centerx - hum_button_text.get_width() // 2, humanbuttonrect.centery - hum_button_text.get_height() // 2))
        pygame.draw.rect(screen, "Brown", aibuttonrect)
        ai_button_text = myfont.render("Decrease "+str(numberButtonText)+"?", True, "White")
        screen.blit(ai_button_text, (aibuttonrect.centerx - ai_button_text.get_width() // 2, aibuttonrect.centery - ai_button_text.get_height() // 2))
    if humanTurn == False and gotNumber == True:
        pygame.draw.rect(screen, "Brown", humanbuttonrect)
        hum_button_text = myfont.render("Decrease "+str(numberButtonText)+"?", True, "White")
        screen.blit(hum_button_text, (humanbuttonrect.centerx - hum_button_text.get_width() // 2, humanbuttonrect.centery - hum_button_text.get_height() // 2))
        pygame.draw.rect(screen, "Brown", aibuttonrect)
        ai_button_text = myfont.render("Increse "+str(numberButtonText)+"?", True, "White")
        screen.blit(ai_button_text, (aibuttonrect.centerx - ai_button_text.get_width() // 2, aibuttonrect.centery - ai_button_text.get_height() // 2))
    if humanTurn == True and gotNumber == False:
        screen.blit(aiupdatetext1, (width//2-(aiupdatetext1.get_width())/2, height//2-aiupdatetext1.get_height()//2-160))
        screen.blit(aiupdatetext2, (width//2-(aiupdatetext2.get_width())/2, height//2-aiupdatetext2.get_height()//2-140))



    # Draw the text
    text_surface = myfont.render(numberButtonText, True, "White")
    text_rect = text_surface.get_rect(center=num_button_pos)
    screen.blit(text_surface, text_rect)

    pygame.display.update()
    clock.tick(60)