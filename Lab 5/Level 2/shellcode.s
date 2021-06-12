movl $0x8013F158,%eax
movl (%eax),%eax
movl $0x8013F160,%ebx
movl %eax,(%ebx)
push $0x80139b69 
ret
