


from neurounits import NeuroUnitParser
import quantities as pq
from neurounits.writers.writer_ast_to_simulatable_object import EqnSimulator


es = NeuroUnitParser.EqnSet("""
        EQNSET lorenz {
            x' = (sigma*(y-x)) * {1s-1}
            y' = (x*( rho-z)-y) * {1s-1}
            z' = (x*y-beta*z) * {1s-1}
            sigma = 1000
            beta = 8/3
            rho= 28

         <=> OUTPUT x:(), y:(), z:()
         <=> INITIAL x:1.0
         <=> INITIAL y:1.0
         <=> INITIAL z:1.0
        }
        """)

#SimulateEquations(es)

#es.to_redoc().to_pdf(filename="/home/michael/Desktop//out1.pdf")

import numpy as np
evaluator = EqnSimulator(es, )


one = es.library_manager.backend.Quantity( 1.0, es.library_manager.backend.Unit() ) 
six = es.library_manager.backend.Quantity( 6.0, es.library_manager.backend.Unit() ) 
print 'Simulating'
res = evaluator(time_data = np.linspace(0.0,2.00, 1000), )

d = evaluator.build_redoc(time_data=np.linspace(0,2.0,1000) )
d.to_pdf("/home/michael/Desktop/newout.pdf")
print 'Done Simulating'
print res
print res.keys()
#res = evaluator(state0In=(), params=()s.params,time_data=s.t)
import pylab
print res['t'].shape
#print res['m'].shape
#pylab.plot(res['t'], res['m'])
pylab.figure()
pylab.plot(res['x'], res['y'])
pylab.figure()
pylab.plot(res['x'], res['z'])
pylab.figure()
pylab.plot(res['z'], res['y'])


pylab.figure()
pylab.plot(res['t'], res['x'])
pylab.plot(res['t'], res['y'])
pylab.plot(res['t'], res['z'])
#pylab.plot(res['t'], res['n'])
pylab.show()