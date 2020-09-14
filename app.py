from terminal_commands import TerminalCommands
from db_interactions import DbInteractions

DbInteractions.create_tables()
print(TerminalCommands.welcome())
TerminalCommands.select_activity()