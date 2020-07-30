import random
import time

import pygame

# //TODO: MAKE THE GAME LOOP A WHILE TRUE ONE, NOT A RECURSIVE ONE!
'''
pygame.display.update must never be called more than once. Add it at the end of every function that draws.
'''
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
gray = (105, 105, 105)
red = (177, 0, 0)
green = (0, 177, 0)
blue = (0, 0, 177)

displayWidth = 1280
displayHeight = 720
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), 0)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


class wall:
    def __init__(self, gridSize):
        self.x = random.randrange(0, displayWidth, gridSize)
        self.y = random.randrange(0, displayHeight, gridSize)
        self.color = black
        self.size = gridSize
        self.maxLength = 10
        self.length = random.randint(1, self.maxLength)
        self.walls = [[self.x, self.y]]
        self.wallDirectionX = 0
        self.wallDirectionY = 0

    def updater(self, gridSize, displayWidth, displayHeight):
        while (gridSize * 16 >= self.x >= gridSize * 3) or (
                gridSize * 13 >= self.y >= gridSize * 7):
            self.x = random.randrange(0, displayWidth, gridSize)
            self.y = random.randrange(0, displayHeight, gridSize)

        self.walls = [[self.x, self.y]]
        self.maxLength += 5
        if random.choice([1, 2]) == 1:
            self.wallDirectionX = random.choice([-1, 1])
        else:
            self.wallDirectionY = random.choice([-1, 1])

        for i in range(0, self.length):
            lastCoordinates = self.walls[-1]
            wallX = lastCoordinates[0] + (gridSize * self.wallDirectionX)
            wallY = lastCoordinates[1] + (gridSize * self.wallDirectionY)
            self.walls.append([wallX, wallY])

        for coordinates in self.walls:
            # coordinatesdex = self.walls.index(coordinates)
            if (coordinates[0] >= displayWidth - gridSize or coordinates[0] <= gridSize or
                    coordinates[1] >= displayHeight - gridSize or coordinates[1] <= gridSize or
                    coordinates[0] <= gridSize * 10 or coordinates[1] <= gridSize * 3):
                self.walls.remove(coordinates)


class snake:

    def __init__(self, color, gridSize):
        self.x = int(gridSize * 10)
        self.y = int(gridSize * 10)
        self.size = gridSize
        self.color = color
        self.directionX = gridSize
        self.directionY = 0
        self.score = 0  # Score is the length - 3
        self.tailCoordinates = [[self.x - gridSize * 2, self.y], [self.x - gridSize * 3, self.y],
                                [self.x - gridSize * 4, self.y]]
        self.length = 3
        self.up = 0
        self.down = 1
        self.right = 2
        self.left = 3
        self.KeysPressed = []

    def move(self, theKey, gridSize):
        # Gets the current location and adds the direction (based on last key pressed) until a new key is pressed

        if theKey == pygame.K_UP and self.directionY != gridSize:
            self.directionY = gridSize * -1
            self.directionX = 0
            self.KeysPressed.append(self.up)

        elif theKey == pygame.K_DOWN and self.directionY != gridSize * -1:
            self.directionY = gridSize
            self.directionX = 0
            self.KeysPressed.append(self.down)

        elif theKey == pygame.K_LEFT and self.directionX != gridSize:
            self.directionY = 0
            self.directionX = gridSize * -1
            self.KeysPressed.append(self.left)

        elif theKey == pygame.K_RIGHT and self.directionX != gridSize * -1:
            self.directionY = 0
            self.directionX = gridSize
            self.KeysPressed.append(self.right)

        self.x += self.directionX
        self.y += self.directionY

    def collisionCheck(self, walls, displayWidth, displayHeight):
        # Return True if snake has collided with walls borders or itself.
        if (self.x > displayWidth or self.x < 0 or
                self.y > displayHeight or self.y < 0):
            # Check if snake collided with the borders
            drawText(font="freesansbold.ttf", gameText="You lost!", gameTextSize=100, gameTextColor=white,
                     gameTextCoordinates=(displayWidth / 3, displayHeight / 2.5))
            pygame.display.update()  # display the text
            print("Cause of death: hit a border")
            time.sleep(2)
            return True

        for wall in walls:
            for coordinates in wall.walls:
                # Check if snake collided with the walls
                if self.x == coordinates[0] and self.y == coordinates[1]:
                    drawText(font="freesansbold.ttf", gameText="You lost!", gameTextSize=100, gameTextColor=white,
                             gameTextCoordinates=(displayWidth / 3, displayHeight / 2.5))
                    pygame.display.update()  # display the text
                    print("Cause of death: hit a wall")
                    time.sleep(2)
                    return True

        for tailCoordinates in self.tailCoordinates[1:]:
            if self.x == tailCoordinates[0] and self.y == tailCoordinates[1]:
                drawText(font="freesansbold.ttf", gameText="You lost!", gameTextSize=100, gameTextColor=white,
                         gameTextCoordinates=(displayWidth / 3, displayHeight / 2.5))
                pygame.display.update()  # display the text
                print("Cause of death: eaten himself")
                time.sleep(2)
                return True

        else:
            return False

    def applecollision(self, snake, apple):
        if apple.x == snake.x and apple.y == snake.y:
            self.score += 1
            self.length += 1
            return True  # Returns True if apple is eaten

        else:
            return False

    def ratcollision(self, snake, rat):
        if rat.x == snake.x and rat.y == snake.y:
            self.score += 5
            self.length += 5
            return True  # Returns True if rat is eaten

        else:
            return False

    def tail(self, appleEaten, lengthCheat, ratEaten):
        # This function creates a tail where the snake's body is and removes the last tail segment.
        # It doesn't delete in the same frame as the snake eats an apple, allowing the tail to grow by one.
        self.tailCoordinates.insert(0, [self.x, self.y])
        if not appleEaten and not lengthCheat:
            del self.tailCoordinates[-1]

        if ratEaten:
            # insert 5 hidden tail segments if a rat is eaten, it allows the tail to grow by 5.
            self.tailCoordinates.insert(-1, [-40, -40])  # Can not insert more than 1 element
            self.tailCoordinates.insert(-1, [-40, -40])
            self.tailCoordinates.insert(-1, [-40, -40])
            self.tailCoordinates.insert(-1, [-40, -40])
            self.tailCoordinates.insert(-1, [-40, -40])


class apple:
    def __init__(self, gridSize):
        self.x = 0
        self.y = 0
        self.color = red
        self.size = gridSize

    def updater(self, snake, walls, displayWidth, displayHeight, gridSize):
        oldX = self.x
        oldY = self.y
        for tailCoordinate in snake.tailCoordinates:
            # Checks if the apple is at the same coordinates as the x and y of the tail
            while self.x in tailCoordinate and self.y in tailCoordinate:
                self.x = random.randrange(0, displayWidth - gridSize, gridSize)
                self.y = random.randrange(0, displayHeight - gridSize, gridSize)

        while oldX == self.x and oldY == self.y:
            # Checks if the apple spawned in the same position
            self.x = random.randrange(0, displayWidth - gridSize, gridSize)
            self.y = random.randrange(0, displayHeight - gridSize, gridSize)

        for wall in walls:
            for coordinates in wall.walls:
                if self.x == coordinates[0] and self.y == coordinates[1]:
                    self.x = random.randrange(0, displayWidth - gridSize, gridSize)
                    self.y = random.randrange(0, displayHeight - gridSize, gridSize)


class rat:
    def __init__(self, gridSize):
        self.x = 0
        self.y = 0
        self.color = blue
        self.size = gridSize
        self.directionX = 0
        self.directionY = 0
        self.directionChance = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.moveChance = [1, 2, 3, 4]

    def move(self, snake, gridSize):
        if self.x <= 0:
            self.directionX = gridSize

        elif self.x >= displayWidth:
            self.directionX = gridSize * -1

        elif self.y <= 0:
            self.directionY = gridSize

        elif self.y >= displayHeight:
            self.directionY = gridSize * -1

        elif random.choice(self.directionChance) >= 7:
            self.directionX = random.choice([gridSize, gridSize * -1])
            self.directionY = random.choice([gridSize, gridSize * -1])

        if random.choice(self.moveChance) >= 3:
            self.x += self.directionX
            self.y += self.directionY

        for segment in snake.tailCoordinates:
            if self.x == segment[0] and self.y == segment[1]:
                self.directionX = self.directionX * -1
                self.directionY = self.directionY * -1
                self.x += self.directionX
                self.y += self.directionY

    def updater(self, snake, displayWidth, displayHeight, gridSize):
        oldX = self.x
        oldY = self.y
        for tailCoordinate in snake.tailCoordinates:
            # Checks if the rat is at the same coordinates as the x and y of the tail
            while self.x in tailCoordinate and self.y in tailCoordinate:
                self.x = random.randrange(0, displayWidth - gridSize, gridSize)
                self.y = random.randrange(0, displayHeight - gridSize, gridSize)

        if oldX == self.x and oldY == self.y:
            # Checks if the rat spawned in the same position
            self.x = random.randrange(0, displayWidth - gridSize, gridSize)
            self.y = random.randrange(0, displayHeight - gridSize, gridSize)


class ability:
    def __init__(self, abilityType, game):
        self.cooldown = 0  # Current time until the ability can be activated again
        self.regenCooldown = 0
        self.regenDuration = 0  # How much the ability lasts after being called
        self.duration = 0  # Current time of the ability's duration
        self.active = False
        self.type = abilityType
        self.normalSpeed = game.speed
        self.x = 0  # Where to draw the ability's icon and/or timer
        self.y = 0

    def main(self):
        if self.type == 0:
            # Speed ability
            self.x = 100
            self.y = 200
            self.regenDuration = 5
            self.regenCooldown = 5

    def countdown(self, game):
        if self.duration > 0 and self.active:
            # Countdown duration
            self.duration -= 1

        elif self.duration == 0:
            self.duration = self.regenDuration
            self.cooldown = self.regenCooldown
            game.speed = self.normalSpeed

            self.active = False

        elif self.cooldown > 0 and self.duration == self.regenDuration:
            # Countdown cooldown
            self.cooldown -= 1

    def speed(self, game):
        if self.cooldown == 0 and not self.active:
            self.active = True
            self.duration = self.regenDuration
            game.speed -= 1
            if game.speed <= 0:
                game.speed = 1


class level:
    def __init__(self, displayWidth, displayHeight):
        # Those are the default values for everything game related
        self.reset(displayWidth, displayHeight)

    def updater(self, displayWidth, displayHeight):
        # Used when going to a higher level

        # gridSize *= 0.9
        # gridSize = int(gridSize)
        self.gridSize = int(displayHeight / 24)
        self.level += 1
        self.numberOfWalls += 1
        if (self.level / 6).is_integer():
            # Make the snake go faster
            self.speed -= 1
        if self.score <= 40:
            self.score *= 1.8

        else:
            self.score *= 1.3
        self.score = int(self.score)

        self.snake = snake(color=green, gridSize=self.gridSize)
        self.rat = rat(gridSize=self.gridSize)
        self.apple = apple(gridSize=self.gridSize)
        self.walls = [wall(self.gridSize) for _ in range(self.numberOfWalls)]
        for walls in self.walls:
            walls.updater(self.gridSize, displayWidth, displayHeight)

        self.speedAbility = ability(abilityType=0, game=self)

        self.initialised = False

    def reset(self, displayWidth, displayHeight):
        # Those variables reset every time you lose/reset the game
        self.gridSize = int(displayHeight / 24)
        self.rightAlign = displayWidth / 1.7
        self.leftAlign = displayWidth / 5
        self.upAlign = displayHeight / 2
        self.resolutionInputUp = pygame.Rect(self.rightAlign, self.upAlign + self.gridSize * 4, self.gridSize,
                                             self.gridSize)
        self.resolutionInputDown = pygame.Rect(self.rightAlign + self.gridSize * 6.5, self.upAlign + self.gridSize * 4,
                                               self.gridSize, self.gridSize)

        self.appleEaten = False
        self.ratEaten = False
        self.gameOver = True
        self.theKey = 0  # Used to pass what key is pressed to the snake.move function

        self.level = 1
        self.score = 10  # Score required to get to the next level TODO: change score to levelscore
        self.fps = 60  # fps cap, default is 60
        self.frameCounter = 0
        self.speed = 4  # Snake speed, smaller is faster

        self.numberOfWalls = 1
        self.walls = [wall(self.gridSize) for _ in range(self.numberOfWalls)]
        self.snake = snake(color=green, gridSize=self.gridSize)
        self.apple = apple(self.gridSize)
        self.rat = rat(self.gridSize)

        self.speedAbility = ability(abilityType=0, game=self)

        self.lengthCheat = False

        self.debug = False
        self.initialised = False


def drawGrid(displayGrid, displayWidth, displayHeight, gridSize):
    if displayGrid:
        for i in range(0, displayHeight, gridSize):
            pygame.draw.lines(gameDisplay, white, False, [(0, i), (displayWidth, i)], 1)  # draw the grid lines

        for j in range(0, displayWidth, gridSize):
            pygame.draw.lines(gameDisplay, white, False, [(j, 0), (j, displayHeight)])


def drawText(font, gameText, gameTextSize, gameTextColor, gameTextCoordinates):
    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", gameTextSize)  # "freesansbold.ttf"
    TextSurface = font.render(gameText, True, gameTextColor)  # (text, anti-aliasing, color), creates an image
    gameDisplay.blit(TextSurface, gameTextCoordinates)  # (image, (x, y))


def drawMenu(fullScreen, displayWidth, displayHeight, rightAlign, leftAlign, upAlign, displayGrid, gridSize):
    gameDisplay.fill(gray)
    drawGrid(displayGrid, displayWidth, displayHeight, gridSize)

    # The resolution changer arrow, this is the one for resolution down
    pygame.draw.polygon(gameDisplay, white, [(rightAlign, upAlign + gridSize * 4.5),
                                             (rightAlign + gridSize, upAlign + gridSize * 4),
                                             (rightAlign + gridSize, upAlign + gridSize * 5)])

    pygame.draw.polygon(gameDisplay, white, [(rightAlign + gridSize * 7.5, upAlign + gridSize * 4.5),
                                             (rightAlign + gridSize * 6.5, upAlign + gridSize * 4),
                                             (rightAlign + gridSize * 6.5, upAlign + gridSize * 5)])

    drawText(font="freesansbold.ttf", gameText="PYGAME", gameTextSize=100, gameTextColor=green,
             gameTextCoordinates=(displayWidth / 3, displayHeight / 5 + gridSize * 2))
    drawText(font="freesansbold.ttf", gameText="Press enter to play", gameTextSize=gridSize, gameTextColor=white,
             gameTextCoordinates=(displayWidth / 3, displayHeight / 2 - gridSize))

    drawText(font="freesansbold.ttf", gameText="Controls:", gameTextSize=gridSize, gameTextColor=white,
             gameTextCoordinates=(leftAlign, upAlign + gridSize))
    drawText(font="freesansbold.ttf", gameText="W,A,S,D to move", gameTextSize=gridSize, gameTextColor=white,
             gameTextCoordinates=(leftAlign, upAlign + gridSize * 2))
    drawText(font="freesansbold.ttf", gameText="G to hide/show grid", gameTextSize=gridSize, gameTextColor=white,
             gameTextCoordinates=(leftAlign, upAlign + gridSize * 3))
    drawText(font="freesansbold.ttf", gameText="F for fullscreen", gameTextSize=gridSize, gameTextColor=white,
             gameTextCoordinates=(leftAlign, upAlign + gridSize * 4))
    drawText(font="freesansbold.ttf", gameText="Esc to exit", gameTextSize=gridSize, gameTextColor=white,
             gameTextCoordinates=(leftAlign, upAlign + gridSize * 5))

    drawText(font="freesansbold.ttf", gameText="Current options:", gameTextSize=gridSize, gameTextColor=white,
             gameTextCoordinates=(rightAlign, upAlign + gridSize))
    drawText(font="freesansbold.ttf", gameText="grid: " + str(displayGrid), gameTextSize=gridSize, gameTextColor=white,
             gameTextCoordinates=(rightAlign, upAlign + gridSize * 2))
    drawText(font="freesansbold.ttf", gameText="fullscreen: " + str(fullScreen), gameTextSize=gridSize,
             gameTextColor=white, gameTextCoordinates=(rightAlign, upAlign + gridSize * 3))
    drawText(font="freesansbold.ttf", gameText=str(displayWidth) + " x " + str(displayHeight), gameTextSize=gridSize,
             gameTextColor=white, gameTextCoordinates=(rightAlign + gridSize, upAlign + gridSize * 4))

    drawText(font="freesansbold.ttf", gameText="Hint: to catch a mouse, try to trap it with your body", gameTextSize=25,
             gameTextColor=blue, gameTextCoordinates=(displayWidth / 20, displayHeight / 2 + gridSize * 6))
    pygame.transform.scale(gameDisplay, (displayWidth, displayHeight))

    pygame.display.update()  # display the menu


def drawGame(snake, apple, rat, walls, speedAbility, levelScore, level, displayWidth, displayHeight, displayGrid, debug,
             gridSize):
    if snake.score > 0:
        score = str(snake.score)
    # Score is null at start for some reason...
    else:
        score = "0"

    gameDisplay.fill(gray)  # This line must always be at the top, it's the background
    pygame.draw.rect(gameDisplay, apple.color, (apple.x, apple.y, apple.size, apple.size),
                     0)  # Draw the apple, 0 at the end means fill
    pygame.draw.rect(gameDisplay, rat.color, (rat.x, rat.y, rat.size, rat.size), 0)  # Draw the rat
    pygame.draw.rect(gameDisplay, snake.color, (snake.x, snake.y, snake.size, snake.size), 0)  # Draw the snake

    for coordinates in snake.tailCoordinates:
        coordinateX = coordinates[0]
        coordinateY = coordinates[1]
        pygame.draw.rect(gameDisplay, snake.color, (coordinateX, coordinateY, snake.size, snake.size),
                         0)  # Draw the tail, a different rectangle for each segment.

    for wall in walls:
        for coordinates in wall.walls:
            coordinateX = coordinates[0]
            coordinateY = coordinates[1]
            pygame.draw.rect(gameDisplay, wall.color, (coordinateX, coordinateY, wall.size, wall.size),
                             0)  # Draw the walls

    drawGrid(displayGrid, displayWidth, displayHeight,
             gridSize)  # Text is drawn over the grid, anything above this line is drawn below it

    drawText(font="freesansbold.ttf", gameText=str(score) + " / " + str(levelScore), gameTextSize=gridSize,
             gameTextColor=white,
             gameTextCoordinates=(displayWidth / 1.12, displayHeight / 25))  # Current score and level score
    drawText(font="freesansbold.ttf", gameText="Current level: " + str(level), gameTextSize=gridSize,
             gameTextColor=white, gameTextCoordinates=(displayWidth / 35, displayHeight / 25))  # Current level
    drawText(font="freesansbold.ttf", gameText=str(speedAbility.duration) + "/" + str(speedAbility.cooldown),
             gameTextSize=gridSize,
             gameTextColor=white,
             gameTextCoordinates=(displayWidth / 35, displayHeight / 25 + gridSize))  # Speed ability

    if debug:
        drawText(font="freesansbold.ttf", gameText="FPS: " + str(int(clock.get_fps())), gameTextSize=25,
                 gameTextColor=white, gameTextCoordinates=(displayWidth / 2, displayHeight / 25))  # Show the FPS

    # pygame.transform.scale(gameDisplay, (displayWidth, displayHeight))
    pygame.display.update()  # This line must always be at the bottom, it displays the game


def gameStop(score):
    if score > 0:
        print("Your score was:", score, "Bye!")

    else:
        print("Bye!")

    pygame.quit()
    quit()


def gameLoop(displayGrid, fullScreen, resolutionIndex, game):
    while True:
        resolutionList = [[800, 600], [1240, 600], [1280, 720], [1366, 768], [1440, 900], [1920, 1080], [2560, 1440],
                          [3840, 2160]]
        currentResolution = resolutionList[resolutionIndex]
        displayWidth = currentResolution[0]
        displayHeight = currentResolution[1]

        while game.gameOver:

            # This is the menu
            game.reset(displayWidth, displayHeight)
            clock.tick(6)  # Lower FPS and less checks for the menu
            for event in pygame.event.get():
                # Gets what key is being pressed and does the appropriate action
                if event.type == pygame.QUIT:
                    gameStop(game.snake.score)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if game.resolutionInputUp.collidepoint(event.pos):
                        resolutionIndex -= 1
                        try:
                            currentResolution = resolutionList[resolutionIndex]
                        except IndexError:
                            resolutionIndex = -1
                            currentResolution = resolutionList[resolutionIndex]

                        displayWidth = currentResolution[0]
                        displayHeight = currentResolution[1]
                        game.reset(displayWidth, displayHeight)

                        if fullScreen:
                            gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), pygame.FULLSCREEN)
                        else:
                            gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), 0)

                    if game.resolutionInputDown.collidepoint(event.pos):
                        resolutionIndex += 1
                        try:
                            currentResolution = resolutionList[resolutionIndex]
                        except IndexError:
                            resolutionIndex = 0
                            currentResolution = resolutionList[resolutionIndex]

                        displayWidth = currentResolution[0]
                        displayHeight = currentResolution[1]
                        game.reset(displayWidth, displayHeight)

                        if fullScreen:
                            gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), pygame.FULLSCREEN)
                        else:
                            gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), 0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game.gameOver = False

                    if event.key == pygame.K_f:
                        fullScreen = not fullScreen

                        if fullScreen:
                            gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), pygame.FULLSCREEN)

                        else:
                            gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), 0)

                    elif event.key == pygame.K_ESCAPE:
                        gameStop(game.snake.score)

                    elif event.key == pygame.K_g:
                        displayGrid = not displayGrid

            drawMenu(fullScreen=fullScreen, displayWidth=displayWidth, displayHeight=displayHeight,
                     rightAlign=game.rightAlign, leftAlign=game.leftAlign,
                     upAlign=game.upAlign, displayGrid=displayGrid, gridSize=game.gridSize)

        while not game.gameOver:

            # This is the game logic loop

            if not game.initialised:
                # Reset apple and rat positions
                game.apple.updater(snake=game.snake, walls=game.walls, displayWidth=displayWidth,
                                   displayHeight=displayHeight, gridSize=game.gridSize)
                game.rat.updater(snake=game.snake, displayWidth=displayWidth, displayHeight=displayHeight,
                                 gridSize=game.gridSize)
                game.speedAbility.main()
                game.initialised = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Your score was: ", game.snake.score)
                    gameStop(game.snake.score)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.gameOver = True
                        print("Your score was: ", game.snake.score)

                    elif event.key == pygame.K_1:
                        game.speedAbility.speed(game=game)

                    elif event.key == pygame.K_F1:
                        game.debug = not game.debug

                    elif event.key == pygame.K_g:
                        displayGrid = not displayGrid

                    elif event.key == pygame.K_k:
                        # Length cheat
                        print("Cheat activated")
                        game.lengthCheat = not game.lengthCheat

                    elif event.key == pygame.K_l:
                        # Score cheat
                        game.snake.score += 10

            else:
                game.theKey = event.key

            if (game.frameCounter / game.speed).is_integer() and game.frameCounter != 0:
                # The snake/rat moves and all checks are done only when the game.speed divided by the current frame is whole

                game.snake.move(game.theKey,
                                game.gridSize)  # Move the snake in the direction of the (last) key pressed (game.theKey)
                game.appleEaten = game.snake.applecollision(snake=game.snake,
                                                            apple=game.apple)  # Check if food has been eaten
                game.ratEaten = game.snake.ratcollision(snake=game.snake, rat=game.rat)
                game.snake.tail(appleEaten=game.appleEaten, lengthCheat=game.lengthCheat,
                                ratEaten=game.ratEaten)  # Move the tail around and adds a segment if game.appleEaten = True
                game.rat.move(snake=game.snake, gridSize=game.gridSize)

                # All movements are one grid size at a time

                if game.appleEaten:
                    game.apple.updater(snake=game.snake, walls=game.walls, displayWidth=displayWidth,
                                       displayHeight=displayHeight,
                                       gridSize=game.gridSize)
                    if game.snake.score >= game.score:
                        game.updater(displayWidth=displayWidth, displayHeight=displayHeight)

                if game.ratEaten:
                    game.rat.updater(snake=game.snake, displayWidth=displayWidth, displayHeight=displayHeight,
                                     gridSize=game.gridSize)
                    if game.snake.score >= game.score:
                        game.updater(displayWidth=displayWidth, displayHeight=displayHeight)

            if game.frameCounter == 60:
                # Do this every second
                game.speedAbility.countdown(game)
                game.frameCounter = 0

            if not game.gameOver:
                # This if forbids snake.collisionCheck() from returning game.gameOver = False after another function set it to True
                game.gameOver = game.snake.collisionCheck(walls=game.walls, displayWidth=displayWidth,
                                                          displayHeight=displayHeight)
            # check if the snake has collided with the walls or itself

            drawGame(snake=game.snake, apple=game.apple, rat=game.rat, walls=game.walls, speedAbility=game.speedAbility,
                     levelScore=game.score, level=game.level,
                     displayWidth=displayWidth, displayHeight=displayHeight, displayGrid=displayGrid, debug=game.debug,
                     gridSize=game.gridSize)
            # drawGame must be at the top of all functions! It renders and displays the game, excluding the game.gameOver message. It's drawn by the drawText.

            game.frameCounter += 1
            clock.tick(game.fps)  # clock.tick is the FPS cap


if __name__ == "__main__":
    game = level(1280, 720)
    gameLoop(displayGrid=True, fullScreen=False, resolutionIndex=2, game=game)
