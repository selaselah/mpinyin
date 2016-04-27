fn_py = './mpinyin/py.txt'
fn_dict = './mpinyin/dict.txt'

fout = open(fn_dict, 'w')
fin = open(fn_py)

for line in (l.strip() for l in fin):
    word, py, freq = line.split('\t')
    fout.write('{} {} n\n'.format(word, freq))

