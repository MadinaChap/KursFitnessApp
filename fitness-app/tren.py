from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from datetime import datetime, timedelta
import random

directory_tr = './trenirovki'
directory_yp = './yprazhnenia'
directory_gr = './grafics'
directory_cal = './data_for_kalendar'

filename_weight = 'weight.txt'
filename_time = 'time.txt'

global_time = 0
global_name = ""

app = Flask(__name__)

#Запись тренировки из файла
def trenirovka_in_file(filename):
    flag = 0 #Проверка того, необходимо ли изменить тренировку
    with open(os.path.join(directory_tr, filename), 'r', encoding='utf-8') as f:
        exercises = []
        lines = f.read().split('\n')
        name, count_podh = lines[0], lines[1]
        for line in lines[2:]:
            if line:
                file, time = line.split(' ')
                fil_path = os.path.join(directory_yp, file)
                if os.path.exists(fil_path):
                    with open(fil_path, 'r', encoding='utf-8') as f:
                        stroki = f.read().split('\n')
                        name_ypr, description, image_path = stroki[0], stroki[1], stroki[2]
                        image_path = "/static/yprazhnenia/" + image_path
                        exercises.append({
                            'file': file,
                            'time': time,
                            'name_ypr': name_ypr,
                            'description': description,
                            'image_path': image_path
                        })
                else:
                    flag = 1
                    lines.pop(lines.index(line))
        exercise_content = {
            'name': name,
            'count_podh': count_podh,
            'exercises': exercises
        }
        if flag == 1:
            with open(os.path.join(directory_tr, filename), 'w', encoding='utf-8') as f:
                for line in lines[:-1]:
                    f.write(line + '\n')
                f.write(lines[-1])

        return exercise_content

    
#Открытие списка тренировок
@app.route('/', methods = ['GET', 'POST'])
def home():
    files_content = {}
    for filename in os.listdir(directory_tr):
        with open(os.path.join(directory_tr, filename), 'r', encoding='utf-8') as f:
                lines = f.read().split('\n')
                name = lines[0]
                files_content[filename] = {
                    'name': name,
                }
    return render_template('indextr.html',files_content = files_content)
    
#Просмотр тренировки
@app.route('/view/<filename>', methods = ['GET'])
def view_trenirovka(filename):
    exercise_content = trenirovka_in_file(filename)
    return render_template('viewingtr.html', filename = filename, exercise_content = exercise_content)

#Возвращение на домашнюю страницу
@app.route('/back', methods = ['POST'])
def back_home():
    return redirect(url_for('home'))

#Редактирование тренировок
@app.route('/edit_trenirovki/<filename>', methods = ['GET', 'POST'])
def editor_trenirovki(filename):
    with open(os.path.join(directory_tr, filename), 'r', encoding='utf-8') as f:
        exercises = []
        lines = f.read().split('\n')
        name, count_podh = lines[0], lines[1]
        number_of_line = 2
        for line in lines[2:]:
            file, time = line.split(' ')
            with open(os.path.join(directory_yp, file), 'r', encoding='utf-8') as f:
                stroki = f.read().split('\n')
                name_ypr = stroki[0]
                exercises.append ({
                    'time': time,
                    'name_ypr': name_ypr,
                    'file': file,
                    'number_of_line': number_of_line
                })
            number_of_line=number_of_line+1
        exercise_content = {
            'name': name,
            'count_podh': count_podh,
            'exercises': exercises
        }
    print(exercise_content)
    exercise = {}
    for name_of_file in os.listdir(directory_yp):
        if name_of_file.endswith('.txt'):
            with open(os.path.join(directory_yp, name_of_file), 'r', encoding='utf-8') as f:
                name = f.readline().strip()
                exercise[name_of_file] = {
                    'name': name,
                    'name_of_file': name_of_file
                }
    return render_template('edittr.html', filename = filename, exercise_content = exercise_content, exercise = exercise)

#Сохранение тренировки
@app.route('/save_tr/<filename>', methods=['POST'])
def save_trenirovka(filename):
    name = request.form['name']
    count_podh = request.form['count_podh']
    files = request.form.getlist('file')
    times = request.form.getlist('time')

    with open(os.path.join(directory_tr, filename), 'w', encoding='utf-8') as f:
        f.write(f"{name}\n")
        f.write(f"{count_podh}")
        for i in range(0,len(files)):
            f.write("\n")
            f.write(f"{files[i]} {times[i]}")
    return redirect(url_for('view_trenirovka', filename=filename))


#удаление упражнения из тренировки
@app.route('/delete_tr/<filename>/<number_of_line>', methods = ['GET'])
def delete_trenirovka(filename, number_of_line):
    with open(os.path.join(directory_tr, filename), 'r', encoding='utf-8') as f:
        lines = f.readlines()
    del lines[int(number_of_line)]
    if int(number_of_line)-1 == len(lines) - 1:
        lines[-1] = lines[-1][:-1]
        
    with open(os.path.join(directory_tr, filename), 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return redirect(url_for('editor_trenirovki', filename=filename))

#Добавление упражнения в тренировку
@app.route('/add_exercise/<filename>/<name_of_file>', methods=['POST'])
def add_exercise(filename,name_of_file):
    name = request.form['name']
    count_podh = request.form['count_podh']
    files = request.form.getlist('file')
    times = request.form.getlist('time')

    with open(os.path.join(directory_tr, filename), 'w', encoding='utf-8') as f:
        f.write(f"{name}\n")
        f.write(f"{count_podh}")
        for i in range(0,len(files)):
            f.write("\n")
            f.write(f"{files[i]} {times[i]}")

    with open(os.path.join(directory_tr, filename), 'a', encoding='utf-8') as f:
        f.write(f'\n{name_of_file} 10')
    return redirect(url_for('editor_trenirovki', filename=filename))

#Добавление тренировок
@app.route('/create_trenirovka', methods = ['GET'])
def create_tr():
    files = [f for f in os.listdir(directory_tr) if f.endswith('.txt')]
    if files:
        fil = files[-1]
        last_number = int(''.join(filter(str.isdigit, fil)))
        tek_number = last_number + 1
        new_filename = f"trenirovka{tek_number}.txt"
    else:
        new_filename = "trenirovka0.txt"
    with open(os.path.join(directory_tr, new_filename), 'w', encoding='utf-8') as f:
        f.write('\n')
    return redirect(url_for('editor_trenirovki', filename=new_filename))

#Удаление тренировок
@app.route('/delete_trenirovka/<filename>', methods = ['GET'])
def del_tr(filename):
    os.remove(os.path.join(directory_tr, filename))
    return redirect(url_for('home'))

#Начать тренировку
@app.route('/start_trenirovka/<filename>/<podhod>/<number_exercise>', methods = ['GET'])
def start_tren(filename, podhod, number_exercise):
    global global_time, global_name
    random_number = random.randint(1, 50)
    with open('phrases.txt', 'r', encoding='utf-8') as file:
        lin = file.readlines()
    phrasa = lin[random_number - 1]
    podhod = int(podhod)
    podhod_view = podhod
    number_exercise = int(number_exercise)
    trenirovka = trenirovka_in_file(filename)
    exercise = trenirovka['exercises'][number_exercise - 1]
    if (podhod == 1) and (number_exercise == 1):
        global_name = trenirovka['name']
        global_time = 0
    if not( podhod > int(trenirovka['count_podh'])):
        global_time  = global_time + int(exercise['time'])
    if(number_exercise<len(trenirovka['exercises'])):
        number_exercise = number_exercise + 1
        return render_template('starttr.html', filename = filename, podhod = podhod, number_exercise = number_exercise, exercise = exercise, trenirovka = trenirovka, podhod_view =podhod_view, phrasa = phrasa )
    else:
        if (podhod)<int(trenirovka['count_podh']):
            number_exercise = 1
            podhod = podhod + 1
            return render_template('starttr.html', filename = filename, podhod = podhod, number_exercise = number_exercise, exercise = exercise, trenirovka = trenirovka, podhod_view =podhod_view, phrasa = phrasa )
        else:
            if podhod > int(trenirovka['count_podh']):
                return redirect(url_for('end_tr'))
            else:
                podhod = podhod + 1
                return render_template('starttr.html', filename = filename, podhod = podhod, number_exercise = number_exercise, exercise = exercise, trenirovka = trenirovka, podhod_view =podhod_view, phrasa = phrasa)

#Сохранение данных в конце тренировки
@app.route('/end_trenirovka', methods = ['GET'])
def end_tr():
    global global_time, global_name
    today = datetime.now()
    date_fil = today.strftime("%m.%Y")+".txt"
    number_str = today.day
    if not(os.path.isfile(os.path.join(directory_cal, date_fil))):
        first_day = datetime(today.year, today.month, 1)
        last_day = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
        with open(os.path.join(directory_cal, date_fil), 'w', encoding='utf-8') as file:
            file.write(f"date;type;kg;name;time;\n")
            while first_day <= last_day:
                if first_day.day == today.day:
                    file.write(f"{first_day.day}.{first_day.month}.{first_day.year};true;{-1};{global_name};{str(global_time)}\n")
                else:
                    file.write(f"{first_day.day}.{first_day.month}.{first_day.year};false;{-1}\n")
                first_day += timedelta(days=1)
    else: 
        with open(os.path.join(directory_cal, date_fil), 'r', encoding='utf-8') as f:
            stroki = f.readlines()
            print(stroki[number_str])
            data, type, weight, *_ = stroki[number_str].split(";")
            if (type == "true"):
                stroki[number_str] = stroki[number_str].rstrip('\n') + ";" + global_name + ";" + str(global_time) + "\n"
            else:
                stroki[number_str] = f"{data};true;{weight}" + ";" + global_name + ";" + str(global_time) + "\n"
            with open(os.path.join(directory_cal, date_fil), 'w', encoding='utf-8') as f:
                    f.writelines(stroki)
    date = today.strftime("%d.%m.%Y")
    with open(os.path.join(directory_gr, filename_time), 'a', encoding='utf-8') as f:
            f.write(f"\n{date};{global_time}")
    return render_template('endtr.html')

#Сохранение данных о весе
@app.route('/add_weight', methods = ['POST', 'GET'])
def addweight():
    if request.method == 'POST':
        weight = request.form['weight']
        today = datetime.now()
        date = today.strftime("%d.%m.%Y")
        date_fil = today.strftime("%m.%Y")+".txt"
        number_str = today.day
        with open(os.path.join(directory_gr, filename_weight), 'a', encoding='utf-8') as f:
            f.write(f"\n{date};{weight}")
        with open(os.path.join(directory_cal, date_fil), 'r', encoding='utf-8') as f:
            stroki = f.readlines()
            data, type, filweight, *values = stroki[number_str].split(";")
            stroki[number_str] = ";".join([data, type, weight] + values)
            with open(os.path.join(directory_cal, date_fil), 'w', encoding='utf-8') as f:
                f.writelines(stroki)
            return redirect(url_for('home'))
    return render_template('addweight.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)