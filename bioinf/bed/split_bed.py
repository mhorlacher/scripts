import argparse
import math
from pathlib import Path

def open_out_bed(fp, suffix):
    assert fp[-4:] == '.bed'
    fp_base = fp[:-4]
    return open(fp_base + f'.{suffix}.bed', 'w')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bed', metavar='<file.bed>')
    parser.add_argument('-o', help='output directory')
    parser.add_argument('-n', type=int)
    args = parser.parse_args()

    assert args.bed[-4:] == '.bed'
    assert Path(args.o).exists() 

    fn = Path(args.bed).name
    new_fp = str(Path(args.o) / fn)

    suffix_ipos = math.ceil(math.log(args.n, 10))

    try:
        out_handles = [open_out_bed(new_fp, f'{i:0{suffix_ipos}}') for i in range(args.n)]

        with open(args.bed) as f:
            for i, line in enumerate(f):
                print(line.strip(), file=out_handles[i % args.n])
    except:
        raise
    finally:
        for handle in out_handles:
            handle.close()