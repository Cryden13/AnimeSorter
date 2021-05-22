from tkinter import Tk, Frame, Label, Spinbox, LabelFrame as LFrame, messagebox as mbox
from scrolledframe import ScrolledFrame as SFrame
from tkinter.ttk import Button, Separator, Style
from re import match as re_match
from changecolor import lighten
from typing import Union as U
from pathlib import Path

from .constants import *


rndto = 1


def zerofrmt(num: U[str, int]) -> str:
    return f'{int(num):0{rndto}d}'


class GUI(Tk):
    data: dict[str, dict[str, U[Frame, Spinbox, Label, Path, str]]]
    cwd: Path
    defBg: str
    litBg: str
    checkValid: tuple[str, str]
    curRow: int
    scrFrm: SFrame
    lastRow: int
    maxRow: int
    lblRow: int

    def __init__(self):
        Tk.__init__(self)
        self.title('Change Order')
        self.geometry(f'{WIDTH}'
                      f'x{HEIGHT}'
                      f'+{(self.winfo_screenwidth() - WIDTH) // 2}'
                      f'+{(self.winfo_screenheight() - HEIGHT) // 2}')
        Style().configure('TSeparator', background='red')
        self.option_add('*font', FONT)
        self.bind_all(sequence='<ButtonRelease-1>',
                      func=lambda e: e.widget.focus_set())
        raise Exception
        self.after_idle(self.start_main)

    def start_main(self) -> None:
        # init vars
        self.data = dict()
        self.cwd = Path(PATH)
        self.defBg = self.cget('bg')
        self.litBg = lighten(color=self.winfo_rgb(self.defBg),
                             percent=5,
                             inputtype='RGB16')
        self.checkValid = (self.register(self.validateRange), '%P')
        self.curRow = int()
        self.createFrame()
        self.insertData()

    def validateRange(self, val: str) -> bool:
        if not val or (val.isdigit() and 0 < int(val) <= self.maxRow):
            return True
        else:
            return False

    def createFrame(self) -> None:
        # create save button
        saveBtn = Button(master=self,
                         text="Save",
                         command=self.submit)
        saveBtn.place(anchor='s',
                      relx=0.5,
                      rely=1,
                      y=(-PAD))
        # create containing frame
        lfrm = LFrame(master=self,
                      text="Anime List")
        lfrm.place(anchor='n',
                   relx=0.5,
                   rely=0,
                   y=PAD,
                   relwidth=1,
                   width=(-PAD * 2),
                   relheight=1,
                   height=(-PAD * 3 - saveBtn.winfo_reqheight()))
        # create scrolling frame
        self.scrFrm = SFrame(master=lfrm,
                             scrollbars='e',
                             padding=PAD,
                             bd=0)
        self.scrFrm.place(anchor='nw',
                          relx=0,
                          relwidth=1,
                          rely=0,
                          relheight=1)
        self.scrFrm.columnconfigure(0, weight=1)

    def insertData(self) -> None:
        global rndto
        maxNum = int()
        new: list[Path] = list()
        nfols: dict[str, tuple[Path, str]] = dict()
        folders = [f for f in self.cwd.iterdir() if f.is_dir()]
        for fol in folders:
            m = re_match(r'(\d+)[\W]*(.+)$', fol.name)
            if m:
                maxNum = max(maxNum, int(m.group(1)))
                nfols[m.group(1)] = (fol, m.group(2))
            else:
                new.append(fol)

        folct = len(folders)
        self.maxRow = max(maxNum, folct)
        rndto = len(str(self.maxRow))
        self.lblRow = (self.maxRow + 1)
        self.lastRow = (self.lblRow + folct)

        newLbl = Label(master=self.scrFrm,
                       text="Non-enumerated Folders:")
        newLbl.grid(column=0,
                    row=self.lblRow,
                    pady=((PAD * 5), (PAD // 2)),
                    sticky='nsew')
        nLbl = Label(master=self.scrFrm,
                     text="None")
        nLbl.grid(column=0,
                  row=self.lastRow,
                  sticky='nsew')
        for n in range(folct):
            s = Separator(master=self.scrFrm,
                          orient='horizontal')
            s.grid(column=0,
                   row=(n + 1),
                   sticky='ew',
                   pady=3)
        for num, (fol, name) in nfols.items():
            self.fillInfo(curRow=int(num),
                          path=fol,
                          name=name)
        for i, fol in enumerate(new):
            num = (self.lastRow - i)
            self.fillInfo(curRow=num,
                          path=fol)

    def fillInfo(self, curRow: int, path: Path, name: str = None) -> None:
        rowLbl = zerofrmt(curRow)
        bg = self.litBg if (curRow % 2) else self.defBg
        # create container
        frm = Frame(master=self.scrFrm,
                    bg=bg,
                    relief='sunken',
                    bd=1)
        frm.columnconfigure(1, weight=1)
        frm.grid(column=0,
                 row=curRow,
                 sticky='ew')
        # create spinbox
        sbox = Spinbox(master=frm,
                       width=3,
                       bg=bg,
                       format=(f'%0{rndto}d' if rndto > 1 else ''),
                       takefocus=False,
                       from_=1,
                       to=self.lblRow,
                       increment=-1,
                       repeatdelay=(10**5),
                       validate='key',
                       validatecommand=self.checkValid)
        sbox.grid(column=0,
                  row=0)

        def btnpress(f=frm, s=sbox): self.updateList(f, s, True)
        def commit(_, f=frm, s=sbox): self.updateList(f, s)
        def cancel(_, f=frm, s=sbox): self.cancelChange(f, s)

        sbox.configure(command=btnpress)
        sbox.delete(0, 'end')
        if name:
            sbox.insert(0, rowLbl)
        else:
            name = path.name
        sbox.bind('<Return>', commit)
        sbox.bind('<Escape>', cancel)
        # create name label
        lbl = Label(master=frm,
                    text=name,
                    bg=bg)
        lbl.grid(column=1,
                 row=0,
                 sticky='w')
        # save to data dict
        self.data[rowLbl] = dict(frm=frm,
                                 sbox=sbox,
                                 lbl=lbl,
                                 path=path,
                                 name=name)

    def cancelChange(self, frm: Frame, sbox: Spinbox) -> None:
        self.focus_set()
        oldRow = zerofrmt(frm.grid_info()['row'])
        if oldRow != sbox.get():
            sbox.delete(0, 'end')
            sbox.insert(0, oldRow)

    def updateList(self, frm: Frame, sbox: Spinbox, btn: bool = False) -> None:
        # get data
        start = frm.grid_info()['row']
        oldInfo = self.data.pop(zerofrmt(start))
        # get spinbox value
        moveToLbl = str(sbox.get())
        if moveToLbl == zerofrmt(start):
            return
        elif not moveToLbl:
            if start < self.lblRow:
                start = (self.lblRow + 1)
                moveToLbl = zerofrmt(self.lastRow)
                self.focus_set()
            else:
                return
        elif btn and int(moveToLbl) == self.lblRow:
            sbox.delete(0, 'end')
            start = (self.lblRow + 1)
            moveToLbl = zerofrmt(self.lastRow)
            self.after(0, self.focus_set)
        elif btn and abs(start - int(moveToLbl)) > 1:
            self.moveInterim(start, zerofrmt(self.lblRow + 1), True)
            start = 0
            moveToLbl = zerofrmt(self.maxRow)
            sbox.delete(0, 'end')
            sbox.insert(0, moveToLbl)
        elif not btn:
            if len(moveToLbl) != rndto:
                moveToLbl = zerofrmt(moveToLbl)
                sbox.delete(0, 'end')
                sbox.insert(0, moveToLbl)
            if start == self.lastRow:
                self.moveInterim(start, zerofrmt(self.lblRow + 1), True)
        sbox.selection_range(0, 'end')
        if moveToLbl == zerofrmt(start):
            return
        if moveToLbl in self.data:
            self.moveInterim(start, moveToLbl, False)
        moveToRow = int(moveToLbl)
        bg = self.litBg if (moveToRow % 2) else self.defBg
        frm.grid(row=moveToRow)
        frm.configure(bg=bg)
        sbox.configure(bg=bg)
        oldInfo['lbl'].configure(bg=bg)
        self.data[moveToLbl] = oldInfo

    def moveInterim(self, start: int, moveToLbl: str, updateNon: bool):
        moveToRow = int(moveToLbl)
        nmin = min(start, moveToRow)
        nmax = max(start, moveToRow)
        add = 1 if moveToRow < start else -1
        if updateNon:
            change = {n: self.data.pop(n) for n in list(self.data)
                      if nmin <= int(n) <= nmax}
            for num, info in change.items():
                self.move(add, num, info)
        else:
            change = {n: v for n, v in self.data.items()
                      if nmin <= int(n) <= nmax}
            curRowLbl = moveToLbl
            self.data.pop(curRowLbl, None)
            while curRowLbl in change:
                curRowLbl = self.move(add, curRowLbl, change.get(curRowLbl))

    def move(self, add: int, rowLbl: str, d: dict[str, U[Frame, Spinbox, Label, Path, str]]) -> str:
        newRow = (int(rowLbl) + add)
        newLbl = zerofrmt(newRow)
        bg = self.litBg if (newRow % 2) else self.defBg
        # update frame
        d['frm'].grid(row=newRow)
        d['frm'].configure(bg=bg)
        # update spinbox
        if d['sbox'].get():
            d['sbox'].delete(0, 'end')
            d['sbox'].insert(0, newLbl)
        d['sbox'].configure(bg=bg)
        # update label
        d['lbl'].configure(bg=bg)
        self.data[newLbl] = d
        return newLbl

    def submit(self):
        for row, info in self.data.items():
            path: Path = info['path']
            num = info['sbox'].get()
            newName = f"{num}{SEPARATOR if num else ''}{info['name']}"
            if path.name != newName:
                newPath = path.rename(path.with_name(newName))
                self.data[row]['path'] = newPath
        mbox.showinfo("Complete", "Files have been successfully renamed.")

    def printdata(self):
        pdict = {k: v['name'] for k, v in self.data.items()}
        print(pdict)
