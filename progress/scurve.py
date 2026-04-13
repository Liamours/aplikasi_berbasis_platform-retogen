import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date

milestones = [
    date(2026, 3, 12),
    date(2026, 4, 9),
    date(2026, 4, 27),
    date(2026, 5, 31),
    date(2026, 6, 7),
]

backend  = [0, 80, 90, 100, 100]
web      = [0, 30, 70, 100, 100]
mobile   = [0,  0,  0,  30, 100]
overall  = [(b + w + m) / 3 for b, w, m in zip(backend, web, mobile)]

labels = ["12 Mar", "9 Apr", "27 Apr", "31 May", "7 Jun"]

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(milestones, backend,  marker='o', linewidth=2.5, label='Backend',          color='#6AADA8')
ax.plot(milestones, web,      marker='o', linewidth=2.5, label='Frontend Web',     color='#B56B52')
ax.plot(milestones, mobile,   marker='o', linewidth=2.5, label='Mobile',           color='#8B7BAB')
ax.plot(milestones, overall,  marker='o', linewidth=2.5, label='Overall',          color='#3A3A3A', linestyle='--')

for i, d in enumerate(milestones):
    ax.annotate(f"{backend[i]}%",  (d, backend[i]),  textcoords="offset points", xytext=(-18, 6),  fontsize=8, color='#6AADA8')
    ax.annotate(f"{web[i]}%",      (d, web[i]),       textcoords="offset points", xytext=(6,  6),   fontsize=8, color='#B56B52')
    ax.annotate(f"{mobile[i]}%",   (d, mobile[i]),    textcoords="offset points", xytext=(6, -14),  fontsize=8, color='#8B7BAB')
    ax.annotate(f"{overall[i]:.0f}%", (d, overall[i]), textcoords="offset points", xytext=(6, 6), fontsize=8, color='#3A3A3A')

for d, label in zip(milestones, labels):
    ax.axvline(x=d, color='gray', linestyle=':', linewidth=0.8, alpha=0.5)

ax.set_ylim(-5, 115)
ax.set_xlim(date(2026, 3, 5), date(2026, 6, 14))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
plt.xticks(rotation=30, ha='right')

ax.set_title('RetoGen — S-Curve Progress', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Completion', fontsize=11)
ax.legend(loc='upper left', fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('scurve.png', dpi=150)
print("Saved to scurve.png")
