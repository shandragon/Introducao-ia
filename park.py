"""Ambiente de simulação do parque"""

from agents import *

class Food(Thing):
    pass

class Water(Thing):
    pass

class Smell(Thing):
    pass

class Park(GraphicEnvironment):
  count_step = 0

  def add_dog(self, agent, location):
    self.add_thing(agent, location)

  def add_food(self, location):
    self.add_thing(Food(), location)
    # Adicionando os cheiros da comida
    for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]:
      self.add_thing(Smell(), [location[0] + x, location[1] + y])

  def add_water(self, location):
    self.add_thing(Water(), location)

  def percept(self, agent):
    '''return a list of things that are in our agent's location'''
    things = self.list_things_at(agent.location)
    # Verifica para onde o agente está indo
    loc = copy.deepcopy(agent.location)

    if agent.direction.direction == Direction.R:
      loc[0] += 1
    elif agent.direction.direction == Direction.L:
      loc[0] -= 1
    elif agent.direction.direction == Direction.D:
      loc[1] += 1
    elif agent.direction.direction == Direction.U:
      loc[1] -= 1

    # Verifique se o agente está prestes a bater em uma parede
    if not self.is_inbounds(loc):
      things.append(Bump())
    return things

  def execute_action(self, agent, action):
    '''changes the state of the environment based on what the agent does.'''
    self.count_step += 1
    print('Simulação no passo {}'.format(self.count_step))
    if action == 'turnright':
      print('{} optou por {} na localização: {}'.format(str(agent)[1:-1], action, agent.location))
      agent.turn(Direction.R)
    elif action == 'turnleft':
      print('{} optou por {} na localização: {}'.format(str(agent)[1:-1], action, agent.location))
      agent.turn(Direction.L)
    elif action == 'moveforward':
      print('{} optou por mover {}wards na localização: {}'.format(str(agent)[1:-1], agent.direction.direction, agent.location))
      agent.moveforward()
    elif action == "eat":
      items = self.list_things_at(agent.location, tclass=Food)
      if len(items) != 0:
        if agent.eat(items[0]):
          print('{} comendo {} na localização: {}'
            .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
          self.delete_thing(items[0])
          # Removendo os cheiros da comida
          location_food = agent.location
          for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]:
            smell = self.list_things_at([location_food[0] + x, location_food[1] + y], tclass=Smell)
            if len(smell) != 0:
              self.delete_thing(smell[0])
    elif action == "drink":
      items = self.list_things_at(agent.location, tclass=Water)
      if len(items) != 0:
        if agent.drink(items[0]):
          print('{} bebendo {} na localização: {}'
            .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
          self.delete_thing(items[0])

  def is_done(self):
    '''By default, we're done when we can't find a live agent,
    but to prevent killing our cute dog, we will stop before itself - when there is no more food or water'''
    no_edibles = not any(isinstance(thing, Food) or isinstance(thing, Water) for thing in self.things)
    dead_agents = not any(agent.is_alive() for agent in self.agents)
    return dead_agents or no_edibles
