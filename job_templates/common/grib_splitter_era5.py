# code to split out the grib fields and time steps for an input grib file
# based on ecCodes exampls from ECMWF.
 
import traceback
import sys
import os
import random
 
from eccodes import *
 
INPUT = '../../data/constant_field.grib1'
OUTPUT = 'out.clone.grib'
VERBOSE = 1  # verbose error reporting
 
 
def grib_splitter(in_grib_file):
    """
    this function will take in a starting grib file
    then find it's path before then splitting out by timestep and 
    parameters
    """
    
    fin = open(in_grib_file, 'rb')
    import pdb;pdb.set_trace()
    f_out_path, fin_name = os.path.split(in_grib_file)
    
    
    
 
    gid = codes_grib_new_from_file(fin)
 
    assert codes_is_missing(gid, 'Ni') == False
    assert codes_is_missing(gid, 'Nj') == False
    nx = codes_get(gid, 'Ni')
    ny = codes_get(gid, 'Nj')
    ntimes = codes_get(gid, 'Nt')
    
    for step in ntimes:
        
        
        output_file_path = os.path.join([f_out_path, f_out_name])
        fout = open(OUTPUT, 'wb')


        clone_id = codes_clone(gid)
        codes_set(clone_id, 'step', step)
 
        values = [random.random() for i in range(nx * ny)]
 
        codes_set_values(clone_id, values)
 
        codes_write(clone_id, fout)
        codes_release(clone_id)
 
    codes_release(gid)
 
    fin.close()
    fout.close()
 
 
def main(in_grib_file):
    try:
        grib_splitter(in_grib_file)
    except CodesInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(err.msg + '\n')
 
        return 1
 
 
if __name__ == "__main__":

    args = sys.argv
    print "\nAttempting to split out files into different steps and parameters from > '%s'  " % args[1:],"\n"
    if len(args) < 2:
       exitNicely("Not enough arguments given.")

    in_file = args[1]

    sys.exit(main(in_file))
