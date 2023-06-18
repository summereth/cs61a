from ants import *
beehive, layout = Hive(AssaultPlan()), dry_layout
gamestate = GameState(None, beehive, ant_types(), layout, (1, 9))

container = ContainerAnt(1)
container2 = ContainerAnt(2)
container3 = ContainerAnt(3)
throw_long = LongThrower(1)
assert not container.can_contain(container2)
assert container3.can_contain(throw_long)

container = ContainerAnt(2)
friend = HungryAnt()
assert container.ant_contained is None
container.store_ant(friend)
assert container.ant_contained is friend

container = ContainerAnt(2)
assert container.ant_contained is None
friend = HungryAnt()
container.store_ant(friend)
assert container.ant_contained is friend
place = gamestate.places["tunnel_0_0"]
place.add_insect(container)
friend.place = place
bee = Bee(3)
place.add_insect(bee)
container.action(gamestate)  # Container holds a HungryAnt that loves to eat!
assert bee.health == 0

container = ContainerAnt()
container.action(gamestate) # ContainerAnt does not have an ant contained, should not have any action taken!
