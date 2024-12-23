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

def doMAG(instance):
    before = time.time()
    instance.gen_manthey_alfonso_graph_features()
    after = time.time()
    instance.features_dict["mag_t"] = after - before


if __name__ == "__main__":
    # Ideal usage - call features, with filename to calculate from, and then options on preprocessing,
    # linux test setup

    parser = argparse.ArgumentParser(prog="SATfeatPy")
    parser.add_argument("--tmp_path", type=str, default=tempfile.gettempdir(), help="Path for temporary files")
    parser.add_argument("--subset", help="Subset of features to analyze, defaults to all", choices=["all", "base", "dpll", "local", "ansotegui", "mag"], default="all")
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
        doMAG(satinstance)
    elif subset ==  "base":
        doBasic(satinstance)
    elif subset ==  "dpll":
        doDPLL(satinstance)
    elif subset ==  "local":
        doLocalProbing(satinstance)
    elif subset ==  "ansotegui":
        doAnsotegui(satinstance)
    elif subset ==  "mag":
        doMAG(satinstance)
    else:
        print(f"Error, unknown argument for subset: {subset}")
        exit(-1)
    export = { k : str(v) for k,v in satinstance.features_dict.items() }
    print("######----######")
    print(json.dumps(export, indent=None))
