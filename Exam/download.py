from urllib.request import urlretrieve, urlopen
import os


DOWNLOAD_DIRECTORY = os.getcwd() + '\\download\\'  # Папка, в которую скачиваются файлы
CHARSET = 'UTF-8'  # Кодировка файла


def write_file(path: str, text: str):  # Записываем скачанный файл в одноименный файл в папку /download
    if text is not None:
        file = open(path, 'w')
        file.write(text)
        file.close()


def download_file():
    while True:
        url = str(input("Введите url: "))
        try:
            text = urlopen(url).read().decode(CHARSET)
            text = text.replace("\r\n", "")
            if text != "":
                with open(DOWNLOAD_DIRECTORY + url.split('/')[-1], "w") as f:
                    f.write(text)
                    f.close()
                print("Файл скачан")
            else:
                print("Такого файла не существует")
        except ValueError:
            print("Неверный формат URL")


if __name__ == "__main__":
    download_file()
