import matplotlib.pyplot as plt

class Person:
  def __init__(self, surname, lastname, babyname, birthdate, deathdate, living_at, ismale, father, mother, child):
    self.surname = surname.strip()
    self.lastname = lastname.strip()
    self.babyname = babyname.strip()
    self.birthdate = birthdate.strip()
    self.deathdate = deathdate.strip()
    self.living_at = living_at.strip()
    self.ismale = ismale.strip().lower() == 'true'
    self.father = father.strip()
    self.mother = mother.strip()
    self.child = child.strip()

  def out(self):
    name = self.surname
    name += f" {self.lastname}" if self.lastname else ""
    name += f" ({self.babyname})" if self.babyname else ""
    name += "\n"
    birth = self.birthdate if self.birthdate else "?"
    death = self.deathdate if self.deathdate else "?"
    birthdeath = f"{birth} - {death}"
    return f"{name} ({birthdeath})\n{self.living_at}"
  
  def name(self):
    return self.surname + " " + self.lastname

class TreeNode:
  def __init__(self, o, l=None, r=None):
    self.o = o
    self.l = l
    self.r = r

def build_tree(value_matrix):
  person_list = []
  for i in range(len(value_matrix)):
    try:
      person_list.append(Person(*value_matrix[i]))
    except Exception as e:
      print(f"Faulty line number {str(i)} {str(value_matrix[i])}")
    
  me = person_list[0]
  while me.child:
    found = False
    for p in person_list:
      if p.name() == me.child:
        me = p
        person_list.remove(p)
        found = True
        break
    if not found:
      break
  
  tree_root = TreeNode(me)
  queue = [tree_root]
  while person_list and queue:
    c = queue.pop(0)
    to_remove = []
    for p in person_list:
      if p.child == c.o.name():
        if c.o.father == p.name() and p.ismale:
          c.l = TreeNode(p)
          queue.append(c.l)
          to_remove.append(p)
        elif c.o.mother == p.name() and not p.ismale:
          c.r = TreeNode(p)
          queue.append(c.r)
          to_remove.append(p)
    for p in to_remove:
      person_list.remove(p)
  return tree_root

def parse_csv(file):
  with open(file, "r") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line for line in lines if not line.startswith("#")]
    lines = [ [elem.strip() for elem in line.split(",")] for line in lines]
    return lines

import matplotlib.pyplot as plt

def plot_tree(node, x=0, y=0, dx=5, dy=2, level=0, positions=None, labels=None, colors=None, depth_factor=1, side=None):
  if positions is None:
    positions = {}
  if labels is None:
    labels = {}
  if colors is None:
    colors = {}

  # Place the current node
  positions[node] = (x, y)
  labels[node] = node.o.out()

  # Set the color of the node
  if level == 0:
    colors[node] = 'lightgreen'  # Root node
  elif side == 'left':
    colors[node] = 'lightblue'  # Left nodes
  elif side == 'right':
    colors[node] = 'lightcoral'  # Right nodes (light red)

  # Adjust the horizontal distance based on the depth of the tree
  adjusted_dx = dx / (2 ** level) * depth_factor

  # Plot left (father)
  if node.l is not None:
    # Arrow from father to child (pointing downwards)
    plt.arrow(x - adjusted_dx, y + dy, adjusted_dx, -dy, head_width=0.2, head_length=0.2, fc='black', ec='black')
    plot_tree(node.l, x - adjusted_dx, y + dy, dx, dy, level + 1, positions, labels, colors, depth_factor, side='left')

  # Plot right (mother)
  if node.r is not None:
    # Arrow from mother to child (pointing downwards)
    plt.arrow(x + adjusted_dx, y + dy, -adjusted_dx, -dy, head_width=0.2, head_length=0.2, fc='black', ec='black')
    plot_tree(node.r, x + adjusted_dx, y + dy, dx, dy, level + 1, positions, labels, colors, depth_factor, side='right')

  return positions, labels, colors

def draw_family_tree(tree_root, depth_factor=1):
  plt.figure(figsize=(10, 8))

  # Generate the positions, labels, and colors
  positions, labels, colors = plot_tree(tree_root, depth_factor=depth_factor)

  # Draw nodes as circles with different colors
  for node, (x, y) in positions.items():
    plt.scatter(x, y, s=2000, color=colors[node], edgecolor='black', zorder=2)
    plt.text(x, y, labels[node], ha="center", va="center", fontsize=8, bbox=dict(facecolor=colors[node], edgecolor="black", boxstyle="round,pad=0.5"))

  # Set axis limits and make the tree aesthetically pleasing
  plt.xlim(-10 * depth_factor, 10 * depth_factor)
  plt.ylim(-10 * depth_factor, 10 * depth_factor)
  plt.axis('off')  # Turn off axis

  # make title big and fancy
  plt.title("Family Tree - " + tree_root.o.name(), fontdict={'fontsize': 20, 'fontweight': 'bold'})
  # save plot as svg
  plt.savefig("family_tree.svg")
  plt.savefig("family_tree.png")
  # show plot
  plt.show()

def main():
  tree = build_tree(parse_csv("family.csv"))
  draw_family_tree(tree)


if __name__ == "__main__":
  main()