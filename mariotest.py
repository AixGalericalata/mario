import pygame
import os
import sys


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level = load_level('mapFile.txt')

pygame.init()
tile_width = tile_height = 50
size = width, height = len(level[0]) * tile_width, len(level) * tile_height
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x + 15
        self.rect.y = tile_height * pos_y + 5

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        tile_x = (self.rect.x - 15) // tile_width
        tile_y = (self.rect.y - 5) // tile_height
        if tile_x >= len(level[0]) or tile_x < 0 or tile_y >= len(level) or tile_y < 0:
            self.rect.x -= x
            self.rect.y -= y
            return
        collider = pygame.sprite.spritecollideany(self, tiles_group)
        if collider.type == 'wall':
            self.rect.x -= x
            self.rect.y -= y


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def start_screen():
    intro_text = ["MARIOGAME",
                  "Двигайте персонажа с помощью стрелочек.",
                  "Примите задачу, пожалуйста",
                  "Нажмите любую кнопку, чтобы продолжить"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (size))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()


def main():
    running = True

    player, level_x, level_y = generate_level(level)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-50, 0)
                if event.key == pygame.K_RIGHT:
                    player.move(50, 0)
                if event.key == pygame.K_UP:
                    player.move(0, -50)
                if event.key == pygame.K_DOWN:
                    player.move(0, 50)

        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    start_screen()
    main()
