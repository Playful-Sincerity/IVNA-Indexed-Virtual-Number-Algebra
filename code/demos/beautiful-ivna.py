"""
Beautiful IVNA — Visual proof that dividing by zero works.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe

# Style
plt.rcParams.update({
    'figure.facecolor': '#0a0a1a',
    'axes.facecolor': '#0a0a1a',
    'text.color': '#e0e0e0',
    'axes.labelcolor': '#e0e0e0',
    'xtick.color': '#666680',
    'ytick.color': '#666680',
    'font.family': 'serif',
    'font.size': 11,
})

fig = plt.figure(figsize=(16, 20))

# ═══════════════════════════════════════════════════════
# Panel 1: The Roundtrip — dividing by zero and coming back
# ═══════════════════════════════════════════════════════
ax1 = fig.add_axes([0.08, 0.78, 0.84, 0.18])
ax1.set_xlim(-0.5, 10.5)
ax1.set_ylim(-1.5, 1.5)
ax1.axis('off')

ax1.text(0.5, 1.3, 'The Roundtrip', fontsize=20, fontweight='bold',
         color='#ffcc44', ha='center', transform=ax1.transAxes)
ax1.text(0.5, 1.12, 'Divide by zero. Multiply back. Nothing lost.',
         fontsize=12, color='#888899', ha='center', transform=ax1.transAxes,
         style='italic')

# The journey: 5 → ÷0₃ → ∞₅⸝₃ → ×0₃ → 5
nodes = [
    (1, 0, '5', '#44aaff', 0.4),
    (3.5, 0, '÷ 0₃', '#ff6666', 0.35),
    (5.5, 0, '∞₅⸝₃', '#ff44cc', 0.4),
    (7.5, 0, '× 0₃', '#66ff66', 0.35),
    (9.5, 0, '5', '#44aaff', 0.4),
]

for x, y, label, color, size in nodes:
    circle = plt.Circle((x, y), size, facecolor=color + '22',
                        edgecolor=color, linewidth=2)
    ax1.add_patch(circle)
    ax1.text(x, y, label, fontsize=16, fontweight='bold',
            color=color, ha='center', va='center')

# Arrows
arrow_style = dict(arrowstyle='->', color='#666688', lw=2,
                   connectionstyle='arc3,rad=0')
for (x1, _, _, _, s1), (x2, _, _, _, s2) in zip(nodes[:-1], nodes[1:]):
    ax1.annotate('', xy=(x2 - s2 - 0.05, 0), xytext=(x1 + s1 + 0.05, 0),
                arrowprops=arrow_style)

# The "impossible" label with strikethrough
ax1.text(5.5, -1.0, 'Standard math says: UNDEFINED',
         fontsize=11, color='#ff4444', ha='center', style='italic',
         path_effects=[pe.withStroke(linewidth=0, foreground='#ff4444')])
ax1.text(5.5, -1.35, 'IVNA says: ∞₅⸝₃  (infinity that remembers the 5)',
         fontsize=11, color='#ff44cc', ha='center')


# ═══════════════════════════════════════════════════════
# Panel 2: Building e from nothing
# ═══════════════════════════════════════════════════════
ax2 = fig.add_axes([0.1, 0.48, 0.80, 0.26])

ax2.text(0.5, 1.12, 'Building  e  from Nothing', fontsize=20, fontweight='bold',
         color='#ffcc44', ha='center', transform=ax2.transAxes)
ax2.text(0.5, 1.03, '(1 + ¹⁄ₙ)ⁿ  approaches e ... IVNA just computes it:  (1 + 0₁)^∞₁ = e',
         fontsize=11, color='#888899', ha='center', transform=ax2.transAxes,
         style='italic')

n_vals = np.arange(1, 201)
y_vals = (1 + 1.0/n_vals) ** n_vals

# The approach curve
ax2.plot(n_vals, y_vals, color='#44aaff', linewidth=2, alpha=0.8, zorder=2)

# Fill under curve approaching e
ax2.fill_between(n_vals, y_vals, np.e, alpha=0.08, color='#44aaff')

# e line
ax2.axhline(y=np.e, color='#ff44cc', linewidth=2, linestyle='--', alpha=0.7, zorder=1)
ax2.text(205, np.e, f'e = {np.e:.6f}...', fontsize=13, fontweight='bold',
         color='#ff44cc', va='center')

# Mark specific points
highlights = [(1, 2.0), (2, 2.25), (5, (1.2)**5), (10, (1.1)**10), (50, (1.02)**50)]
for n, val in highlights:
    ax2.plot(n, val, 'o', color='#ffcc44', markersize=6, zorder=3)
    if n <= 10:
        ax2.annotate(f'n={n}: {val:.3f}', xy=(n, val), xytext=(n+8, val-0.12),
                    fontsize=9, color='#ffcc44',
                    arrowprops=dict(arrowstyle='->', color='#ffcc44', lw=0.8))

# The IVNA point — a star at the end
ax2.plot(200, np.e, '*', color='#ff44cc', markersize=20, zorder=4)
ax2.annotate('IVNA: no limit needed\n(1 + 0₁)^∞₁ = e  exactly',
             xy=(200, np.e), xytext=(130, 2.35),
             fontsize=11, color='#ff44cc', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#ff44cc', lw=1.5))

ax2.set_xlabel('n  (number of steps)', fontsize=11)
ax2.set_ylabel('(1 + ¹⁄ₙ)ⁿ', fontsize=13)
ax2.set_xlim(0, 230)
ax2.set_ylim(1.9, 2.85)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_color('#333355')
ax2.spines['left'].set_color('#333355')


# ═══════════════════════════════════════════════════════
# Panel 3: The Dirac Delta — the impossible function
# ═══════════════════════════════════════════════════════
ax3 = fig.add_axes([0.1, 0.15, 0.80, 0.28])

ax3.text(0.5, 1.10, 'The Dirac Delta', fontsize=20, fontweight='bold',
         color='#ffcc44', ha='center', transform=ax3.transAxes)
ax3.text(0.5, 1.02, 'Infinitely tall.  Infinitely narrow.  Area = exactly 1.',
         fontsize=12, color='#888899', ha='center', transform=ax3.transAxes,
         style='italic')

x = np.linspace(-4, 4, 1000)

# Show Gaussian approximations getting sharper
sigmas = [1.0, 0.5, 0.2, 0.08]
colors_g = ['#224466', '#336688', '#4488aa', '#55aadd']
alphas = [0.3, 0.4, 0.6, 0.8]

for sigma, col, alpha in zip(sigmas, colors_g, alphas):
    gauss = (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-x**2 / (2*sigma**2))
    ax3.fill_between(x, gauss, alpha=alpha*0.3, color=col)
    ax3.plot(x, gauss, color=col, linewidth=1.5, alpha=alpha)

# The "true" delta — a single tall spike
spike_x = np.array([0, 0])
spike_y = np.array([0, 12])
ax3.plot(spike_x, spike_y, color='#ff44cc', linewidth=3, zorder=5)
ax3.plot(0, 12, marker='^', color='#ff44cc', markersize=12, zorder=5)

# Arrow indicating "goes to infinity"
ax3.annotate('height = ∞₁', xy=(0, 12), xytext=(1.5, 11),
             fontsize=13, fontweight='bold', color='#ff44cc',
             arrowprops=dict(arrowstyle='->', color='#ff44cc', lw=1.5))

# Width annotation
ax3.annotate('', xy=(-0.15, 0.5), xytext=(0.15, 0.5),
             arrowprops=dict(arrowstyle='<->', color='#66ff66', lw=2))
ax3.text(0.6, 0.8, 'width = 0₁', fontsize=13, fontweight='bold', color='#66ff66')

# The punchline
ax3.text(0.5, 0.88, 'IVNA:   ∞₁  ×  0₁  =  1  ×  1  =  1',
         fontsize=16, fontweight='bold', color='#ffcc44',
         ha='center', transform=ax3.transAxes,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcc4411',
                   edgecolor='#ffcc44', linewidth=1.5))

ax3.text(0.5, 0.78, 'That\'s it.  Height × Width = Area.  No limits.  No distribution theory.',
         fontsize=11, color='#888899', ha='center', transform=ax3.transAxes,
         style='italic')

# Labels for the Gaussians
ax3.text(-2.5, 1.5, 'Gaussians\napproaching δ', fontsize=10,
         color='#55aadd', ha='center', style='italic')

ax3.set_xlabel('x', fontsize=12)
ax3.set_xlim(-4, 4)
ax3.set_ylim(-0.3, 14)
ax3.set_yticks([])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_visible(False)
ax3.spines['bottom'].set_color('#333355')


# ═══════════════════════════════════════════════════════
# Bottom title
# ═══════════════════════════════════════════════════════
fig.text(0.5, 0.07, 'I  V  N  A', fontsize=32, fontweight='bold',
         color='#ffcc44', ha='center', alpha=0.3,
         fontfamily='serif')
fig.text(0.5, 0.04, 'Indexed Virtual Number Algebra',
         fontsize=12, color='#666680', ha='center',
         style='italic')
fig.text(0.5, 0.015, 'The notation is the contribution.',
         fontsize=10, color='#444460', ha='center')

out = '/Users/wisdomhappy/Playful Sincerity/PS Research/IVNA/code/demos/beautiful-ivna.png'
plt.savefig(out, dpi=200, bbox_inches='tight',
            facecolor='#0a0a1a', edgecolor='none')
print(f"Saved to {out}")
plt.close()
