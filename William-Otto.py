# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:58:16 2024

@author: gh00616
"""

from pyomo.environ import ConcreteModel, Param, Reals, NonNegativeReals, Var, log, exp, Constraint, Objective, minimize, maximize
from pyomo.opt import SolverFactory

m = ConcreteModel()

m.name = 'Example: William-Otto process'

Scaling_V = 1000
Scaling_flows = 1000
Scaling_temp = 100

# Parameters
m.p = Param(default=50)
m.a1 = Param(default=5.9755*(10**9))
m.a2 = Param(default=2.5962*(10**12))
m.a3 = Param(default=9.6283*(10**15))

# Variables
m.V = Var(bounds=(0.03,0.1), initialize = 0.06)
m.T = Var(bounds=(5.8,6.8), initialize = 5.8)
m.Fp = Var(bounds=(0,4.763), initialize = 0.5)
m.Fpurge = Var(bounds=(0, None), initialize=0)
m.Fg = Var(bounds=(0, None), initialize=1)
m.Feff = Var(range(6), within=NonNegativeReals, initialize=0.)
m.Feff[0] = 10
m.Feff[1] = 30
m.Feff[2] = 3
m.Feff[4] = 3
m.Feff[5] = 5
m.Feff_sum = Var(bounds=(1, None), initialize=52)
m.FR = Var(range(6), within=NonNegativeReals, initialize=0.)
m.Fa = Var(bounds=(1, None), initialize=10)
m.Fb = Var(bounds=(1, None), initialize=20)
m.r = Var(range(3), initialize=2.)
m.x = Var(range(6), initialize=2.)
m.n = Var(within=NonNegativeReals, initialize=0.2)

# Constraints
m.c1 = Constraint(expr = m.r[0] == (m.a1 * exp(-120/(m.T))) * m.x[0] * m.x[1] * (m.V) * m.p)
m.c2 = Constraint(expr = m.r[1] == (m.a2 * exp(-150/(m.T))) * m.x[2] * m.x[1] * (m.V) * m.p)
m.c3 = Constraint(expr = m.r[2] == (m.a3 * exp(-200/(m.T))) * m.x[4] * m.x[2] * (m.V) * m.p)

m.c4 = Constraint(expr = m.Feff[0] == m.Fa + (m.FR[0]) - m.r[0])
m.c5 = Constraint(expr = m.Feff[1] == m.Fb + (m.FR[1]) - (m.r[0] + m.r[1]))
m.c6 = Constraint(expr = m.Feff[2] == (m.FR[2]) + (2 * m.r[0]) - (2 * m.r[1]) - m.r[2])
m.c7 = Constraint(expr = m.Feff[3] == (m.FR[3]) + (2 * m.r[1]))
m.c8 = Constraint(expr = m.Feff[4] == (0.1 * (m.FR[3])) + m.r[1] - (0.5 * m.r[2]))
m.c9 = Constraint(expr = m.Feff[5] == 1.5 * m.r[2])
m.c10 = Constraint(expr = m.Feff_sum == sum(list(m.Feff.values())))
m.c11 = Constraint(expr = m.Feff[0] == m.Feff_sum * m.x[0])
m.c12 = Constraint(expr = m.Feff[1] == m.Feff_sum * m.x[1])
m.c13 = Constraint(expr = m.Feff[2] == m.Feff_sum * m.x[2])
m.c14 = Constraint(expr = m.Feff[3] == m.Feff_sum * m.x[3])
m.c15 = Constraint(expr = m.Feff[4] == m.Feff_sum * m.x[4])
m.c16 = Constraint(expr = m.Feff[5] == m.Feff_sum * m.x[5])

m.c17 = Constraint(expr = m.Fg == m.Feff[5])

m.c18 = Constraint(expr = m.Fp == m.Feff[4] - (0.1 * m.Feff[3]))

m.c19 = Constraint(expr = m.Fpurge == m.n *((m.Feff[0]) + (m.Feff[1]) + (m.Feff[2]) + (1.1 * (m.Feff[3]))))

m.c20 = Constraint(expr = m.FR[0] == (1 - m.n) * (m.Feff[0]))
m.c21 = Constraint(expr = m.FR[1] == (1 - m.n) * (m.Feff[1]))
m.c22 = Constraint(expr = m.FR[2] == (1 - m.n) * (m.Feff[2]))
m.c23 = Constraint(expr = m.FR[3] == (1 - m.n) * (m.Feff[3]))
m.c24 = Constraint(expr = m.FR[4] == (1 - m.n) * (m.Feff[4]))
m.c25 = Constraint(expr = m.FR[5] == (1 - m.n) * (m.Feff[5]))

# Objective
m.obj = Objective(expr = -(100 * ((2207 * (m.Fp)) + (50 * (m.Fpurge)) - (168 * (m.Fa)) -(252 * (m.Fb)) - (2.22 * (m.Feff_sum)) - (84 * (m.Fg)) - (60 * (m.V) * m.p)) / (600 * (m.V) * m.p)), sense=minimize)

# Solver configuration
solver = SolverFactory('ipopt') 
#solver = SolverFactory('gams') # using suitable solver from GAMS
result = solver.solve(m, tee = True)

print('Optimisation outputs')
print(m.V.value)
print(m.T.value)
print(m.Fp.value)
print(m.Fpurge.value)
print(m.Fg.value)
print(m.Feff_sum.value)
print(m.Feff[0].value)
print(m.Feff[1].value)
print(m.Feff[2].value)
print(m.Feff[3].value)
print(m.Feff[4].value)
print(m.Feff[5].value)
print(m.FR[0].value)
print(m.FR[1].value)
print(m.FR[2].value)
print(m.FR[3].value)
print(m.FR[4].value)
print(m.FR[5].value)
print(m.Fa.value)
print(m.Fb.value)
print(m.r[0].value)
print(m.r[1].value)
print(m.r[2].value)
print(m.x[0].value)
print(m.x[1].value)
print(m.x[2].value)
print(m.x[3].value)
print(m.x[4].value)
print(m.x[5].value)
print(m.n.value)
print(100 * ((2207 * (m.Fp.value)) + (50 * (m.Fpurge.value)) - (168 * (m.Fa.value)) -(252 * (m.Fb.value)) - (2.22 * (m.Feff[0].value + m.Feff[1].value + m.Feff[2].value + m.Feff[3].value + m.Feff[4].value + m.Feff[5].value)) - (84 * (m.Fg.value)) - (60 * (m.V.value) * m.p.value)) / (600 * (m.V.value) * m.p.value))


# Scaled / actual values
print('Optimisation outputs with removed scaling effects')
print(m.V.value * Scaling_V)
print(m.T.value * Scaling_temp)
print(m.Fp.value * Scaling_flows)
print(m.Fpurge.value * Scaling_flows)
print(m.Fg.value * Scaling_flows)
print(m.Feff_sum.value * Scaling_flows)
print(m.Feff[0].value * Scaling_flows)
print(m.Feff[1].value * Scaling_flows)
print(m.Feff[2].value * Scaling_flows)
print(m.Feff[3].value * Scaling_flows)
print(m.Feff[4].value * Scaling_flows)
print(m.Feff[5].value * Scaling_flows)
print(m.FR[0].value * Scaling_flows)
print(m.FR[1].value * Scaling_flows)
print(m.FR[2].value * Scaling_flows)
print(m.FR[3].value * Scaling_flows)
print(m.FR[4].value * Scaling_flows)
print(m.FR[5].value * Scaling_flows)
print(m.Fa.value * Scaling_flows)
print(m.Fb.value * Scaling_flows)
print(m.r[0].value)
print(m.r[1].value)
print(m.r[2].value)
print(m.x[0].value)
print(m.x[1].value)
print(m.x[2].value)
print(m.x[3].value)
print(m.x[4].value)
print(m.x[5].value)
print(m.n.value)
print(100 * ((2207 * (m.Fp.value * Scaling_flows)) + (50 * (m.Fpurge.value * Scaling_flows)) - (168 * (m.Fa.value * Scaling_flows)) -(252 * (m.Fb.value * Scaling_flows)) - (2.22 * (m.Feff_sum.value * Scaling_flows)) - (84 * (m.Fg.value * Scaling_flows)) - (60 * (m.V.value * Scaling_V) * m.p.value)) / (600 * (m.V.value * Scaling_flows) * m.p.value))
