# This is a changelog in English. Starts with version 6

# MaxMineOS 6

* Added help for the `pkghelp` package
* Added the `syslog` command
* Added the `pkghelp` package
* Fixed a bug when updating the system and then running the `syslog` command

# IMPORTANT

# To update the system to version 6, you need:

1. Start the system and log in
2. Run the `sysupdate` command
3. Shutdown the system
4. Delete file `System\logs\system.log`
5. Start the system again and check that everything works

**Update complete!**


# MaxMineOS 7
* Fixed updating kernel
* Adding updating messages to console
* Adding `pkg list` command
* Adding `pkg update` command
* Added logging encoding - UTF-8
* Hostnamectl internet checking


# MaxMineOS 8 and MaxMineOS 9 are skipped as it was just bugfixes

# MaxMineOS 10

* Added base pkghelp
* Added `history` command
* Added package manifest
* Added package updates check
* Added `pkg list upgradeable` command
* Added `pkg update --upgradeable` command
