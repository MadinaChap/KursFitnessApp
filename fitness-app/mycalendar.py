from flask import Flask, render_template, redirect, url_for
from datetime import datetime, timedelta
import os
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

directory = './data_for_kalendar'
directory_gr = './grafics'

@app.route("/",methods = ['GET'])
def home():
    return render_template('analys.html')
#функция генерации календаря
def generate_calendar(year, month, filename):

    dates = []
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = lines[1:]
        for line in lines:
            data, type, *_ = line.split(";")
            file_day, *_ = map(int, data.split(".")) 
            dates.append({
                    'day': file_day,
                    'type': type
                })
    
    calendar = []
    firstday = datetime(year, month, 1)
    while firstday.weekday() != 0:
        firstday -= timedelta(days=1)

    lastday = datetime(year, month + 1, 1) - timedelta(days=1)

    for _  in range(6):
        week = []
        for _ in range(7):
            if firstday.month == month:
                if firstday <= lastday:
                    i = firstday.day
                    week.append(dates[i-1])
                else:
                    week.append(None)  # Добавляем None для дат, которые выходят за пределы месяца
            else:
                week.append(None)  # Добавляем None для дат, не относящихся к текущему месяцу
            firstday += timedelta(days=1)
        calendar.append(week)
    return calendar
 
@app.route('/<filename>/<cal_date>', methods = ['GET'])
def calendar(cal_date,filename):
    #Иницилизация переменных
    cal_date = int(cal_date)
    content = {}
    tren = []
    month, year = map(int, filename.split('.')[:2])
    flag = 1
    #Создание файла, если такого нет
    if not(os.path.isfile(os.path.join(directory, filename))):
        flag = 0
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as file:
            file.write(f"date;type;kg;name;time;\n")
            while first_day <= last_day:
                file.write(f"{first_day.day}.{first_day.month}.{first_day.year};false;{-1}\n")
                first_day += timedelta(days=1)

    #Создание календаря
    calendar = generate_calendar(year, month, filename)

    #Формирование данных
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
        line = f.readlines()
    for number in range(1,len(line)-1):
        line[number].split(";")
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
         for i, line in enumerate(f):
            if i == cal_date:
                list = line.strip().split(";")
                if list[2]=="-1":
                    weight = "Нет данных о весе"
                else:
                    weight = list[2]
                if(len(list)==2):
                    content = {
                    'date': list[0],
                    'type': list[1],
                    'weight': weight }

                else:
                    j = 3
                    while( j <len(list)-1):
                        tren.append({
                            'name': list[j],
                            'time': list[j+1]
                        })
                        j = j+2
                    content = {
                        'date': list[0],
                        'type': list[1],
                        'weight': weight,
                        'tren': tren
                    }
    if flag == 0:
        os.remove(os.path.join(directory, filename))
    return render_template('calendar.html', year=year, month=month, calendar=calendar,content = content, cal_date = cal_date,filename = filename)

@app.route("/left/<filename>", methods = ['GET'])
def return_left(filename):
    month, year = map(int, filename.split('.')[:2])
    date = datetime(year, month, 1)
    next_date = date - timedelta(days=2)
    next_month = next_date.month
    next_year = next_date.year
    next_month_str = f"{next_month:02d}"
    next_year_str = f"{next_year}"
    next_filename = f"{next_month_str}.{next_year_str}.txt"
    return redirect(url_for('calendar', filename=next_filename, cal_date = 1))

@app.route("/right/<filename>", methods = ['GET'])
def return_right(filename):
    month, year = map(int, filename.split('.')[:2])
    date = datetime(year, month, 1)
    next_date = date + timedelta(days=32)
    next_month = next_date.month
    next_year = next_date.year
    next_month_str = f"{next_month:02d}"
    next_year_str = f"{next_year}"
    next_filename = f"{next_month_str}.{next_year_str}.txt"
    return redirect(url_for('calendar', filename=next_filename, cal_date = 1))

@app.route("/home", methods = ['GET'])
def return_home():
    return redirect(url_for('home'))

@app.route("/viewing_calendar", methods = ['GET'])
def view_calendar():
    today = datetime.now()
    day = today.day
    filename = today.strftime("%m.%Y")+".txt"
    return redirect(url_for('calendar', filename = filename, cal_date = day))

@app.route("/viewing_grafics/", methods = ['GET'])
def view_grafic():
    data = pd.read_csv('./grafics/time.txt', sep=';', header=0, names=['date', 'time'])
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y', errors='coerce')
    print(data['time'])
    data['time'] = data['time'].astype(int)
    data = data.groupby('date').sum().reset_index()
    data = data.sort_values('date')
    last_10_records = data.tail(30)

    print(last_10_records)
    plt.figure(figsize=(10, 6))
    plt.plot(last_10_records['date'], last_10_records['time'], marker='o') 
    plt.title('Время тренировок')
    plt.xlabel('Дата')
    plt.ylabel('Время, с')
    plt.grid(True)
    plt.savefig('static/grafics/time.png')  
    data = pd.read_csv('./grafics/weight.txt', sep=';', header=0, names=['date', 'weight'])
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y', errors='coerce')
    data['weight'] = data['weight'].astype(int)
    data = data.sort_values('date')
    last_10_records = data.tail(30)
    plt.figure(figsize=(10, 6))
    plt.plot(last_10_records['date'], last_10_records['weight'], marker='o') 
    plt.title('Данные о весе')
    plt.xlabel('Дата')
    plt.ylabel('Вес, кг')
    plt.grid(True)
    plt.savefig('static/grafics/weight.png')
    return render_template('grafics.html', path_to_time = 'grafics/time.png')

@app.route("/left_time/<value>", methods = ['GET'])
def lefttime_grafic(value):
    value = int(value)
    with open(os.path.join(directory_gr, 'time.txt'), 'r') as file:
        lines = file.readlines()  # Читаем все строки файла в список
    num_lines = len(lines)
    if abs(value-10)>num_lines:
        return render_template('grafics.html', path_to_time = 'grafics/time.png', value = value)
    else:
        render_template('grafics.html', path_to_time = 'grafics/time.png', value = value-1)
        
@app.route("/right_time/<value>", methods = ['GET'])
def righttime_grafics(value):
    value = int(value)
    if(value+1)>0:
        return render_template('grafics.html', path_to_time = 'grafics/time.png', value = value)
    else:
        return render_template('grafics.html', path_to_time = 'grafics/time.png', value = value + 1)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
