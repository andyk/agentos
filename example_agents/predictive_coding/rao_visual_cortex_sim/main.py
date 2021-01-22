# A simple implementation of predictive coding as desctribed in: 
# Predictive coding in the visual cortex: a functional interpretation
# of some extra-classical receptive-field effects, by Rajesh P. N. Rao
# and Dana H. Ballard.
#
# Inputs and errors propogate up the hierarchy
# representations propogate down.

# TODO:
# - Simplified version of 3-layer architecture from the paper:
#   - pure python
#   - input image that is either all black (0) or all white (1)
#   - one unit per layer (no branching in the hierarchy)

#######

class Unit:
  """
  A layer in the visual cortex hierarchy.
    r = the inferred causes of this units predictions, used as params
        to generative model to produce prediction images.
    e = the errors
  """
  def __init__(self, child):
    self.children = []
    self.parents = []
    self.r = 0
    self.e = 0
    self.add_child(child)

  def __str__(self):
    return (f"Num children: {len(self.children)}; " +
            f"Num Parents: {len(self.parents)}")


  # the generative function which takes r as in put and produces predictions.
  def f_of_r(self):
    return r

  def add_child(self, child):
    self.children.append(child)
    if self not in child.parents:
      child.add_parent(self)

  def add_parent(self, parent):
    self.parents.append(parent)
    if self not in parent.children:
      parent.add_child(self)
  
  def step(self):
    #TODO: allow more than one child per unit.
    assert len(self.children) == 1, "Cannot step a Unit until a child is set"
    for child in self.children:
      i = child.e # input
    a_hat = self.f_of_r(self.r)
    self.r = 0.5 * self.r +  0.5 * (self.r - self.e) # r_t depends on r_(t-1), e_(t-1)
    self.e = a_hat - i
    print(f"i={i}; a_hat={a_hat}; self.e={self.e}; self.r={self.r}") 


class InputUnit:
  """A special layer that represents an image coming into the visual cortex."""
  def __init__(self, input_series):
    self.parents = []
    assert len(input_series) > 0
    self.input_series = input_series
    self.next_e_index = -1
    self.e = None

  def add_parent(self, parent):
    self.parents.append(parent)
    if self not in parent.children:
      parent.add_child(self)

  def step(self):
    assert self.has_next()
    self.next_e_index += 1
    self.e = self.input_series[self.next_e_index]

  def has_next(self):
    return self.next_e_index < len(self.input_series) - 1 


if __name__ == '__main__':
  input_series = InputUnit([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0])
  layer_0 = Unit(input_series)
  layer_1 = Unit(layer_0)

  print(layer_0)
  print(layer_1)

  while input_series.has_next():
    i = input_series
    i.step()
    while len(i.parents) > 0:
      i = next(iter(i.parents))
    


def test_input_unit():
  i = InputUnit([2,3])
  assert i.e == None and i.has_next()
  i.step()
  assert i.e == 2 and i.has_next()
  i.step()
  assert i.e == 3 and not i.has_next()


def test_unit():
  i = InputUnit([2,3,4])
  u = Unit(i)
  assert u.r == 0
  assert u.e == 0
  u.step()

