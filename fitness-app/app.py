from flask import Flask, request, render_template, redirect, url_for
import os
from class_upr import exercise

app = Flask(__name__, static_folder='yprazhnenia/image')

#Вывод всех упражнений 
@app.route('/', methods=['GET', 'POST'])
def home():
    files_content = {}
    for filename in os.listdir('./yprazhnenia'):
        if filename.endswith('.txt'):
            with open(os.path.join('./yprazhnenia', filename), 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines()]
                if all(line for line in lines): 
                    name, description, image_path = lines[0], lines[1], lines[2] #Добавить видео?
                    files_content[filename] = {
                        'name': name,
                        'description': description,
                        'image_path': image_path
                    }

    return render_template('index.html', files_content=files_content)

#Сохранение картинки
@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            filename = photo.filename
            photo.save(os.path.join('yprazhnenia/image', filename))
            return "Фотография успешно загружена!"
        else:
            return "Ошибка: Файл не выбран."
    else:
        return "Ошибка: Файл не найден."

#Открытие упражнения для редактирования
@app.route('/edit/<filename>', methods=['GET'])
def edit_exercise(filename):
    with open(os.path.join('./yprazhnenia', filename), 'r', encoding='utf-8') as f:
        lines = f.read().split('\n') #Добавить видео?
        name, description, image_path = lines[0], lines[1], lines[2] 
        ex_name = name
        exercise_content = {
            'name': name,
            'description': description,
            'image_path': image_path
        }
    
    return render_template('edit.html', filename = filename, ex_name = ex_name, exercise_content=exercise_content)

#Сохранение упражнения
@app.route('/save/<filename>', methods=['POST'])
def save_exercise(filename):
    name = request.form['name']
    description = request.form['description']
    image = request.files['image']
    if os.path.exists(os.path.join('yprazhnenia/image', filename.replace('.txt', '.jpg'))):
        os.remove(os.path.join('yprazhnenia/image', filename.replace('.txt', '.jpg')))
    image.save(os.path.join('yprazhnenia/image', image.filename))

    with open(os.path.join('./yprazhnenia', filename), 'w', encoding='utf-8') as f:
        image.filename = './' + image.filename
        f.write(f"{name}\n{description}\n{image.filename}")

    return redirect(url_for('home'))

#удаление упражнения
@app.route('/delete/<filename>', methods=['POST'])
def delete_exercise(filename):
    if os.path.exists(os.path.join('yprazhnenia/image', filename.replace('.txt', '.jpg'))):
        os.remove(os.path.join('yprazhnenia/image', filename.replace('.txt', '.jpg')))
    os.remove(os.path.join('./yprazhnenia', filename))

    return redirect(url_for('home'))

#создание упражнения
@app.route('/create', methods=['GET'])
def add_exercise():
    directory = './yprazhnenia'
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    print(files)
    if files:
        fil = files[-1]
        print(fil)
        last_number = int(''.join(filter(str.isdigit, fil)))
        print(last_number)
        tek_number = last_number + 1
        print(tek_number)
        new_filename = f"file{tek_number}.txt"
        print(new_filename)
    else:
        new_filename = "file0.txt"
    with open(os.path.join(directory, new_filename), 'w', encoding='utf-8') as f:
        f.write('\n\n')
    return redirect(url_for('edit_exercise', filename=new_filename))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
