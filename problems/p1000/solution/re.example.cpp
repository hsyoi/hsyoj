#include <iostream>
int main()
{
    int a, b;
    std::cin >> a >> b;
    // Cannot division by zero
    std::cout << a + b / 0 << std::endl;
    return 0;
}
