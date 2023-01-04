from drawer import Drawer
from handler import Handler

# drawing chunk
drawer = Drawer()
data = drawer.run()

# saving info about it
handler = Handler()
handler.run()