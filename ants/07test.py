from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

print(HungryAnt.implemented)

# Testing HungryAnt parameters
hungry = HungryAnt()
assert HungryAnt.food_cost == 4
assert hungry.health == 1
assert hungry.chewing_turns == 3
assert hungry.turns_to_chew == 0

# Abstraction tests
original = Ant.__init__
Ant.__init__ = lambda self, health: print("init")  # If this errors, you are not calling the parent constructor correctly.
hungry = HungryAnt()
Ant.__init__ = original
hungry = HungryAnt()

# Class vs Instance attributes
assert not hasattr(HungryAnt, 'turns_to_chew')  # turns_to_chew should be an instance attribute
assert hungry.turns_to_chew == 0  # HungryAnt is ready to eat a bee
assert HungryAnt.chewing_turns == 3

# Testing HungryAnt eats and chews
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

hungry = HungryAnt()
bee1 = Bee(1000)              # A Bee with 1000 health
place = gamestate.places["tunnel_0_0"]
place.add_insect(hungry)
place.add_insect(bee1)         # Add the Bee to the same place as HungryAnt
hungry.action(gamestate)
assert bee1.health == 0
bee2 = Bee(1)                 # A Bee with 1 health
place.add_insect(bee2)
for _ in range(3):
    hungry.action(gamestate)     # Digesting...not eating
assert bee2.health == 1
hungry.action(gamestate)
bee2.health == 0

# Testing HungryAnt eats and chews for allotted time
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

hungry = HungryAnt()
bee1 = Bee(1000)              # A Bee with 1000 health
place = gamestate.places["tunnel_0_0"]
place.add_insect(hungry)
place.add_insect(bee1)         # Add the Bee to the same place as HungryAnt
hungry.action(gamestate)
assert bee1.health == 0
bee2 = Bee(1)                 # A Bee with 1 health
place.add_insect(bee2)
for _ in range(2):
    hungry.action(gamestate)     # Digesting...not eating, should not finish eating!
assert bee2.health == 1
hungry.action(gamestate)
assert bee2.health == 1

# Testing HungryAnt eats and chews
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

hungry = HungryAnt()
super_bee, wimpy_bee = Bee(1000), Bee(1)
place = gamestate.places["tunnel_0_0"]
place.add_insect(hungry)
place.add_insect(super_bee)
hungry.action(gamestate)         # super_bee is no match for HungryAnt!
assert super_bee.health == 0
place.add_insect(wimpy_bee)
for _ in range(3):
    hungry.action(gamestate)     # chewing...not eating
assert wimpy_bee.health == 1
hungry.action(gamestate)         # back to eating!
assert wimpy_bee.health == 0

# Testing HungryAnt only waits when chewing
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

hungry = HungryAnt()
place = gamestate.places["tunnel_0_0"]
place.add_insect(hungry)
# Wait a few turns before adding Bee
for _ in range(5):
    hungry.action(gamestate)  # shouldn't be chewing
bee = Bee(3)
place.add_insect(bee)
hungry.action(gamestate)  # Eating time!
assert bee.health == 0
bee = Bee(3)
place.add_insect(bee)
for _ in range(3):
    hungry.action(gamestate)     # Should be chewing
assert bee.health == 3
hungry.action(gamestate)
assert bee.health == 0

# Testing HungryAnt chew duration looked up on instance
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

very_hungry = HungryAnt()  # Add very hungry caterpi- um, ant
HungryAnt.chewing_turns = 0
place = gamestate.places["tunnel_0_0"]
place.add_insect(very_hungry)
for _ in range(100):
    place.add_insect(Bee(3))
for _ in range(100):
    very_hungry.action(gamestate)   # Eat all the bees!
assert len(place.bees) == 0

# Testing HungryAnt dies while eating
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

hungry = HungryAnt()
place = gamestate.places["tunnel_0_0"]
place.add_insect(hungry)
place.add_insect(Bee(3))
hungry.action(gamestate)
assert len(place.bees) == 0
bee = Bee(3)
place.add_insect(bee)
bee.action(gamestate) # Bee kills chewing ant
assert place.ant is None
assert len(place.bees) == 1

# Testing HungryAnt can't eat a bee at another space
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

hungry = HungryAnt()
gamestate.places["tunnel_0_0"].add_insect(hungry)
gamestate.places["tunnel_0_1"].add_insect(Bee(3))
hungry.action(gamestate)
assert len(gamestate.places["tunnel_0_1"].bees) == 1

# test proper call to death callback
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

original_death_callback = Insect.death_callback
Insect.death_callback = lambda x: print("insect died")
ant = HungryAnt()
bee = Bee(1000)              # A Bee with 1000 health
place = gamestate.places["tunnel_0_0"]
place.add_insect(bee)
place.add_insect(ant)
ant.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_health or Insect.reduce_health
Insect.death_callback = original_death_callback

# Testing HungryAnt removes bee when eating.
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

hungry = HungryAnt()
place = gamestate.places["tunnel_0_0"]
place.add_insect(hungry)
place.add_insect(Bee(3))
place.add_insect(Bee(3))
hungry.action(gamestate)
assert len(place.bees) == 1
bee = Bee(3)
place.add_insect(bee)
bee.action(gamestate) # Bee kills chewing ant
assert place.ant is None
assert len(place.bees) == 2