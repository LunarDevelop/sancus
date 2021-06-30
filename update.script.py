import os

newModules = [
    "discord.py",
    "discord",
    "APScheduler",
    "requests",
    "validators",
    "dpymenus",
    "schedule",
    "statcord.py",
]

for module in newModules:

    os.system(f"pip install {module} --upgrade")