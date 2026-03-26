#include <stdio.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

int main() {
    WSADATA wsa;
    SOCKET s, new_socket;
    struct sockaddr_in server, client;
    int c;
    char buffer[4096] = {0};

    printf("[C] Initializez serverul...\n");
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) return 1;

    s = socket(AF_INET, SOCK_STREAM, 0);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(12345);

    if (bind(s, (struct sockaddr *)&server, sizeof(server)) == SOCKET_ERROR) {
        printf("[C] Eroare la BIND! Portul e ocupat.\n");
        return 1;
    }
    
    listen(s, 3);
    printf("[C] Astept date pe portul 12345...\n");

    c = sizeof(struct sockaddr_in);
    while((new_socket = accept(s, (struct sockaddr *)&client, &c)) != INVALID_SOCKET) {
        recv(new_socket, buffer, 4096, 0);
        printf("\n[C] Am primit date:\n%s\n", buffer);
        
        FILE *f = fopen("iesire.html", "w");
        if (f) { fprintf(f, "%s", buffer); fclose(f); }
        
        memset(buffer, 0, 4096);
        closesocket(new_socket);
    }

    WSACleanup();
    return 0;
}