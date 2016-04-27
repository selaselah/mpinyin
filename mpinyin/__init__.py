#!/usr/bin/env python

import sys, os, jieba

MARK = {
    -1: u"aoeiuv\u00fc",
    0: u"aoeiu\u00fc\u00fc",
    1: u"\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
    2: u"\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
    3: u"\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
    4: u"\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
}

class PyInfo:
    def __init__(self):
        self.pys = []
        self.tones = []
        self.freq = 0

    def num_tone(self):
        ret = []
        for py, tone in zip(self.pys, self.tones):
            ret.append(py+str(tone))
        return ret

    @staticmethod
    def _make_tone_inner(py, tone):
        chs = [c for c in py]
        for i in range(len(chs)):
            r = len(chs) - 1 - i
            mark_i = MARK[-1].find(chs[r])
            if mark_i != -1:
                chs[r] = MARK[tone][mark_i]
                return ''.join(chs)
        return py
        
    def mark_tone(self):
        ret = []
        for py, tone in zip(self.pys, self.tones):
            ret.append(PyInfo._make_tone_inner(py, tone)) 
        return ret

NO_TONE=0
NUM_TONE=1
MARK_TONE=2

class Pinyin:
    def __init__(self):
        self.is_load = False
        # load package default dict
        self.dict_path = os.path.split(os.path.realpath(__file__))[0] + '/py.txt'
        self.jieba_dict_path = os.path.split(os.path.realpath(__file__))[0] + '/dict.txt'

    def get_max_py(self, sentence, tone=NO_TONE):
        if not self.is_load:
            self.load()
        segs = self.segger.cut(sentence, HMM=False)
        ret = []
        for seg in segs:
            pyinfos = self.pydict.get(seg)
            if pyinfos:
                pyinfo = pyinfos[0]
                if tone == NO_TONE:
                    pys = pyinfo.pys
                elif tone == NUM_TONE:
                    pys = pyinfo.num_tone()
                elif tone == MARK_TONE:
                    pys = pyinfo.mark_tone()
                else:
                    raise ValueError("wrong tone")
            else:
                pys = [seg]
            ret.extend(pys)
        return ret
        
    def load(self):
        # load jieba first
        self.segger = jieba.Tokenizer(self.jieba_dict_path)
        self.segger.initialize()
        # load pydict
        self.pydict = {}
        f = None
        try:
            f = open(self.dict_path)
            for line in (l.strip() for l in f):
                parts = line.split('\t')
                if len(parts) != 3:
                    print('bad format line [%s]' % line, file=sys.stderr)
                    continue
                word = parts[0]
                pytones = parts[1].split()
                pys = []
                tones = []
                for pytone in pytones:
                    if pytone[-1] in '01234':
                        py = pytone[:-1] 
                        tone = int(pytone[-1])
                    else:
                        py = pytone
                        tone = 0
                    pys.append(py)
                    tones.append(tone)
                freq = float(parts[2])

                if word in self.pydict:
                    # update prev pyInfo
                    pyinfos = self.pydict[word]
                    wordInfoLen = len(self.pydict[word])
                    i = 0
                    dup = False
                    for i, pyinfo in enumerate(pyinfos):
                        if pyinfo.pys == pys and pyinfo.tones == tones:
                            pyinfo.freq = max(pyinfo.freq, freq)
                            dup = True
                            break
                        if pyinfo.freq < freq:
                            break
                    if not dup:
                        pyinfo = PyInfo()
                        pyinfo.pys = pys
                        pyinfo.tones = tones
                        pyinfo.freq = freq
                        pyinfos.insert(i, pyinfo)
                        # delete same pyinfo
                        for j in range(i+1, len(pyinfos)):
                            if pyinfos[j].pys == pys:
                                del pyinfos[j]
                                break
                else:
                    # create new pyInfos
                    pyinfo = PyInfo()
                    pyinfo.pys = pys
                    pyinfo.tones = tones
                    pyinfo.freq = freq
                    self.pydict[word] = [pyinfo]
        except Exception as e:
            print("error occur:", e)
            try:
                f.close()
            except:
                pass
            return False
        self.is_load = True
        return True
