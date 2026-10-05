import math

def start_animation(canvas, root):
    """Animate the pulsing rings on the given canvas."""
    outer = canvas.create_oval(40, 40, 310, 310, outline="#0088ff", width=10)
    inner = canvas.create_oval(60, 60, 290, 290, outline="#44ccff", width=4)
    angle = 0

    def animate():
        nonlocal angle
        angle += 4
        pulsing = 8 * math.sin(math.radians(angle))

        canvas.coords(outer, 40 - pulsing, 40 - pulsing, 310 + pulsing, 310 + pulsing)
        canvas.coords(inner, 60 - pulsing/2, 60 - pulsing/2, 290 + pulsing/2, 290 + pulsing/2)

        glow = int((math.sin(math.radians(angle * 2)) + 1) * 120)
        color_outer = f"#00{format(glow, '02x')}ff"
        color_inner = f"#44{format(glow, '02x')}ff"

        canvas.itemconfig(outer, outline=color_outer)
        canvas.itemconfig(inner, outline=color_inner)

        root.after(40, animate)

    animate()