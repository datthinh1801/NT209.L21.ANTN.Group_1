# Phase 5
## Solution
Mở IDA Pro 32bit và xem pseudocode.  

```c
unsigned int __cdecl phase_5(int input_string)
{
  int i; // eax
  char v3[7]; // [esp+11h] [ebp-17h] BYREF
  unsigned int v4; // [esp+18h] [ebp-10h]

  v4 = __readgsdword(0x14u);
  if ( string_length(input_string) != 6 )
    explode_bomb();

  for ( i = 0; i != 6; ++i )
    v3[i] = array_3249[*(_BYTE *)(input_string + i) & 0xF];

  v3[6] = 0;
  if ( strings_not_equal(v3, "oilers") )
    explode_bomb();
  return __readgsdword(0x14u) ^ v4;
}
```
