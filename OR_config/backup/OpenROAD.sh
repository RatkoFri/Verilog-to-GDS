
SRC_DIR=/OpenROAD-flow/flow/mults_src
DEST_DIR=/OpenROAD-flow/flow/designs/src/mult_approx
PYTHON_DIR=/OpenROAD-flow/flow/python

arr_mult=("ADaPT_shift_w4Q8_v2")

i=0
# Loop upto size of array
# starting from index, i=0
while [ $i -lt ${#arr_mult[@]} ]
#while [ $i -lt 2 ]
do
    cp $SRC_DIR/${arr_mult[$i]}.v $DEST_DIR/${arr_mult[$i]}.v

    python $PYTHON_DIR/mult_change.py ${arr_mult[$i]}

    make

    python $PYTHON_DIR/parse_results.py ${arr_mult[$i]}

    make clean_all

    rm $DEST_DIR/${arr_mult[$i]}.v
    # Increment the i = i + 1
    i=`expr $i + 1`
done


