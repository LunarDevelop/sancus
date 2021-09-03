import os

disc = [
    "discord.py==1.7.3",
    "discord==1.0.1",
    "APScheduler==3.6.3",
    "requests==2.25.0",
    "validators==0.18.2",
    "dpymenus==1.3.1",
    "schedule==1.0.0",
    "statcord.py"
]

for module in disc:
    os.system(f"pip install {module}")