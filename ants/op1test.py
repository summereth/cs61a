from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

# Testing NinjaAnt parameters
ninja = NinjaAnt()
assert ninja.health == 1
assert NinjaAnt.food_cost == 5

# Testing blocks_path
assert not NinjaAnt.blocks_path
assert HungryAnt.blocks_path
assert FireAnt.blocks_path

# Testing NinjaAnts do not block bees
p0 = gamestate.places["tunnel_0_0"]
p1 = gamestate.places["tunnel_0_1"]  # p0 is p1's exit
bee = Bee(2)
ninja = NinjaAnt()
thrower = ThrowerAnt()
p0.add_insect(thrower)            # Add ThrowerAnt to p0
p1.add_insect(bee)
p1.add_insect(ninja)              # Add the Bee and NinjaAnt to p1
bee.action(gamestate)
assert bee.place is not ninja.place     # Did NinjaAnt block the Bee from moving?
assert bee.place is p0
assert ninja.health == 1
bee.action(gamestate)
assert bee.place is p0                # Did ThrowerAnt block the Bee from moving?

# Testing non-blocking ants do not block bees
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

p0 = gamestate.places["tunnel_0_0"]
p1 = gamestate.places["tunnel_0_1"]  # p0 is p1's exit
bee = Bee(2)
ninja_fire = FireAnt(1)
ninja_fire.blocks_path = False
thrower = ThrowerAnt()
p0.add_insect(thrower)            # Add ThrowerAnt to p0
p1.add_insect(bee)
p1.add_insect(ninja_fire)              # Add the Bee and NinjaAnt to p1
bee.action(gamestate)
assert bee.place is not ninja_fire.place        # Did the "ninjaish" FireAnt block the Bee from moving?
assert bee.place is p0
assert ninja_fire.health == 1
bee.action(gamestate)
assert bee.place is p0                 # Did ThrowerAnt block the Bee from moving?

# Testing NinjaAnt strikes all bees in its place
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

test_place = gamestate.places["tunnel_0_0"]
for _ in range(3):
    test_place.add_insect(Bee(2))
ninja = NinjaAnt()
test_place.add_insect(ninja)
ninja.action(gamestate)   # should strike all bees in place
assert [bee.health for bee in test_place.bees] == [1, 1, 1]

# Testing NinjaAnt doesn't hardcode damage
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

test_place = gamestate.places["tunnel_0_0"]
for _ in range(3):
    test_place.add_insect(Bee(100))
ninja = NinjaAnt()
ninja.damage = 50
test_place.add_insect(ninja)
ninja.action(gamestate)   # should strike all bees in place
assert [bee.health for bee in test_place.bees] == [50, 50, 50]

# Testing NinjaAnt strikes all bees, even if some expire
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

test_place = gamestate.places["tunnel_0_0"]
for _ in range(3):
    test_place.add_insect(Bee(1))
ninja = NinjaAnt()
test_place.add_insect(ninja)
ninja.action(gamestate)   # should strike all bees in place
assert len(test_place.bees) == 0

# Testing damage is looked up on the instance
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

place = gamestate.places["tunnel_0_0"]
bee = Bee(900)
place.add_insect(bee)
buffNinja = NinjaAnt()
buffNinja.damage = 500  # Sharpen the sword
place.add_insect(buffNinja)
buffNinja.action(gamestate)
assert bee.health == 400

# Testing Ninja ant does not crash when left alone
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

ninja = NinjaAnt()
gamestate.places["tunnel_0_0"].add_insect(ninja)
ninja.action(gamestate)

bee = Bee(3)
gamestate.places["tunnel_0_1"].add_insect(bee)
bee.action(gamestate)
