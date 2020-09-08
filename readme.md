# Eso-Bot
Your Elder Scrolls online companion brought to discord. \
You are welcome to join our [support server](https://discord.gg/5xvAHhU).

## Contributors
Thanks to the following people for their contributions to the project:

-[Ruben Eekhof](https://github.com/RubenJ01) *project leader* \
-[Barbara Sofia](https://github.com/BarbaraSofia) *database management* \
-[RohanJnr](https://github.com/RohanJnr) *several contributions*

## Contributing
### Requirements
- Python 3.8 or higher
- Pipenv 
  - Get it by running
  
    -`pip install pipenv`

### Starting
##### 1.Cloning the repo
- Clone the repo or fork it and then clone from your profile.
- Cd into **eso-bot**
- Create a new branch by doing the following:

  - `git checkout -b branch_name`
##### 2.Pipenv and migrations
- Go to directory where the pipfile is and run 

  -`pipenv sync --dev`
- Activate pipenv by doing 

  -`pipenv shell`
  
##### 4.Config vars
- Go into the folder **eso_bot** and create a file called **authentication.py**
- Copy everything from **authentication.py.example** into your **authentication.py**.
- Replace the token value with your own bot token and the logging channel id to your own logging channel id.
  
##### 5.Running the bot
- Go into the folder **eso-bot** and open up you terminal/cmd.
- Activate pipenv by running

  -`pipenv shell`
- Run the bot by using

  -`pipenv run start`

## Progress
### Dungeons:
Arx Corinium :white_check_mark: \
Blackheart Haven :white_check_mark: \
Blessed Crucible :white_check_mark: \
Bloodroot Forge :white_check_mark: \
City of Ash I :white_check_mark: \
City of Ash II :white_check_mark: \
Cradle of Shadows :white_check_mark: \
Crypt of Hearts I :white_check_mark: \
Crypt of Hearts II :white_check_mark: \
Darkshade Caverns I :white_check_mark: \
Darkshade Caverns II\
Depths of Malatar\
DireFrost Keep\
Elden Hollow I\
Elden Hollow II\
Falkreath Hold\
Fang Lair\
Frostvault\
Fungal Grotto I\
Fungal Grotto II\
Imperial City Prison\
Lair of Maarselok\
March of Scarifices\
Moon Hunter Keep\
Moongrave Fane\
Ruins of Mazzatun\
Scalecaller Peak\
Selenes's Web\
Spindleclutch I\
Spindleclutch II\
Tempest Island\
Vaults of Madness\
Volenfell\
Wayrest Sewers I\
Wayrest Sewerest II\
White-Gold Tower
