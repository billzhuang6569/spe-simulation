import argparse
from engine.turnloop import TurnEngine

def main(argv=None):
    parser = argparse.ArgumentParser(prog='lucidity')
    subparsers = parser.add_subparsers(dest='command')

    start_parser = subparsers.add_parser('start', help='Start the simulation')
    start_parser.add_argument('--dummy', action='store_true', help='Run in dummy mode')
    start_parser.add_argument('--turns', type=int, default=10, help='Number of turns to run')
    start_parser.add_argument('--log', type=str, help='Path to save event log')

    replay_parser = subparsers.add_parser('replay', help='Replay a saved session')
    replay_parser.add_argument('log', help='Path to log file')

    args = parser.parse_args(argv)

    if args.command == 'start':
        if args.dummy:
            engine = TurnEngine(turns=args.turns)
            log_file = None
            if args.log:
                log_file = open(args.log, 'w')
            try:
                for event in engine.run_dummy():
                    print(event)
                    if log_file:
                        log_file.write(event + "\n")
            finally:
                if log_file:
                    log_file.close()
        else:
            raise NotImplementedError('Game logic not implemented yet')
    elif args.command == 'replay':
        with open(args.log) as f:
            for line in f:
                print(line.strip())
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
