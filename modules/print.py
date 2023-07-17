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
    
def hexdump(src, length=16) -> None:
    '''
    Print a hex dump (or text) of bytes
    '''
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len (src), length):
        s = src[i:i + length]
        hex = b' '.join([b'%0*X' % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b'%04X %-*s %s' % (i, length * (digits + 1), hex, text))
        
    print_color('[>] Dump', 'yellow')
    print(b'\n'.join(result))
  