import os


class file_memory:

    def __init__(self):
        self.__path = "/mem.txt"
        self.__object = ""
        self.__dataset = ""

    def save_current_img(self, object, dataset, img):
        with open(self.__path, 'a', encoding='utf-8') as f:
            f.write(str(object)+","+str(dataset)+","+str(img)+'\n')

    def get_all(self):
        try:
            with open(self.__path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            open(self.__path, 'w+', encoding='utf-8')
            return []

    def is_img_already_processed(self, object, dataset, img):

        processed_imgs = self.get_all()

        line_to_find = str(object)+","+str(dataset)+","+str(img)+'\n'

        return line_to_find in processed_imgs

    def get_latest_img(self):
        with open(self.__path, 'r', encoding='utf-8') as f:
            data = f.readlines()
            data = data[-1]

        data = data.split(sep=',')

        return data[0], data[1], data[2]
