import parser as d_p
import problem as p_p
import grounding as g
import sys

def main(argv):
    d_p.parse(argv[0])
    p_p.problem_parser(argv[1])
    g.groundind(argv[0], argv[1])

if __name__ == '__main__':
    main(sys.argv[1:])
