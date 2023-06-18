from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
thrower = ThrowerAnt()
ant_place = gamestate.places["tunnel_0_0"]
ant_place.add_insect(thrower)
 
near_bee = Bee(2) # A Bee with 2 health
far_bee = Bee(3)  # A Bee with 3 health
hive_bee = Bee(4) # A Bee with 4 health
hive_place = gamestate.beehive
assert hive_place.is_hive == True
hive_place.add_insect(hive_bee)
assert (thrower.nearest_bee() is hive_bee) == False # Bees in the Hive can never be attacked
near_place = gamestate.places['tunnel_0_3']
far_place = gamestate.places['tunnel_0_6']
assert near_place.is_hive == False
near_place.add_insect(near_bee)
far_place.add_insect(far_bee)
nearest_bee = thrower.nearest_bee()
assert (nearest_bee is far_bee) == False
assert (nearest_bee is near_bee) == True
assert nearest_bee.health == 2
thrower.action(gamestate)    # Attack! ThrowerAnts do 1 damage
assert near_bee.health == 1
assert far_bee.health == 3
assert thrower.place is ant_place    # Don't change self.place!

'''
# Testing Nearest bee not in the beehive
    beehive = gamestate.beehive
    bee = Bee(2)
    beehive.add_insect(bee)      # Adding a bee to the beehive
    thrower.nearest_bee() is bee
          False
    thrower.action(gamestate)    # Attempt to attack
    bee.health                 # Bee health should not change
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
    # Test that ThrowerAnt attacks bees on its own square
    near_bee = Bee(2)
    ant_place.add_insect(near_bee)
    thrower.nearest_bee() is near_bee
          True
    thrower.action(gamestate)   # Attack!
    near_bee.health           # should do 1 damage
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
    # Test that ThrowerAnt attacks bees at end of tunnel
    near_bee = Bee(2)
    gamestate.places["tunnel_0_8"].add_insect(near_bee)
    thrower.nearest_bee() is near_bee
          True
    thrower.action(gamestate)   # Attack!
    near_bee.health           # should do 1 damage
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
    # Test that ThrowerAnt attacks bees 4 places away
    near_bee = Bee(2)
    gamestate.places["tunnel_0_4"].add_insect(near_bee)
    thrower.nearest_bee() is near_bee
          True
    thrower.action(gamestate)   # Attack!
    near_bee.health           # should do 1 damage
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
    # Testing ThrowerAnt chooses a random target
    bee1 = Bee(1001)
    bee2 = Bee(1001)
    gamestate.places["tunnel_0_3"].add_insect(bee1)
    gamestate.places["tunnel_0_3"].add_insect(bee2)
    # Throw 1000 times. The first bee should take ~1000*1/2 = ~500 damage,
    # and have ~501 remaining.
    for _ in range(1000):
          ...     thrower.action(gamestate)
    # Test if damage to bee1 is within 6 standard deviations (~95 damage)
    # If bees are chosen uniformly, this is true 99.9999998% of the time.
    def dmg_within_tolerance():
          ...     return abs(bee1.health-501) < 95
    dmg_within_tolerance()
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
    from ants import *
    ThrowerAnt.implemented
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""

#
      """,
      'teardown': '',
      'type': 'doctest'
    }
'''