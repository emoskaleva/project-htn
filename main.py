import parser as d_p
import problem as p_p
import sys

def main(argv):
    d_p.parse(argv[1])
    p_p.problem_parser(argv[2])

if __name__ == '__main__':
    main(sys.argv[1:])
