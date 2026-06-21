#include <cassert>
#include <string>

std::string describe_project() {
  // Time complexity: O(1). Space complexity: O(1).
  return "{{project_name}}: minimal deterministic {{language}} scaffold";
}

int main() {
  assert(describe_project() == "{{project_name}}: minimal deterministic {{language}} scaffold");
  return 0;
}
