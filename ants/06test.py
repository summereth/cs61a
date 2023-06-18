from ants import *
WallAnt.implemented

# Testing WallAnt parameters
wall = WallAnt()
assert wall.name == 'Wall'
assert wall.health == 4
# `health` should not be a class attribute
assert not hasattr(WallAnt, 'health') # hasattr checks if the WallAnt class has a class attribute called 'health'
assert WallAnt.food_cost == 4

# Abstraction tests
original = Ant.__init__
Ant.__init__ = lambda self, health: print("init") #If this errors, you are not calling the parent constructor correctly.
wall = WallAnt()
Ant.__init__ = original
wall = WallAnt()

# Testing WallAnt holds strong
beehive, layout = Hive(AssaultPlan()), dry_layout
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))
place = gamestate.places['tunnel_0_4']
wall = WallAnt()
bee = Bee(1000)
place.add_insect(wall)
place.add_insect(bee)
for i in range(3):
    bee.action(gamestate)
    wall.action(gamestate)   # WallAnt does nothing
assert wall.health == 1
assert bee.health == 1000
assert wall.place is place
assert bee.place is place