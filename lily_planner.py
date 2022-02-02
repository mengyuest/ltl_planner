import os, sys, time

class FTS:
    def __init__(self):
        self.initials = list()
        self.nodes = list()
        self.edges = {}
        self.aps = {}
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
            self.aps[x].append(ap_item)

    def generate_ltl(self):
        init_ltl = self.generate_init_ltl()
        trans_ltl = self.generate_trans_ltl()
        label_ltl = self.generate_label_ltl()
        spec_ltl = self.generate_spec_ltl()
        return "\n".join([init_ltl, trans_ltl, label_ltl, spec_ltl])

    def generate_init_ltl(self):
        return " && ".join(self.initials) + ";"

    def generate_trans_ltl(self):
        exclusive_ltl = self.generate_exclusive_ltl()
        out_list = [exclusive_ltl]
        for x in self.edges:
            out_list.append("( %s -> X( %s ) )" % (x, " || ".join(self.edges[x])))
        return FTS.forever(" && ".join(out_list)) + ";"

    def generate_exclusive_ltl(self):
        if len(self.nodes) > 2:
            out_list = []
            for i in range(len(self.nodes)-1):
                for j in range(i+1, len(self.nodes)):
                    out_list.append("(!( %s && %s ))"%(self.nodes[i], self.nodes[j]))
            out_list.append("( %s )" % (" || ".join(self.nodes)))
            ltl = " && ".join(out_list)
        elif len(self.nodes) == 2:
            ltl = "%s XOR %s" % (self.nodes[0], self.nodes[1])
        else:
            ltl = self.nodes[0]
        return "( " + ltl + ")"

    def generate_label_ltl(self):
        out_list = []
        for x in self.edges:
            if len(self.aps[x])>0:
                out_list.append("(%s -> (%s))" % (x, " && ".join(self.aps[x])))
        return FTS.forever(" && ".join(out_list)) +";"

    @staticmethod
    def forever(s):
        return "G( %s )"%s

    def generate_spec_ltl(self):
        spec = "( " + self.ltl_spec + " )" if self.ltl_spec is not None else "True"
        return spec + ";"


def main():
    fts = FTS()
    fts.add_from(['X0', 'X1', 'X2', 'X3', 'X4', 'X5'])
    fts.initials.append('X0')
    fts.add_link({'X0'}, {'X1', 'X3'})
    fts.add_link({'X1'}, {'X0', 'X4', 'X2'})
    fts.add_link({'X2'}, {'X1', 'X5'})
    fts.add_link({'X3'}, {'X0', 'X4'})
    fts.add_link({'X4'}, {'X3', 'X1', 'X5'})
    fts.add_link({'X5'}, {'X4', 'X2', 'X5'})
    fts.add_label('X0', ap={'home'})
    fts.add_label('X5', ap={'lot'})

    fts.ltl_spec = "F(G(lot))"

    s = fts.generate_ltl()
    print(s)


if __name__ == "__main__":
    main()