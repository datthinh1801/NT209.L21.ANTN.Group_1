# Level 2
## Task
Buffer overflow hàm `getbuf` để thực thi được hàm `bang` với `global_value == cookie`.  
```c
void __noreturn bang()
{
  if ( global_value == cookie )
  {
    printf("Bang!: You set global_value to 0x%x\n", global_value);
    validate(2);
  }
  else
  {
    printf("Misfire: global_value = 0x%x\n", global_value);
  }
  exit(0);
}
```
