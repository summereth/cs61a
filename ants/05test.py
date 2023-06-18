from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

# Testing FireAnt parameters
fire = FireAnt()
assert FireAnt.food_cost == 5
assert fire.health == 3

# Abstraction tests
original = Ant.__init__
Ant.__init__ = lambda self, health: print("init") #If this errors, you are not calling the parent constructor correctly.
fire = FireAnt()
Ant.__init__ = original
fire = FireAnt()
original = Ant.reduce_health
Ant.reduce_health = lambda self, amount: print("reduced") #If this errors, you are not calling the inherited method correctly
place = gamestate.places['tunnel_0_4']
place.add_insect(fire)
fire.reduce_health(1)
Ant.reduce_health = original

# Testing fire does damage to all Bees in its Place
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
fire = FireAnt(health=1)
place.add_insect(fire)        # Add a FireAnt with 1 health
place.add_insect(Bee(3))      # Add a Bee with 3 health
place.add_insect(Bee(5))      # Add a Bee with 5 health
assert len(place.bees) == 2               # How many bees are there?
place.bees[0].action(gamestate)  # The first Bee attacks FireAnt
assert fire.health == 0
assert fire.place is None
assert len(place.bees) == 1               # How many bees are left?
assert place.bees[0].health == 1           # What is the health of the remaining Bee?

gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
ant = FireAnt(health=1)           # Create a FireAnt with 1 health
place.add_insect(ant)      # Add a FireAnt to place
assert ant.place is place
place.remove_insect(ant)   # Remove FireAnt from place
assert not ant.place is place         # Is the ant's place still that place?

# Testing fire damage when the fire ant does not die
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
bee = Bee(5)
ant = FireAnt(health=100)
place.add_insect(bee)
place.add_insect(ant)
bee.action(gamestate) # attack the FireAnt
assert ant.health == 99
assert bee.health == 4
 
# Testing no hardcoded 3
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
bee = Bee(100)
ant = FireAnt(health=1)
ant.damage = 49
place.add_insect(bee)
place.add_insect(ant)
bee.action(gamestate) # attack the FireAnt
assert ant.health == 0
assert bee.health == 50

# Testing fire damage when the fire ant does die
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
bee = Bee(5)
ant = FireAnt(health=1)
place.add_insect(bee)
place.add_insect(ant)
bee.action(gamestate) # attack the FireAnt
assert ant.health == 0
assert bee.health == 1

# Testing fire does damage to all Bees in its Place
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
place.add_insect(FireAnt(1))
for i in range(100):          # Add 100 Bees with 3 health
    place.add_insect(Bee(3))
place.bees[0].action(gamestate)  # The first Bee attacks FireAnt
assert len(place.bees)== 0               # How many bees are left?

# Testing fire damage is instance attribute
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
bee = Bee(900)
buffAnt = FireAnt(1)
buffAnt.damage = 500   # Feel the burn!
place.add_insect(bee)
place.add_insect(buffAnt)
bee.action(gamestate) # attack the FireAnt
assert bee.health == 399  # is damage an instance attribute?

# General FireAnt Test
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
bee = Bee(10)
ant = FireAnt(1)
place.add_insect(bee)
place.add_insect(ant)
bee.action(gamestate)    # Attack the FireAnt
assert bee.health == 6
assert ant.health == 0
assert (place.ant is None) == True     # The FireAnt should not occupy the place anymore
bee.action(gamestate)
assert bee.health == 6             # Bee should not get damaged again
assert bee.place.name == 'tunnel_0_3'        # Bee should not have been blocked

# General FireAnt Test
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
place = gamestate.places['tunnel_0_4']
bee = Bee(10)
ant = FireAnt()
place.add_insect(bee)
place.add_insect(ant)
ant.reduce_health(0.1) # Poke the FireAnt
assert bee.health == 9.9             # Bee should only get slightly damaged
assert ant.health == 2.9
assert (place.ant is ant) == True      # The FireAnt should still be at place


# test proper call to death callback
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
original_death_callback = Insect.death_callback
Insect.death_callback = lambda x: print("insect died")
place = gamestate.places["tunnel_0_0"]
bee = Bee(3)
ant = FireAnt()
place.add_insect(bee)
place.add_insect(ant)
bee.action(gamestate)
bee.action(gamestate)
bee.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_health or Insect.reduce_health
Insect.death_callback = original_death_callback

from ants import *
FireAnt.implemented

'''
init
reduced
insect died
insect died
True
'''