import pygame
import random
import sys


def draw_grid(screen, grid, grid_size, cell_size, show_grid=True):
    for row in range(grid_size[1]):
        for col in range(grid_size[0]):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            color = (0, 0, 0) if grid[row][col] == 1 else (255, 255, 255)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Серые границы


def calculate_accuracy(original_grid, user_grid):
    correct = 0
    total = sum(sum(row) for row in original_grid)
    for row in range(len(original_grid)):
        for col in range(len(original_grid[row])):
            if original_grid[row][col] == 1 and user_grid[row][col] == 1:
                correct += 1
    return (correct / total) * 100 if total > 0 else 0


def main(grid_width, grid_height):
    pygame.init()
    display_info = pygame.display.Info()
    screen_height = display_info.current_h
    cell_size = screen_height / grid_height  # size of one square
    screen_width = grid_width * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Grid restore")
    grid = [[1 if random.random() < 0.5 else 0 for _ in range(grid_width)] for _ in range(grid_height)]
    user_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

    grid_visible = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # space to hide or show the grid
                    grid_visible = not grid_visible
                    if not grid_visible:
                        print("The grid is hidden.")
                    else:
                        accuracy = calculate_accuracy(grid, user_grid)
                        print(f"Accuracy: {accuracy:.2f}%")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not grid_visible:  # LMB and grid are hidden
                    pos = pygame.mouse.get_pos()
                    col, row = int(pos[0] // cell_size), int(pos[1] // cell_size)
                    if 0 <= row < grid_height and 0 <= col < grid_width:
                        user_grid[row][col] = 1 if user_grid[row][col] == 0 else 0
                if event.button == 3:
                    main(grid_width, grid_height)

        screen.fill((255, 255, 255))

        if grid_visible:
            draw_grid(screen, grid, (grid_width, grid_height), cell_size)
        else:
            draw_grid(screen, user_grid, (grid_width, grid_height), cell_size, show_grid=False)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    try:
        grid_width, grid_height = map(int, input().split())
        if grid_width < 1 or grid_height < 1:
            raise ValueError("Need positive numbers")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    main(grid_width, grid_height)
