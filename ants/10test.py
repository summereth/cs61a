from ants import *
from ants_plans import *
beehive, layout = Hive(make_test_assault_plan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

# Testing water with Ants
test_water = Water('Water Test1')
ant = HarvesterAnt()
test_water.add_insect(ant)
assert (ant.health, test_water.ant is None) == (0, True)
ant = Ant()
test_water.add_insect(ant)
assert (ant.health, test_water.ant is None) == (0, True)
ant = ThrowerAnt()
test_water.add_insect(ant)
assert (ant.health, test_water.ant is None) == (0, True)

# Testing water with soggy (non-waterproof) bees
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

test_bee = Bee(1000000)
test_bee.is_waterproof = False    # Make Bee non-waterproof
test_water = Water('Water Test2')
test_water.add_insect(test_bee)
assert test_bee.health == 0
assert len(test_water.bees) == 0

# Testing water with waterproof bees
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

test_bee = Bee(1)
test_water = Water('Water Test3')
test_water.add_insect(test_bee)
assert test_bee.health == 1
assert test_bee in test_water.bees

# test proper call to death callback
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

original_death_callback = Insect.death_callback
Insect.death_callback = lambda x: print("insect died")
place = Water('Water Test4')
soggy_bee = Bee(1)
soggy_bee.is_waterproof = False
place.add_insect(soggy_bee)
place.add_insect(Bee(1))
place.add_insect(ThrowerAnt())
Insect.death_callback = original_death_callback

from ants import *
from ants_plans import *
beehive, layout = Hive(make_test_assault_plan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
old_add_insect = Place.add_insect

# Testing water inheritance
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

old_add_insect = Place.add_insect
def new_add_insect(self, insect):
    print("called add_insect")
    old_add_insect(self, insect)
Place.add_insect = new_add_insect
test_bee = Bee(1)
test_water = Water('Water Test4')
test_water.add_insect(test_bee) # if this fails you probably didn't call `add_insect`
Place.add_insect = old_add_insect