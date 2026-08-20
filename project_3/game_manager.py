"""
Overall control for 2048 clone 512.  Coordinates
model and view and implements controller
functionality by interpreting keyboard input
"""
import model
import tk_view as view
#import text_view as view
import commands
import sys


def main():
    # Set up model component
    grid = model.Board()
    # Set up view component
    game_view = view.GameView(600, 600)
    grid_view = view.GridView(game_view, grid)
    grid.add_listener(grid_view)
    # Handle control component responsibility here
    user_commands = view.Command(game_view)

    # FIXME: We will change this to 
    #  grid.place_tile(value=2) after
    #  creating the keyword argument in model.py
    grid.place_tile()

    # Game continues until there is no empty
    # space for a tile
    while grid.has_empty():
        grid.place_tile()
        grid_view.refresh()
        cmd = user_commands.next()
        if cmd == commands.LEFT:
            grid.left()
        elif cmd == commands.RIGHT:
            grid.right()
        elif cmd == commands.UP:
            grid.up()
        elif cmd == commands.DOWN:
            grid.down()
        elif cmd == commands.CLOSE:
            game_view.close()  # OK if it's already closed
            print(f"Your score: {grid.score()}")
            sys.exit(0)
        else: 
            assert cmd == commands.UNMAPPED

    game_view.lose(grid.score())


if __name__ == "__main__":
    main()
