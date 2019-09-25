import sys
from datatypes import *
import content
import network

def EmitMembers(obj):
    has_array = False
    for v in obj.variables:
        if isinstance(v, NetIntRange) or isinstance(v, NetIntAny) or isinstance(v, NetEnum) or isinstance(v, NetFlag) or isinstance(v, NetTick):
            print('\t\tObjectSetMemberInt("%s", Obj.%s);' % (v.name, v.name))
        elif isinstance(v, NetString) or isinstance(v, NetStringStrict):
            print('\t\tObjectSetMemberString("%s", Obj.%s);' % (v.name, v.name))
        elif isinstance(v, NetBool):
            print('\t\tObjectSetMemberBool("%s", Obj.%s);' % (v.name, v.name))
        elif isinstance(v, NetArray):
            if not has_array:
                print('\t\tduk_idx_t Array = duk_push_array(Ctx());')
                has_array = True
            else:
                print('\t\tArray = duk_push_array(Ctx());')

            print('\t\tfor(int i = 0; i < %d; i++)' % v.size)
            print('\t\t{')

            if isinstance(v.var, NetIntRange) or isinstance(v.var, NetIntAny) or isinstance(v.var, NetEnum) or isinstance(v.var, NetFlag) or isinstance(v.var, NetTick):
                print('\t\t\tduk_push_int(Ctx(), Obj.%s[i]);' % (v.base_name))
            elif isinstance(v.var, NetString) or isinstance(v.var, NetStringStrict):
                print('\t\t\tduk_push_string(Ctx(), Obj.%s[i]);' % (v.base_name))
            elif isinstance(v.var, NetBool):
                print('\t\t\tduk_push_bool(Ctx(), Obj.%s[i]);' % (v.base_name))

            print('\t\t\tduk_put_prop_index(Ctx(), Array, i);')
            print('\t\t}')
            print('\t\tObjectSetMember("%s");' % v.base_name)
            print('\t\t')



print("#include <game/client/components/duck_js.h>")
print("")
print("bool CDuckJs::MakeVanillaJsNetObj(int MsgID, void* pRawMsg)\n{")

for obj in network.Objects + network.Messages:
    print("\tif(MsgID == %s)" % obj.enum_name)
    print("\t{")
    print("\t\tconst %s& Obj = *(%s*)pRawMsg;" % (obj.struct_name, obj.struct_name))
    print("\t\tPushObject();")
    print('\t\tObjectSetMemberInt("tw_id", %s);' % (obj.enum_name))
    print('\t\tObjectSetMemberString("tw_name", "%s");' % (obj.struct_name))

    # inheritence
    cur = obj
    while not cur.base == "":
        for b in network.Objects + network.Messages:
            if b.name == obj.base:
                EmitMembers(b)
                cur = b
                break
    
    EmitMembers(obj)
    
    print("\t\treturn true;")
    print("\t}")

print("\treturn false;")
print("}\n")