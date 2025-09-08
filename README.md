# pou

pou is a discord bot to interact with databases and run SQL commands. it is designed for educational purposes and for me to learn sql.

`INSERT INTO` commands automatically starts a transaction. you can commit the changes by specifying the commit parameter in /exec_command or run /commit_changes afterwards. committed database data will be saved across restarts of the bot.

### features

- connect to different databases (/connect_database)
- list all databases (/list_databases)
- delete databases (/delete_database)
- rename databases (/rename_database)
- backup databases (/backup_database)
- run SQL commands (/exec_command)
- commit transactions (/commit_changes)
- rollback transactions (/rollback_changes)

### usage

make sure you have [python](https://www.python.org/downloads/) installed.

1. clone the repository
   ```
   git clone https://github.com/ducky4life/pou.git
   ```
2. move to directory
   ```
   cd pou
   ```
3. install dependencies
   ```
   pip install -r requirements.txt
   ```
4. create .env file
   ```
   touch .env
   ```
5. put your secrets in the .env file (without the brackets: `[ ]`)
   ```
   POU_TOKEN="[your bot token]"
   ```
6. make database directory
   ```
   mkdir databases
   ```
7. run pou.py
   ```
   python pou.py
   ```

### todo

- [x] delete/rename databases
- [ ] transactions
- [x] backup databases