import random
import arcade
import time
import datetime

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.50
COIN_COUNT = 10

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 780
SCREEN_TITLE = "Juego recolección de gemas"
GAME_DURATION = 30  # Game duration in seconds
PLAYER_MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = None
        self.coin_list = None

        self.player_sprite = None
        self.score = 0
        self.time_left = GAME_DURATION
        self.game_over = False
        self.history = []
        self.showing_history = False

        self.player_dx = 0
        self.player_dy = 0

        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.ELECTRIC_ULTRAMARINE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        self.score = 0
        self.time_left = GAME_DURATION
        self.game_over = False
        self.showing_history = False

        img = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.generate_coins()
        arcade.schedule(self.update_timer, 1)

    def generate_coins(self):
        """ Generates new coins at random positions """
        if not self.game_over:
            self.coin_list = arcade.SpriteList()
            for _ in range(COIN_COUNT):
                coin = arcade.Sprite(":resources:images/items/gemblue.png", SPRITE_SCALING_COIN)
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)
                self.coin_list.append(coin)

    def update_timer(self, delta_time):
        """ Reduce el tiempo restante y finaliza el juego si el tiempo se acaba """
        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.game_over = True
            self.history.append((self.score, datetime.datetime.now()))
            arcade.unschedule(self.update_timer)

    def on_update(self, delta_time):
        """ Game logic update """
        if not self.game_over:
            self.player_sprite.center_x += self.player_dx
            self.player_sprite.center_y += self.player_dy

            self.player_sprite.center_x = max(0, min(SCREEN_WIDTH, self.player_sprite.center_x))
            self.player_sprite.center_y = max(0, min(SCREEN_HEIGHT, self.player_sprite.center_y))

            coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
            for coin in coins_hit:
                coin.remove_from_sprite_lists()
                self.score += 1

            if len(self.coin_list) == 0:
                self.generate_coins()

    def draw_history(self):
        """ Display history screen """
        self.clear()
        arcade.draw_text("Historial de puntuaciones", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50,
                         arcade.color.YELLOW, 30, anchor_x="center")
        y_offset = SCREEN_HEIGHT - 100
        for score, date in self.history[-10:]:
            arcade.draw_text(f"{date.strftime('%Y-%m-%d %H:%M:%S')}: {score} puntos", SCREEN_WIDTH // 2, y_offset,
                             arcade.color.WHITE, 20, anchor_x="center")
            y_offset -= 30
        arcade.draw_text("Presiona R para reiniciar", SCREEN_WIDTH // 2, 50,
                         arcade.color.WHITE, 20, anchor_x="center")

    def on_draw(self):
        """ Draw everything """
        self.clear()

        if self.showing_history:
            self.draw_history()
        else:
            self.coin_list.draw()
            self.player_list.draw()

            if self.game_over:
                arcade.draw_text(f"Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                                 arcade.color.WHITE, 50, anchor_x="center")
                arcade.draw_text(f"Score: {self.score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                                 arcade.color.YELLOW, 40, anchor_x="center")
                arcade.draw_text("Presiona R para reiniciar o H para ver el historial", SCREEN_WIDTH // 2,
                                 SCREEN_HEIGHT // 2 - 80,
                                 arcade.color.WHITE, 20, anchor_x="center")
            else:
                output = f"Score: {self.score}"
                arcade.draw_text(text=output, start_x=10, start_y=20,
                                 color=arcade.color.WHITE, font_size=14)

                timer_output = f"Time Left: {self.time_left}s"
                arcade.draw_text(text=timer_output, start_x=SCREEN_WIDTH - 150, start_y=20,
                                 color=arcade.color.WHITE, font_size=14)

    def on_key_press(self, key, modifiers):
        """ Handle key presses """
        if key == arcade.key.R:
            self.setup()
        elif key == arcade.key.H:
            self.showing_history = not self.showing_history
            self.clear()
            self.on_draw()
        elif key == arcade.key.UP:
            self.player_dy = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_dy = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_dx = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_dx = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Handle key releases """
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.player_dy = 0
        elif key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player_dx = 0


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()


