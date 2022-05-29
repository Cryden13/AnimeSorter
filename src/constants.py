from pathlib import Path
from configparser import (
    ExtendedInterpolation as _ExtInterp,
    ConfigParser as _ConfigParser
)


_cfgfile = Path(__file__).parent.with_name('config.cfg')
_cfg = _ConfigParser(interpolation=_ExtInterp())
_cfg.optionxform = str
_cfg.read_file(open(_cfgfile))


_sct = 'Default'
WIDTH = _cfg.getint(_sct, 'width')
HEIGHT = _cfg.getint(_sct, 'height')
PAD = _cfg.getint(_sct, 'padding')
FONT = _cfg.get(_sct, 'font')
SEPARATOR = _cfg.get(_sct, 'separator')
PATH = Path(_cfg.get(_sct, 'path')).resolve()
