#include <iostream>
#include <set>
#include <string>
#include <vector>

// produced by ChatGPT as a direct translation of Part1 of the Python's day9 program
int Part1(const std::vector<std::string>& lines) {
  int headx = 0, heady = 0;
  int tailx = 0, taily = 0;
  std::set<std::pair<int, int>> places_visited = {{0, 0}};

  for (const auto& line : lines) {
    if (line.empty()) continue;

    auto direction = line[0];
    auto numstr = line.substr(1);
    auto num = std::stoi(numstr);

    for (int ii = 0; ii < num; ++ii) {
      auto old_headx = headx, old_heady = heady;

      if (direction == 'R') {
        headx += 1;
      } else if (direction == 'L') {
        headx -= 1;
      } else if (direction == 'U') {
        heady += 1;
      } else if (direction == 'D') {
        heady -= 1;
      }

      if (abs(headx - tailx) > 1 || abs(heady - taily) > 1) {
        tailx = old_headx;
        taily = old_heady;
        places_visited.insert({tailx, taily});
      }
    }
  }

  return places_visited.size();
}

int main() {
  std::vector<std::string> lines = {
    "R2",
    "U3",
    "L1",
    "D1"
  };

  std::cout << Part1(lines) << std::endl;

  return 0;
}