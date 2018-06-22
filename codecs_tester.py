import codecs

ENCODING = 'utf-8'

tmp0 = "test string"
tmp1 = codecs.encode(tmp0, 'utf8', 'strict')
tmp2 = codecs.encode(tmp1, 'base64', 'strict')
tmp3 = codecs.decode(tmp2, 'base64', 'strict')
tmp4 = codecs.decode(tmp3, 'utf8', 'strict')

print("tmp0:", tmp0)
print("tmp1:", tmp1)
print("tmp2:", tmp2)
print("tmp3:", tmp3)
print("tmp4:", tmp4)

tmp5 = codecs.decode(tmp2, 'utf8', 'strict')
tmp6 = codecs.encode(tmp5, 'utf8', 'strict')
tmp7 = codecs.decode(tmp6, 'base64', 'strict')
tmp8 = codecs.decode(tmp7, 'utf8', 'strict')
print("tmp5:", tmp5)
print("tmp6:", tmp6)
print("tmp7:", tmp7)
print("tmp8:", tmp8)
