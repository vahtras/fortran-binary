import argparse
from unformatted import FortranBinary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--records', action='store_true', help='List record lengths')
    parser.add_argument('filename', help='Fortran binary flie')
    args = parser.parse_args()

    if args.records:
        file_ = FortranBinary(args.filename)
        print(file_.record_byte_lengths())
        
if __name__ == "__main__":
    import sys
    sys.exit(main())
