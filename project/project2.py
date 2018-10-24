import csv, re


with open('1.txt', 'r', encoding='utf-8') as f:
    content = f.read().split('\n')

    
# year sname fname mname address status
people = []
year = content.pop(0)

human = ''
last_surname = ''
for s in content:
    try:
        first = s.split()[0]
    except IndexError:
        continue
    if first.isupper() and first[-1] != '.':
        last_surname = first
        people.append(human)
        human = s
    elif first[0] == '—':
        people.append(human)
        human = last_surname + s[1:]
    else:
        human += s

people.append(human)
people.pop(0)

statuses = {}
with open('dict2.csv', 'r', encoding='cp1251') as f:
    reader = csv.reader(f, delimiter=";")
    #reader = csv.reader(f.read()[1:].splitlines(), delimiter=";")
    for row in reader:
        statuses[row[0]] = row[1], row[2]

with open('result.csv', 'w', newline='', encoding='utf-8') as f:
    f.write(u'\ufeff')
    writer = csv.writer(f, delimiter=";")
    writer.writerow(['Год', 'Фамилия', 'Имя', 'Отчество', 'Статус', 'Адрес', 'Описание', 'Телефон'])
    for h in people:
        st = ""
        if len(h) < 3:
            continue
        h = h.split()
        sname = h.pop(0)
        if h[0] == "кн.":
            st = h.pop(0)
        if h[0] == "кп.":
            st = h.pop(0)
        if h[0] == "гр.":
            st = h.pop(0)
        if h[0] == "бар.":
            st = h.pop(0)
        fname = h.pop(0)
        try:
            while h[0][0].islower():
                fname += h.pop(0)
            mname = h.pop(0)
            #while h[0][0].islower():
                #mname += h.pop(0)
        
            description = ' '.join(h)
            description += " "
            description += st
        except IndexError:
            pass
        try:
            address = re.findall(r"\w+(?:\-?\s*?\w+?)?\.?\,?(?:\s+(?:пер|пл|наб|нер|кан|кап|пор)\.?)?,?\.?\s*\d+", description)[0]
        except IndexError:
            address = None
        try:
            tel = re.findall(r"(?:\Тлф|тлф)\.?\,?\—?\s*\d+", description)[0]
        except IndexError:
            tel = None

        matches = {}
        for key, value in statuses.items():
            try:
                matches[description.index(key)] = value[0]
            except ValueError:
                pass
        try:
            status = matches[min(matches.keys())]
        except ValueError:
            status = None
        writer.writerow([year, sname, fname, mname, status, address, description, tel])
        