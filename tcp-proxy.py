from modules.args import parse_args
from modules.print import *
from modules.server import server_loop

import os
import logging
import datetime

def start_log() -> None:
    '''
    Start logging and report errors to log file
    '''
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"logs/proxy-errors_{datetime.datetime.now().strftime('%d%m%Y')}.log",
        filemode='a',
        encoding='utf-8'
    )
        
def main() -> None:
    print_logo()
    start_log()
    
    args = parse_args()    
    
    server_loop(args.lh, args.lp, args.rh, args.rp, args.r)
    
if __name__ == '__main__':
    main()
    