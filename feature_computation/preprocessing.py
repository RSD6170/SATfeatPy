import os
import random
import string

def id_generator(size=6, chars=string.ascii_letters + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def satelite_preprocess(cnf_path="cnf_examples/basic.cnf"):
    # pre process using SatELite binary files
    preprocessed_path = cnf_path[0:-4] + "_preprocessed.cnf"
    satelite_command = "./SatELite/SatELite_v1.0_linux " + cnf_path + " " + preprocessed_path
    os.system(satelite_command)
    return preprocessed_path


def satelite_preprocess_tmp(cnf_path, tmpPath ):
    # make a temporary file
    temp_fn = os.path.join(tmpPath, "pre_"+id_generator(size=8) + '.dimacs')
    satelite_command = "./SatELite/SatELite_v1.0_linux " + cnf_path + " " + temp_fn
    os.system(satelite_command)
    return temp_fn
