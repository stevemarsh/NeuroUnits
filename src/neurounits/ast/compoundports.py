

import base
from neurounits.units_misc import LookUpDict

class CompoundPortDefWire(base.ASTObject):
    DirRight = 'DirRight'
    DirLeft = 'DirLeft'

    DirCute = {DirRight:'==>>', DirLeft:'<<=='}

    def __init__(self, symbol, direction, optional=False):
        assert direction in [CompoundPortDefWire.DirRight, CompoundPortDefWire.DirLeft]
        self.symbol = symbol
        self.direction = direction
        self.optional = optional

class CompoundPortDefWireContinuous(CompoundPortDefWire):
    def __init__(self, symbol, direction, unit, optional=False):
        super(CompoundPortDefWireContinuous, self).__init__( symbol=symbol, direction=direction, optional=optional)
        self.unit = unit

    def _summarise(self):
        print '  ', self.DirCute[self.direction],self.symbol.ljust(5),  'Analog', self.unit, 'Optional:', self.optional

class CompoundPortDefWireEvent(CompoundPortDefWire):
    def __init__(self, symbol, direction, parameters, optional=False):
        super(CompoundPortDefWireEvent, self).__init__( symbol=symbol, direction=direction, optional=optional)
        self.parameters = parameters
    def _summarise(self):
        print '  ', self.DirCute[self.direction],self.symbol.ljust(5),  'Event', ['%s:%s'%p for p in self.parameters ], 'Optional:', self.optional



class CompoundPortDef(base.ASTObject):

    def accept_visitor(self, visitor, **kwargs):
        return visitor.VisitCompoundPortDef(self, **kwargs)


    def __init__(self, name, connections):
        super(CompoundPortDef, self).__init__()
        self.name = name
        self.connections = LookUpDict(connections, accepted_obj_types=(CompoundPortDefWire,))

    def summarise(self):
        print
        print 'Compound Port: %s' % self.name
        for conn in self.connections:
            conn._summarise()
        print

    def get_wire(self, wire_name):
        return self.connections.get_single_obj_by(symbol=wire_name)


class CompoundPortConnectorWireMapping(base.ASTObject):
    def __init__(self, component_port, compound_port):
        super(CompoundPortConnectorWireMapping,self).__init__()
        self.component_port = component_port
        self.compound_port = compound_port


class CompoundPortConnector(base.ASTObject):
    def __init__(self, name, compound_port_def, wire_mappings):
        super(CompoundPortConnector, self).__init__()
        
        self.name = name
        self.compound_port_def =  compound_port_def
        self.wire_mappings = LookUpDict(wire_mappings, accepted_obj_types=(CompoundPortConnectorWireMapping,) )