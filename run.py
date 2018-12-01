#!/usr/bin/env python

import errno
import os
import os.path
import sys
import time

from driller import Driller


def save_input(content, dest_dir, count):
    """Saves a new input to a file where AFL can find it.

    File will be named id:XXXXXX,driller (where XXXXXX is the current value of
    count) and placed in dest_dir.
    """
    name = 'id:%06d,driller' % count
    with open(os.path.join(dest_dir, name), 'w') as destfile:
        destfile.write(content)


def main():
    if len(sys.argv) != 4:
        print 'Usage: %s <binary> <fuzzer_input_dir> <fuzzer_output_dir>' % sys.argv[0]
        sys.exit(1)

    _, binary, fuzzer_input_dir, fuzzer_out_dir = sys.argv

    os.system('afl-fuzz -i %s -o %s -M master -Q ./%s &' %(fuzzer_input_dir, fuzzer_out_dir, binary))
    
    time.sleep(20)
    with open(os.path.join(fuzzer_out_dir, 'master', 'fuzz_bitmap')) as bitmap_file:
        fuzzer_bitmap = bitmap_file.read()
    source_dir = os.path.join(fuzzer_out_dir, 'master', 'queue')
    dest_dir = os.path.join(fuzzer_out_dir, 'tracer','queue')
    
   
    try:
        os.makedirs(dest_dir)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise

    seen = set()  
    count = len(os.listdir(dest_dir))  

    
    while True:
        
        for source_name in os.listdir(source_dir):
            file_id = 'id:%06d' % (len(os.listdir(source_dir))-2)
            #if source_name in seen or not source_name.startswith('id:%06d' % (len(os.listdir(source_dir))-1)):
            if source_name in seen or not source_name.startswith(file_id):
                continue
            seen.add(source_name)
            with open(os.path.join(source_dir, source_name)) as seedfile:
                seed = seedfile.read()

            print 'Tracing input: %s' % seed
            for _, new_input in Driller(binary, seed, fuzzer_bitmap).drill_generator():
                new_input = seed.replace("\00","").strip() + new_input.replace("\00","").strip()           
                save_input(new_input, dest_dir, count)
                count += 1

            
            seed1 = seed + '0000'
            print 'Try Larger and Tracing input: %s' % seed1
            for _, new_input in Driller(binary, seed1, fuzzer_bitmap).drill_generator():
                new_input = seed.replace("\00","").strip() + new_input.replace("\00","").strip() 
                save_input(new_input, dest_dir, count)
                count += 1
        time.sleep(5)

if __name__ == '__main__':
    main()
