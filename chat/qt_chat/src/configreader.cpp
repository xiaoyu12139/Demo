#include "configreader.h"
#include <fstream>
#include <string>
#include <iostream>   // 如果你也要输出日志

ConfigReader::ConfigReader()
{
}
unordered_map<string, string> ConfigReader::readServerConfig(){
    ifstream in(SERVER_CONFIG_PATH, ios::in);
    unordered_map<string, string> configMap;
    if(in.is_open()){
        string line;
        while(std::getline(in, line)){
            int index = line.find('=');
            configMap[line.substr(0, index)] = line.substr(index+1);
        }
    }
    return configMap;
}
string ConfigReader::SERVER_CONFIG_PATH = "server.conf";
