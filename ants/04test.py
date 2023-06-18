from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

# Testing Long/ShortThrower parameters
assert ShortThrower.food_cost == 2
assert LongThrower.food_cost == 2
short_t = ShortThrower()
long_t = LongThrower()
assert short_t.health == 1
assert long_t.health == 1


from ants import *
LongThrower.implemented == True
ShortThrower.implemented == True

# Test ShortThrower hit
ant = ShortThrower()
in_range = Bee(2)
gamestate.places['tunnel_0_0'].add_insect(ant)
gamestate.places["tunnel_0_3"].add_insect(in_range)
ant.action(gamestate)
assert in_range.health == 1

# Testing ShortThrower miss
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

ant = ShortThrower()
out_of_range = Bee(2)
gamestate.places["tunnel_0_0"].add_insect(ant)
gamestate.places["tunnel_0_4"].add_insect(out_of_range)
ant.action(gamestate)
assert out_of_range.health == 2

# Test LongThrower hit
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

ant = LongThrower()
in_range = Bee(2)
gamestate.places['tunnel_0_0'].add_insect(ant)
gamestate.places["tunnel_0_5"].add_insect(in_range)
ant.action(gamestate)
assert in_range.health == 1

# Testing LongThrower miss
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

ant = LongThrower()
out_of_range = Bee(2)
gamestate.places["tunnel_0_0"].add_insect(ant)
gamestate.places["tunnel_0_4"].add_insect(out_of_range)
ant.action(gamestate)
assert out_of_range.health == 2

# Testing LongThrower hit after skipping an bee out of range
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
ant = LongThrower()
out_of_range = Bee(2)
in_range = Bee(2)
gamestate.places["tunnel_0_0"].add_insect(ant)
gamestate.places["tunnel_0_4"].add_insect(out_of_range)
gamestate.places["tunnel_0_5"].add_insect(in_range)
ant.action(gamestate)
assert out_of_range.health == 2
assert in_range.health == 1

# Testing LongThrower miss next to the hive
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
ant = LongThrower()
gamestate.places["tunnel_0_4"].add_insect(ant)
ant.action(gamestate) # should not error

# Testing LongThrower targets farther one
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
ant = LongThrower()
out_of_range = Bee(2)
in_range = Bee(2)
gamestate.places["tunnel_0_0"].add_insect(ant)
gamestate.places["tunnel_0_4"].add_insect(out_of_range)
gamestate.places["tunnel_0_5"].add_insect(in_range)
ant.action(gamestate)
assert out_of_range.health == 2
assert in_range.health == 1

# Testing LongThrower ignores bees outside range
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
thrower = LongThrower()
gamestate.places["tunnel_0_0"].add_insect(thrower)
bee1 = Bee(1001)
bee2 = Bee(1001)
gamestate.places["tunnel_0_4"].add_insect(bee1)
gamestate.places["tunnel_0_5"].add_insect(bee2)
thrower.action(gamestate)
assert bee1.health == 1001
assert bee2.health == 1000

# Testing LongThrower attacks nearest bee in range
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
thrower = LongThrower()
gamestate.places["tunnel_0_0"].add_insect(thrower)
bee1 = Bee(1001)
bee2 = Bee(1001)
gamestate.places["tunnel_0_5"].add_insect(bee1)
gamestate.places["tunnel_0_6"].add_insect(bee2)
thrower.action(gamestate)
assert bee1.health == 1000
assert bee2.health == 1001

# Testing case when lower_bound of LongThrower is outside of the tunnel
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
bee = Bee(2)
ant = LongThrower()
gamestate.places["tunnel_0_6"].add_insect(ant)
gamestate.places["tunnel_0_7"].add_insect(bee)
ant.action(gamestate)
assert bee.health == 2

# Testing if upper_bound is looked up in the instance
# and check that the code isnt dependent on the ants name
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
ant = ShortThrower()
ant.name = 'short2'
ant.upper_bound = 10   # Buff the ant's range
gamestate.places["tunnel_0_0"].add_insect(ant)
bee = Bee(2)
gamestate.places["tunnel_0_6"].add_insect(bee)
ant.action(gamestate)
assert bee.health == 1

# Testing there is no new nearest_bee function in ShortThrower / LongThrower
assert ShortThrower.nearest_bee is ThrowerAnt.nearest_bee
assert LongThrower.nearest_bee is ThrowerAnt.nearest_bee


from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 100)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

# Testing if lower_bound is set appropriately in ThrowerAnt
ant = ThrowerAnt()
gamestate.places["tunnel_0_0"].add_insect(ant)
bee = Bee(2)
gamestate.places["tunnel_0_0"].add_insect(bee)
ant.action(gamestate)
assert bee.health == 1

# Testing if upper_bound is set appropriately in ThrowerAnt
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
ant = ThrowerAnt()
gamestate.places["tunnel_0_0"].add_insect(ant)
bee = Bee(2)
gamestate.places["tunnel_0_99"].add_insect(bee)
ant.action(gamestate)
assert bee.health == 1

# Special thrower class that just hits things 6 away
class JustSixThrower(ThrowerAnt):
    lower_bound = upper_bound = 6

gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
ant = JustSixThrower()
gamestate.places["tunnel_0_0"].add_insect(ant)
exact_bee = Bee(2)
gamestate.places["tunnel_0_6"].add_insect(exact_bee)
ant.action(gamestate)
assert exact_bee.health == 1

# Special thrower class that just hits things 6 away
class JustSixThrower(ThrowerAnt):
    lower_bound = upper_bound = 6

gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
ant = JustSixThrower()
gamestate.places["tunnel_0_0"].add_insect(ant)
close_bee = Bee(2)
gamestate.places["tunnel_0_5"].add_insect(close_bee)
ant.action(gamestate)
assert close_bee.health == 2


from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
old_thrower_action = ThrowerAnt.action
old_throw_at = ThrowerAnt.throw_at
ThrowerAnt.action = old_thrower_action
ThrowerAnt.throw_at = old_throw_at

# Special thrower class that just hits things 6 away
class JustSixThrower(ThrowerAnt):
    lower_bound = upper_bound = 6

gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
ant = JustSixThrower()
gamestate.places["tunnel_0_0"].add_insect(ant)
far_bee = Bee(2)
gamestate.places["tunnel_0_7"].add_insect(far_bee)
ant.action(gamestate)
assert far_bee.health == 2

# Testing LongThrower Inheritance from ThrowerAnt
def new_action(self, gamestate):
    raise NotImplementedError()
def new_throw_at(self, target):
    raise NotImplementedError()

ThrowerAnt.action = new_action
test_long = LongThrower()
passed = 0
try:
    test_long.action(gamestate)
except NotImplementedError:
    passed += 1

ThrowerAnt.action = old_thrower_action
ThrowerAnt.throw_at = new_throw_at
test_long = LongThrower()
try:
    test_long.throw_at(Bee(1))
except NotImplementedError:
    passed += 1
ThrowerAnt.throw_at = old_throw_at
assert passed == 2

# Testing ShortThrower Inheritance from ThrowerAnt
def new_action(self, gamestate):
    raise NotImplementedError()
def new_throw_at(self, target):
    raise NotImplementedError()
ThrowerAnt.action = new_action
test_short = ShortThrower()
passed = 0
try:
    test_short.action(gamestate)
except NotImplementedError:
    passed += 1
          
ThrowerAnt.action = old_thrower_action
ThrowerAnt.throw_at = new_throw_at
test_short = ShortThrower()
try:
    test_short.throw_at(Bee(1))
except NotImplementedError:
    passed += 1
          
ThrowerAnt.throw_at = old_throw_at
assert passed == 2