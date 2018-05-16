import pickle

idaapi.autoWait()

save_path =idc.ARGV[1]

opcode = []

for seg_ea in Segments() :
    for func_ea in Functions(seg_ea, SegEnd(seg_ea)):
        func_opcode = []
        for (start_ea, end_ea) in Chunks(func_ea) :
            for head in Heads(start_ea, end_ea):
                if isCode(GetFlags(head)) :
                    func_opcode.append('%02x' %(Byte(head)))
        opcode.append(func_opcode)

with open(save_path, 'wb') as f :
    pickle.dump(opcode, f)

idc.Exit(0)