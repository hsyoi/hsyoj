#include <fstream>

int main()
{
    int a, b;
    std::ifstream fin("1000.in");
    std::ofstream fout("1000.out");
    fin >> a >> b;
    fout << a + b << std::endl;
    return 0;
}
