from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)

laser = LaserAnt()
ant = HarvesterAnt(2)
bee1 = Bee(2)
bee2 = Bee(2)
bee3 = Bee(2)
bee4 = Bee(2)
gamestate.places["tunnel_0_0"].add_insect(laser)
gamestate.places["tunnel_0_0"].add_insect(bee4)
gamestate.places["tunnel_0_3"].add_insect(bee1)
gamestate.places["tunnel_0_3"].add_insect(bee2)
gamestate.places["tunnel_0_4"].add_insect(ant)
gamestate.places["tunnel_0_5"].add_insect(bee3)
laser.action(gamestate)
print(bee4.health, bee1.health, bee2.health, ant.health, bee3.health)
assert bee4.health == 0.0
assert bee1.health == 0.8125
assert bee2.health == 0.875
assert ant.health == 1.1875
assert bee3.health == 1.5