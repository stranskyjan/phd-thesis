# eq. 3.36 -> eq. 3.38
import sympy as s
E,Eb,Gb,C = s.symbols('E Eb Gb C',real=True,positive=True)
l,v,n,a = s.symbols('l v n a',real=True,positive=True)
nu = s.symbols('nu',real=True)
s1 = E/(1+nu)
v1 = 3*E*nu/(1+nu)/(1-2*nu)
s2 = C*(2*Eb+3*Gb)
v2 = 3*C*(Eb-Gb)
sv1 = s1/v1
sv2 = s2/v2

eq = sv1-sv2
nu2 = s.simplify(s.solve(eq,nu))[0]
print nu2

eq = s1-s2
eq = eq.subs(nu,nu2).subs(C,n*l*a/v/15)
E2 = s.simplify(s.solve(eq,E))[0]
print E2
