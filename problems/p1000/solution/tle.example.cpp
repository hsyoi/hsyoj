#include <iostream>
#include <unistd.h>
int main()
{
    int a, b;
    std::cin >> a >> b;
    std::cout << a + b << std::endl;
    // Timeout after wait 3 sec
    sleep(3);
    return 0;
}
