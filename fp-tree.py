# Tested on python=3.9
# -> dicts should hold insertion order (python>=3.6).
# "UniqueDotExporter" requires Graphiz program to be installed.

from anytree import NodeMixin, RenderTree
from anytree.exporter import UniqueDotExporter

class FpNode(NodeMixin):
    """Nodes of the fp-tree."""

    def __init__(self, name, path_to_root:str=None, parent=None, link=None, count=1):
        super(FpNode, self).__init__()
        self.count = count
        self.name = name
        self.parent = parent
        self.path_to_root = path_to_root
        self.link = link

class  FpTree:
    """Generate Fp-tree for 10 items."""

    def __init__(self):
        self.tree_nodes = {}

        self.last_nodes = {"0": FpNode("Head-0", "Head-0"), "1": FpNode("Head-1", "Head-1"),
                           "2": FpNode("Head-2", "Head-2"), "3": FpNode("Head-3", "Head-3"),
                           "4": FpNode("Head-4", "Head-4"), "5": FpNode("Head-5", "Head-5"),
                           "6": FpNode("Head-6", "Head-6"), "7": FpNode("Head-7", "Head-7"),
                           "8": FpNode("Head-8", "Head-8"), "9": FpNode("Head-9", "Head-9")}

    def build(self, parent_node, further_items: dict, path_to_root: str = "R"):
        """Build the Fp-tree with nodes and save its structure in tree_nodes dict."""

        cur_item = list(further_items)[0]
        path_to_root += cur_item

        if path_to_root not in self.tree_nodes:
            cur_node = FpNode(cur_item, path_to_root, parent_node,
                              self.last_nodes[cur_item], further_items[cur_item])

            self.last_nodes[cur_item] = cur_node
            self.tree_nodes[path_to_root] = cur_node

            if len(further_items) != 1:
                self.build(cur_node, dict(list(further_items.items())[1:]), path_to_root)

        else:
            cur_node = self.tree_nodes[path_to_root]
            cur_node.count += 1

            if len(further_items) != 1:
                self.build(cur_node, dict(list(further_items.items())[1:]), path_to_root)
        
    def print_nodes_on_terminal(self):
        """Print each node of the fp-tree on terminal."""

        for node_path, node in self.tree_nodes.items():
            print(f"Path: {node_path} | Node: {node.name} | Parent: {node.parent.name} | "
            f"link: {node.link.path_to_root} | Count: {node.count}")

    def save_ascii_tree(self, root_node):
        """Save fp-tree structure graph in ASCII format."""

        with open("fp-tree-ascii-graph.txt","w", encoding='utf8') as outfile:
            for pre, _, node in RenderTree(root_node):
                if node.name == "root":
                    treestr = f"{pre}{node.name}: {node.count}"
                else:
                    treestr = f"{pre}{node.name}: {node.count} (Link={node.link.path_to_root})"
                outfile.write(treestr.ljust(8)+'\n')

        print("-----------------------------------------\n"
        "Tree saved in fp-tree-ascii-graph.txt")

    def save_visual_tree(self, root_node):
        """Save fp-tree structure graph in visual format."""

        UniqueDotExporter(
        root_node,
        nodeattrfunc=lambda node: "shape=box",
        graph="graph",
        edgetypefunc=lambda node,child: "--",
        nodenamefunc=lambda n: f"'{n.name}': {n.count}\n({n.path_to_root})"
        ).to_picture("fp-tree-visual-graph.png")

        print("-----------------------------------------\n"
        "Tree saved in fp-tree-visual-graph.png")


def count_item_freq(input_file_name: str, min_sup: int) -> dict:
    """First scan: Create sorted items frequency with min sup"""

    items = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}
    with open(input_file_name,"r") as dataset:
        for record in dataset:
            for item in record.strip().split():
                if int(item) in range(0, 10):
                    items[item] += 1

    sorted_items = sorted(items.items(), key= lambda x: x[1], reverse=True)
    return {k: v for k, v in sorted_items if v >= min_sup}


def main():
    """Initiate the tree and run the program"""

    MIN_SUP = 1
    dataset_file_name = "records.txt"
    item_freq_list = count_item_freq(dataset_file_name, MIN_SUP)  # First Scan

    tree = FpTree()
    root_node = FpNode("root")
    freq = "".join(list(item_freq_list.keys()))

    with open(dataset_file_name,"r") as dataset:  # Second Scan
        for record in dataset:
            node_path = {}
            record = record.strip().split()
            for item in freq:
                if item in record:
                    node_path[item] = record.count(item)
            if len(node_path) != 0:
                tree.build(root_node, node_path)

    tree.print_nodes_on_terminal()
    tree.save_ascii_tree(root_node)
    tree.save_visual_tree(root_node)

    print("-----------------------------------------")
    print(f"Items frequent list (ordered) (MIN_SUP={MIN_SUP}):\n{item_freq_list}")

if __name__ == "__main__":
    main()