idaapi.autoWait()

save_path =idc.ARGV[1]

opcode = []

for seg_ea in Segments() :
    for head in Heads(seg_ea, SegEnd(seg_ea)):
        if isCode(GetFlags(head)):
            opcode.append('%02x' %(Byte(head)))

with open(save_path, 'w') as f :
    f.write('\n'.join(opcode))

idc.Exit(0)