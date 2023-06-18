from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

# Testing status parameters
slow = SlowThrower()
assert SlowThrower.food_cost == 6
assert slow.health == 1

# Testing Slow
slow = SlowThrower()
bee = Bee(3)
gamestate.places["tunnel_0_0"].add_insect(slow)
gamestate.places["tunnel_0_5"].add_insect(bee)
slow.action(gamestate)
gamestate.time = 1
bee.action(gamestate)
assert bee.place.name == "tunnel_0_5" # SlowThrower should cause slowness on odd turns
gamestate.time += 1
bee.action(gamestate)
assert bee.place.name == "tunnel_0_4" # SlowThrower should cause slowness on odd turns
for _ in range(5):
    gamestate.time += 1
    bee.action(gamestate)
    # print(gamestate.time, bee.place.name)
assert bee.place.name == "tunnel_0_1"

# Testing Slow
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

slow = SlowThrower()
bee = Bee(3)
gamestate.places["tunnel_0_0"].add_insect(slow)
gamestate.places["tunnel_0_5"].add_insect(bee)
slow.action(gamestate)
gamestate.time = 1
bee.action(gamestate)
assert bee.place.name == "tunnel_0_5"
gamestate.time += 1
bee.action(gamestate)
assert bee.place.name == "tunnel_0_4"
slow.action(gamestate) # SlowThrower throws syrup again
for _ in range(5):
    gamestate.time += 1
    bee.action(gamestate)
assert bee.place.name == "tunnel_0_2"

# Testing that Bee.action was not modified
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

slow = SlowThrower()
bee = Bee(3)
gamestate.places["tunnel_0_0"].add_insect(slow)
gamestate.places["tunnel_0_5"].add_insect(bee)
slow.action(gamestate)
gamestate.time = 1
Bee.action(bee, gamestate) # uses original Bee.action
assert bee.place.name == 'tunnel_0_4'
gamestate.time += 1
Bee.action(bee, gamestate) # uses original Bee.action
assert bee.place.name == 'tunnel_0_3'
for _ in range(3):
    gamestate.time += 1
    bee.action(gamestate) # uses original new slowed action
assert bee.place.name == 'tunnel_0_2'
