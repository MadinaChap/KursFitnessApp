import os

class exercise:
    def __init__(self, name, description, image_name, video_name):
        self.name = name
        self.description = description
        self.image_name = image_name
        self.video_name = video_name
        directory = './yprazhnenia'
        files = os.listdir(directory)
        if files:
            #sorted_files = sorted(files,key=lambda x: int(''.join(filter(str.isdigit, x))))
            fil = files[-1]
            last_number =  int(''.join(filter(str.isdigit, fil)))
            tek_number = last_number + 1
            self.file_name = f"{directory}/file{tek_number}.txt"
        else:
            self.file_name = "./yprazhnenia/file0.txt"

    def print_exercise(self):
        with open(self.file_name, 'w') as f:
            f.write(self.name + '\n' + self.description + '\n' + self.image_name + '\n' + self.video_name)

    def change_description(self, name):
        self.description = name
    
    def change_name(self, name):
        self.name = name
    
    def change_image(self, name):
        self.image_name = name

    def change_video(self, name):
        self.change_video = name