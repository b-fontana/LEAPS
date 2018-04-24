#!/bin/sh
rm xv.out
rm ce.out
rm info.out
rm big.dmp
rm small.dmp
rm param.dmp
rm restart.dmp
rm big.tmp
rm small.tmp
rm param.tmp
rm restart.tmp
rm *.aei

fort77 mercury6_2.for -o mercury6
fort77 element6.for -o element6
fort77 close6.for -o close6

SECONDS=0
./mercury6
./element6
echo "The code took $SECONDS seconds to finish."
