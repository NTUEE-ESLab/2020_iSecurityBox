/*
 * Copyright (c) 2006-2020 Arm Limited and affiliates.
 * SPDX-License-Identifier: Apache-2.0
 */
#include "mbed.h"
#include "MFRC522.h"
#include "Servo.h"
#include "rfid.h"
#include "Websocket.h"
#include <time.h>
#include <string>
#include <iostream>

using namespace std;

#define WIFI_IDW0XX1    2

#if (defined(TARGET_DISCO_L475VG_IOT01A) || defined(TARGET_DISCO_F413ZH))
#include "ISM43362Interface.h"
ISM43362Interface wifi(/*MBED_CONF_APP_WIFI_SPI_MOSI, MBED_CONF_APP_WIFI_SPI_MISO, MBED_CONF_APP_WIFI_SPI_SCLK, MBED_CONF_APP_WIFI_SPI_NSS, MBED_CONF_APP_WIFI_RESET, MBED_CONF_APP_WIFI_DATAREADY, MBED_CONF_APP_WIFI_WAKEUP,*/ false);

#else // External WiFi modules

#if MBED_CONF_APP_WIFI_SHIELD == WIFI_IDW0XX1
#include "SpwfSAInterface.h"
SpwfSAInterface wifi(MBED_CONF_APP_WIFI_TX, MBED_CONF_APP_WIFI_RX);
#endif // MBED_CONF_APP_WIFI_SHIELD == WIFI_IDW0XX1

#endif

MFRC522 *mfrc522 = new MFRC522(D11, D12, D13, D10, D8);
PwmOut servo(PWM_OUT);
bool idSent = false;
char recv_buffer[1024];

const char *sec2str(nsapi_security_t sec)
{
    switch (sec) {
        case NSAPI_SECURITY_NONE:
            return "None";
        case NSAPI_SECURITY_WEP:
            return "WEP";
        case NSAPI_SECURITY_WPA:
            return "WPA";
        case NSAPI_SECURITY_WPA2:
            return "WPA2";
        case NSAPI_SECURITY_WPA_WPA2:
            return "WPA/WPA2";
        case NSAPI_SECURITY_UNKNOWN:
        default:
            return "Unknown";
    }
}

void lock(clock_t clk, Servo svo){
    svo.write(0.5);
}

void unlock(clock_t clk, Servo svo){
    svo.write(0);
}

int main()
{
    printf("\nConnecting to %s...\n", MBED_CONF_APP_WIFI_SSID);
    int ret = wifi.connect(MBED_CONF_APP_WIFI_SSID, MBED_CONF_APP_WIFI_PASSWORD, NSAPI_SECURITY_WPA_WPA2);
    if (ret != 0) {
        printf("\nConnection error\n");
        return -1;
    }

    printf("Success\n\n");
    printf("MAC: %s\n", wifi.get_mac_address());
    printf("IP: %s\n", wifi.get_ip_address());
    printf("Netmask: %s\n", wifi.get_netmask());
    printf("Gateway: %s\n", wifi.get_gateway());
    printf("RSSI: %d\n\n", wifi.get_rssi());
    clock_t t = clock();
    int buffer_sent;
    //servo.position(0);
    servo.pulsewidth(0.0025f); // close
    while(1)
    {
        bool isConnected, isRead;
        char *addr = (char *)"ws://esys-final.herokuapp.com/0.0.0.0:80";
        Websocket websocket(addr, &wifi);
        /*
        isConnected = websocket.connect();
        if(!isConnected){
            cout << "Error Connecting... " << endl;
            continue;
        }
        else cout << "connected!!" << endl;
        */
        RFID_Reader rfidReader(mfrc522);
        printf("Scanning RFID...\n");
        printf("cycles per sec: %d\n", CLOCKS_PER_SEC);
        websocket.read(recv_buffer);
        cout << recv_buffer << endl;
        memset(recv_buffer, 0, sizeof(recv_buffer));
        while(1)
        {
            if(idSent){
                /*
                isRead = websocket.read(recv_buffer);
                if(!isRead)
                {
                    cout << "Receiving Error!!!" << endl;
                    cout << "Disconnecting" << endl;
                    break;
                }
                else
                {
                    cout << recv_buffer << endl;
                    memset(recv_buffer, 0, sizeof(recv_buffer));
                    servo.position(1);
                    idSent = false;
                }
                */
            }
            else
            {
                if(rfidReader.read())
                {
                    printf("New card detected: \n");
                    t = clock();
                    printf("Time: %d\n", t);
                    printf("Card ID: ");
                    char id[2 * rfidReader.getSize()];
                    rfidReader.getCharID(id);
                    for(int i = 0; i < 8; ++i) printf("%c", id[i]);
                    printf("\n");
                    buffer_sent = websocket.send(id);
                    cout << "Sending: " << buffer_sent;
                    if(buffer_sent <= 0)
                    {
                        cout << "Sending Error!!!" << endl;
                        cout << "Disconnecting" << endl;
                        break;
                    }
                    cout << "ID Sending..." << endl;
                    //idSent = true;
                    servo.pulsewidth(0.0005f); // open
                }
            }
            if(float(clock() - t)/CLOCKS_PER_SEC > 5){
                printf("time expired: %d\n", clock());
                t = clock();
                /*
                if(idSent)
                {
                    cout << "Sending Timeout !!!" << endl;
                    cout << "Disconnecting... " << endl;
                    idSent = false;
                    break;
                }
                */
                servo.pulsewidth(0.0025f); // close
            }
        }
        websocket.close();
    }
    return 0;
}
