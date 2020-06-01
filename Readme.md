# simple tecplot IO 
## Features
* a bridge between tecplot binary file and numpy nd-array, read and write are both supported.
* variant data location is supported.
* ONLY ordered data format is supported.
## Acknowledgement
tecplot reader was originated from https://github.com/dpettas/ReadBinaryTecplotFiles.
## Notes
* In plt file format, data is serialized and stored in **Fortran** style.
* When dealing with cell-centered location data, the **TWO fast moving indices (the first two indices in Fortran)** are aligned by adding one extra ghost cell of zero value,
which is ambiguous or misleading in Page 188 of \<\<tecplot data format guide>>.