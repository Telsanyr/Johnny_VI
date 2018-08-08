# Johnny VI

## Introduction

**Johnny VI** is a IRC bot based on *python-irclib* created by Joel Rosdahl: https://github.com/jbalogh/python-irclib

## What is the purpose of this bot ?

> *I don't know, maybe we'll never know. What does it matter?* - Davos Seaworth

## Installation

#### Clone the repository
Clone this repository (*bot* folder) in an empty folder (the *project* folder) because the installation process will create a *database* folder at the same level. After complete deployment, your *project* folder will look like this:

~~~~
<project folder>
├── bot/
│   ├── libs/
|   |   └── ...
│   ├── logs/
|   |   └── ...
│   ├── src/
|   |   └── ...
│   ├── tools/
|   |   └── ...
│   ├── web/
|   |   └── ...
|   ├── ...
|   ├── README.md
│   ├── deploy_database.cmd
│   ├── deploy_website.cmd
│   ├── run_bot.cmd
│   ├── run_bot_debug.cmd
│   ├── run_bot_mockup.cmd
│   └── run_website.cmd
└── database/
    ├── bootstrap/
    │   ├── debug_connection.json
    │   └── prod_connection.json
    └── services/
        └── ...
~~~~

#### Deploy the database
For the moment, your *database* folder has not been created. You need to run the script `deploy_database.cmd`. Then, you need to complete both following files :
~~~~
<project folder>
└── database/
    └── bootstrap/
        ├── debug_connection.json
        └── prod_connection.json
~~~~

With the following information:
- IRC_HOST_IP
- IRC_HOST_PORT
- IRC_ACCOUNT_USERNAME
- IRC_ACCOUNT_PASSWORD
- ACTIVE_ROOM
- DEBUG_ROOM
- ADMIN_NICKNAME
- BOT_NICKNAME
- LUTRA_NICKNAME
- WEBSITE_URL

The `prod_connection.json` file contains information used when the bot is run in production mode.
The `debug_connection.json` file contains information used when the bot is run in debug mode.

#### Website installation
##### Requirement
The will need to install both **Node.js** and **npm** in order to setup and run the website. See https://nodejs.org/

##### Installation
For your website installation, you need to run the script `deploy_website.cmd`. It will install all node-packages needed with **npm**.

## How to start everything ?

### Bot launcher

You can start the bot with the `run_bot.cmd` script. Connection information will be based on `prod_connection.json` file. The bot should connect to the mentioned IRC server and join the *active room*.

You can run the bot in *debug mode* with `run_bot_debug.cmd` if you want to use the `debug_connection.json` file.
You can run the bot in *mock-up mode* with `run_bot_mockup.cmd`, it will not connect to any IRC server but you can interact with it in command line (as if you were in a IRC room). In *mock-up mode*, *debug* information are used.

### Website launcher

You can start the dedicated website with the `run_website.cmd` script. By default it will be run on the port **14623**.
