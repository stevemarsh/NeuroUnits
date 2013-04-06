#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# -------------------------------------------------------------------------------

from .astobjects import ASTObject, ASTExpressionObject

from neurounits.misc import SeqUtils


class EqnAssignmentByRegime(ASTObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitEqnAssignmentByRegime(self, **kwargs)

    def __init__(self, lhs, rhs_map, **kwargs):
        assert isinstance(rhs_map, EqnRegimeDispatchMap)
        self.lhs = lhs
        self.rhs_map = rhs_map

    def __repr__(self):
        return '<Assignment to: %s>' % self.lhs.symbol


class EqnTimeDerivativeByRegime(ASTObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitTimeDerivativeByRegime(self, **kwargs)

    def __init__(self, lhs, rhs_map, **kwargs):
        self.lhs = lhs
        assert isinstance(rhs_map, EqnRegimeDispatchMap)
        self.rhs_map = rhs_map

    def set_rhs_map(self, o):
        assert o is not None
        self._rhs_map = o

    def get_rhs_map(self):
        return self._rhs_map

    rhs_map = property(get_rhs_map, set_rhs_map)

    def __repr__(self):
        return '<TimeDerivative (new) of: %s>' % self.lhs.symbol


class EqnRegimeDispatchMap(ASTExpressionObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitRegimeDispatchMap(self, **kwargs)

    def __init__(self, rhs_map):
        super(EqnRegimeDispatchMap, self).__init__()
        assert isinstance(rhs_map, dict)
        for key in rhs_map:
            assert isinstance(key, Regime)
        self.rhs_map = rhs_map

    def set_rhs_map(self, o):
        assert o is not None
        self._rhs_map = o

    def get_rhs_map(self):
        return self._rhs_map

    rhs_map = property(get_rhs_map, set_rhs_map)

    def get_rt_graph(self):
        rts = list(set([regime.parent_rt_graph for regime in self.rhs_map]))
        assert len(rts) == 1
        return rts[0]

    def get_rhs_for_regime(self, regime):
        if regime in self.rhs_map:
            return self.rhs_map[regime]
        return self.rhs_map[None]


class Transition(ASTObject):
    def __init__(self, src_regime, actions, target_regime=None,  **kwargs):
        super(Transition, self).__init__(**kwargs)
        self.target_regime = target_regime
        self.src_regime = src_regime
        self.actions = actions


class OnTriggerTransition(Transition):

    def __init__(self, trigger, **kwargs):
        super(OnTriggerTransition, self).__init__(**kwargs)
        self.trigger = trigger

    def __repr__(self):
        return '<Transition %s -> %s (%d actions)>' % (self.src_regime, self.target_regime, len(self.actions))

    def accept_visitor(self, v, **kwargs):
        return v.VisitOnTransitionTrigger(self, **kwargs)


class OnEventTransition(Transition):

    def __init__(self, port, parameters, **kwargs):
        super(OnEventTransition, self).__init__(**kwargs)
        self.port = port
        self.parameters = parameters
        print self.parameters
        assert isinstance( self.parameters, LookUpDict)

    def __repr__(self):
        return '<OnEventTransition [%s] %s -> %s (%d actions)>' % (self.port, self.src_regime, self.target_regime, len(self.actions))

    def accept_visitor(self, v, **kwargs):
        return v.VisitOnTransitionEvent(self, **kwargs)


class OnEventDefParameter(ASTExpressionObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitOnEventDefParameter(self, **kwargs)

    def __init__(self, symbol=None, dimension=None, **kwargs):
        ASTExpressionObject.__init__(self, **kwargs)
        self.symbol = symbol
        if dimension is not None:
            self.set_dimensionality(dimension)

    def __repr__(self):
        return "<OnEventDefParameter '%s'>" % self.symbol


class EmitEvent(ASTObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitEmitEvent(self, **kwargs)

    def __init__(self, port, parameters, **kwargs):
        self.port = port
        self.parameters = parameters
        assert isinstance( self.parameters, LookUpDict)

    def __repr__(self):
        return "<EmitEvent: '%s'>" % self.port

class EmitEventParameter(ASTExpressionObject):
    def accept_visitor(self, v, **kwargs):
        return v.VisitEmitEventParameter(self, **kwargs)
    def __init__(self, _symbol, rhs, port_parameter_obj=None, **kwargs):
        super(EmitEventParameter, self).__init__(**kwargs)
        self._symbol = _symbol
        self.port_parameter_obj = None
        if port_parameter_obj:
            self.set_port_parameter_obj(port_parameter_obj)
        self.rhs = rhs
    def set_port_parameter_obj(self, p_obj):
        assert isinstance (p_obj, OutEventPortParameter )
        self.port_parameter_obj = p_obj
        del self._symbol


class Regime(ASTObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitRegime(self)

    def __init__(self, name, parent_rt_graph):
        super(Regime, self).__init__()
        self.name = name
        self.parent_rt_graph = parent_rt_graph

    def __repr__(self):
        return "<Regime: '%s'>" % self.ns_string()

    def ns_string(self):
        return '%s.%s' % (self.parent_rt_graph.ns_string(), self.name)


from neurounits.units_misc import LookUpDict
class RTBlock(ASTObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitRTGraph(self)


    def __init__(self, name=None,):
        self.name = name
        self.regimes = LookUpDict([Regime(None, parent_rt_graph=self)])

    def ns_string(self):
        return (self.name if self.name is not None else '')

    def get_regime(self, name):
        return self.regimes.get_single_obj_by(name=name)
        #return self.regimes[name]

    def get_or_create_regime(self, name):
        if not self.regimes.has_obj(name=name):
            self.regimes._add_item( Regime(name=name, parent_rt_graph=self) )
        return self.regimes.get_single_obj_by(name=name)

        #if not name in self.regimes:
        #    self.regimes[name] = Regime(name=name, parent_rt_graph=self)

        #return self.regimes[name]

    def __repr__(self):
        return '<RT Block: %s>' % self.name

    def has_regime(self, name):
        return self.regimes.has_obj(name=name)
        #for (r_name, r) in self.regimesitems():
        #    assert r_name == r.name
        #rreturn name in self.regimes


 # Temporary objects used only during building:
 # ----------------------------------------------

class EqnTimeDerivativePerRegime(ASTObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitEqnTimeDerivativePerRegime(self, **kwargs)

    def __init__(self,lhs,rhs, regime, **kwargs):
        super(EqnTimeDerivativePerRegime, self).__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.regime = regime


class EqnAssignmentPerRegime(ASTObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitEqnAssignmentPerRegime(self, **kwargs)

    def __init__(self,lhs,rhs, regime, **kwargs):
        super(EqnAssignmentPerRegime, self).__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.regime = regime


class AnalogReducePort(ASTExpressionObject):

    def accept_visitor(self, v, **kwargs):
        return v.VisitAnalogReducePort(self, **kwargs)

    def __init__(self, symbol, **kwargs):
        super(AnalogReducePort, self).__init__(**kwargs)
        self.symbol = symbol
        self.rhses = []



class InEventPort(ASTObject):
    def accept_visitor(self, v, **kwargs):
        return v.VisitInEventPort(self, **kwargs)

    def __init__(self, name, parameters, **kwargs):
        super(InEventPort, self).__init__(**kwargs)
        self.name = name
        self.parameters = parameters
        assert isinstance(self.name, basestring)
        assert isinstance(self.parameters, LookUpDict)

    

class InEventPortParameter(ASTExpressionObject):
    def accept_visitor(self, v, **kwargs):
        return v.VisitInEventPortParameter(self, **kwargs)

    def __init__(self, symbol, **kwargs):
        super(InEventPortParameter, self).__init__(**kwargs)
        self.symbol = symbol




class OutEventPort(ASTObject):
    def accept_visitor(self, v, **kwargs):
        return v.VisitOutEventPort(self, **kwargs)

    def __init__(self, name, parameters, **kwargs):
        super(OutEventPort, self).__init__(**kwargs)
        self.name = name
        self.parameters = parameters
        assert isinstance(self.name, basestring)
        assert isinstance(self.parameters, LookUpDict)

    

class OutEventPortParameter(ASTExpressionObject):
    def accept_visitor(self, v, **kwargs):
        return v.VisitOutEventPortParameter(self, **kwargs)

    def __init__(self, symbol, **kwargs):
        super(OutEventPortParameter, self).__init__(**kwargs)
        self.symbol = symbol
    

class EventPortConnection(ASTObject):
    def __init__(self, src_port, dst_port, delay):
        super(EventPortConnection, self).__init__()
        self.dst_port = dst_port
        self.src_port = src_port
        self.delay = delay
        assert isinstance( dst_port, InEventPort)
        assert isinstance( src_port, InEventPort)


