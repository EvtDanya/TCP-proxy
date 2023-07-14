import argparse
import ipaddress
import logging

from modules.print import print_color

class Validation:
    '''
    Class for args validation
    '''
    @staticmethod
    def validate_ip_address(ip_address) -> str:
        try:
            ipaddress.ip_address(ip_address) # try to convert str to ip address
            return ip_address
        except ValueError:
            logging.error(f'[!] Invalid IP address: {ip_address}')
            raise argparse.ArgumentTypeError(f'Invalid IP address: {ip_address}')
    @staticmethod
    def validate_num(count):
        if not count or int(count) <= 0:
            logging.error(f'[!] Integer must be a positive (>= 0)!')
            raise argparse.ArgumentTypeError('Integer must be a positive (>= 0)!')
        return int(count)

def parse_args() -> argparse.Namespace:
    '''
    Parse command line arguments
    '''
    try:
        parser = argparse.ArgumentParser(
            description='TCP-proxy server by d00m_r34p3r',
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=56)
        )
        parser.add_argument( 
            '-lh', '--localhost',
            metavar='ip',
            type=Validation.validate_ip_address,
            required=True,
            help='ip address of localhost'
        )
        parser.add_argument( 
            '-lp', '--local-port',
            metavar='number',
            type=int,
            required=True,
            help='local port number'
        )
        parser.add_argument( 
            '-rh', '--remote-host',
            metavar='ip',
            type=Validation.validate_ip_address,
            required=True,
            help='ip address of remote host'
        )
        parser.add_argument( 
            '-rp', '--remote-port',
            metavar='number',
            type=int,
            required=True,
            help='remote port number'
        )
        parser.add_argument( 
            '-r', '--receive-first',
            action='store_true',
            required=True,
            help='remote port number'
        )
        parser.add_argument( 
            '-V', '--verbose',
            action='store_true',
            help='print more information'
        )
         
    except Exception as ex:
        print_color(f'\n[!] {ex}', 'red')
        logging.error(f'[!] {ex}')
        input('\nPress Enter to continue...') 
        exit(1)
    
    return parser.parse_args()