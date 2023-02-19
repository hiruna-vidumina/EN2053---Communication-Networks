from .packet import PKT_TYPE
from .packet import Packet


class Node:
    def __init__(self, id, x, y, range):
        """
            Attributes:
                id: Node address
                x:  x-coordinate
                y:  y-coordinate
                range: Maximum transmission range
                queue_in: Input queue.Packets entering will be present here with the earliest one at index 0
                queue_out: Output queue of node. Packets forwarded to by this node must be appended to this list
                adjacent_nodes: A dictionary of neighboring nodes which  will be updated every time step
                routing_cache: A dictionary containing the routes discovered so far. Implemented with a expiration duration if not used recently.
                expire_time: expire time of a route in cache
                recent: A list of recently recieved packets (RREQ only)
                count : Used to generate a unique id  for data packets originating from this node
                buffer: A dictionary of Buffered DATA packets
                recieved: A list of data packets sent to this node( i.e packet target == node.id)
        """
        self.id = id
        self.x = x
        self.y = y
        self.range = range
        self.queue_in = []
        self.queue_out = []
        self.adjacent_nodes = {}
        self.routing_cache = {}
        self.expire_time = 30
        self.recent = []
        self.count = 1
        self.buffer = {}
        self.received = []

    def generate_pkt_id(self):
        """
            Generates a unique packet id
        """
        return self.id + str(self.count+1)

    def forward(self):
        """
            Packet forwarding
        """
        pkt = None
        if self.queue_in != []:
            pkt = self.queue_in.pop(0)
        if pkt is not None:
            self.route(pkt)

    def check_in_recent(self, pkt):
        """
            Checks whether the given pkt is in the nodes recently forwarded packets.
            For RREQ packets
        """
        assert pkt.type == PKT_TYPE.RREQ,"Invalid packet type"
        if (pkt.source, pkt.target, pkt.id) in self.recent:
            return True
        return False

    def add_to_recent(self, pkt):
        """
            Adds the pkt to the recent history of the node
            For RREQ packets
        """
        assert pkt.type == PKT_TYPE.RREQ,"Invalid packet type"
        self.recent.append((pkt.source, pkt.target, pkt.id))

    def add_to_cache(self, pkt):
        """
            Add the packets source_route to the route cache
            For RREP packets
        """
        self.routing_cache[pkt.target] = [pkt.source_route,self.expire_time]

    def check_in_cache(self, pkt):
        """
            Check whether a route has been already discovered from the node to the target
        """
        if pkt.target in self.routing_cache.keys():
            return True
        return False

    def add_path_from_cache(self, pkt):
        """
            Add route from cache to the source route of the packet
        """
        pkt.source_route = self.routing_cache[pkt.target][0]
        self.routing_cache[pkt.target][1] = self.expire_time

    def check_in_buffer(self, pkt):
        if pkt.id in self.buffer.keys():
            return True
        return False

    def add_to_buffer(self, pkt):
        self.buffer[pkt.id] = pkt

    def retrieve_from_buffer(self, pkt):
        DATA_pkt = self.buffer[pkt.id]
        del self.buffer[pkt.id]
        DATA_pkt.source_route = pkt.source_route
        DATA_pkt.next_hop += 1
        return DATA_pkt

    def generate_RREP(self, pkt):
        assert pkt.type == PKT_TYPE.RREQ, "RREP can be generated only for RREQ pkts. pkt recieved {}".format(pkt.type)
        pkt.type = PKT_TYPE.RREP
        pkt.source_route.append(self.id)
        return pkt

    def generate_RREQ(self, pkt):
        RREQ_pkt = Packet(pkt.id, PKT_TYPE.RREQ)
        RREQ_pkt.source = pkt.source
        RREQ_pkt.target = pkt.target
        RREQ_pkt.source_route.append(self.id)
        return RREQ_pkt

    def add_to_queue_out(self, pkt):
        if pkt.type == PKT_TYPE.RREQ and pkt.source != self.id:
            pkt.next_hop += 1
        elif pkt.type == PKT_TYPE.DPKT and pkt.source != self.id:
            pkt.next_hop += 1
        elif pkt.type == PKT_TYPE.RREP and pkt.target != self.id:
            pkt.next_hop -= 1
        self.queue_out.append(pkt)

    def route(self, pkt):
        """
            A packet can be RREQ (Route Request), RREP(Route reply) or a DPKT(Data packet)
            A data packet originating from this node will have an empty list as the pkt.source_route)
            Your task is complete the routing algorithm using the helper functions given. Feel free to add your own
            functions and make sure you add comments appropiately.
            
            If a packet is to be broadcasted or to be forwarded to another node it should be appened to the queue_out.
            Take note next hop should give the index of the next node it must be forwarded in the source route. Make sure you update
            the pkt.next_hop before appending to queue_out.
        """
        if pkt.type == PKT_TYPE.DPKT:
            if pkt.source_route!=[]:
                self.add_to_cache(pkt)
                self.add_to_queue_out(pkt)
            else:
                self.add_to_buffer(pkt)
                RREQ_pkt = self.generate_RREQ(pkt)
                self.add_to_queue_out(RREQ_pkt)


        elif pkt.type == PKT_TYPE.RREQ:
            if (self.check_in_recent(pkt)) or (pkt.check_id(self.id)):
                self.forward()
            elif pkt.target == self.id:
                if (self.check_in_recent(pkt)) or (pkt.check_id(self.id)):
                    self.forward()
                else:
                    self.add_to_recent(pkt)
                    RREP_pkt = self.generate_RREP(pkt)
                    self.add_to_queue_out(RREP_pkt)

            else:
                pkt.add_id(self.id)
                self.add_to_recent(pkt)
                self.add_to_queue_out(pkt)

        else:
            if self.id == pkt.source:
                self.add_to_cache(pkt)
                if self.check_in_buffer(pkt):
                    DATA_pkt = self.retrieve_from_buffer(pkt)
                    self.add_path_from_cache(DATA_pkt)
                    self.add_to_queue_out(DATA_pkt)

            else:
                self.add_to_queue_out(pkt)


























