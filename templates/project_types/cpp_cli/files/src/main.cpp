#include <iostream>
#include <string>

std::string describe_project() {
  // Time complexity: O(1). Space complexity: O(1).
  return "{{project_name}}: minimal deterministic {{language}} scaffold";
}

int main() {
  std::cout << describe_project() << '\n';
  return 0;
}
