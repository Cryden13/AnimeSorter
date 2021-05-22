try:
    from .sorter import GUI
except ImportError:
    from pathlib import Path
    from subprocess import run
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit

if __name__ == '__main__':
    try:
        GUI().mainloop()
    except:
        from pathlib import Path
        from subprocess import Popen
        from traceback import format_exc
        errLog = Path(__file__).parent.joinpath('errorlog.txt')
        errLog.write_text(format_exc())
        Popen(['powershell',
               '-command',
               f'[system.media.systemsounds]::Hand.play(); Start-Process "{errLog}"'])
