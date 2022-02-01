## <p align="center">Телеграм бот</p>
### <p align="center">Aiogram StyleTransfer CycleGAN Webhook</p>

<img src='images/examples/main_screen.png' align="left" width=384>
<br>
## Telegram Bot
Для написания бота использовалась библиотека aiogram для построения асинхронной архитектуры.
Весь код в файле _bot.py_. В файле _keyboards.py_ находятся используемые клавиатуры и некоторые сообщения.

Функционал бота:
1. Перенос стиля
   * Для работы необходимо отправить боту сначала фотографию стиля, а затем фотографию, на которую необходимо перенести стиль.
   * Есть возможность выбрать картинку стиля у бота. Предлагается на выбор 6 разных картин художников
2. Использовать CycleGAN
   * Превратить лошадь в зебру
   * Превратить зебру в лошадь
3. Бот может отправить примеры, получаемые в результате работы 3 вышеназванных алгоритмов
4. Перенаправить на данный репозиторий, чтобы ознакомиться с проектом.

__Особенности__:
1. Запоминание пользователей и отправляемых ими фотографий реализовано через словарь, в котором сохраняются объекты класса для каждого пользователя, начавшего общение с ботом. В объекте класса хранится id пользователя, название выбранного алгоритма и в случае использования style transfer сохраняется фотография стиля. Фотография контента и фото для CycleGAN не сохраняются, а передаются сразу в пайплайн выбранного алгоритма.
2. Бот отдает фотографию в том же разрешении, что и получил от пользователя. Так как для моделей необходимы квадратные фотографии, то используются паддинги
   * StyleTranfer: сжатие до 250 пикселей. Увеличение показателя улучшает получаемое качество, однако, увеличивает время инференса.
   * CycleGAN: сжатие до 512 пикселей
3. Алгоритмы запускаются в отдельном потоке с помощью threading.Thread
4. Длительность работы:
   * StyleTrasfer: в среднем 4 минуты
   * CycleGAN: в среднем 10 секунд

## StyleTransfer
Для переноса стилей были выполнены следующие действия:
1. Взята предобученная модель VGG19 с весами ImageNet
2. Модель была дополнительно доучена на датасете Caltech 101, содержащим 101 категорию данных и 8677 картинок. Код обучения представлен в файле _model_nst/train_vgg19.ipynb_
3. Из обученной модели сохранены веса только нужных слоев (первые 11) в файл _models_wts/vgg19.pth_. При обучении использовались алгоритмы семплирования и аугментации исходных изображений. Подобранное количество эпох и других мета-параметров позволило добиться хорошей "сходимости" модели
4. Для переноса стилей использован классический алгоритм Гатиса, который подразумевает итеративное изменение входной картинки на основе разницы между style и content картинками
5. Дообучение модели осуществлено в Google Colab Pro на GPU (Tesla P100)

## CycleGAN
Для использования CycleGAN был взят код junyanz [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
Исходный код дает возможность использовать CycleGAN и pix2pix моделей в различных режимах на различных датасетах

Для использования такого большого проекта в собственных нуждах были выполнены следующие действия:
1. Взята архитектура только CycleGAN в режиме для теста, чтобы генерировать изображения только в одну сторону (папка _models_)
    * Убраны лишние функции
    * Переделан вход модели так, чтобы она принимала не датасет, а сразу картинки
    * Модель сразу отдает результат генерации, а не пускает его дальше по пайплайну
2. Пред и пост обработка фотографий делается собственными функциями
3. Взяты параметры для запуска скрипта в тестовом режиме (папка _options_)
4. Код переработан так, чтобы не использовать датасеты, также удалены любые функции связанные с ними.
5. В папке _scripts_ находится 1 скрипт для загрузки весов натренированного CycleGAN. Для загрузки необходимо перейти в папку с CycleGAN и запустить скрипт с выбранными весами. Я использовал horse2zebra и zebra2horse. Веса загружаются в папку _checkpoints_
```
$ cd model_cyclegan
$ bash ./scripts/download_cyclegan_model.sh horse2zebra
```
6. Был переделан скрипт test.py таким образом, чтобы создать модель со стандартными параметрами и сохранить ее полностью в файлы pth для дальнейшего использования ботом. Сделано это для того, чтобы отпала необходимость сложного создания модели при работе бота. Модели сохраняются в папку _models_wts_. Скрипт test.py запускается следующим образом:
```
$ cd model_cyclegan
$ python test.py --name horse2zebra_pretrained --model test --no_dropout --gpu_ids -1
```
gpu_ids равняется -1, так как подразумевается использование модели только на CPU

## VPS
Бот был задеплоен на внешний VPS c "белым" IP-адресом.
Установленная ОС - Debian 11.2

Для работы бота в режиме __webhook__ на сторонних хостингах необходимо туннелирование localhost-а.
Задача решается использованием утилит типа ngrok и ей подобных. При этом, использование custom-ного постоянного имени поддомена
является желательным для повышения автономности работы бота. Данный функционал в случае с ngrok является платным, однако,
существует бесплатные альтернативы и решения. В частности, я использовал решение от localtunnel.me
 
Настройки телеграм бота, в том числе, его токен и параметры для __webhook__ хранятся в файле .env:
* API_TOKEN = '2507456574:ileo_FAKE_FAKE_FAKE_hr51k2_99j'
* WEBHOOK_HOST='your_sub_domain.loca.lt'
* WEBHOOK_PORT = 443
* WEBHOOK_URL_PATH = ''
* WEBAPP_HOST=0.0.0.0
* WEBAPP_PORT=5000

## requirements.txt
Все вычисления происходят на CPU. Перечень основных пакетов и их версии:
```
python==3.9.2
aiogram==2.18
Pillow==9.0.0
torch==1.10.1
torchvision==0.11.2
```

## Структура репозитория
| | | Описание файлов и папок |
| --- | --- | --- |
| images | | |
|  | examples | Примеры работы модели |
|  | styles | Варианты картинок для стиля |
| model_cyclegan | | |
|  | checkpoints | Веса, используемые для создания СycleGAN |
|  | models | Архитектура СycleGAN |
|  | options | Параметры для создания СycleGAN |
|  | scripts | Внутри скрипт для загрузки весов CycleGAN |
|  | CycleGAN.py | Пайплайн для СycleGAN |
|  | test.py | Скрипт для создания моделей с загруженными весами|
| model_nst | | |
|  | StyleTransfer.py | Модель и пайплайн для StyleTransfer |
|  | train_vgg19.py | Дообучение модели VGG19 |
| models_wts | | Веса для всех моделей |
| bot.py | | Код телеграм бота |
| keyboards.py | | Клавиатуры и сообщения для бота |
| image_processing.py | | Запуск пайплайнов для NST и CycleGAN |
| requirements.txt | | Необходимые пакеты |
