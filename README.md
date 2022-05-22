# Chun's Discord Toolkit

## Setup

- After adding the bot to your server, go to *Integrations*
- Find Chun's Toolkit and go to *Manage*
- Set the appropriate permissions (safest to turn off permissions for everyone)

## Features

Simple bot to check stuff in your server to make sure there is not shady shit going on.

- Warns server admins if *administrator* permissions have been granted to another role
- Warns server admins if *manage server* permissions have been granted to a role
- Quickly see all members and bots with administrator permissions
- Quickly see all server members who failed to gain a role within after 21 days of joining
- Add Discord users to a blacklist by their userID (No follow up actions yet)
- Ban blacklisted Discord users as soon as they join (NOTE: revoking ban in Discord does not remove users from the blacklist atm)

## Upcoming
- Ban server members as soon as they are added to the blacklist
- Warning on webhooks changes
- Remove user from blacklist when their ban is revoked (very low priority)