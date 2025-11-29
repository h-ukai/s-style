#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CS-2 small utility, with b64 capabilities, and quite no checks...
 - See https://ciphersaber.gurus.com for information.
 - Basically, this is a python implementation of the ARC4 cipher algorithm.
 - ARC4 is probably not a good choice if you want top level encryption.
 - The text to encrypt must be passed in a 8bit format (aka not a unicode 
   string), due to the use of the array module. 

Changelog since version 1.0: 
 - better description
 - use True/False booleans for the enc parameter
 - change indent.
 
"""

import sys
import string
import random
import array
import base64

__version__="$Id: cs.py 2330 2005-05-08 19:40:46Z jd $"

version="1.1"


'''
https://d.hatena.ne.jp/Fio/20081030/p1


Ciphersaber in pythonにあるcs.pyを利用します。
何箇所かにあるファイルはどれも同じもののようです。
CipherSaberはアルゴリズムが簡単で、スピードが速く、しかもかなり強力だと思います。
使いやすくするために、cs.pyに次のラッパーを追加

'''
def EnCipher(keytxt,txt):
    return base64.encodestring(cipher(txt,keytxt,True,20))

def DeCipher(keytxt,txt):
    return cipher(base64.decodestring(txt),keytxt,False,20)
'''
import cs
import base64

PlainText="私はカモメ"*10
Key="日本語パスワード"

print PlainText
CipherText = cs.EnCipher(Key,PlainText)
print CipherText
PlainText2 = cs.DeCipher(Key,CipherText)
print PlainText2
'''

def cipher(txt,keytxt,enc=False,csn=20):
    """txt: string to encrypt or decrypt (8bit chars),
    keytxt: passphrase string (8bit chars),
    enc : encryption flag, False to decrypt, True to encrypt,
    csn: cs-2 default of length 20, use csn=1 for CS-1
    """
    
    atxt=array.array('B',txt)
    akeytxt=array.array('B',keytxt)
    if enc:
        r10=array.array('B',"")
        for i in range(10):
            r10.append(random.randrange(256))
    else:
        r10=atxt[:10]
        atxt=atxt[10:]
    bkey=akeytxt+r10
    lk=len(bkey)
    
    #init s
    s=range(256)
    j=0
    for k in range(csn):
        for i in range(256):
            j=(j+s[i]+bkey[i%lk])%256
            s[i],s[j]=s[j],s[i]
    #now, cipher:
    i=j=0
    otxt=array.array('B',"")
    for c in atxt:
        i=(i+1)%256
        j=(j+s[i])%256
        s[i],s[j]=s[j],s[i]
        k=(s[i]+s[j])%256
        otxt.append(c^s[k])
    
    if enc:
        return r10.tostring()+otxt.tostring()
    else:
        return otxt.tostring()

def b64cipher(txt,keytxt,enc=False,csn=20):
    "base64 wrapper for cipher()"
    if enc:
        return base64.encodestring(cipher(txt,keytxt,enc,csn))
    else:
        return cipher(base64.decodestring(txt),keytxt,enc,csn)

def usage():
    sys.stderr.write("""cs.py v.%s: CS-2 encoder/decoder with base64 capabilities.
(c) 2003-2005 jd@hamete.org, perl artistic license, or whatever other free 
license you want, at your choice :-).
usage:
cs.py [-b] [-n N] [-e|-d] passphrase <input >output
    -b: use base64 encrypted input (-d) or base64 encrypted output (-e),
    -n N: CS-2 loop of N iterations (default 20, use N=1 for CS-1),
    -e passphrase : encrypt using the passphrase,
    -d passphrase : decrypt using the passphrase.
"""%version)
    sys.exit(0)
        

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    #cs-2 of length 20, use csn=1 for CS-1
    csn=20
    useb64=0
    needn=0    
    needp=0
    enc=False
    try:
        for a in sys.argv[1:]:
            if needn:
                csn=int(a)
                needn=0
                continue
            if needp:
                keytxt=a
                needp=0
                continue
            if a=="-b":
                useb64=1
            elif a=="-n":
                needn=1
            elif a=="-e":
                enc=True
                needp=1
            elif a=="-d":
                enc=False
                needp=1
            else:
                usage()
    except:
        usage()
        
    txt=sys.stdin.read()
    
    if useb64:
        sys.stdout.write(b64cipher(txt,keytxt,enc,csn))
    else:
        sys.stdout.write(cipher(txt,keytxt,enc,csn))
