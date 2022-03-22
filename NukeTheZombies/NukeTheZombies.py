import random
import time

"""
    -------NUKETHEZOMBIES-------
    How it will work:
    1. A 5x5 grid will have random no of enemies, randomly placed.
    2. You will have 8 bullets to take down the enemies that are placed.
    3. You have to figure out the co-ordinates to where to shoot.
    4. For every shot that hits or misses it will show up.
    5. If all enemies are dead before using up all bullets, you win
        else, you lose
    Legend:
    1. "﹏" = ground or empty space
    2. "🧟" = enemies
    3. "💀" = enemy that has been shot
    4. "╳" = ground that was shot with bullet, a miss because it didn't hit.
"""

# Global variable for grid
grid = [[]]
# Global variable for grid size
gridSize = 5
# Global variable for number of enemies to place
numofEnemies = 2
# Global variable for bullets left
bullets_left = 8
# Global variable for game over
game_over = False
# Global variable for number of enemies shot
numofenemyShot = 0
# Global variable for enemy positions
enemyPositions = [[]]
# Global variable for alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def validate_grid_and_place_enemy(startingRow, endingRow, startingColumn, endingColumn):
    """Will check the row or column to see if it is safe to place an enemy there"""
    global grid
    global enemyPositions

    valid = True
    for r in range(startingRow, endingRow):
        for c in range(startingColumn, endingColumn):
            if grid[r][c] != "﹏":
                valid = False
                break
    if valid:
        enemyPositions.append([startingRow, endingRow, startingColumn, endingColumn])
        for r in range(startingRow, endingRow):
            for c in range(startingColumn, endingColumn):
                grid[r][c] = "🧟"
    return valid


def try_to_place_enemy_on_grid(row, column, direction, length):
    """Based on direction will call helper method to try and place an enemy on the grid"""
    global gridSize

    startRow, endRow, startColumn, endColumn = row, row + 1, column, column + 1
    if direction == "left":
        if column - length < 0:
            return False
        startColumn = column - length + 1

    elif direction == "right":
        if column + length >= gridSize:
            return False
        endColumn = column + length

    elif direction == "up":
        if row - length < 0:
            return False
        startRow = row - length + 1

    elif direction == "down":
        if row + length >= gridSize:
            return False
        endRow = row + length

    return validate_grid_and_place_enemy(startRow, endRow, startColumn, endColumn)


def create_grid():
    """Will create a 5x5 grid and randomly place down enemies
       of different sizes in different directions"""
    global grid
    global gridSize
    global numofEnemies
    global enemyPositions

    random.seed(time.time())

    rows, cols = (gridSize, gridSize)

    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append("﹏")
        grid.append(row)

    numOfEnemiesPlaced = 0

    enemyPositions = []

    while numOfEnemiesPlaced != numofEnemies:
        random_row = random.randint(0, rows - 1)
        random_column = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        enemy_size = random.randint(1, 3)
        if try_to_place_enemy_on_grid(random_row, random_column, direction, enemy_size):
            numOfEnemiesPlaced += 1


def print_grid():
    """Will print the grid with rows A-J and columns 0-9"""
    global grid
    global alphabet

    debug_mode = True

    alphabet = alphabet[0: len(grid) + 1]

    for row in range(len(grid)):
        print(alphabet[row], end=") ")
        for col in range(len(grid[row])):
            if grid[row][col] == "🧟":
                if debug_mode:
                    print("🧟", end=" ")
                else:
                    print("﹏", end=" ")
            else:
                print(grid[row][col], end=" ")
        print("")

    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")


def accept_valid_bullet_placement():
    """Will get valid row and column to place bullet shot"""
    global alphabet
    global grid

    is_valid_placement = False
    row = -1
    col = -1
    while is_valid_placement is False:
        placement = input("Enter co-ordinates to drop the missile using row (A-E) and column (0-4) such as A3: ")
        print("( う-´)づ︻╦̵̵̿╤──⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍\(˚☐˚”)/")
        placement = placement.upper()
        if len(placement) <= 0 or len(placement) > 2:
            print("Error: Please enter only one row and column such as A3")
            continue
        row = placement[0]
        col = placement[1]
        if not row.isalpha() or not col.isnumeric():
            print("Error: Please enter letter (A-E) for row and (0-4) for column")
            continue
        row = alphabet.find(row)
        if not (-1 < row < gridSize):
            print("Error: Please enter letter (A-E) for row and (0-4) for column")
            continue
        col = int(col)
        if not (-1 < col < gridSize):
            print("Error: Please enter letter (A-E) for row and (0-4) for column")
            continue
        if grid[row][col] == "╳" or grid[row][col] == "💀":
            print("You have already shot a bullet here, pick somewhere else")
            continue
        if grid[row][col] == "﹏" or grid[row][col] == "🧟":
            is_valid_placement = True

    return row, col


def check_for_enemy_shot(row, col):
    """If all enemies have been shot, and we later increment enemies shot"""
    global enemyPositions
    global grid

    for position in enemyPositions:
        start_row = position[0]
        end_row = position[1]
        start_col = position[2]
        end_col = position[3]
        if start_row <= row <= end_row and start_col <= col <= end_col:
            # enemy found, now check if it is all shot
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if grid[r][c] != "💀":
                        return False
    return True


def shoot_bullet():
    """Updates grid and enemies based on where the bullet was shot"""
    global grid
    global numofenemyShot
    global bullets_left

    row, col = accept_valid_bullet_placement()
    print("")
    print("︻デ═一⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍━╤デ╦︻")

    if grid[row][col] == "﹏":
        print("You missed")
        grid[row][col] = "╳"
    elif grid[row][col] == "🧟":
        print("Head shot!", end=" ")
        grid[row][col] = "💀"
        if check_for_enemy_shot(row, col):
            print("Nice shot!")
            numofenemyShot += 1
        else:
            print("Critical hit.")

    bullets_left -= 1


def check_for_game_over():
    """If all enemies have been shot, or we run out of bullets its game over"""
    global numofenemyShot
    global numofEnemies
    global bullets_left
    global game_over

    if numofEnemies == numofenemyShot:
        print("Congrats you won ٩(˘◡˘)۶!")
        game_over = True
    elif bullets_left <= 0:
        print("Sorry, you lost! You ran out of bullets, try again next time!")
        game_over = True


def main():
    """Main entry point of application that runs the game loop"""
    global game_over

    print("(　-_･) ︻デ═一 ▸Welcome to 🧟NukeTheZombies🧟︻┻┳══━一 ")
    print("You have 8 missiles to take down enemies, Your survival depends solely upon your mathematical skills, may the battle begin!")

    create_grid()

    while game_over is False:
        print_grid()
        print("Number of enemies remaining: " + str(numofEnemies - numofenemyShot))
        print("Number of bullets left: " + str(bullets_left))
        shoot_bullet()
        print("︻デ═一⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍ ⁍━╤デ╦︻")
        print("")
        check_for_game_over()


if __name__ == '__main__':
    """Will only be called when program is run from terminal or an IDE like PyCharms"""
    main()
