import tulip
import csv
from tulip import transys, spec, synth

loc = "LTL_dataset-Sheet1.csv"


def load_csv(csv_path):
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        formulas = []
        for row in reader:
            #print ' @ '.join(row)
            formulas.append(row[1])
        return formulas

def parse_aps(formula):
    return ap_list


def demo_sys(formula):
    sys = transys.FTS()
    num_states = 10
    num_rands = 8
    s_list=['X%d'%i for i in range(num_states)]
    sys.states.add_from(s_list)
    sys.states.initial.add(s_list[0])
    for i in range(num_states):
        sys.transitions.add_comb({s_list[i]}, {s_list[j] for j in range(num_rands)})

    # TODO
    ap_list = parse_aps(formula)
    sys.atomic_propositions.add_from(ap_list)
    
    env_vars=set()
    env_init=set()
    env_prog=set()
    env_safe=set()

    sys_vars = set()
    sys_init = set()
    sys_prog = set()
    sys_safe = {formula}
    
    specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe, env_prog, sys_prog)
    specs.moore = True

    specs.qinit = '\E \A'
    ctrl = synth.synthesize('omega', specs, sys=sys)
    
    print(ctrl)


def ltl2aps(ltl):
    words = ltl.strip().split(" ")
    #print "words=",words
    aps = []
    for wi,w in enumerate(words):
        if "_v" in w:
            live = 0
            cache=[]
            # v without n case (TODO)
            for swi, sw in enumerate(words[wi+1:]):
                if "(" in sw:
                    live+=1
                elif ")" in sw:
                    live-=1
                    if live == 0:
                        ap = [w]+cache
                        aps.append(ap)
                        break
                elif "|" in sw or "&" in sw:
                    ap = [w]+cache
                    aps.append(ap)
                    cache = []
                elif "_n" in sw:
                    cache.append(sw)
                    
    return aps


def toy(ltl):
    sys = transys.FTS()
    sys.states.add_from['X0', 'X1']
    sys.states.initial.add('X0')
    sys.transitions.add_comb({'X0'}, {'X0', 'X1'})
    sys.transitions.add_comb({'X1'}, {'X1', 'X0'})
    sys.atomic_propositions.add_from({'home'})
    sys.states.add('X0', ap={'home'})
    sys.states.add('X1', ap=set())
    
    env_vars = set()
    env_init = set()
    env_prog = set()
    env_safe = set()

    sys_vars = set()
    sys_init = set()
    sys_prog = set()
    sys_safe = {'home'}

    return


def main():
    formulas = load_csv(loc)
    for form in formulas[:6]:
        print form

    #demo_sys(formulas[1])
    
    toy(formula[1])
    exit()

    for form in formulas[1:150]:
        aps = ltl2aps(form)
        print form, aps



if __name__ == "__main__":
    main()
