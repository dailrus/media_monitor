

#include <GyverOLED.h>
String strData = "";
boolean recievedFlag;

// примеры:
GyverOLED<SSD1306_128x32, OLED_BUFFER> oled;


void setup() {
  Serial.begin(9600);
  oled.init();  // инициализация

  oled.clear();   // очистить дисплей (или буфер)
  oled.update();  // обновить. Только для режима с буфером! OLED_BUFFER

  // --------------------------
  oled.home();   // курсор в (пиксель X, строка Y)
  oled.setScale(1);
  oled.autoPrintln(true); 
  oled.print("Waiting for \n\r Python script...");
  oled.update();
  delay(2000);
  oled.home();
  oled.textMode(BUF_ADD);


  // --------------------------
  // СЕРВИС
  //oled.setContrast(10);   // яркость 0..15
  //oled.setPower(true);    // true/false - включить/выключить дисплей
  //oled.flipH(true);       // true/false - отзеркалить по горизонтали
  //oled.flipV(true);       // true/false - отзеркалить по вертикали
  //oled.isEnd();           // возвращает true, если дисплей "кончился" - при побуквенном выводе
  Serial.begin(19200);
  oled.update();
}

void loop() {
   while (Serial.available() > 0) {         // ПОКА есть что то на вход    
    strData += (char)Serial.read();        // забиваем строку принятыми данными
    recievedFlag = true;                   // поднять флаг что получили данные
    delay(2);                              // ЗАДЕРЖКА. Без неё работает некорректно!
  }
  if (recievedFlag) {                      // если данные получены
    oled.home();
    oled.clear();
    oled.print(strData);               // вывести
    oled.update();
    strData = "";                          // очистить
    recievedFlag = false;                  // опустить флаг
  } 
}
