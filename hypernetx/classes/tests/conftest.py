import pytest
import os
import itertools as it
import networkx as nx
import pandas as pd
import numpy as np

from hypernetx import Hypergraph, HarryPotter, Entity, LesMis as LM
from collections import OrderedDict, defaultdict


class SevenBySix:
    """Example hypergraph with 7 nodes and 6 edges."""

    def __init__(self, static=False):
        a, c, e, k, t1, t2, v = nd = ("A", "C", "E", "K", "T1", "T2", "V")
        i, l, o, p, r, s = ("I", "L", "O", "P", "R", "S")
        self.edges = [{a, c, k}, {a, e}, {a, k, t2, v}, {c, e}, {t1, t2}, {k, t2}]
        self.nodes = set(nd)
        self.edgedict = OrderedDict(
            [
                (p, {a, c, k}),
                (r, {a, e}),
                (s, {a, k, t2, v}),
                (l, {c, e}),
                (o, {t1, t2}),
                (i, {k, t2}),
            ]
        )

        self.arr = np.array(
            [
                [0, 0, 0, 1, 0, 1, 0],
                [0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0],
                [1, 1, 0, 1, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0],
                [1, 0, 0, 1, 0, 1, 1],
            ]
        )
        self.labels = OrderedDict(
            [
                ("edges", ["P", "R", "S", "L", "O", "I"]),
                ("nodes", ["A", "C", "E", "K", "T1", "T2", "V"]),
            ]
        )

        self.data = np.array(
            [
                [0, 0],
                [0, 1],
                [0, 2],
                [1, 2],
                [1, 3],
                [2, 0],
                [2, 2],
                [2, 4],
                [2, 5],
                [3, 1],
                [3, 3],
                [4, 5],
                [4, 6],
                [5, 0],
                [5, 5],
            ]
        )


class TriLoop:
    """Example hypergraph with 2 two 1-cells and 1 2-cell forming a loop"""

    def __init__(self):
        A, B, C, D = "A", "B", "C", "D"
        AB, BC, ACD = "AB", "BC", "ACD"
        self.edgedict = {AB: {A, B}, BC: {B, C}, ACD: {A, C, D}}
        self.hypergraph = Hypergraph(self.edgedict, name="TriLoop")


class SBSDupes:
    def __init__(self):
        self.edgedict = OrderedDict(
            [
                ("I", {"K", "T2"}),
                ("L", {"C", "E", "F"}),
                ("M", {"C", "E", "F"}),
                ("O", {"T1", "T2"}),
                ("P", {"A", "C", "K"}),
                ("R", {"A", "E", "F"}),
                ("S", {"A", "K", "T2", "V"}),
            ]
        )


class LesMis:
    def __init__(self):
        self.edgedict = OrderedDict(
            [
                (1, {"CL", "CV", "GE", "GG", "MB", "MC", "ME", "MY", "NP", "SN"}),
                (2, {"IS", "JL", "JV", "MB", "ME", "MR", "MT", "MY", "PG"}),
                (3, {"BL", "DA", "FA", "FN", "FT", "FV", "LI", "ZE"}),
                (4, {"CO", "FN", "TH", "TM"}),
                (5, {"BM", "FF", "FN", "JA", "JV", "MT", "MY", "VI"}),
                (6, {"FN", "JA", "JV"}),
                (
                    7,
                    {
                        "BM",
                        "BR",
                        "CC",
                        "CH",
                        "CN",
                        "FN",
                        "JU",
                        "JV",
                        "PO",
                        "SC",
                        "SP",
                        "SS",
                    },
                ),
                (8, {"FN", "JA", "JV", "PO", "SP", "SS"}),
            ]
        )
        self.hypergraph = Hypergraph(self.edgedict)


class Dataframe:
    def __init__(self):
        fname = os.path.join(os.path.dirname(__file__), "sample.csv")
        self.df = pd.read_csv(fname, index_col=0)


class CompleteBipartite:
    def __init__(self, n1, n2):
        self.g = nx.complete_bipartite_graph(n1, n2)
        self.left, self.right = nx.bipartite.sets(self.g)


@pytest.fixture
def sbs():
    return SevenBySix()


@pytest.fixture
def ent_sbs(sbs):
    return Entity(data=np.asarray(sbs.data), labels=sbs.labels)


@pytest.fixture
def sbs_edgedict(sbs):
    return sbs.edgedict


@pytest.fixture
def triloop():
    return TriLoop()


@pytest.fixture
def sbs_hypergraph(sbs):
    return Hypergraph(sbs.edgedict, name="sbsh")


@pytest.fixture
def sbs_graph(sbs):
    edges = set()
    for _, e in sbs.edgedict.items():
        edges.update(it.combinations(e, 2))
    G = nx.Graph(name="sbsg")
    G.add_edges_from(edges)
    return G


@pytest.fixture
def sbsd_hypergraph():
    sbsd = SBSDupes()
    return Hypergraph(sbsd.edgedict)


@pytest.fixture
def lesmis():
    return LesMis()


@pytest.fixture
def G():
    return nx.karate_club_graph()


@pytest.fixture
def H():
    G = nx.karate_club_graph()
    return Hypergraph({f"e{i}": e for i, e in enumerate(G.edges())})


@pytest.fixture
def bipartite_example():
    from networkx.algorithms import bipartite

    return bipartite.random_graph(10, 5, 0.4, 0)


@pytest.fixture
def complete_bipartite_example():
    return CompleteBipartite(2, 3).g


@pytest.fixture
def dataframe():
    return Dataframe()


@pytest.fixture
def dataframe_example():
    M = np.array([[1, 1, 0, 0], [0, 1, 1, 0], [1, 0, 1, 0]])
    index = ["A", "B", "C"]
    columns = ["a", "b", "c", "d"]
    return pd.DataFrame(M, index=index, columns=columns)


@pytest.fixture
def harry_potter():
    return HarryPotter()


@pytest.fixture
def array_example():
    return np.array(
        [[0, 1, 1, 0, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 0], [0, 0, 0, 0, 1]]
    )


@pytest.fixture
def ent_hp(harry_potter):
    return Entity(data=np.asarray(harry_potter.data), labels=harry_potter.labels)


####################Fixtures suite for test_hypergraph.py####################
####################These fixtures are modular and thus have inter-dependencies####################
@pytest.fixture
def les_mis():
    return LM()


@pytest.fixture
def scenes():
    return {
        "0": ("FN", "TH"),
        "1": ("TH", "JV"),
        "2": ("BM", "FN", "JA"),
        "3": ("JV", "JU", "CH", "BM"),
        "4": ("JU", "CH", "BR", "CN", "CC", "JV", "BM"),
        "5": ("TH", "GP"),
        "6": ("GP", "MP"),
        "7": ("MA", "GP"),
    }


@pytest.fixture
def edges(scenes):
    return list(set(list(scenes.keys())))


@pytest.fixture
def nodes(scenes):
    return list(set(list(np.concatenate([v for v in scenes.values()]))))


@pytest.fixture
def edge_properties(edges):
    edge_properties = defaultdict(dict)
    edge_properties.update(
        {str(ed): {"weight": np.random.randint(2, 10)} for ed in range(0, 8, 2)}
    )
    for ed in edges:
        edge_properties[ed].update({"color": np.random.choice(["red", "green"])})
    return edge_properties


@pytest.fixture
def node_properties(les_mis, nodes):
    return {
        ch: {
            "FullName": les_mis.dnames.loc[ch].FullName,
            "Description": les_mis.dnames.loc[ch].Description,
            "color": np.random.choice(["pink", "blue"]),
        }
        for ch in nodes
    }


@pytest.fixture
def scenes_dataframe(scenes):
    scenes_dataframe = (
        pd.DataFrame(pd.Series(scenes).explode())
        .reset_index()
        .rename(columns={"index": "Scenes", 0: "Characters"})
    )
    scenes_dataframe["color"] = np.random.choice(
        ["red", "green"], len(scenes_dataframe)
    )
    scenes_dataframe["heaviness"] = np.random.rand(len(scenes_dataframe))

    return scenes_dataframe


@pytest.fixture
def hyp_no_props():
    return Hypergraph(
        np.array(
            [
                np.random.choice(list("ABCD"), 50),
                np.random.choice(list("abcdefghijklmnopqrstuvwxyz"), 50),
            ]
        ).T,  # creates a transposed ndarray
        edge_col="Club",
        node_col="Member",
    )


@pytest.fixture
def hyp_df_with_props(scenes_dataframe, node_properties, edge_properties):
    return Hypergraph(
        scenes_dataframe,
        cell_properties=["color"],
        cell_weight_col="heaviness",
        node_properties=node_properties,
        edge_properties=edge_properties,
    )


@pytest.fixture
def hyp_dict_with_props(scenes):
    scenes_with_cellprops = {
        ed: {
            ch: {
                "color": np.random.choice(["red", "green"]),
                "cell_weight": np.random.rand(),
            }
            for ch in v
        }
        for ed, v in scenes.items()
    }

    return Hypergraph(
        scenes_with_cellprops,
        edge_col="Scenes",
        node_col="Characters",
        cell_weight_col="cell_weight",
        cell_properties=scenes_with_cellprops,
    )


@pytest.fixture
def hyp_props_on_edges_nodes(scenes_dataframe, edge_properties, node_properties):
    return Hypergraph(
        setsystem=scenes_dataframe,
        edge_col="Scenes",
        node_col="Characters",
        cell_weight_col="cell_weight",
        cell_properties=["color"],
        edge_properties=edge_properties,
        node_properties=node_properties,
        default_edge_weight=2.5,
        default_node_weight=6,
    )


####################Fixtures suite for test_hypergraph.py####################
