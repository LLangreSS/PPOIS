#include "src/machine_post.h"
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 2 || argc > 3) {
        std::cerr << "Usage: " << argv[0] << " <file | -> [-log]\n";
        return 1;
    }
    std::string source;
    bool logging = false;
    if (argc == 2) {
        source = argv[1];
    } else {
        if (argv[1] == std::string("-log")) {
            logging = true;
            source = argv[2];
        } else if (argv[2] == std::string("-log")) {
            logging = true;
            source = argv[1];
        } else {
            std::cerr << "Error: unknown flag. Use -log.\n";
            return 1;
        }
    }
    try {
        MachinePost machine(logging);
        machine.load(source);
        machine.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << '\n';
        return 1;
    }
    return 0;
}