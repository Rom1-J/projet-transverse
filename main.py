from objects.constants import *
from objects.player import Player, Arm, Life
from objects.weapons import Tomato
from objects.world import World
from objects.gui import Angle, Fuel


def main():
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    clock = pg.time.Clock()

    level = 1
    turn = 1

    screen = pg.display.set_mode(SCREENRECT.size)

    img = {
        'patrick': {
            -1: pg.transform.flip(
                pg.transform.scale(
                    pg.image.load(f"resources/sprites/player/patrick/body.png").convert_alpha(),
                    (64, 128)
                ),
                True, False
            ),
            1: pg.transform.scale(
                pg.image.load(f"resources/sprites/player/patrick/body.png").convert_alpha(),
                (64, 128)
            )
        },
        'bob': {
            -1: pg.transform.flip(
                pg.transform.scale(
                    pg.image.load(f"resources/sprites/player/bob/body.png").convert_alpha(),
                    (64, 128)
                ),
                True, False
            ),
            1: pg.transform.scale(
                pg.image.load(f"resources/sprites/player/bob/body.png").convert_alpha(),
                (64, 128)
            )
        },
    }

    Player.images = img
    Player.life = 100
    Player.fuel = 10e10

    img = {-1: {}, 1: {}}
    for i in range(-4, 15, 2):
        loaded_img = pg.transform.scale(
            pg.image.load(f"resources/sprites/player/patrick/arm/{i}.png").convert_alpha(),
            (128, 128)
        )

        img[-1][i] = pg.transform.flip(loaded_img, True, False)
        img[1][i] = loaded_img
    Arm.images = img

    text = pg.font.Font(None, 20)
    text.set_italic(True)
    Life.life = 100
    Life.images = [
        text.render(f"Life: {Player.life}%", 0, (0, 0, 0))
    ]

    img = pg.transform.scale(
        pg.image.load(f"resources/sprites/bullets/tomato.png").convert_alpha(),
        (16, 16)
    )
    Tomato.images = [
        img
    ]

    Fuel.fuel = 100

    world = World()
    world.load_map(level)
    world.save_map()

    background = pg.Surface(SCREENRECT.size)
    background.blit(pg.image.load(f"resources/levels/{level}/map.png").convert_alpha(), (0, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    all_sprites = pg.sprite.RenderUpdates()

    Player.containers = all_sprites
    Arm.containers = all_sprites
    Life.containers = all_sprites
    Tomato.containers = all_sprites

    Angle.containers = all_sprites
    Fuel.containers = all_sprites

    player1 = Player(screen.get_rect(), world.level.players.get(1), 1, 'patrick')
    player2 = Player(screen.get_rect(), world.level.players.get(2), -1, 'bob')

    arm1 = Arm(screen.get_rect(), world.level.players.get(1), 1)
    arm2 = Arm(screen.get_rect(), world.level.players.get(2), -1)

    life1 = Life(screen.get_rect(), world.level.players.get(1))
    life2 = Life(screen.get_rect(), world.level.players.get(2))

    angle_gui = Angle()
    fuel_gui = Fuel()

    player = {
        1: [player1, life1, arm1],
        2: [player2, life2, arm2],
    }

    if pg.font:
        all_sprites.add(angle_gui)
        all_sprites.add(fuel_gui)

    while player.get(turn)[0].alive():
        pg.display.set_caption(f"Tank! - fps:{round(clock.get_fps())}")
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return

        keystate = pg.key.get_pressed()
        all_sprites.clear(screen, background)
        all_sprites.update()

        if player.get(turn)[0].fuel > 0:
            direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
            player.get(turn)[0].move(direction)
            player.get(turn)[1].move(direction, player.get(turn)[0].life)
            player.get(turn)[2].move(direction)
            fuel_gui.fuel = player.get(turn)[0].fuel

        if not player.get(turn)[0].is_shooting:
            # player.get(turn)[0].rotate(keystate[pg.K_UP] - keystate[pg.K_DOWN])
            player.get(turn)[2].rotate(keystate[pg.K_UP] - keystate[pg.K_DOWN])
            angle_gui.angle = player.get(turn)[2].angle

            if keystate[pg.K_SPACE]:
                player.get(turn)[0].is_shooting = True
                tomato = Tomato(
                    screen_rect=screen.get_rect(),
                    velocity=150, x=player.get(turn)[0].get_pos()[0], y=player.get(turn)[0].get_pos()[1],
                    direction=player.get(turn)[0].facing,
                    angle=player.get(turn)[2].angle,
                    adv=player.get(turn % 2 + 1)[0].get_pos(),
                    world=world.hit_box()
                )
                tomato.update()

        floor = all_sprites.draw(screen)
        pg.display.update(floor)

        clock.tick(20)

    pg.time.wait(1000)
    pg.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pg.quit()
        quit()
