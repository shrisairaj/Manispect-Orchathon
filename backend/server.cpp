#include <iostream>
#include <string>
#include <sstream>
#include <map>
#include <vector>
#include <memory>
#include <thread>
#include <cstdlib>
#include "core/engine.h"

#ifdef _WIN32
    #include <winsock2.h>
    #pragma comment(lib, "ws2_32.lib")
    #define close closesocket
    typedef int socklen_t;
#else
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <unistd.h>
    #include <arpa/inet.h>
    #define INVALID_SOCKET -1
    typedef int SOCKET;
#endif

class SimpleJSONParser {
public:
    static std::string escape(const std::string& str) {
        std::string result;
        for (char c : str) {
            switch (c) {
                case '"': result += "\\\""; break;
                case '\\': result += "\\\\"; break;
                case '\b': result += "\\b"; break;
                case '\f': result += "\\f"; break;
                case '\n': result += "\\n"; break;
                case '\r': result += "\\r"; break;
                case '\t': result += "\\t"; break;
                default:
                    if (c < 32) {
                        char buf[7];
                        snprintf(buf, sizeof(buf), "\\u%04x", (unsigned char)c);
                        result += buf;
                    } else {
                        result += c;
                    }
            }
        }
        return result;
    }

    static std::string objectToJson(const std::map<std::string, int>& obj) {
        std::string json = "{";
        bool first = true;
        for (const auto& pair : obj) {
            if (!first) json += ",";
            json += "\"" + escape(pair.first) + "\":" + std::to_string(pair.second);
            first = false;
        }
        json += "}";
        return json;
    }

    static std::string arrayToJson(const std::vector<std::map<std::string, int>>& arr) {
        std::string json = "[";
        for (size_t i = 0; i < arr.size(); ++i) {
            if (i > 0) json += ",";
            json += objectToJson(arr[i]);
        }
        json += "]";
        return json;
    }

    static std::map<std::string, std::string> parseJson(const std::string& json) {
        std::map<std::string, std::string> result;
        size_t pos = 0;
        while ((pos = json.find("\"", pos)) != std::string::npos) {
            pos++;
            size_t keyEnd = json.find("\"", pos);
            if (keyEnd == std::string::npos) break;
            std::string key = json.substr(pos, keyEnd - pos);
            pos = keyEnd + 1;

            pos = json.find(":", pos);
            if (pos == std::string::npos) break;
            pos++;

            while (pos < json.length() && (json[pos] == ' ' || json[pos] == '\t' || json[pos] == '\n' || json[pos] == '\r')) pos++;

            if (json[pos] == '"') {
                pos++;
                size_t valEnd = json.find("\"", pos);
                if (valEnd == std::string::npos) break;
                result[key] = json.substr(pos, valEnd - pos);
                pos = valEnd + 1;
            } else if (json[pos] == '[') {
                size_t brackEnd = json.find("]", pos);
                if (brackEnd == std::string::npos) break;
                result[key] = json.substr(pos, brackEnd - pos + 1);
                pos = brackEnd + 1;
            } else {
                size_t valEnd = json.find_first_of(",}", pos);
                if (valEnd == std::string::npos) valEnd = json.length();
                result[key] = json.substr(pos, valEnd - pos);
                pos = valEnd;
            }
        }
        return result;
    }

    static std::vector<std::string> parseArray(const std::string& arr) {
        std::vector<std::string> result;
        size_t start = arr.find('[');
        size_t end = arr.rfind(']');
        if (start == std::string::npos || end == std::string::npos) return result;

        size_t pos = start + 1;
        while (pos < end) {
            while (pos < end && (arr[pos] == ' ' || arr[pos] == ',' || arr[pos] == '\t' || arr[pos] == '\n' || arr[pos] == '\r')) pos++;
            if (pos >= end || arr[pos] != '"') break;
            pos++;
            size_t strEnd = arr.find('"', pos);
            if (strEnd == std::string::npos || strEnd >= end) break;
            result.push_back(arr.substr(pos, strEnd - pos));
            pos = strEnd + 1;
        }
        return result;
    }
};

std::string addCORSHeaders(std::string response) {
    response += "Access-Control-Allow-Origin: *\r\n";
    response += "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n";
    response += "Access-Control-Allow-Headers: Content-Type\r\n";
    return response;
}

class HTTPServer {
public:
    HTTPServer(int port = 8080) : port_(port), running_(false) {}

    void start() {
#ifdef _WIN32
        WSADATA wsa_data;
        if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
            std::cerr << "WSAStartup failed\n";
            return;
        }
#endif

        SOCKET listen_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (listen_socket == INVALID_SOCKET) {
            std::cerr << "Socket creation failed\n";
            return;
        }

        int opt = 1;
        if (setsockopt(listen_socket, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt)) < 0) {
            std::cerr << "setsockopt failed\n";
        }

        sockaddr_in server_addr;
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(port_);
        server_addr.sin_addr.s_addr = INADDR_ANY;

        if (bind(listen_socket, (sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
            std::cerr << "Bind failed on port " << port_ << "\n";
            return;
        }

        listen(listen_socket, 5);
        running_ = true;
        std::cout << "QuantSolve C++ Backend Server listening on 0.0.0.0:" << port_ << "\n";

        while (running_) {
            sockaddr_in client_addr;
            socklen_t client_len = sizeof(client_addr);
            SOCKET client_socket = accept(listen_socket, (sockaddr*)&client_addr, &client_len);

            if (client_socket == INVALID_SOCKET) continue;

            std::thread(&HTTPServer::handle_client, this, client_socket, client_addr).detach();
        }

        close(listen_socket);
    }

    void stop() {
        running_ = false;
    }

private:
    int port_;
    bool running_;

    void handle_client(SOCKET client_socket, sockaddr_in client_addr) {
        std::cout << "New connection from " << inet_ntoa(client_addr.sin_addr) << std::endl;

        char buffer[65536];
        std::string request;
        int bytes_received;
        ssize_t content_length = 0;
        bool headers_parsed = false;

        do {
            bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
            if (bytes_received <= 0) break;
            buffer[bytes_received] = '\0';
            request += buffer;

            if (!headers_parsed) {
                size_t header_end = request.find("\r\n\r\n");
                if (header_end != std::string::npos) {
                    headers_parsed = true;
                    content_length = parse_content_length(request.substr(0, header_end));
                }
            }

            size_t body_start = request.find("\r\n\r\n");
            if (body_start != std::string::npos) {
                size_t body_length = request.length() - (body_start + 4);
                if (body_length >= content_length) break;
            }
        } while (bytes_received > 0 && request.length() < 1024*1024);

        if (request.empty()) {
            close(client_socket);
            return;
        }

        std::string method, path, http_version, body;
        parse_http_request(request, method, path, http_version, body);

        std::cout << method << " " << path << std::endl;

        std::string response = "HTTP/1.1 404 Not Found\r\n";
        response = addCORSHeaders(response);
        response += "Content-Length: 0\r\n\r\n";

        if (method == "OPTIONS") {
            response = "HTTP/1.1 204 No Content\r\n";
            response = addCORSHeaders(response);
            response += "Content-Length: 0\r\n\r\n";
        } else if (method == "POST" && path == "/solve") {
            response = handle_solve_request(body);
        } else if (method == "GET" && path == "/health") {
            response = "HTTP/1.1 200 OK\r\n";
            response = addCORSHeaders(response);
            response += "Content-Type: text/plain\r\n";
            response += "Content-Length: 2\r\n\r\nOK";
        }

        send(client_socket, response.c_str(), response.length(), 0);
        close(client_socket);
    }

    ssize_t parse_content_length(const std::string& headers) {
        std::string search = "Content-Length:";
        size_t pos = headers.find(search);
        if (pos == std::string::npos) return 0;
        pos += search.length();
        while (pos < headers.length() && isspace(headers[pos])) pos++;
        size_t end = headers.find("\r\n", pos);
        if (end == std::string::npos) end = headers.length();
        std::string value = headers.substr(pos, end - pos);
        try {
            return std::stoll(value);
        } catch (...) {
            return 0;
        }
    }

    std::string handle_solve_request(const std::string& body) {
        auto params = SimpleJSONParser::parseJson(body);

        std::string expression = params.count("expression") ? params["expression"] : "";
        std::string constraints_str = params.count("constraints") ? params["constraints"] : "[]";
        int display_limit = params.count("displayLimit") ? std::stoi(params["displayLimit"]) : 10;

        if (expression.empty()) {
            return create_error_response("Missing expression");
        }

        std::vector<std::string> constraints = SimpleJSONParser::parseArray(constraints_str);

        try {
            quant::EngineResult result = quant::solve_equation(expression, constraints, display_limit);

            std::string json_response = "{";
            json_response += "\"totalSolutions\":" + std::to_string(result.totalSolutions) + ",";
            json_response += "\"shownSolutions\":" + std::to_string(result.shownSolutions) + ",";
            json_response += "\"solutions\":" + SimpleJSONParser::arrayToJson(result.solutions);
            json_response += "}";

            std::string response = "HTTP/1.1 200 OK\r\n";
            response = addCORSHeaders(response);
            response += "Content-Type: application/json\r\n";
            response += "Content-Length: " + std::to_string(json_response.length()) + "\r\n\r\n";
            response += json_response;
            return response;
        } catch (const std::exception& e) {
            return create_error_response(std::string(e.what()));
        }
    }

    std::string create_error_response(const std::string& error_msg) {
        std::string json = "{\"error\":\"" + SimpleJSONParser::escape(error_msg) + "\"}";
        std::string response = "HTTP/1.1 400 Bad Request\r\n";
        response = addCORSHeaders(response);
        response += "Content-Type: application/json\r\n";
        response += "Content-Length: " + std::to_string(json.length()) + "\r\n\r\n";
        response += json;
        return response;
    }

    void parse_http_request(const std::string& request, std::string& method, std::string& path, std::string& http_version, std::string& body) {
        std::istringstream stream(request);
        stream >> method >> path >> http_version;

        size_t body_start = request.find("\r\n\r\n");
        if (body_start != std::string::npos) {
            body = request.substr(body_start + 4);
        }
    }
};

int main(int argc, char* argv[]) {
    char* port_env = std::getenv("PORT");
    int port = 8080;
    if (port_env) {
        port = std::stoi(port_env);
    } else if (argc > 1) {
        port = std::stoi(argv[1]);
    }

    std::cout << "Starting QuantSolve server on 0.0.0.0:" << port << std::endl;

    HTTPServer server(port);
    server.start();

    return 0;
}

