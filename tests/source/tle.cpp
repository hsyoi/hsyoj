#include <iostream>
#include <unistd.h>

int main()
{
    int a, b;
    std::cin >> a >> b;
    std::cout << a + b << std::endl;
    sleep(3);
    return 0;
}
