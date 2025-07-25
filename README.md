Скрипт позволяет автоматически установить XRay на Debian 12/Ubuntu по ssh

Скрипт находится в разработке, поэтому:
  - доступен для запуска только на windows;
  - установка возможна только под пользователем root
    
Как пользоваться?

1. При первом запуске будут запрошены логин, пароль и IP адрес сервера
2. Если на сервере не установлен XRay, то будет предложено его установить
3. После установки нажмите 1, чтобы добавить пользователя и получить конфиг. Конфиг выдается под одного пользователя, т.е., если вы собираетесь сидеть с телефона, компьютера и планшета, вам нужно сгенерировать трех пользователей
4. Вставить полученный конфиг в клиент, поддерживающий VLESS, например, nekoray
   На примере nekoray, сначала копируем:
   
   <img width="1083" height="77" alt="vless" src="https://github.com/user-attachments/assets/6c4c57fa-65f5-4fb1-b469-f1e9d1a6e67d" />
   
   Потом вставляем в клиент:
   
   <img width="337" height="103" alt="image" src="https://github.com/user-attachments/assets/243b5c19-359e-4a94-85b4-50262d7db159" />

   Конфиг можно вставить в любой VLESS клиент на любом устройстве

   Например, так выглядит nekoray
  <img width="1919" height="537" alt="image" src="https://github.com/user-attachments/assets/0ef621f9-5cf9-4c21-a411-810d1a2232ec" />

   просто нажимаем CTRL + V и у вас появляется строчка с подключением

   <img width="1919" height="221" alt="image" src="https://github.com/user-attachments/assets/86d96faa-7fd3-4720-b71f-333981f34137" />

    Для запуска нажимаем ПКП по строчке и выбираем запустить
   <img width="1375" height="205" alt="image" src="https://github.com/user-attachments/assets/2c35bc80-3ae0-4bf4-9367-62fc42119d86" />

  После чего нажимаем 2 галочки
  
  <img width="793" height="101" alt="image" src="https://github.com/user-attachments/assets/e02865f5-f059-4b2b-808f-b3f4a757af60" />

   Также nekoray н позволяет создать QR код, щелкнув ПКМ по строке подключения и нажав кнопку "Поделиться"

<img width="846" height="64" alt="image" src="https://github.com/user-attachments/assets/a5ec8cf1-fd00-4181-a26d-3c97d30525a5" />

Покажу как подключить VPN на IOS на примере клиента v2box:

1. Собственно, скачиваем v2box
2. Открываем, заходим в Configs снизу
<img width="400" height="200" alt="image" src="https://github.com/user-attachments/assets/ebd06974-f7e6-4daa-91bc-679344acf47e" />

3. Жмем на значок QR кода и сканируем QR, полученный из nekoray
<img width="300" height="200" alt="image" src="https://github.com/user-attachments/assets/b381694d-cfaf-4166-8497-82223ef278c3" />
   
4. Конфиг будет добавлен автоматически, вам нужно выбрать его и нажать Connect

   
Если вы разбираетесь в программировании и ООП, то прежде, чем критиковать мой код, уточню, я не разработчик
