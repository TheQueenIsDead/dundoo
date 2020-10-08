from commands.command import Command
from linker.linker import Linker

action1 = Command()
action1.set_action(lambda: print("Hello from Action 1!"))
action2 = Command()
action2.set_action(lambda: print("Hello from Action 2!"))


action1.run()


linker = Linker()
linker.load('./flow.yml')
linker.validate()
linker.link()
