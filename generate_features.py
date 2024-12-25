import argparse
import sys
import json
import tempfile
import time
from nis import match

from sat_instance.sat_instance import SATInstance


def doBasic(instance):
    before = time.time()
    instance.gen_basic_features()
    after = time.time()
    instance.features_dict["base_t"] = after - before


def doDPLL(instance):
    before = time.time()
    instance.gen_dpll_probing_features()
    after = time.time()
    instance.features_dict["dpll_t"] = after - before


def doLocalProbing(instance):
    before = time.time()
    instance.gen_local_search_probing_features()
    after = time.time()
    instance.features_dict["local_probing_t"] = after - before


def doAnsotegui(instance):
    before = time.time()
    instance.gen_ansotegui_features()
    after = time.time()
    instance.features_dict["ansotegui_t"] = after - before


def doMAG_VCG(instance):
    before = time.time()
    instance.gen_manthey_alfonso_graph_features_VCG()
    after = time.time()
    instance.features_dict["mag_VCG_t"] = after - before


def doMAG_VGAL(instance):
    before = time.time()
    instance.gen_manthey_alfonso_graph_features_VGAL()
    after = time.time()
    instance.features_dict["mag_VGAL_t"] = after - before


def doMAG_CGAL(instance):
    before = time.time()
    instance.gen_manthey_alfonso_graph_features_CGAL()
    after = time.time()
    instance.features_dict["mag_CGAL_t"] = after - before


def doMAG_RG(instance):
    before = time.time()
    instance.gen_manthey_alfonso_graph_features_RG()
    after = time.time()
    instance.features_dict["mag_RG_t"] = after - before


def doMAG_BIG(instance):
    before = time.time()
    instance.gen_manthey_alfonso_graph_features_BIG()
    after = time.time()
    instance.features_dict["mag_BIG_t"] = after - before


def doMAG_EB(instance):
    before = time.time()
    instance.gen_manthey_alfonso_graph_features_EB()
    after = time.time()
    instance.features_dict["mag_EB_t"] = after - before


def doMAG_RWH(instance):
    before = time.time()
    instance.gen_manthey_alfonso_graph_features_RWH()
    after = time.time()
    instance.features_dict["mag_RWH_t"] = after - before


if __name__ == "__main__":
    # Ideal usage - call features, with filename to calculate from, and then options on preprocessing,
    # linux test setup

    parser = argparse.ArgumentParser(prog="SATfeatPy")
    parser.add_argument("--tmp_path", type=str, default=tempfile.gettempdir(), help="Path for temporary files")
    parser.add_argument("--subset", help="Subset of features to analyze, defaults to all",
                        choices=["all", "base", "dpll", "local", "ansotegui", "mag_VCG", "mag_VGAL", "mag_CGAL", "mag_RG", "mag_BIG", "mag_EB", "mag_RWH"], default="all")
    parser.add_argument("cnf_path", help="Path to CNF to analyse in dimacs format")

    args = parser.parse_args()

    satinstance = SATInstance(args.cnf_path, preprocess=True, preprocess_tmp=True, tmpPath=args.tmp_path)

    subset = args.subset

    if subset == "all":
        doBasic(satinstance)
        doDPLL(satinstance)
        # N.b. ubcsat binary currently only runs on linux
        doLocalProbing(satinstance)
        doAnsotegui(satinstance)
        doMAG_VCG(satinstance)
        doMAG_VGAL(satinstance)
        doMAG_CGAL(satinstance)
        doMAG_RG(satinstance)
        doMAG_BIG(satinstance)
        doMAG_EB(satinstance)
        doMAG_RWH(satinstance)
    elif subset == "base":
        doBasic(satinstance)
    elif subset == "dpll":
        doDPLL(satinstance)
    elif subset == "local":
        doLocalProbing(satinstance)
    elif subset == "ansotegui":
        doAnsotegui(satinstance)
    elif subset == "mag_VCG":
        doMAG_VCG(satinstance)
    elif subset == "mag_VGAL":
        doMAG_VGAL(satinstance)
    elif subset == "mag_CGAL":
        doMAG_CGAL(satinstance)
    elif subset == "mag_RG":
        doMAG_RG(satinstance)
    elif subset == "mag_BIG":
        doMAG_BIG(satinstance)
    elif subset == "mag_EB":
        doMAG_EB(satinstance)
    elif subset == "mag_RWH":
        doMAG_RWH(satinstance)
    else:
        print(f"Error, unknown argument for subset: {subset}")
        exit(-1)
    export = {k: str(v) for k, v in satinstance.features_dict.items()}
    print("######----######")
    print(json.dumps(export, indent=None))
