import music21.environment as env
from pathlib import Path

user_env = env.UserSettings()
# user_env.create() # uncomment if the flle doesn't exist

# After creating an environment file, the resulting XML preference file can be edited directly by the user
#  or using the UserSettings object. The keys tell you what can be changed:
for key in sorted(user_env.keys()):
    print(key)

# path of the xml file
print(user_env.getSettingsPath())

# #set the enviroment:
# path = Path("C:/Program Files (x86)/LilyPond/usr/bin/lilyPound.exe")
# user_env['lilypondPath'] = path
# print(user_env['lilypondPath'])