# -*- coding:utf8 -*-
import sys
import struct


class PltFile(object):
    """
    PltFile:
        this class is a helpfull class to read a binary file characters.
        Mainly, converts bytes to char, long integers, float, double, text
    """

    def __init__(self, filename, mode='rb'):
        """
        Arguments:
            ** filename = str() # the name of the binary file.
        """
        self.filename = filename
        try:
            self.binaryfile = open(filename, mode=mode)
        except IOError:
            sys.exit("Error occured when opening the file.")

    
    def close(self):
        self.binaryfile.close()


    def _read_line(self, size=4):
        """
            This is the Kernel of the class that read
            some bytes from the file.
            The default size is 4 bytes.
            Parameters:
                size = int() # the number of bytes
        """
        return self.binaryfile.read(size)

    def _write_line(self, writtenBytes):
        self.binaryfile.write(writtenBytes)

    def read_char(self, size=4):
        """
            This method reads a sequence of the bytes from 
            the file and converts to utf-8 format.
        """
        return self._read_line(size).decode("utf-8")
    
    def write_raw(self, rawBytes):
        self.binaryfile.write(rawBytes)

    def read_long_integer(self):
        """
            read struct module for more information.
            This function reads a long integer.
        """
        return struct.unpack('l', self._read_line(4))[0]

    def write_long_integer(self, lIntNum):
        self.binaryfile.write(struct.pack('l', lIntNum))

    def read_integer(self):
        """
            This function reads 4 bytes from the file and 
            convert to an integer. 
        """
        return struct.unpack('i', self._read_line(4))[0]

    def write_integer(self, intNum):
        self.binaryfile.write(struct.pack('i', intNum))

    def read_integer_list(self, num):
        """
            This function reads num integers continuously.
        """
        buffer = self._read_line(4*num)
        int_list = struct.unpack('={:d}i'.format(num), buffer)
        return int_list

    def write_integer_list(self, intList):
        self.binaryfile.write(struct.pack('{:d}i'.format(len(intList)), *intList))

    def read_float(self):
        """
            This function reads 4 bytes from the file and 
            convert to a float number. 
        """
        return struct.unpack('f', self._read_line(4))[0]
    
    def write_float(self, floatNum):
        self.binaryfile.write(struct.pack('f', floatNum))

    def read_float_list(self, num):
        """
            This function reads num floats continuously.
        """
        buffer = self._read_line(4*num)
        float_list = struct.unpack('={:d}f'.format(num), buffer)
        return float_list

    def write_float_list(self, floatList):
        self.binaryfile.write(struct.pack('{:d}f'.format(len(floatList)), *floatList))

    def read_double(self):
        """
        This function reads 4 bytes from the file and
        convert to a float number.
        """
        return struct.unpack('d', self._read_line(8))[0]

    def write_double(self, doubleNum):
        self.binaryfile.write(struct.pack('d', doubleNum))

    def read_double_list(self, num):
        """
            This function reads num doubles continuously.
        """
        buffer = self._read_line(4*num)
        float_list = struct.unpack('={:d}d'.format(num), buffer)
        return double_list

    def write_double_list(self, doubleList):
        self.binaryfile.write(struct.pack('{:d}d'.format(len(doubleList)), *doubleList))

    def read_string(self):
        """
            This method reads a string from a file.
            The method continuously reads the file untile the null char
            is read.
            In tecplot data format, char are encoded as its ascii code.
        """
        string = ""
        while True:
            ascii = self._read_line().decode('utf-8').replace(chr(0), "")
            if ascii == "":
                break
            string += ascii
        return string

    def write_string(self, str):
        for c in str:
            self.write_integer(ord(c))
        self.write_integer(0)



