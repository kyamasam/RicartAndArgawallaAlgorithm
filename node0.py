#samuel kyama muasya
#p15-42924/2017
import threading
from ricart_functions import *


node_zero = Node(12345, 0)
node_zero.send_cs_requests([12346,12347,12348,12349])
print("total okay count ", node_zero.total_okay_count)

node_zero.listen_for_replies()
