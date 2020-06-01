# -*- coding:utf8 -*-
import struct
import numpy as np
from .pltFile import PltFile

__ZONE__ = 299.0
__EOH__ = 357.0
__GEOMETRY__ = 399.0
__AUXILIARY__ = 1

__ORDERED__ = 0
__FELINESEG__ = 1
__FETRIANGLE__ = 2
__FEQUADRILATERAL__ = 3
__FETETRAHEDRON__ = 4
__FEBRICK__ = 5
__FEPOLYGON__ = 6
__FEPOLYHEDRON__ = 7

__NO_SHARE_CONNECTIVITY__ = -1

__TEC_FLOAT__ = 1
__TEC_DOUBLE__ = 2
__TEC_LONG_INT__ = 3
__TEC_INT__ = 4


class Zone(object):
    def __init__(self, numOfVariables):

        self.name = ""
        self.numOfVariables = numOfVariables
        self.variablesName = []
        self.parent_zone = int()
        self.strand_id = int()
        self.solutiontime = float()  # double precision 8 bytes
        self.not_used = int()

        self.variables_format = []
        self.passive_variables = []
        self.variable_sharing = []

        self.ShareConnectivity = int()  # if -1 no sharing
        self.connectivity = []  # double list each element is []
        self.min_value = []
        self.max_value = []
        self.data = []  # double list each element is the data the viariable
        # ------------------------------------------------------------------------
        # Zone Type:
        # 0 = ORDERED       1 = FELINESEG 2 = FETRIANGLE 3 = FEQUADRILATERAL
        # 4 = FETETRAHEDRON 5 = FEBRICK   6 = FEPOLYGON  7 = FEPOLYHEDRON
        # ------------------------------------------------
        self.type = int()
        # ------------------------------------------------
        # Data Packing:
        # 0 = BLOCK
        # 1 = POINT
        # ------------------------------------------------
        self.datapacking = int()

        # ------------------------------------------------
        # Zones
        # -------------------------------------------------

        # if varlocation
        self.variablesLocation = []
        # if face_neighbors is not equal to zero you must do more stuff ...
        self.face_neighbors = int()

        self.numCells = int()
        self.numPoints = int()
        # -------------------------------------------------
        # ORDERED ZONE
        # -------------------------------------------------
        self.imax = int()
        self.jmax = int()
        self.kmax = int()
        self.iCell = int()
        self.jCell = int()
        self.kCell = int()

    def _read_zone_vars(self, pltFile):
        self.name = pltFile.read_string()
        self.parentzone = pltFile.read_integer()
        self.strand_id = pltFile.read_integer()
        self.solutiontime = pltFile.read_double()
        self.not_used = pltFile.read_integer()
        self.type = pltFile.read_integer()

        var_location = pltFile.read_integer()
        if var_location == 0:
            self.variablesLocation = [0*self.numOfVariables]
        else:
            self.variablesLocation = pltFile.read_integer_list(
                self.numOfVariables)

        # if face_neighbors is not equal to zero you must do more stuff ...
        self.faceNeighbors = pltFile.read_integer()
        assert self.face_neighbors == 0
        self.numUdfConnections = pltFile.read_integer()
        assert self.numUdfConnections == 0

        if self.type == __ORDERED__:
            self.ordered_zone(pltFile)
        if self.type == __FELINESEG__       \
                or self.type == __FETRIANGLE__      \
                or self.type == __FEQUADRILATERAL__ \
                or self.type == __FETETRAHEDRON__   \
                or self.type == __FEPOLYGON__       \
                or self.type == __FEPOLYHEDRON__:
            sys.exit('only ordered data format is supported!')

    def ordered_zone(self, pltFile):

        self.imax = pltFile.read_integer()
        self.jmax = pltFile.read_integer()
        self.kmax = pltFile.read_integer()
        self.iCell = 1 if self.imax == 1 else self.imax-1
        self.jCell = 1 if self.jmax == 1 else self.jmax-1
        self.kCell = 1 if self.kmax == 1 else self.kmax-1

        self.numPoints = self.imax * self.jmax * self.kmax
        self.numCells = self.iCell * self.jCell * self.kCell

    def read_variable(self, varIdx, pltFile):
        if self.variablesLocation[varIdx] == 0:
            num = self.numPoints
            out_shape = (self.imax, self.jmax, self.kmax)
        else:
            # num = self.iCell*self.jCell*self.kmax
            # out_shape = (self.iCell, self.jCell, self.kmax)
            num = self.imax*self.jmax*self.kCell
            out_shape = (self.imax, self.jmax, self.kCell)
        vfmt = self.variablesFormat[varIdx]
        if vfmt == __TEC_FLOAT__:
            data = pltFile.read_float_list(num)
        elif vfmt == __TEC_DOUBLE__:
            data = pltFile.read_double_list(num)
        elif vfmt == __TEC_LONG_INT__:
            data = pltFile.read_long_list(num)
        elif vfmt == __TEC_INT__:
            data = pltFile.read_integer_list(num)
        else:
            print("type of data not supported: {}".format(vfmt))
            sys.exit(1)
        if self.variablesLocation[varIdx] == 0:
            np_array = np.array(data).reshape(out_shape, order='F')
        else:
            np_array = np.array(data).reshape(out_shape, order='F')
            # np_array = np_array[:, :, :-1]
            np_array = np_array[:-1, :-1, :]
        return np_array

    def read_minmax_of_values(self, pltFile):

        for _ in range(self.numOfVariables):
            self.min_value.append(pltFile.read_double())
            self.max_value.append(pltFile.read_double())

    def read_data(self, pltFile):
        for var in range(self.numOfVariables):
            self.data.append(self.read_variable(var, pltFile))

    # access by name
    def get_data(self, var_name):
        '''
        access data by name
        '''
        return self.data[self.variable.index(var_name)]

    # access by index
    def __getitem__(self, var_id):
        '''
        access data by index
        '''
        return self.data[var_id]

    def __repr__(self):
        line = ""
        commit = "    Zone Name           : {} \n".format(self.name)
        line += commit
        commit = "    Zone Type           : {} \n".format(self.type)
        line += commit
        commit = "    Zone shape [I,J,K]  : [{:d},{:d},{:d}] \n".format(
            self.imax, self.jmax, self.kmax)
        line += commit
        commit = "    Parent Zone         : {} \n".format(self.parent_zone)
        line += commit
        commit = "    Strand Id           : {} \n".format(self.strand_id)
        line += commit
        commit = "    Solution Time       : {} \n".format(self.solutiontime)
        line += commit
        commit = "    Finite Element Type : {} \n".format(self.type)
        line += commit
        commit = "    Number of Points    : {} \n".format(self.numPoints)
        line += commit

        return line

class TecplotBinaryReader():
    def __init__(self, filename, info=False):
        self.filename = filename
        self.pltFile = PltFile(filename)

        self.version = ""
        self.byte_order = int()
        self.file_type = int()
        self.title = ""
        self.numVariables = int()
        self.variablesName = []
        self.variablesLocation = []
        self.zone = []  # in most cases, there is only one zone

        self.version = self.pltFile._read_line(8).decode('utf-8')
        self.__verification()
        self.__read_file_info()

        # Zone
        zonecounter = -1

        vm = self.__get_ValidationMarker()
        while (vm != __EOH__):
            if vm == __ZONE__:
                z = Zone(self.numVariables)
                z._read_zone_vars(self.pltFile)
                self.zone.append(z)
                vm = self.__get_AuxiliaryMarker()
                assert vm == 0
                # while vm == __AUXILIARY__:
                #     self._read_auxiliary()
                #     vm = self.__get_AuxiliaryMarker()
            if vm == __GEOMETRY__:
                pass
            vm = self.__get_ValidationMarker()
        # end while

        for z in self.zone:
            assert self.__get_ValidationMarker() == __ZONE__
            z.variablesFormat = self.pltFile.read_integer_list(
                self.numVariables)
            hasPassive = self.pltFile.read_integer()
            assert hasPassive == 0
            if hasPassive == 1:
                z.passiveVariables = self.pltFile.read_integer_list(
                    self.numVariables)
            hasSharing = self.pltFile.read_integer()
            assert hasSharing == 0
            if hasSharing == 1:
                z.sharingVariables = self.pltFile.read_integer_list(
                    self.numVariables)
            zoneShare = self.pltFile.read_integer()  # no use

            z.read_minmax_of_values(self.pltFile)
            z.read_data(self.pltFile)

        if info:
            self.__repr__()

    def __getitem__(self, var_id):
        '''
        access data by index
        '''
        return self.zone[0][var_id]

    def get_name_list(self):
        return self.variablesName

    def get_shape(self):
        return (self.zone[0].imax, self.zone[0].jmax, self.zone[0].kmax)

    def get_location_list(self):
        return self.zone[0].variablesLocation

    def get_name(self, var_idx):
        return self.variablesName[var_idx]

    def get_location(self, var_idx):
        return self.zone[0].variablesLocation[var_idx]

    def get_data_list(self):
        return self.zone[0].data

    def get_format(self, var_idx):
        vf = self.zone[0].variablesFormat[var_idx]
        if vf == 1:
            return np.float32
        elif vf == 2:
            return np.float64
        elif vf == 3:
            return np.int64
        elif vf == 4:
            return np.int32

    def __get_ValidationMarker(self):
        return self.pltFile.read_float()

    def __get_AuxiliaryMarker(self):
        return self.pltFile.read_integer()

    def __verification(self):
        if not self.version == "#!TDV112":
            raise Exception(
                "UnSupported Format. We get {} instead of #!TDV112".format(self.version))

    def _read_auxiliary(self, pltFile):
        self.auxiliary = pltFile.read_integer()
        print(self.auxiliary)
        if self.auxiliary == 1:
            self.auxiliary_name = pltFile.read_string()
            self.auxiliary_format = pltFile.read_integer()
            self.auxiliary_value = pltFile.read_string()

    def __read_file_info(self):
        '''
        read tecplot file's head section
        the following words will be read from file:
            byteOrder   :
            fileType    :
            title       :
            numVariables  :
            variablesName :
        '''
        self.byte_order = self.pltFile.read_integer()
        self.file_type = self.pltFile.read_integer()
        self.title = self.pltFile.read_string()
        self.numVariables = self.pltFile.read_integer()
        for _ in range(self.numVariables):
            self.variablesName.append(self.pltFile.read_string())

    def __repr__(self):
        line = ""
        commit = "Tecplot File in Binary Form \n"
        line += commit
        commit = "Version             : {} \n".format(self.version)
        line += commit
        commit = "Byte Order          : {} \n".format(self.byte_order)
        line += commit
        commit = "File Type           : {} \n".format(self.file_type)
        line += commit
        commit = "Title               : {} \n".format(self.title)
        line += commit
        commit = "Number of Variables : {} \n".format(self.numVariables)
        line += commit
        commit = "Variables           : {} \n".format(
            ', '.join(self.variablesName))
        line += commit

        line += "\n"
        for z in range(len(self.zone)):
            commit = "--> Zone            : {} \n".format(z)
            line += commit
            line += repr(self.zone[z])

        print(line)


class TecplotBinaryWriter():
    '''tecplot file writer.
    initialization parameters:
        filename :  string, save path and file name
        vars     :  list of numpy nd-array 
        varsName :  list of string, names of every variable, if default, set to V1, V2...
        varsLoc  :  list of [0|1], data location, 0: vertex; 1: cell-centered, default is 0
        dataFormat : 'f' or 'd', denotes float or double
    '''
    def __init__(self, filename, vars,  varsName=None, varsLoc=None, dataFormat='f'):
        self.filename = filename
        self.pltFile = PltFile(filename, mode='wb')
        nVars = len(vars)
        if varsName is None:
            varsName = []
            for i in range(nVars):
                varsName.append('V{:d}'.format(i+1))
        if varsLoc is None:
            varsLoc = [0]*nVars

        self.pltFile.write_raw('#!TDV112'.encode('utf-8'))
        self.pltFile.write_integer(1)  # byte_order
        self.pltFile.write_integer(0)  # file type
        self.pltFile.write_string('Simple Dataset')
        self.pltFile.write_integer(nVars)
        for varName in varsName:
            self.pltFile.write_string(varName)
        # write zone head
        self.pltFile.write_float(__ZONE__)
        self.pltFile.write_string('Simple Zone')  # zone name
        self.pltFile.write_integer(-1)  # parentZone
        self.pltFile.write_integer(-1)  # strand ID
        self.pltFile.write_double(0.0)  # solution time
        self.pltFile.write_integer(-1)  # not used
        self.pltFile.write_integer(0)  # zone type, 0: ordered
        self.pltFile.write_integer(1)  # var location flag
        self.pltFile.write_integer_list(varsLoc)  # vars location
        self.pltFile.write_integer(0)  # face neighbor
        self.pltFile.write_integer(0)  # user-defined face neighbor
        # shape
        self.pltFile.write_integer_list(vars[0].shape)
        # auxiliary name/value
        self.pltFile.write_integer(0)  # auxiliary name/value flag
        # end of head section
        self.pltFile.write_float(__EOH__)
        # data section of zone
        self.pltFile.write_float(__ZONE__)
        varsFormat = [2]*nVars if dataFormat == 'd' else [1]*nVars
        self.pltFile.write_integer_list(varsFormat)  # vars location
        self.pltFile.write_integer(0)  # has passive variables
        self.pltFile.write_integer(0)  # has sharing variables
        self.pltFile.write_integer(-1)  # sharing zone number
        # write min and max of variables
        for var in vars:
            self.pltFile.write_double(var.min())
            self.pltFile.write_double(var.max())
        # write data of variables
        for loc, var in zip(varsLoc, vars):
            if loc == 0:
                pass
            else:
                var = np.append(var, np.zeros(
                    (1, var.shape[1], var.shape[2])), axis=0)
                var = np.append(var, np.zeros(
                    (var.shape[0], 1, var.shape[2])), axis=1)
            if dataFormat == 'd':
                self.pltFile.write_double_list(
                    var.reshape(-1, order='F').tolist())
            else:
                self.pltFile.write_float_list(
                    var.reshape(-1, order='F').tolist())

        self.pltFile.close()
