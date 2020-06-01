import numpy as np
from tecplotIO.tecplotIO import TecplotBinaryReader, TecplotBinaryWriter

if __name__ == "__main__":
    # test write from user defined
    name_list = ['x', 'y', 'z', 'T']
    loc_list = [0, 0, 0, 1]
    imax = 6
    jmax = 11
    kmax = 16
    xx = np.empty((imax, jmax, kmax))
    yy = np.empty((imax, jmax, kmax))
    zz = np.empty((imax, jmax, kmax))
    T = np.empty((imax-1, jmax-1, kmax-1))
    for i in range(imax):
        for j in range(jmax):
            for k in range(kmax):
                xx[i, j, k] = 1.0*i
                yy[i, j, k] = 1.0*j
                zz[i, j, k] = 1.0*k
    for i in range(imax-1):
        for j in range(jmax-1):
            for k in range(kmax-1):
                T[i, j, k] = (i+1)*(j+1)*(k+1)
    TecplotBinaryWriter('test.plt', name_list,
                        loc_list, [xx, yy, zz, T])
    # test reading
    plt = TecplotBinaryReader("test.plt", info=True)
    print(plt.get_name_list())
    print(plt.get_location_list())
    print(plt.get_shape())