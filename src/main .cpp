#include <Arduino.h>
#include <math.h>


#define STEP 3
#define DIR 4
#define EN 5

bool running = false;
int delay_us = 0;


void setup() {
    Serial.begin(115200);


    pinMode(DIR, OUTPUT);
    pinMode(EN, OUTPUT);
    pinMode(STEP, OUTPUT);

    digitalWrite(DIR, HIGH);
}

void loop() {
    if (Serial.available()) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();

        if (cmd == "Stop") {
            digitalWrite(EN , HIGH);
        }
        else if (cmd.startsWith("Delay:")) {
            digitalWrite(EN, LOW);
            Serial.println("Delay empfangen!");

            String data = cmd.substring(6);

            while (data.length() > 0) {
                int komma = data.indexOf(',');
                if (komma == -1) {
                    delay_us = data.toInt();
                    data = "";
                } else {
                    delay_us = data.substring(0, komma).toInt();
                    data = data.substring(komma + 1);
                }


                    digitalWrite( STEP , HIGH);
                    delayMicroseconds(delay_us/2);
                    digitalWrite( STEP , LOW);
                    delayMicroseconds(delay_us/2);

                }
            running = true;
            }
        }
    if (running) {
        digitalWrite(STEP , HIGH);
        delayMicroseconds(delay_us/2);
        digitalWrite(STEP , LOW);
        delayMicroseconds(delay_us/2);
    }
    }

