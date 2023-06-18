from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

# Container ant added before another ant
container = ContainerAnt()
other_ant = ThrowerAnt()
place = gamestate.places['tunnel_0_0']
place.add_insect(container)  # ContainerAnt in place first
place.add_insect(other_ant)
assert not place.ant is other_ant
assert place.ant is container
assert container.ant_contained is other_ant

# Any Container Ant can be added after another ant
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))
container = ContainerAnt()
other_ant = ThrowerAnt()
place = gamestate.places['tunnel_0_0']
place.add_insect(other_ant)  # Other ant in place first
assert place.ant is other_ant
place.add_insect(container)
assert place.ant is container
assert container.ant_contained is other_ant
