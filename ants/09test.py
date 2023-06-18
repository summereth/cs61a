from ants_plans import *
from ants import *
beehive, layout = Hive(make_test_assault_plan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

# Testing TankAnt parameters
assert TankAnt.food_cost == 6
assert TankAnt.damage == 1
tank = TankAnt()
assert tank.health == 2

# Testing TankAnt action
tank = TankAnt()
place = gamestate.places['tunnel_0_1']
other_place = gamestate.places['tunnel_0_2']
place.add_insect(tank)
for _ in range(3):
    place.add_insect(Bee(3))
other_place.add_insect(Bee(3))
tank.action(gamestate)
assert [bee.health for bee in place.bees] == [2, 2, 2]
assert [bee.health for bee in other_place.bees] == [3]

# Testing TankAnt container methods
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

tank = TankAnt()
thrower = ThrowerAnt()
place = gamestate.places['tunnel_0_1']
place.add_insect(thrower)
place.add_insect(tank)
assert place.ant is tank
bee = Bee(3)
place.add_insect(bee)
tank.action(gamestate)   # Both ants attack bee
assert bee.health == 1

from ants_plans import *
from ants import *
beehive, layout = Hive(make_test_assault_plan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
 
# Testing TankAnt action
tank = TankAnt()
place = gamestate.places['tunnel_0_1']
place.add_insect(tank)
for _ in range(3):  # Add three bees with 1 health each
    place.add_insect(Bee(1))
tank.action(gamestate)
assert len(place.bees) == 0  # Bees removed from places because of TankAnt damage

# Testing TankAnt.damage
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

tank = TankAnt()
tank.damage = 100
place = gamestate.places['tunnel_0_1']
place.add_insect(tank)
for _ in range(3):
    place.add_insect(Bee(100))
tank.action(gamestate)
assert len(place.bees) == 0

# Placement of ants
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

tank = TankAnt()
harvester = HarvesterAnt()
place = gamestate.places['tunnel_0_0']
# Add tank before harvester
place.add_insect(tank)
place.add_insect(harvester)
gamestate.food = 0
tank.action(gamestate)
assert gamestate.food == 1
try:
    place.add_insect(TankAnt())
except AssertionError:
    print("error!")
assert place.ant is tank
assert tank.ant_contained is harvester
try:
    place.add_insect(HarvesterAnt())
except AssertionError:
    print("error!")
assert place.ant is tank
assert tank.ant_contained is harvester

# Placement of ants
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

tank = TankAnt()
harvester = HarvesterAnt()
place = gamestate.places['tunnel_0_0']
# Add harvester before tank
place.add_insect(harvester)
place.add_insect(tank)
gamestate.food = 0
tank.action(gamestate)
assert gamestate.food == 1
try:
    place.add_insect(TankAnt())
except AssertionError:
    print("error!")
assert place.ant is tank
assert tank.ant_contained is harvester
try:
    place.add_insect(HarvesterAnt())
except AssertionError:
    print("error!")
assert place.ant is tank
assert tank.ant_contained is harvester

# Removing ants
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

tank = TankAnt()
test_ant = Ant()
place = Place('Test')
place.add_insect(tank)
place.add_insect(test_ant)
place.remove_insect(test_ant)
assert tank.ant_contained is None
assert test_ant.place is None
place.remove_insect(tank)
assert place.ant is None
assert tank.place is None

tank = TankAnt()
place = Place('Test')
place.add_insect(tank)
tank.action(gamestate)

# test proper call to death callback
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

original_death_callback = Insect.death_callback
Insect.death_callback = lambda x: print("insect died")
place = gamestate.places["tunnel_0_0"]
bee = Bee(3)
tank = TankAnt()
ant = ThrowerAnt()
place.add_insect(bee)
place.add_insect(ant)
place.add_insect(tank)
bee.action(gamestate)
bee.action(gamestate)
bee.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_health or Insect.reduce_health
Insect.death_callback = original_death_callback

from ants import *
# Abstraction tests
original = Ant.__init__
Ant.__init__ = lambda self, health: print("init") #If this errors, you are not calling the parent constructor correctly.
tank = TankAnt()
Ant.__init__ = original
tank = TankAnt()