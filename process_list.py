#!/usr/bin/env python

from argparse import ArgumentParser
import xlwt

parser = ArgumentParser(description="Creates BOM variants from a kicad BOM file")
parser.add_argument("-i", dest="filename", required=True,
                    help="input file with two matrices", metavar="FILE")
parser.add_argument('-v', dest='variants', required=False,
                    help='variants to use')
args = parser.parse_args()
variants = args.variants
if variants is not None:
    variants = variants.split(',')

print('using variants %s' % variants)

with open(args.filename) as f:
    content = f.readlines()
    content2 = []
    newcontent = []
    parts = []
    i = 0
    for line in content:
        line = line.strip().replace('"', '')
        i += 1
        if (i == 1):
            continue

        linedata = line.split(',')
        variant = linedata[6]
        if (variants is not None) and (variant not in variants) or linedata[4] == 'None':
            continue
        parts.append(linedata[5])
        content2.append(line)

    content = content2

    book = xlwt.Workbook()
    sh = book.add_sheet('parts')
    boldStyle = xlwt.XFStyle()
    # font
    font = xlwt.Font()
    font.bold = True
    boldStyle.font = font
    sh.write(0, 0, 'Reference', style=boldStyle)
    sh.col(0).width = 256 * 55
    sh.write(0, 1, 'Value', style=boldStyle)
    sh.col(1).width = 256 * 25
    sh.write(0, 2, 'Mfg', style=boldStyle)
    sh.col(2).width = 256 * 25
    sh.write(0, 3, 'PartNo', style=boldStyle)
    sh.col(3).width = 256 * 25
    sh.write(0, 4, 'Count', style=boldStyle)
    sh.col(4).width = 256 * 10

    parts = list(set(parts))
    totalcount = 0
    for i, part in enumerate(parts):
        names = []
        count = 0
        value = ''
        manufacturer = ''
        for line in content:
            linedata = line.split(',')
            partname = linedata[5]
            if (partname == part):
                names.append(linedata[0])
                value = linedata[1]
                manufacturer = linedata[4]
                count += 1
        sh.write(i + 1, 0, ' '.join(names))
        sh.write(i + 1, 1, value)
        sh.write(i + 1, 2, manufacturer)
        sh.write(i + 1, 3, part)
        sh.write(i + 1, 4, str(count))
        totalcount += count
    f.close()
    sh.write(len(parts) + 2, 3, 'Different parts', style=boldStyle)
    sh.write(len(parts) + 2, 4, str(len(parts)), style=boldStyle)
    sh.write(len(parts) + 3, 3, 'Total parts', style=boldStyle)
    sh.write(len(parts) + 3, 4, str(totalcount), style=boldStyle)

    book.save('%s_Variant_%s.xls' % (args.filename.split('.csv')[0], '_'.join(variants or [])))
