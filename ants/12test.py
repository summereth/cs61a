from ants import *
beehive = Hive(AssaultPlan())
dimensions = (2, 9)
gamestate = GameState(None, beehive, ant_types(), dry_layout, dimensions, food=100)

# Testing QueenAnt parameters
assert QueenAnt.food_cost == 7
queen = QueenAnt()
assert queen.health == 1

# Abstraction tests
original = ScubaThrower.construct
ScubaThrower.__init__ = lambda self, health=2: print("scuba init")
def modified_construct(cls, gamestate):
    print("scuba construct")
    return super(ScubaThrower, cls).construct(gamestate)
ScubaThrower.construct = classmethod(modified_construct)
queen = QueenAnt.construct(gamestate)
ScubaThrower.construct = original
queen = QueenAnt.construct(gamestate)

import ants, importlib
importlib.reload(ants)
beehive = ants.Hive(ants.AssaultPlan())
dimensions = (2, 9)
gamestate = ants.GameState(None, beehive, ants.ant_types(),ants.dry_layout, dimensions, food=20)
ants.ants_lose = lambda: None

# QueenAnt Placement
queen = ants.QueenAnt.construct(gamestate)
impostor = ants.QueenAnt.construct(gamestate)
assert impostor is None # you cannot create a second QueenAnt!
front_ant, back_ant = ants.ThrowerAnt(), ants.ThrowerAnt()
tunnel = [gamestate.places['tunnel_0_{0}'.format(i)] for i in range(9)]
tunnel[1].add_insect(back_ant)
tunnel[7].add_insect(front_ant)
assert tunnel[4].ant is None
assert back_ant.damage == 1          # Ants should not have double damage
assert front_ant.damage == 1
tunnel[4].add_insect(queen)
queen.action(gamestate)
assert queen.health == 1              # Long live the Queen!
assert back_ant.damage == 2           # Ants behind queen should have double damage
assert front_ant.damage ==1


# QueenAnt Removal
gamestate = ants.GameState(None, beehive, ants.ant_types(),ants.dry_layout, dimensions, food=20)

queen = ants.QueenAnt.construct(gamestate)
place = gamestate.places['tunnel_0_2']
place.add_insect(queen)
place.remove_insect(queen)
assert place.ant is queen        # True queen cannot be removed

# QueenAnt knows how to swim
gamestate = ants.GameState(None, beehive, ants.ant_types(),ants.dry_layout, dimensions, food=20)

queen = ants.QueenAnt.construct(gamestate)
water = ants.Water('Water')
water.add_insect(queen)
assert queen.health == 1

# Testing damage multiplier
gamestate = ants.GameState(None, beehive, ants.ant_types(),ants.dry_layout, dimensions, food=20)

queen_tunnel, side_tunnel = [[gamestate.places['tunnel_{0}_{1}'.format(i, j)] for j in range(9)] for i in range(2)]
# layout
# queen_tunnel: [Back, Guard/Guarded, Queen, Front, Bee     ]
# side_tunnel : [Side,              ,      ,      , Side Bee]
queen = ants.QueenAnt.construct(gamestate)
back = ants.ThrowerAnt()
front = ants.ThrowerAnt()
guard = ants.BodyguardAnt()
guarded = ants.ThrowerAnt()
side = ants.ThrowerAnt()
bee = ants.Bee(10)
side_bee = ants.Bee(10)
queen_tunnel[0].add_insect(back)
queen_tunnel[1].add_insect(guard)
queen_tunnel[1].add_insect(guarded)
queen_tunnel[2].add_insect(queen)
queen_tunnel[3].add_insect(front)
side_tunnel[0].add_insect(side)
queen_tunnel[4].add_insect(bee)
side_tunnel[4].add_insect(side_bee)
queen.action(gamestate)
assert bee.health == 9
back.action(gamestate)
assert bee.health == 7
front.action(gamestate)
bee.health == 6
guard.action(gamestate)
assert bee.health == 4 # if this is 5 you probably forgot to double the damage of the guard's contents
side.action(gamestate)
assert side_bee.health == 9

import ants, importlib
importlib.reload(ants)
beehive = ants.Hive(ants.AssaultPlan())
dimensions = (2, 9)
gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

'''
# Testing game over

queen = ants.QueenAnt.construct(gamestate)
tunnel = [gamestate.places['tunnel_0_{0}'.format(i)] for i in range(9)]
tunnel[4].add_insect(queen)
bee = ants.Bee(3)
tunnel[6].add_insect(bee)     # Bee in a different place from the queen
bee.action(gamestate)         # Game should not end
bee.move_to(tunnel[4])        # Bee moved to place with queen
bee.action(gamestate)         # Game should end: AntsLoseException
'''

# Testing if queen will not crash with no one to double
gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

queen = ants.QueenAnt.construct(gamestate)
gamestate.places['tunnel_0_2'].add_insect(queen)
queen.action(gamestate)
# Attack a bee
bee = ants.Bee(3)
gamestate.places['tunnel_0_4'].add_insect(bee)
queen.action(gamestate)
assert bee.health == 2 # Queen should still hit the bee

# Testing QueenAnt action method
gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

queen = ants.QueenAnt.construct(gamestate)
bee = ants.Bee(10)
ant = ants.ThrowerAnt()
gamestate.places['tunnel_0_0'].add_insect(ant)
gamestate.places['tunnel_0_1'].add_insect(queen)
gamestate.places['tunnel_0_4'].add_insect(bee)
queen.action(gamestate)
assert bee.health == 9  # Queen should damage bee
assert ant.damage == 2  # Queen should double damage
ant.action(gamestate)
assert bee.health == 7  # If failed, ThrowerAnt has incorrect damage
assert queen.health == 1  # Long live the Queen


import ants, importlib
importlib.reload(ants)
beehive = ants.Hive(ants.AssaultPlan())
dimensions = (2, 9)
gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

# Extensive damage doubling tests
gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

queen_tunnel, side_tunnel = [[gamestate.places['tunnel_{0}_{1}'.format(i, j)] for j in range(9)] for i in range(2)]
queen = ants.QueenAnt.construct(gamestate)
queen_tunnel[7].add_insect(queen)
# Turn 0
thrower = ants.ThrowerAnt()
fire = ants.FireAnt()
side = ants.ThrowerAnt()
front = ants.ThrowerAnt()
queen_tunnel[0].add_insect(thrower)
queen_tunnel[1].add_insect(fire)
queen_tunnel[8].add_insect(front)
side_tunnel[0].add_insect(side)
# layout right now
# [thrower, fire, , , , , , queen, front]
# [side   ,     , , , , , ,      ,      ]
thrower.damage, fire.damage = 101, 102
front.damage, side.damage = 104, 105
queen.action(gamestate)
# print(thrower.damage, fire.damage, front.damage, side.damage)
# print([queen_tunnel[i].ant for i in range(9)])
# print([side_tunnel[i].ant for i in range(9)])
assert (thrower.damage, fire.damage) == (202, 204)
assert (front.damage, side.damage) == (104, 105)
# Turn 1
tank = ants.TankAnt()
guard = ants.BodyguardAnt()
queen_tank = ants.TankAnt()
queen_tunnel[6].add_insect(tank)          # Not protecting an ant
queen_tunnel[1].add_insect(guard)         # Guarding FireAnt
queen_tunnel[7].add_insect(queen_tank)    # Guarding QueenAnt
# layout right now
# [thrower, guard/fire, , , , , tank, queen_tank/queen, front]
# [side   ,           , , , , ,     ,                 ,      ]
tank.damage, guard.damage, queen_tank.damage = 1001, 1002, 1003
queen.action(gamestate)
# unchanged
assert (thrower.damage, fire.damage) == (202, 204)
assert (front.damage, side.damage) == (104, 105)
assert (tank.damage, guard.damage) == (2002, 2004)
assert queen_tank.damage == 1003
# Turn 2
thrower1 = ants.ThrowerAnt()
thrower2 = ants.ThrowerAnt()
queen_tunnel[6].add_insect(thrower1)      # Add thrower1 in TankAnt
queen_tunnel[5].add_insect(thrower2)
# layout right now
# [thrower, guard/fire, , , , thrower2, tank/thrower1, queen_tank/queen, front]
# [side   ,           , , , ,         ,              ,                 ,      ]
thrower1.damage, thrower2.damage = 10001, 10002
queen.action(gamestate)
assert (thrower.damage, fire.damage) == (202, 204)
assert (front.damage, side.damage) == (104, 105)
assert (tank.damage, guard.damage) == (2002, 2004)
assert queen_tank.damage == 1003
assert (thrower1.damage, thrower2.damage) == (20002, 20004)
# Turn 3
tank.reduce_health(tank.health)             # Expose thrower1
queen.action(gamestate)
assert (thrower.damage, fire.damage) == (202, 204)
assert (front.damage, side.damage) == (104, 105)
assert guard.damage == 2004
assert queen_tank.damage == 1003
assert (thrower1.damage, thrower2.damage) == (20002, 20004)

# Adding/Removing QueenAnt with Container
gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

place = gamestate.places['tunnel_0_3']
queen = ants.QueenAnt.construct(gamestate)
container = ants.TankAnt()
place.add_insect(container)
assert place.ant is container
assert container.place is place
assert container.ant_contained is None
place.add_insect(queen)
print(queen.place.name)
assert container.ant_contained is queen
assert queen.place is container
queen.action(gamestate) # should not error

# test proper call to death callback
gamestate = ants.GameState(None, beehive, ants.ant_types(), ants.dry_layout, dimensions, food=20)

original_death_callback = ants.Insect.death_callback
ants.Insect.death_callback = lambda x: print("insect died")
real = ants.QueenAnt.construct(gamestate)
gamestate.places['tunnel_0_2'].add_insect(real)
ants.Insect.death_callback = original_death_callback

