import make_fh, make_idb_ops
import time

if __name__ == '__main__' :
    start = time.time()
    make_idb_ops.run()
    print("Making I64 and OPS Done {}".format(time.time() - start))
    start = time.time()
    make_fh.run()
    print("Making FH Done {}".format(time.time() - start))