import datetime as dt
import os

m_now = (dt.datetime.now()).month
d_now = (dt.datetime.now()).day
print('Welocome to the DeadlineTracker!\nCommands:\n' + \
      '> Enter "add" to add new deadline\n' + \
      '> Enter "next" to see closest deadline\n' + \
      '> Enter "all" to see all deadlines\n' + \
      '> Enter "date" (MM/DD) to see deadlines for specific day\n' + \
      '> Enter "clear" to remove all deadlines\n' + \
      '> Enter "exit" to close\n')

with open('C:/Users/One/.spyder-py3/deadlines.txt', 'a+') as dl:
    if os.stat("deadlines.txt").st_size == 0:  
        deadlines = {}
    else:
        for line in dl:
            date = line[:line.index(':') - 1]
            if date >= str(m_now) + '/' + str(d_now):
                deadlines += deadlines.update({line[:line.index(':')] : line[line.index(':') + 1:]})                 
    while True:        
        usr_inp = input()
        if usr_inp == 'add':
            add_course = input('Please enter the name of a course:')
            add_date = input('And a deadline date (MM/DD):')
            if add_date < str(m_now) + '/' + str(d_now):
                add_date = input('This date has already passed, please enter another date:')
            deadlines.update({add_date: add_course})
            for i in deadlines.items():
                l = [i[0], ' : ', i[1]]
                dl.writelines(l)
                dl.write('\n')
            print('Deadline set for the', add_course, 'on', add_date)
        elif usr_inp == 'next':
            print(min(deadlines.keys()), ':', deadlines.get(min(deadlines.keys())))
        elif usr_inp == 'all':
            for i in sorted(deadlines.items()):
                print(i[0], ':', i[1])
        elif usr_inp == 'date':
            date = input('Please specify the date (MM/DD):')
            for i in deadlines.keys():
                if i == date:
                    print(deadlines.get(i))
        elif usr_inp == 'clear':
            deadlines = {}
        elif usr_inp == 'exit':
            break