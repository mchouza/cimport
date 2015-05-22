#include <stdio.h>

void bar(const char *s)
{
    printf("%s!\n", s);
}

void foo(void)
{
    bar("Hello world");
}
