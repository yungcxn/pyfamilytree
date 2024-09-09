from tree import build_tree, parse_csv, build_levelmap

import svgwrite
import cairosvg
    

def draw_box(dwg, x, y, w, h, text, fontsize=20, color="green"):
  dwg.add(dwg.rect((x, y), (w, h), stroke="black", fill=color))
  # Text data
  lines = text.split("\n")
  # Font and text positioning
  line_height = fontsize + 5  # Adjusting line height
  text_x = x + w / 2  # Center horizontally
  text_y = y + (h - (line_height * len(lines))) / 2 + fontsize  # Center vertically
  
  for i, line in enumerate(lines):
    dwg.add(dwg.text(line, insert=(text_x, text_y + i * line_height), text_anchor="middle", font_size=fontsize, fill="black"))

def draw_arrow(dwg, x1, y1, x2, y2):
  dwg.add(dwg.line((x1, y1), (x2, y2), stroke="black", stroke_width=3))

def draw_family_tree(tree_root, tree_height):
  BOX_WIDTH = 220
  BOX_HEIGHT = 100
  BOX_MARGIN = 10
  BOX_DIST = BOX_MARGIN * 2
  max_level_cells = (2 ** tree_height)
  max_width = max_level_cells * (BOX_WIDTH + BOX_DIST)
  max_height = (tree_height + 1) * (BOX_DIST + BOX_HEIGHT)
  dwg = svgwrite.Drawing("family.svg", size=(f"{max_width}px", f"{max_height}px"))
  # draw all white
  dwg.add(dwg.rect((0, 0), (max_width, max_height), fill="white"))

  def draw_recursive(dwg, node, x, y, ox, oy, level):
    if node:
      color = "green"
      if node.o.ismale:
        color = "lightblue"
      elif not node.o.ismale:
        color = "pink"

      draw_box(dwg, x, y, BOX_WIDTH, BOX_HEIGHT, node.o.out(),color=color)
      if level > 1:
        draw_arrow(dwg, x + BOX_WIDTH / 2, y + BOX_HEIGHT, ox + BOX_WIDTH / 2 + (-20 if x <= ox else +20), oy)

      newy = y - BOX_HEIGHT - BOX_DIST
      if node.l:
        newx = x + BOX_WIDTH / 2 - max_width / (2 ** (level+1)) - BOX_WIDTH / 2
        draw_recursive(dwg, node.l, newx, newy, x, y, level + 1)
      if node.r:
        newx = x + BOX_WIDTH / 2 + max_width / (2 ** (level+1)) - BOX_WIDTH / 2
        draw_recursive(dwg, node.r, newx, newy, x, y, level + 1)

  draw_recursive(dwg, tree_root, max_width / 2 - BOX_WIDTH / 2, max_height - BOX_MARGIN - BOX_HEIGHT, 0, 0, 1)

  # Save the SVG
  dwg.save()
  
  # render as png
  cairosvg.svg2png(url="family.svg", write_to="family.png")

def main():
  tree_root = build_tree(parse_csv("family.csv"))
  level_map = build_levelmap(tree_root)
  draw_family_tree(tree_root, max(level_map.keys()))

if __name__ == "__main__":
  main()