/**
 * @file ole.cpp
 * @author Joschka Seydell (joschka@seydell.org)
 * @brief Simple application for learning the use of overlays.
 * @version 0.1
 * @date 2025-03-28
 * 
 * @copyright Copyright (c) 2025
 * 
 */
#include <array>
#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>
#include <functional>
#include <format>
#include <map>
#include <string>
#include <string_view>
#include <sstream>


// Constants
constexpr std::string_view HELP_TEXT {
    "Prints elePi quest solution fragments... if configured correctly.\n\n"
    "Usage: ole [options] \n\n"
    "Options: \n"
    "\t-h, --help Show this help message.\n\n"
    "Notes: Basic configuration is provided in /usr/share/ole/app.ini."
    "There, you also find user configuration (both required and additional ones).\n\n"
    "To select which quest solution code fragment to print, you have to provide"
    "an extra user config named 'fragment.ini'.\n"};

constexpr std::string_view DEFAULT_CONF {"/usr/share/ole/defaults/app.ini"};
constexpr std::string_view REQUIRED_CONF {"/usr/share/ole/user/required/logging.ini"};
constexpr std::string_view EXTRA_CONF {"/usr/share/ole/user/extra/fragment.ini"};

constexpr std::array<std::string_view, 4U> FRAGMENTS = {
    "76bb5c213c6fde54e6e905db751246f2",
    "d07a98fa253d47c640235fd4a2f032f5",
    "81b0a9b680044be8a935c46cbac72558",
    "81534e2cf0e7be8c45b4136a6110edb5"
};


// Types
using Configuration = std::map<std::string, std::string>;

/**
 * @brief Conditionally prints the message to cerr.
 */
void PrintErrorIf(std::string_view msg, bool verbose = true)
{
    if (!verbose)
    {
        return;
    }
    std::cerr << "[ERROR] " << msg << std::endl;
}

/**
 * @brief Parse the configuration at the given path.
 */
bool ParseConfiguration(std::string_view filePath, Configuration& config, bool required = true)
{
    if (!std::filesystem::exists(filePath))
    {
        PrintErrorIf(std::format("File does not exist: {}", filePath), required);
        return false;
    }

    std::ifstream configFile{filePath.data()};
    if (!configFile.is_open())
    {
        PrintErrorIf(std::format("Unable to open file: {}", filePath), required);
        return false;
    }

    std::string line;
    std::string key;
    std::string value;
    while (std::getline(configFile, line))
    {
        std::istringstream sstr(line);
        if (std::getline(sstr, key, '=') && std::getline(sstr, value))
        {
            config[key] = value;
        }
        else 
        {
            PrintErrorIf(std::format("Format error in file: {}", filePath), required);
            return false;
        }
    }
    return true;
}

/**
 * @brief Prints the usage instructions to the console.
 */
void PrintHelp()
{
    std::cout << HELP_TEXT;
}


int PrintFragment()
{
    Configuration config{};

    if (!ParseConfiguration(DEFAULT_CONF, config))
    {
        PrintErrorIf("Provide a valid default app configuration under /usr/share/ole/defaults.");
        return 1;
    }

    if (!ParseConfiguration(REQUIRED_CONF, config))
    {
        PrintErrorIf("Usually, the required user configuration is provisioned under /usr/share/ole/user/required"
                     " - this may hint at a misconfiguration of the system.");
        return 1;
    }

    std::cout << "Default solution fragment: " << FRAGMENTS[0] << std::endl;
    
    if (!ParseConfiguration(EXTRA_CONF, config, false))
    {
        std::cout << "Note: No valid configuration to select other solution code fragments found." << std::endl;
        return 0;
    }
    
    if (!config.contains("fragment"))
    {
        PrintErrorIf("To specifying an extra user configuration to select another solution code fragment, "
                     "you need to set the key 'fragment' to a numeric value between 1 and 4.");
        return 1;
    }
    auto fragmentNumber = std::stoul(config["fragment"]);
    if (fragmentNumber == 0 || fragmentNumber > 4)
    {
        PrintErrorIf("Invalid fragment selected in user configuration!");
        return 1;
    }
    std::cout << "Selected solution fragment: " << FRAGMENTS[fragmentNumber - 1] << std::endl;
    return 0;
}


int main(int argc, char* argv[])
{
    std::map<std::string, std::function<void()>> commandMapping = {
        {"-h", PrintHelp},
        {"--help", PrintHelp}
    };

    if (argc > 1)
    {
        const std::string& command = argv[1];
        if (!commandMapping.contains(command))
        {
            std::cerr << "[ERROR] Unknown command " << command << std::endl;
            return 1;
        }
        commandMapping[command]();
        return 0;
    }

    return PrintFragment();
}