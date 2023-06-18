from ants import *

# Testing ScubaThrower parameters
scuba = ScubaThrower()
assert ScubaThrower.food_cost == 6
assert scuba.health == 1

from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

# Testing if ScubaThrower is waterproof
water = Water('Water')
ant = ScubaThrower()
water.add_insect(ant)
assert ant.place is water
assert ant.health == 1

# Testing that ThrowerAnt is not waterproof
water = Water('Water')
ant = ThrowerAnt()
water.add_insect(ant)
assert not ant.place is water
assert ant.health == 0

# Testing ScubaThrower on land
place1 = gamestate.places["tunnel_0_0"]
place2 = gamestate.places["tunnel_0_4"]
ant = ScubaThrower()
bee = Bee(3)
place1.add_insect(ant)
place2.add_insect(bee)
ant.action(gamestate)
assert bee.health == 2  # ScubaThrower can throw on land

# Testing ScubaThrower in the water
from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

water = Water("water")
water.entrance = gamestate.places["tunnel_0_1"]
target = gamestate.places["tunnel_0_4"]
ant = ScubaThrower()
bee = Bee(3)
water.add_insect(ant)
target.add_insect(bee)
ant.action(gamestate)
assert bee.health == 2  # ScubaThrower can throw in water

from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
old_thrower_action = ThrowerAnt.action
old_throw_at = ThrowerAnt.throw_at

# Testing ScubaThrower Inheritance from ThrowerAnt
def new_action(self, gamestate):
    raise NotImplementedError()
def new_throw_at(self, target):
    raise NotImplementedError()
ThrowerAnt.action = new_action
test_scuba = ScubaThrower()
try:
    test_scuba.action(gamestate)
except NotImplementedError:
    print('inherits action!')
ThrowerAnt.action = old_thrower_action
ThrowerAnt.throw_at = new_throw_at
test_scuba = ScubaThrower()
try:
    test_scuba.throw_at(Bee(1))
except NotImplementedError:
    print('inherits throw_at!')
