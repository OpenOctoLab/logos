#set page(width: 16cm, height: 16cm, margin: 0cm)
#set text(font: ("Noto Color Emoji", "JuliaMono"), spacing: 0.67em)
#set par(leading: 0cm, spacing: 0cm)
#set block(above: 0fr, below: 0fr, inset: 0cm, outset: 0cm, spacing: 0fr)
#let file-svg = bytes(
  `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#161b22" class="icon icon-tabler icons-tabler-filled icon-tabler-file">
	<path d="M12 2l.117 .007a1 1 0 0 1 .876 .876l.007 .117v4l.005 .15a2 2 0 0 0 1.838 1.844l.157 .006h4l.117 .007a1 1 0 0 1 .876 .876l.007 .117v9a3 3 0 0 1 -2.824 2.995l-.176 .005h-10a3 3 0 0 1 -2.995 -2.824l-.005 -.176v-14a3 3 0 0 1 2.824 -2.995l.176 -.005h5z" />
	<path d="M19 7h-4l-.001 -4.001z" />
</svg>`.text,
)
#place(center + horizon, image(file-svg, height: 100%))
#align(center + horizon, move(dy: 2cm)[
  #text(size: 6cm, fill: rgb("#c9d1d9"))[{]
  #h(-2cm)
  #box(move(dy: -0.5cm, text(size: 4cm)[🐙]))
  #h(-2cm)
  #text(size: 6cm, fill: rgb("#c9d1d9"))[}]
])
