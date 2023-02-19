from simulator.graph import Graph
from simulator.visualizer import step
import cv2

manet = Graph()

# initialize network
"""
Make sure  the ranges of all nodes are the same to enable bidirectional 
communication so as to simplify the protocol
"""
tx_range = 200
dynamic = False  # True to use mobile model

manet.add_node(500-200, 550-200, tx_range)  # "Add node 0 at 500,500"
manet.add_node(690-200, 600-200, tx_range)  # "Add node 1 at 690,600"
manet.add_node(780-200, 700-200, tx_range)  # "Add node 2 at 780,700"
manet.add_node(780-200, 500-200, tx_range)
manet.add_node(870-200, 600-200, tx_range)
manet.add_node(890-200, 750-200, tx_range)
manet.add_node(630-200, 420-200, tx_range)
manet.add_node(720-200, 350-200, tx_range)

#manet.send(2, 4, 1, 'Test')  # send a data packet at time step 1 from node 0 to 2

#manet.send(7, 2, 1, 'Test1')
#manet.send(5, 7, 7, 'Test2')
manet.send(0, 3, 12, 'Test3')
for t in range(20):  # Simulate for 20 time steps # Do not increase the timesteps beyond 30. If you want to increase set self.expire_time in node.py to a high value
    step(manet, t, dynamic)
cv2.destroyAllWindows()
