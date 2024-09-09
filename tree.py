class Person:
  def __init__(self, surname, lastname, babyname, birthdate, deathdate, living_at, ismale, father, mother, *children):
    self.surname = surname.strip()
    self.lastname = lastname.strip()
    self.babyname = babyname.strip()
    self.birthdate = birthdate.strip()
    self.deathdate = deathdate.strip()
    self.living_at = living_at.strip()
    self.ismale = ismale.strip().lower() == 'true'
    self.father = father.strip()
    self.mother = mother.strip()
    self.children = [c.strip() for c in children] if children else []

  def out(self):
    name = self.surname
    name += f" {self.lastname}" if self.lastname else ""
    name += f" ({self.babyname})" if self.babyname else ""
    name += "\n"
    birth = self.birthdate if self.birthdate else "?"
    death = self.deathdate if self.deathdate else "?"
    birthdeath = "" if birth == "?" and death == "?" else f"{birth}-{death}\n"
    return f"{name}{birthdeath}{self.living_at}"
  
  def name(self):
    return self.surname if self.lastname == '' else self.surname + " " + self.lastname

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
  while me.children:
    found = False
    for p in person_list:
      if p.name() == me.children[0]:
        me = p
        person_list.remove(p)
        found = True
        break
    if not found:
      break
  
  tree_root = TreeNode(me)
  queue = [tree_root]
  while queue:
    c = queue.pop(0)
    for p in person_list:
      for child in p.children:
        if child == c.o.name():
          if c.o.father == p.name() and p.ismale:
            c.l = TreeNode(p)
            queue.append(c.l)
          elif c.o.mother == p.name() and not p.ismale:
            c.r = TreeNode(p)
            queue.append(c.r)
  return tree_root

def build_levelmap(tree_root):
  levelmap = {}
  queue = [(tree_root, 0)]
  while queue:
    c, l = queue.pop(0)
    if l not in levelmap:
      levelmap[l] = []
    levelmap[l].append(c.o)
    if c.l:
      queue.append((c.l, l + 1))
    if c.r:
      queue.append((c.r, l + 1))

  return levelmap

def parse_csv(file):
  with open(file, "r") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    lines = [line for line in lines if not line.startswith("#")]
    lines = [ [elem.strip() for elem in line.split(",")] for line in lines]
    return lines