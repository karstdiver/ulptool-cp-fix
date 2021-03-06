#!/usr/bin/env python
# esp32ulp_mapgen utility converts a symbol list provided by nm into an export script
# for the linker and a header file.
#
# Copyright (c) 2016-2017 Espressif Systems (Shanghai) PTE LTD.
# Distributed under the terms of Apache License v2.0 found in the top-level LICENSE file.

from optparse import OptionParser

BASE_ADDR = 0x50000000


def gen_ld_h_from_sym(f_sym, f_ld, f_h):
    f_ld.write("/* Variable definitions for ESP32ULP linker\n")
    f_ld.write(" * This file is generated automatically by esp32ulp_mapgen.py utility.\n")
    f_ld.write(" */\n\n")
    f_h.write("// Variable definitions for ESP32ULP\n")
    f_h.write("// This file is generated automatically by esp32ulp_mapgen.py utility\n\n")
    f_h.write("#pragma once\n\n")

    #with open("/media/psf/Downloads/ulp_main.sym", "rb") as f:
        #for line in f:
    for line in f_sym:
        f_ld.write("/* line:{0}: */\n".format(line))

        if line[1] == '\'': # assume line is b'. . 12345678\r\n...' formatted

        #bytes_read = f.read() # read total file into memory
        #for b in bytes_read:
            #process_byte(b)
        #    f_ld.write(b)

            # process each symbol
            while len(line) >= len('n s 12345678'):  # min line is: n s 12345678
                if line[1] == '\'': # check for /^b'/
                    line = line[2 : ]  # shift left 2  shift off ^b'

                eos = line.find('\\') # find end of symbol in string
                name, _, addr_str = line[ : eos].split() # get symbol's values

                # write symbols to ld files
                addr = int(addr_str, 16) + BASE_ADDR
                f_h.write("extern uint32_t ulp_{0};\n".format(name))
                f_ld.write("PROVIDE ( ulp_{0} = 0x{1:08x} );\n".format(name, addr))

                line = line[eos+len('\\r\\n') : ] # shift off just read/written symbol
                f_ld.write("/* line:{0}: */\n".format(line))

        else: # assume it is a normal input formatted line by line
            #for line in f_sym:
            name, _, addr_str = line.split()
            addr = int(addr_str, 16) + BASE_ADDR
            f_h.write("extern uint32_t ulp_{0};\n".format(name))
            f_ld.write("PROVIDE ( ulp_{0} = 0x{1:08x} );\n".format(name, addr))


def main():
    description = ("This application generates .h and .ld files for symbols defined in input file. "
                   "The input symbols file can be generated using nm utility like this: "
                   "esp32-ulp-nm -g -f posix <elf_file> > <symbols_file>")

    parser = OptionParser(description=description)
    parser.add_option("-s", "--symfile", dest="symfile",
                      help="symbols file name", metavar="SYMFILE")
    parser.add_option("-o", "--outputfile", dest="outputfile",
                      help="destination .h and .ld files name prefix", metavar="OUTFILE")

    (options, args) = parser.parse_args()
    if options.symfile is None:
        parser.print_help()
        return 1

    if options.outputfile is None:
        parser.print_help()
        return 1

    # Dec-2021 open sym file with universal to allow for Windows vs. Unix text file formats
    with open(options.outputfile + ".h", 'w') as f_h, open(options.outputfile + ".ld", 'w') as f_ld, open(options.symfile, 'rb') as f_sym:
        gen_ld_h_from_sym(f_sym, f_ld, f_h)
    return 0


if __name__ == "__main__":
    exit(main())
