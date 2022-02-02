# In due time, reach the house and eventually collect the pear	( F ( ( reach_v ( house_n ) ) U ( collect_v ( pear_n ) ) ) )

from tulip import transys, spec, synth

def cat(dict1, dict2):
    return(dict2.update(dict1))

sys = transys.FTS()

n_grid=5
s_list=['X%02d'%(i) for i in range(n_grid*n_grid)]
sys.states.add_from(s_list)
sys.states.initial.add(s_list[0])

init_loc={}
house_loc={}
pear_loc={}
obs_loc={}

def order(row_i, col_j):
    return row_i * n_grid + col_j

offsets=[[-1, 0], [0, 1], [1, 0], [0, -1]]
for i in range(n_grid):
    for j in range(n_grid):
        connects=set()
        for k in range(len(offsets)):
            new_i = i + offsets[k][0]
            new_j = j + offsets[k][1]
            if 0<=new_i<n_grid and 0<=new_j<n_grid:
                connects.add(s_list[order(new_i,new_j)])
        sys.transitions.add_comb({s_list[order(i, j)]}, connects)

# random assigned targets
sys.atomic_propositions.add_from({'house', 'pear'})
sys.states.add(s_list[(n_grid * n_grid)//2], ap={'pear'})
sys.states.add(s_list[-1], ap={'house'})

# env settings
#env_vars = set()
#env_init = set()
#env_prgo = set()
#env_safe = set()
#sys_vars = set()
#sys_init = set()
#sys_prog = set()
#sys_safe = set()
#specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe, env_prog, sys_prog)
#specs = spec.str_to_grspec("F (house U pear)")
from tulip.spec import gr1_fragment
from tulip.spec import GRSpec
specs1 = gr1_fragment.eventually_to_gr1("house", aux='aux_house')
specs2 = gr1_fragment.eventually_to_gr1("pear", aux='aux_pear')

#print(specs1)
#print(specs2)
#specs = GRSpec(sys_vars=cat(specs1.sys_vars,specs2.sys_vars), 
#        sys_init=specs1.sys_init+specs2.sys_init, 
#        sys_safety=specs1.sys_safety+specs2.sys_safety, 
#        sys_prog=specs1.sys_prog+specs2.sys_prog)
#print(specs)


sys_vars = {"aux0", "aux1", "p"}
sys_init = {"! aux0", "! aux1", "! p", "! house", "! pear"}
sys_safety = {"aux0 -> X aux0", "aux1 -> X aux1", "p -> X p", "! aux0 -> ! aux1", "! aux1 -> ! p", 
        "(! house && ! aux0) -> X ! aux0", "(! pear && ! p) -> X ! p",
        "! aux1 -> X ! pear"
        }
sys_prog = {"aux0", "aux1", "p"}

specs3 = GRSpec(sys_vars=sys_vars, sys_init=sys_init, sys_safety=sys_safety, sys_prog=sys_prog)

specs = specs1
specs = specs3


# run planner synthesize
specs.moore = True
specs.qinit = '\E \A'
ctrl = synth.synthesize('omega', specs, sys=sys)
#ctrl = synth.synthesize('lily', specs, sys=sys)
assert ctrl is not None, 'unrealizable'

# generate trace
print(ctrl)

