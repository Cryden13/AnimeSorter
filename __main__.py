from pathlib import Path
import logging

from commandline import openfile

try:
    from src.sorter import GUI
except ImportError:
    from pathlib import Path
    from subprocess import run
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit


def main():
    errlog = Path(__file__).with_name('errorlog.txt')
    logging.basicConfig(filename=errlog,
                        filemode='w',
                        level=logging.ERROR,
                        format='[%(asctime)s] %(levelname)s: %(module)s.%(funcName)s\n%(message)s\n',
                        datefmt='%m/%d/%Y %I:%M:%S%p')
    try:
        GUI().mainloop()
    except:
        logging.exception('')
        raise
    finally:
        if errlog.read_text():
            openfile(errlog)


if __name__ == '__main__':
    main()
