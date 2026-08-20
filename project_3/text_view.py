"""
View component of 512 (2048 clone).  Responsible for
depiction of game state. This simple textual interface
is intended to be a drop-in replacement for tk_view,
and thus contains many methods that don't do anything.

We require one method that was not in the old tk_view
(which was just called "view"), viz., a notification that
the whole board should be displayed.  This is a no-op for
tk_view, which updates the graphical display incrementally
as each tile moves, but we need to batch updates and show
the whole board only after a move is complete.
"""
import commands
import game_element
import model

##########################
# Configuration constants
#########################

# Commands for controlling the game.  Can be bound
# to different inputs (keystrokes, whatever)
COMMAND_LEFT = "Left"
COMMAND_RIGHT = "Right"
COMMAND_UP = "Up"
COMMAND_DOWN = "Down"
COMMAND_UNMAPPED = "Unmapped"
COMMAND_CLOSE = "Close"    # Quit the game



#######
# End configuration constants
######

# Events we need to respond to:
#   - A new tile has been created.  Draw it and listen to it.
#   - A tile has been removed (maybe swallowed by another).
#   - A tile has been updated. Update its position and/or value.
#


class GameView(object):
    """The overall view (game window).
    Does almost nothing, because we use the existing console.
    """

    def __init__(self, height=0, width=0):
        """We just use the console."""
        pass

    def get_key(self) -> str:
        """Uses "input" because keystroke level control
        could interfere with a screen reader like JAWS.
        FIXME:  Find out if keyboard module is compatible with JAWS
        """
        return input("Your move: ")

    def close(self):
        """Nothing to close."""
        pass

    def lose(self, score=0):
        """Display 'Game Over' and close after next keystroke"""
        if score:
            print(f"Game over. Your score: {score}")
        else:
            print("Game over")



class GridView(game_element.GameListener):
    """The grid of spaces in the game, displayed
    within a GameView.
    """

    def __init__(self, game: GameView, grid: model.Board):
        """
        Args:
           game: The surrounding GameView object
        """
        self.game = game
        self.grid = grid


    def notify(self, event: game_element.GameEvent):
        """When a tile is created, we attach a new TileView
        to draw and redraw it as needed.
        """
        if event.kind == game_element.EventKind.tile_created:
            view = TileView(self, event.tile)
            event.tile.add_listener(view)
        else:
            raise Exception("Unexpected event: {}".format(event))

    def refresh(self):
        """Ensure current state of board is visible.
        For textual view, we print the values of tiles,
        with a mark 'e' for empty spaces.  They are separated
        by spaces so that a screen reader will read each
        character separately.
        """
        print("Board: ")
        for row in self.grid.tiles:
            print("/", end=" ")
            for col in row:
                if col is not None:
                    print(col.value, end=" ")  # Will fail until Tile objects are defined
                else:
                    print("e", end=" ")
            print("/")




class TileView(object):
    """A Tile is the thing with a number that slides around the grid.
    In the textual view, we can just use the underlying model.Board instead.
    """

    def __init__(self, grid: GridView, tile: model.Tile):
        """Add tile to grid.  (Not used for text view.)
        """
        pass


    def slide_to(self, row, col):
        """Slide the tile to row,col"""
        pass


    def notify(self, event: game_element.GameEvent):
        """Receive notification of change from a tile.
        """
        pass



# We can bind different areas of the keyboard to the
# commands. "Left", "right", etc are Tk codes for the
# arrow keys.  "jil," are a similar spatial pattern under
# the right hand.
KEY_BINDINGS = { # Arrow keys are not strings, can't use them
                 # But we can read whole strings
                 "up": commands.UP, "down": commands.DOWN, "left": commands.LEFT, "right": commands.RIGHT,
                 # left-hand --- some people use this pattern?
                 "a": commands.LEFT, "w": commands.UP, "s": commands.RIGHT, "z": commands.DOWN,
                 # VI / Vim editor movement
                 "h": commands.LEFT, "j": commands.DOWN, "k": commands.UP, "l": commands.RIGHT,
                 # Numeric keypad (one common mapping)
                 "4": commands.LEFT, "6": commands.RIGHT, "8": commands.UP, "2": commands.DOWN,
                 # Ways to quit
                "q": commands.CLOSE, "Q": commands.CLOSE, "quit": commands.CLOSE, "exit": commands.CLOSE
                 }



class Command(object):
    """Interpret keyboard input as commands from the
    set LEFT, RIGHT, UP, DOWN, and UNMAPPED, CLOSEor a
    key that does not have a binding.
    """

    def __init__(self, game_view):
        self.game_view = game_view

    def next(self):
        key = self.game_view.get_key()
        if key not in KEY_BINDINGS:
            return commands.UNMAPPED
        else:
            return KEY_BINDINGS[key]



if __name__ == "__main__":
    game_view = GameView(600, 600)
    grid_view = GridView(game_view, model.Board(4, 4))
    grid = model.Board()
    grid.add_listener(grid_view)
    grid.place_tile()
    game_view.lose()
