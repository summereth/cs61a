from ants import *

# Abstraction tests
original = ContainerAnt.__init__
ContainerAnt.__init__ = lambda self, health: print("init") #If this errors, you are not calling the parent constructor correctly.
bodyguard = BodyguardAnt()
ContainerAnt.__init__ = original
bodyguard = BodyguardAnt()
assert hasattr(bodyguard, 'ant_contained')

from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

# Testing removing a bodyguard doesn't remove contained ant
place = gamestate.places['tunnel_0_0']
bodyguard = BodyguardAnt()
test_ant = Ant(1)
# add ant first
place.add_insect(test_ant)
place.add_insect(bodyguard)
gamestate.remove_ant('tunnel_0_0')
assert place.ant is test_ant
assert bodyguard.place is None

# Testing bodyguarded ant keeps instance attributes
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

test_ant = Ant()
def new_action(gamestate):
    test_ant.health += 9000
test_ant.action = new_action
place = gamestate.places['tunnel_0_0']
bodyguard = BodyguardAnt()
place.add_insect(test_ant)
place.add_insect(bodyguard)
place.ant.action(gamestate)
assert place.ant.ant_contained.health== 9001

'''
# Testing single BodyguardAnt cannot hold two other ants
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

bodyguard = BodyguardAnt()
first_ant = ThrowerAnt()
place = gamestate.places['tunnel_0_0']
place.add_insect(bodyguard)
place.add_insect(first_ant)
second_ant = ThrowerAnt()
place.add_insect(second_ant)
'''

'''
# Testing BodyguardAnt cannot hold another BodyguardAnt
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

bodyguard1 = BodyguardAnt()
bodyguard2 = BodyguardAnt()
place = gamestate.places['tunnel_0_0']
place.add_insect(bodyguard1)
place.add_insect(bodyguard2)
'''

# Testing BodyguardAnt takes all the damage
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

thrower = ThrowerAnt()
bodyguard = BodyguardAnt()
bee = Bee(1)
place = gamestate.places['tunnel_0_0']
place.add_insect(thrower)
place.add_insect(bodyguard)
place.add_insect(bee)
assert bodyguard.health == 2
bee.action(gamestate)
assert (bodyguard.health, thrower.health) == (1, 1)
bee.action(gamestate)
assert (bodyguard.health, thrower.health) == (0, 1)
assert bodyguard.place is None
assert place.ant is thrower
bee.action(gamestate)
assert thrower.health == 0
assert place.ant is None

# test proper call to death callback
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

original_death_callback = Insect.death_callback
Insect.death_callback = lambda x: print("insect died")
place = gamestate.places["tunnel_0_0"]
bee = Bee(3)
bodyguard = BodyguardAnt()
ant = ThrowerAnt()
place.add_insect(bee)
place.add_insect(ant)
place.add_insect(bodyguard)
bee.action(gamestate)
bee.action(gamestate)
bee.action(gamestate) # if you fail this test you probably didn't correctly call Ant.reduce_health or Insect.reduce_health
Insect.death_callback = original_death_callback
