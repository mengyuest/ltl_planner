import os, sys, time
import subprocess
import errno
import networkx as nx
import pydot
from tulip.interfaces.lily import lily_strategy2moore
from tulip.transys.machines import moore2mealy, random_run
import matplotlib.pyplot as plt
import viz_utils

def tr(s):
    return "%s=1" % s

def trs(ss):
    return [tr(s) for s in ss]

def fal(s):
    return "%s=0" % s

def fals(ss):
    return [fal(s) for s in ss]

class FTS:
    def __init__(self):
        self.initials = list()
        self.nodes = list()
        self.edges = {}
        self.aps = {}
        self.all_aps = []
        self.ltl_spec = None

    def add_from(self, x_list):
        for x in x_list:
            assert x not in self.nodes, "The point to add: %s is already in nodes" % (x)
            self.nodes.append(x)
            self.edges[x] = list()
            self.aps[x] = list()

    def add_link(self, x_list, to_list):
        for x in x_list:
            assert x in self.nodes, "The start point %s is not in nodes" % x
            for node in to_list:
                assert node in self.nodes, "The end point %s is not in nodes" % node
                self.edges[x].append(node)

    def add_label(self, x, ap):
        assert x in self.nodes, "The label point %s is not in nodes" % x
        for ap_item in ap:
            if ap_item not in self.all_aps:
                self.all_aps.append(ap_item)
            self.aps[x].append(ap_item)

    def generate_ltl(self):
        init_ltl = self.generate_init_ltl()
        trans_ltl = self.generate_trans_ltl()
        label_ltl = self.generate_label_ltl()
        spec_ltl = self.generate_spec_ltl()
        return "\n".join([init_ltl, trans_ltl, label_ltl, spec_ltl]) +"\n"

    def generate_init_ltl(self):
        return " * ".join(trs(self.initials)) + ";"

    def generate_trans_ltl(self):
        # exclusive_ltl = self.generate_exclusive_ltl()
        # out_list = [exclusive_ltl]
        # for x in self.edges:
        #     out_list.append("( %s -> X( %s ) )" % (tr(x), " + ".join(trs(self.edges[x]))))
        # return FTS.forever(" * ".join(out_list)) + ";"
        out_list = self.generate_exclusive_ltl()
        for x in self.edges:
            out_list.append("( %s -> X( %s ) )" % (tr(x), " + ".join(trs(self.edges[x]))))
        return "\n".join([FTS.forever(xxx)+";" for xxx in out_list])

    def generate_exclusive_ltl(self):
        # if len(self.nodes) > 2:
        #     out_list = []
        #     for i in range(len(self.nodes)-1):
        #         for j in range(i+1, len(self.nodes)):
        #             out_list.append("(!( %s * %s ))"%(tr(self.nodes[i]), tr(self.nodes[j])))
        #     out_list.append("( %s )" % (" + ".join(trs(self.nodes))))
        #     ltl = " * ".join(out_list)
        # elif len(self.nodes) == 2:
        #     ltl = "%s XOR %s" % (tr(self.nodes[0]), tr(self.nodes[1]))


        # if len(self.nodes) >= 2:
        #     out_list = []
        #     for i in range(len(self.nodes)):
        #         no_ego = [xx for xx in self.nodes if xx!=self.nodes[i]]
        #         out_list.append("*".join([tr(self.nodes[i])] + fals(no_ego) ))
        #         out_list[-1] = "(" + out_list[-1] + ")"
        #     ltl = "+".join(out_list)
        # else:
        #     ltl = tr(self.nodes[0])
        # return ["( " + ltl + ")"]

        out_list=[]
        for i in range(len(self.nodes)):
            no_ego = [xx for xx in self.nodes if xx != self.nodes[i]]
            out_list.append("%s->(%s)"%(tr(self.nodes[i]), "*".join(fals(no_ego))))
        return out_list

    def generate_label_ltl(self):
        out_list = []
        for x in self.edges:
            # if len(self.aps[x])>0:
            trues = self.aps[x]
            falses = [yy for yy in self.all_aps if yy not in self.aps[x]]
            out_list.append("(%s -> (%s))" % (tr(x), " * ".join(trs(trues) +fals(falses))))
        # return FTS.forever(" * ".join(out_list)) +";"
        return "\n".join([FTS.forever(xxx)+";" for xxx in out_list])

    @staticmethod
    def forever(s):
        return "G( %s )"%s

    def generate_spec_ltl(self):
        spec = "( " + self.ltl_spec + " )" if self.ltl_spec is not None else "True"
        # spec = self.ltl_spec if self.ltl_spec is not None else "True"
        return spec + ";"


def fts1():
    fts = FTS()
    fts.add_from(['X0', 'X1', 'X2'])
    fts.all_aps = ["home", "lot"]
    fts.initials.append('X0')
    fts.add_link({'X0'}, {'X1'})
    fts.add_link({'X1'}, {'X0', 'X2'})
    fts.add_link({'X2'}, {'X2', 'X1'})
    fts.add_label('X0', ap={'home'})
    fts.add_label('X2', ap={'lot'})
    fts.ltl_spec = "F(G(lot=1))"
    return fts

def fts2():
    fts = FTS()
    fts.add_from(['X0', 'X1', 'X2', 'X3', 'X4', 'X5'])
    fts.all_aps = ["home", "lot"]
    fts.initials.append('X0')
    fts.add_link({'X0'}, {'X1', 'X3'})
    fts.add_link({'X1'}, {'X0', 'X4', 'X2'})
    fts.add_link({'X2'}, {'X1', 'X5'})
    fts.add_link({'X3'}, {'X0', 'X4'})
    fts.add_link({'X4'}, {'X3', 'X1', 'X5'})
    fts.add_link({'X5'}, {'X4', 'X2', 'X5'})
    fts.add_label('X0', ap={'home'})
    fts.add_label('X5', ap={'lot'})
    fts.ltl_spec = "F(G(lot=1))"
    return fts

def fts3():
    fts = FTS()
    fts.add_from(['X0', 'X1', 'X2', 'X3'])
    fts.all_aps = ["home", "lot"]
    fts.initials.append('X0')
    fts.add_link({'X0'}, {'X1', 'X2'})
    fts.add_link({'X1'}, {'X0', 'X3'})
    fts.add_link({'X2'}, {'X0', 'X3'})
    fts.add_link({'X3'}, {'X1', 'X2', 'X3'})
    fts.add_label('X0', ap={'home'})
    fts.add_label('X3', ap={'lot'})
    fts.ltl_spec = "G(F(lot=1))"
    return fts

def fts4():
    fts = FTS()
    fts.add_from(['X0', 'X1', 'X2', 'X3'])
    fts.all_aps = ["home", 'pear', "tree"]
    fts.initials.append('X0')
    fts.add_link({'X0'}, {'X1', 'X2'})
    fts.add_link({'X1'}, {'X0', 'X3'})
    fts.add_link({'X2'}, {'X0', 'X3'})
    fts.add_link({'X3'}, {'X1', 'X2', 'X3'})
    fts.add_label('X0', ap={'home'})
    fts.add_label('X2', ap={'pear'})
    fts.add_label('X3', ap={'tree'})
    fts.ltl_spec = "F (pear=1 U tree=1)"
    return fts

def main():
    fts = fts4()

    with open(IO_LTL_FILE, 'w') as fid:
        s = fts.generate_ltl()
        print(s)
        fid.write(s)

    with open(IO_PARTITION_FILE, 'w') as fid:
        env_vars = [""]
        sys_vars = fts.nodes + fts.all_aps
        s = '.inputs {inp}\n.outputs {out}'.format(
            inp=' '.join(env_vars),
            out=' '.join(sys_vars))
        fid.write(s)

    # call lily
    try:
        p = subprocess.Popen([LILY, '-syn', IO_PARTITION_FILE, '-ltl', IO_LTL_FILE],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True)
        out = p.stdout.read()
        print(out)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise Exception(
                'lily.pl not found in path.\n'
                'See the Lily docs for setting PERL5LIB and PATH.')
        else:
            raise

    dotf = open(DOTFILE, 'r')
    fail_msg = 'Formula is not realizable'
    if dotf.read(len(fail_msg)) == fail_msg:
        return None
    dotf.seek(0)
    data = dotf.read()
    (pd,) = pydot.graph_from_dot_data(data)
    g = nx.drawing.nx_pydot.from_pydot(pd)
    dotf.close()
    moore = lily_strategy2moore(g, env_vars, sys_vars)
    mealy = moore2mealy(moore)

    # print(moore)
    # print(mealy)

    n_grid = 2
    viz_loc={
        'X0': (0, 0),
        'X1': (0, 1),
        'X2': (1, 0),
        'X3': (1, 1),
    }

    states_seq, output_seqs = random_run(mealy, N=12)
    for ti in range(len(output_seqs['X0'])):
        plt.figure()
        for xi in viz_loc:
            i, j = viz_loc[xi]
            viz_utils.viz_grid_text(i, j, n_grid, text=",".join([xi]+fts.aps[xi]), color="orange" if output_seqs[xi][ti] else "lightgray")
        plt.xlim(0, n_grid)
        plt.ylim(0, n_grid)
        # plt.xticks(fontsize=24)
        # plt.yticks(fontsize=24)
        text = ",".join([(xxx+":"+str(output_seqs[xxx][ti])) for xxx in output_seqs if "X" not in xxx])
        plt.title(fts.ltl_spec+"\n"+"Trace (t=%d/%d) %s"%(ti, len(output_seqs['X0']), text), fontsize=18)
        plt.axis("scaled")
        plt.axis("off")
        plt.savefig("viz2/fig_%02d.png" % (ti), bbox_inches='tight', pad_inches=0.1)
        plt.close()
    os.system("convert -delay 100 -loop 0 viz2/*.png viz2/ani_est.gif")


if __name__ == "__main__":
    t1=time.time()
    LILY = 'lily.pl'
    IO_LTL_FILE = 'cache/example.ltl'
    IO_PARTITION_FILE = 'cache/io_partition.txt'
    DOTFILE = 'ltl2vl-synthesis.dot'
    main()
    t2=time.time()
    print("Finished in %.4f seconds"%(t2-t1))