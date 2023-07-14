from colorama import Fore, Style

def print_logo() -> None:
    print(Fore.GREEN +
          ' _____ ____ ____                                 \n'         
          '|_   _/ ___|  _ \   _ __  _ __ _____  ___   _    \n'
          '  | || |   | |_) | | \'_ \| \'__/ _ \ \/ / | | | \n'
          '  | || |___|  __/  | |_) | | | (_) >  <| |_| |   \n'
          '  |_| \____|_|     | .__/|_|  \___/_/\_\\__,  |  \n'
          '                   |_|                  |___/    \n\n'
          'download link: https://github.com/EvtDanya/TCP-proxy\n\n'
          + Style.RESET_ALL)
    
def print_color(text, color=None) -> None:
    '''
    Print color text
    '''
    if color:
        color_obj = getattr(Fore, color.upper(), None)
        if color_obj:
            print(color_obj + text + Style.RESET_ALL)
            return
    print(text)  
  