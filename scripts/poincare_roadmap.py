import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def poincare_to_euclidean(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

fig, ax = plt.subplots(1, 1, figsize=(20, 20), facecolor='#0d1117')
ax.set_facecolor('#0d1117')
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect('equal')
ax.axis('off')

# Poincare disk boundary
boundary = plt.Circle((0, 0), 1.0, fill=False, color='#30363d', linewidth=2)
ax.add_patch(boundary)

# Inner depth circles
for r in [0.3, 0.6, 0.85]:
    ax.add_patch(plt.Circle((0, 0), r, fill=False, color='#21262d', linewidth=0.5, linestyle='--'))

# Colors
C = {
    'core': '#f0883e', 'gov': '#4cb050', 'music': '#7289da',
    'sci': '#e06c75', 'human': '#c678dd', 'infra': '#56b6c2', 'meta': '#e5c07b',
}

# CENTER: Demerzel
ax.plot(0, 0, 'o', color=C['core'], markersize=30, zorder=10)
ax.text(0, 0.05, 'Demerzel', ha='center', va='bottom', fontsize=18, fontweight='bold', color='white')
ax.text(0, -0.05, 'Governance', ha='center', va='top', fontsize=11, color='#8b949e')

# RING 1 (r=0.3): Core systems
ring1 = [
    ('Constitution\n11 Articles', 0, C['gov']),
    ('Tetravalent\nT/F/U/C', np.pi/3, C['core']),
    ('Streeling\n13 Depts', 2*np.pi/3, C['music']),
    ('Driver\n8-Phase', np.pi, C['infra']),
    ('Meta-Grammar\nSelf-Governing', 4*np.pi/3, C['meta']),
    ('Conscience\nSignals', 5*np.pi/3, C['gov']),
]
for label, theta, color in ring1:
    x, y = poincare_to_euclidean(0.3, theta)
    ax.plot(x, y, 'o', color=color, markersize=20, zorder=8)
    ax.text(x, y + 0.07, label, ha='center', va='bottom', fontsize=11, fontweight='bold', color='white')
    ax.plot([0, x], [0, y], '-', color=color, alpha=0.3, linewidth=1.5)

# RING 2 (r=0.6): Active systems
ring2 = [
    ('Fuzzy\nEnum/DU', -0.15, C['gov'], 'SPEC READY'),
    ('BS Detector\n10 Domains', 0.2, C['gov'], 'v2'),
    ('Staleness\nDetection', 0.5, C['gov'], '30+ STALE'),
    ('Blind Spots', 0.8, C['gov'], 'GRAMMAR'),
    ('23 Courses\n6 Languages', 1.1, C['music'], 'ALL DEPTS'),
    ('Satriani\nAdvanced', 1.4, C['music'], 'NEW'),
    ('Research\nCycle', 1.7, C['music'], 'VALIDATE'),
    ('ML Pipelines\nGrammar', 2.1, C['sci'], 'ix'),
    ('151 tars\nMCP Tools', 2.5, C['sci'], 'CATALOGED'),
    ('MOG Executor\n42 Tasks', 2.9, C['sci'], 'PLANNED'),
    ('Discord Bot', 3.3, C['infra'], 'LIVE'),
    ('MetaFix\n5 Levels', 3.65, C['meta'], 'SKILL'),
    ('MetaBuild\nFactory', 4.0, C['meta'], 'FACTORY'),
    ('Context\nBudget', 4.4, C['human'], 'ECC'),
    ('Continuous\nLearning', 4.8, C['human'], 'POLICY'),
    ('Patterns\nCatalog', 5.2, C['human'], '5 FOUND'),
    ('README\nSync', 5.6, C['human'], 'POLICY'),
    ('18 Grammars\nPrefixed', 6.0, C['core'], 'LIVING'),
]
for label, theta, color, status in ring2:
    x, y = poincare_to_euclidean(0.6, theta)
    ax.plot(x, y, 'o', color=color, markersize=14, zorder=7)
    ax.text(x, y + 0.055, label, ha='center', va='bottom', fontsize=8.5, color='white')
    ax.text(x, y - 0.045, status, ha='center', va='top', fontsize=7, color=color, fontstyle='italic')

# RING 3 (r=0.88): Horizon
ring3 = [
    ('55 Course\nTranslations', 0.2), ('K-Theory\nBundles', 0.6),
    ('External\nGrammars', 1.0), ('F# Type\nProvider', 1.4),
    ('File\nWatcher', 1.8), ('Dashboard\nReports', 2.2),
    ('Belief\nRefresh', 2.6), ('Process\nSignals', 3.0),
    ('Discord\nChannels', 3.4), ('SymPy\nMCP', 3.8),
    ('NotebookLM\nExpand', 4.2), ('GA MCP\nIntegrate', 4.6),
    ('GitHub\nPages', 5.0), ('Hook\nProfiles', 5.4), ('Board\nViews', 5.8),
]
for label, theta in ring3:
    x, y = poincare_to_euclidean(0.88, theta)
    ax.plot(x, y, 'o', color='#8b949e', markersize=9, zorder=6, alpha=0.6)
    ax.text(x, y + 0.045, label, ha='center', va='bottom', fontsize=7, color='#8b949e', alpha=0.8)

# Legend
legend = [
    ('Core / Foundation', C['core']), ('Governance', C['gov']),
    ('Music / Education', C['music']), ('Science / Engineering', C['sci']),
    ('Human Sciences', C['human']), ('Infrastructure', C['infra']),
    ('Meta (factories)', C['meta']),
]
for i, (label, color) in enumerate(legend):
    y = -1.05 + i * 0.04
    ax.plot(-1.1, y, 's', color=color, markersize=10)
    ax.text(-1.05, y, label, va='center', fontsize=9, color='#c9d1d9')

# Depth legend
ax.text(1.08, -0.82, 'Center = Core', fontsize=8, color='#8b949e', ha='right')
ax.text(1.08, -0.87, 'Middle = Active', fontsize=8, color='#8b949e', ha='right')
ax.text(1.08, -0.92, 'Edge = Horizon', fontsize=8, color='#8b949e', ha='right')

# Title
ax.text(0, 1.08, 'GuitarAlchemist Ecosystem Roadmap', ha='center', fontsize=22, fontweight='bold', color='white')
ax.text(0, 1.035, 'Poincare Disk Model — center = core, edge = horizon (infinite distance)', ha='center', fontsize=10, color='#8b949e')

# Stats
stats = '7 repos  |  200+ MCP tools  |  18 grammars  |  24 policies  |  13 departments  |  23 courses  |  6 languages'
ax.text(0, -1.12, stats, ha='center', fontsize=9, color='#58a6ff')

plt.tight_layout()
plt.savefig('C:/Users/spare/source/repos/Demerzel/docs/roadmap-poincare.png', dpi=200, bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
print("Saved!")
