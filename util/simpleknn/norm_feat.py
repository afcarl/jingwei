import os, sys, array, shutil
import numpy as np
from optparse import OptionParser
from basic.common import checkToSkip, makedirsforfile

def process(options, feat_dim, inputfile):
    newname = ''
    if options.ssr:
        newname = 'ssr'
    newname += 'l%d' % options.p
    resfile = os.path.join(os.path.split(inputfile)[0] + newname, 'feature.bin')
    if checkToSkip(resfile, options.overwrite):
        return 0

    offset = np.float32(1).nbytes * feat_dim
    res = array.array('f')
    
    idfile = os.path.join(os.path.split(inputfile)[0], 'id.txt')
    nr_of_images = len(open(idfile).readline().strip().split())
    fr = open(inputfile, 'rb')
    makedirsforfile(resfile)
    fw = open(resfile, 'wb')
    print ('>>> writing results to %s' % resfile)
    

    for i in xrange(nr_of_images):
        res.fromfile(fr, feat_dim)
        vec = res
        if options.ssr:
            vec = [np.sign(x) * np.sqrt(abs(x)) for x in vec]
        if options.p == 1:
            Z = sum(abs(x) for x in vec) + 1e-9
        else:
            Z = np.sqrt(sum([x**2 for x in vec])) + 1e-9
        if i % 1e4 == 0:
            print ('image_%d, norm_%d=%g' % (i, options.p, Z))
        vec = [x/Z for x in vec]
        del res[:]
        vec = np.array(vec, dtype=np.float32)
        vec.tofile(fw)
    fr.close()
    fw.close()
    print ('>>> %d lines parsed' % nr_of_images)
    shutil.copyfile(idfile, os.path.join(os.path.split(resfile)[0], 'id.txt'))
    shutil.copyfile(os.path.join(os.path.split(inputfile)[0], 'shape.txt'), os.path.join(os.path.split(resfile)[0], 'shape.txt'))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = OptionParser(usage="""usage: %prog [options] feat_dim inputfile""")
    parser.add_option("--overwrite", default=0, type="int", help="overwrite existing file (default=0)")
    parser.add_option("--ssr", default=0, type="int", help="do signed square root per dim (default=0)")
    parser.add_option("--p", default=2, type="int", help="L_p normalization (default p=2)")
    
    
    (options, args) = parser.parse_args(argv)
    if len(args) < 2:
        parser.print_help()
        return 1
    assert(options.p in [1, 2])
    return process(options, int(args[0]), args[1])


if __name__ == "__main__":
    sys.exit(main())