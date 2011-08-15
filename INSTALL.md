# Downloading BBot
There are various ways to download BBot, but the easiest way is to download a compressed archive from GitHub: <https://github.com/aj00200/BBot/archives/master>

# Installing and configuring BBot
Extract those files anywhere on your hard drive and open a terminal.
When you are in the terminal, change the directory (cd) to the one in which the BBot files are stored.
Afterwards, rename or copy the config-dist file to "config.cfg" and modify it to fit your needs or run
(On *NIX only) bbot-makeconf.

You also have the option of placing a config file in ~/.BBot/ where ~ denotes your home directory as defind by the global HOME variable. This config will be used over all others.

# Running BBot
Lastly, run the following command (without quotes): `python bbot.py`
You will need to have Python installed to do this.

If you want it to keep running after you close the terminal, use a multiplexer such as GNU Screen.

BBot should now be running on your system, but if it isn't, you can always ask for help in #bbot on irc.ospnet.org (6667; SSL 6697)
