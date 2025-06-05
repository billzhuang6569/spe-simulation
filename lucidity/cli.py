import argparse
from engine.turnloop import TurnEngine

def main(argv=None):
    parser = argparse.ArgumentParser(prog='lucidity')
    subparsers = parser.add_subparsers(dest='command')

    start_parser = subparsers.add_parser('start', help='Start the simulation')
    start_parser.add_argument('--dummy', action='store_true', help='Run in dummy mode')
    start_parser.add_argument('--turns', type=int, default=10, help='Number of turns to run')

    args = parser.parse_args(argv)

    if args.command == 'start':
        if args.dummy:
            engine = TurnEngine(turns=args.turns)
            for event in engine.run_dummy():
                print(event)
        else:
            raise NotImplementedError('Game logic not implemented yet')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
