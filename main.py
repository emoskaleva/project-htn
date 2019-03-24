import parser as d_p
import problem as p_p
import grounding as g
import HTN as planner
import sys

def main(argv):
    #d_p.parser(argv[0])
    #p_p.problem_parser(argv[1])
    #g.grounding(argv[0], argv[1])
    plan = planner.HTN_planner()
    plan.function(argv[0], argv[1], argv[2])

if __name__ == '__main__':
    main(sys.argv[1:])
