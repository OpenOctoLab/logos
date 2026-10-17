#set page(width: 16cm, height: 16cm, margin: 0cm, fill: rgb("#161b22"))
#set text(font: ("Noto Color Emoji", "JuliaMono"), spacing: 0.67em)
#set par(leading: 0cm, spacing: 0cm)
#set block(above: 0fr, below: 0fr, inset: 0cm, outset: 0cm, spacing: 0fr)
#align(center + horizon, move(dy: 0.75cm)[
  #text(size: 10cm, fill: rgb("#c9d1d9"))[{]
  #h(-3cm)
  #box(move(dy: -0.5cm, text(size: 8cm)[🐙]))
  #h(-3cm)
  #text(size: 10cm, fill: rgb("#c9d1d9"))[}]
  #v(3cm)
  #text(weight: "extrabold", size: 1.8cm)[#text(fill: rgb("#ff7b72"))[Open]#text(fill: rgb("#d2a8ff"))[Octo]]
  #v(1cm)
  #block[
    #set text(
      weight: "extralight",
      size: 0.5cm,
      fill: rgb("#c9d1d9"),
    )
    #text(fill: rgb("#79c0ff"))[one]
    #text(fill: rgb("#d2a8ff"))[*octopus*] #text(fill: rgb("#ff7b72"))[ignites]
    #text(fill: rgb("#79c0ff"))[an]
    #text(fill: rgb("#a5d6ff"))[entire]
    #text(fill: rgb("#ffa657"))[*ecosystem*]
  ]
])
