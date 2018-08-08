# TelsaBOTage Commands

## Bootstrap

| Command | Usage |
| :--- | : ---|
| !update | Reload the supervisor. It will also reload all services |
| !uptime | Give bot uptime (time since when it is started) |
| !switch debug | Switch bot on debug channel |
| !switch standard | Switch bot on default channel |

## Supervisor

The supervisor manage all services available with the bot. It can enable, disable, or reload any services.
*Supervisor must be running to access the following commands. If not, reload it with* !update *.*

| Command | Usage |
| :--- | : ---|
| !status | Show status of all services (c.f. service status table). |
| !update <_service_> | Reload the _service_. It can be useful for updating the _service_ version or for restarting the _service_ in case of failure.  |
| !enable <_service_> | Enable the _service_. The _service_ need to be loaded to execute this command. |
| !disable <_service_> | Disable the _service_. The _service_ need to be loaded to execute this command. |

### Service Status Table

| Status | Description |
| :--- | : ---|
| MISSING | The service could not be loaded. Can be due to errors is source code. Fix it and reload the service with !update <_service_> command. |
| ON | The service is loaded and enabled. You can interact with it. |
| OFF | The service is loaded but disabled. All interactions are deactivated.  |
| R.I.P | The service encountered an error and is now disabled. It must be reload with !update <_service_> command. |

## Services

### Core

*Core service must be enabled to access the following commands. If not, see supervisor commands.*

| Command | Usage |
| :--- | : ---|
| !help | Show TelsaBOTage commands dedicated web page. |
| !patchnote | Show patch notes dedicated web page. |

### PokemOnIRC

*PokemOnIRC service must be enabled to access the following commands. If not, see supervisor commands.*

| Command | Usage |
| :--- | : ---|
| !pokedex [_user_] | Show pokedex of the _user_ (list of owned pokemons). *If no user is specified, show your pokedex.*|
| !pokestuff [_user_] | Show pokestuff of the _user_ (stuff used to catch pokemon: *pokeball*, *superball*, etc.). *If no user is specified, show your pokestuff.* |
| !pokemon [_arena_] | Show if there is any pokemon in the arena. |
| !pokemon <_name_/*id*> | Show information of the _name_ pokemon (or with *id* identifier). |
| !crush <_name_/*id*> | If you own any _name_ pokemon (or with *id* identifier), dismember it and make some kebabs with it. |
| !evolve <_name_/*id*> | Try to evolve _name_ pokemon (or with *id* identifier) into its pokemon evolution. You will need a _moonstone_ and some _kebabs_. |
| !buy barbapapa [_user_] | Try to buy 10 *barbapapa* for _user_. You must negotiate with a stupid bot to get them. *If no user is specified, buy them for yourself.* |
| !buy pokeball [_user_] | Try to buy a *pokeball* for _user_. You must negotiate with a stupid bot to get it. *If no user is specified, buy it for yourself.* |
| !buy superball [_user_] | Try to buy a *superball* for _user_. You must negotiate with a stupid bot to get it. *If no user is specified, buy it for yourself.* |
| !catch [*pokestuff*] [*number*] | Enter the arena. You will try to catch the pokemon with *pokestuff* and you will have *number* tries to succeed. *If no pokestuff is specified, barbapapa will be selected by default. If no number is specified, you will have one try.* |


### Ideabox

*Ideabox service must be enabled to access the following commands. If not, see supervisor commands.*

| Command | Usage |
| :--- | : ---|
| !ideabox | Show ideas dedicated web page. |
| !idea <_description_> | Add a new _idea_ to the box. |
| !ideabox vote <*id*> | Vote for the idea with the *id* identifier |
| !ideabox archive <*id*> | Archive the idea with the *id* identifier |

### Karma

*Karma service must be enabled to access the following commands. If not, see supervisor commands.*

| Command | Usage |
| :--- | : ---|
| !karma | Show my karma score. |
| !karmas | Show karma scores of all users. |