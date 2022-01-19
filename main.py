from tkinter import *
from tkinter import ttk, messagebox
import os, random, collections



def load_words(arg):
    if arg == 'all':
        #words accepted as valid on entry
        with open(f'{turd_dir}/Resources/English Words/words_alpha.txt') as f:
            valid_words = [w for w in f.read().split() if len(w) == 5]

        return valid_words

    else:
        #acceptable words to generate so that it doesn't pick 'fconv' or some shit
        with open(f'{turd_dir}/Resources/English Words/shitlesscorn.txt') as f:
            valid_words = f.read().split()

        return valid_words


def load_gui(gui):
    gui.title("Turdle")
    gui.bind("<Key>", key_press)

    gui.columnconfigure(0, weight=1, uniform='side')
    gui.columnconfigure(2, weight=1, uniform='side')

    lbl_frm = ttk.Frame(gui, padding='10')
    make_labgrid(lbl_frm)

    kb_frm = ttk.Frame(gui, padding='10')
    make_keyboard(kb_frm)

    side_frm1 = ttk.Frame(gui, padding='10')
    side_frm2 = ttk.Frame(gui, padding='10')
    make_sides(side_frm1, side_frm2)

    side_frm1.grid(row=0, column=0)
    lbl_frm.grid(row=0, column=1)
    side_frm2.grid(row=0, column=2)
    kb_frm.grid(row=1, column=0, columnspan=3)


def make_keyboard(frm):
    kb_dicts = [{0: "q", 2: "w", 4: "e", 6: "r", 8: "t", 10: "y", 12: "u", 14: "i", 16: "o", 18: "p"},
                {1: "a", 3: "s", 5: "d", 7: "f", 9: "g", 11: "h", 13: "j", 15: "k", 17: "l"},
                {3: "z", 5: "x", 7: "c", 9: "v", 11: "b", 13: "n", 15: "m"}]

    n = 0
    for y in range(0, 3):
        for x in kb_dicts[y].keys():
            letter = kb_dicts[y][x]

            cmd = lambda k=letter: btn_press(k)
            temp_btn = ttk.Button(frm, text=f'\n{letter.upper()}\n', image=img['empty'],
                                  compound='center', command=cmd)
            temp_btn.grid(column=x, row=y * 2, columnspan=2, rowspan=2, sticky='nesw')

            btns.update({letter.lower() : temp_btn})
            n += 1

    btn_return = ttk.Button(frm, text='ENTER', image=img['empty_wide'],
                            compound='center', command=lambda: btn_press('return'))
    btn_return.grid(column=0, row=4, columnspan=3, rowspan=2, sticky='nesw')

    btn_delete = ttk.Button(frm, text='<', image=img['empty_wide'],
                            compound='center', command=lambda: btn_press('backspace'))
    btn_delete.grid(column=17, row=4, columnspan=3, rowspan=2, sticky='nesw')


def make_sides(frm1, frm2):
    fnt = ('Helvetica', '16', 'bold')

    reset_btn = ttk.Button(frm1, text="Reset", command=reset, image=img['empty_wide'], compound='center')
    reset_btn.grid(row=0, column=0)

    global check_var
    check_var = BooleanVar()
    check_var.set(True)
    showvis_btn = ttk.Checkbutton(frm2, text="Show Known:", variable=check_var, command=show_vis)
    showvis_btn.grid(row=0, column=0)

    global show_var
    show_var = StringVar()
    show_var.set('_ _ _ _ _')
    show_lab = ttk.Label(frm2, textvariable=show_var, font=fnt, image=img['empty_wide'], compound='center')
    show_lab.grid(row=1, column=0)


def make_labgrid(frm):
    fnt = ('Helvetica', '24', 'bold')

    n = 0
    for y in range(0, 6):
        for x in range(0, 5):
            text_vars.append(StringVar())

            labs.append(ttk.Label(frm, textvariable=text_vars[n], font=fnt, image=img['light'],
                                  compound='center', foreground='white'))
            labs[n].grid(column=x, row=y)
            n += 1


def btn_press(btn_str):
    if pointer != [-1, -1]:
        do_stuff(btn_str.lower())


def key_press(event):
    if pointer != [-1, -1]:
        do_stuff(event.keysym.lower())


def do_stuff(inp):
    letter = labs[pos()].cget('text')
    
    if inp in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:

        if letter == '':  
            #print(f"setting to {inp}")
            text_vars[pos()].set(inp.upper())
            
        else:
            if pointer[0] not in range(4, 30, 5):
                move_pointer()
                #print(f"setting to {inp}")
                text_vars[pos()].set(inp.upper())
            

    elif inp == 'backspace':
        if letter == '':
            if pointer[0] not in range(0, 26, 5):
                move_pointer('backward')
                #print(f"deleting {text_vars[pos()].get().lower()}")
                text_vars[pos()].set('')

        else:
            #print(f"deleting {text_vars[pos()].get().lower()}")
            text_vars[pos()].set('')

    elif inp == 'return':
        word = get_word()
        #print(f'trying {word}..')
        
        if len(word) == 5:
            #print('checking definition..')
            
            if word in all_words:
                #print('valid submission')
                check_word(word)
                move_pointer('next line')
            else:
                print('not a real word')
                #make all labels in row red for a sec
                turn_red()


def turn_red():
        for x in range(0, 5):
            labs[row() + x].configure(image=img['red'])
        root.update_idletasks()
        root.after(500, turn_back())

        
def turn_back():
    for x in range(0, 5):
            labs[row() + x].configure(image=img['light'])


def check_word(word):
    global word_shown

    if word == rand_word:
        #you win!!
        for i in range(0, 5):
            labs[row() + i].configure(image=img['green'])
            known[i] = word[i].upper()

        if check_var.get() == True:
            show_var.set(f'{known[0]} {known[1]} {known[2]} {known[3]} {known[4]}')

        move_pointer('end')
        word_shown = True

    else:
        if pointer[1] == 5:
            # you lose :( :(
            for i in range(0, 5):
                labs[row() + i].configure(image=img['red'])

            move_pointer('end')

            messagebox.showerror(message=f"The word was {rand_word}")
            word_shown = True

        else:
            #you got some wrong. that's ok.
            rand_dict = collections.Counter(rand_word)
            correct_inds = []

            for i in range(0, 5):
                if word[i] == rand_word[i]:
                    labs[row() + i].configure(image=img['green'])
                    rand_dict[word[i]] -= 1
                    correct_inds.append(i)

                    known[i] = word[i].upper()

            for i in range(0, 5):
                if i in correct_inds:
                    continue

                elif word[i] in rand_word:
                    #not a match, but is somewhere else
                    if  rand_dict[word[i]] > 0:
                        labs[row() + i].configure(image=img['yellow'])
                        rand_dict[word[i]] -= 1

                    else:
                        labs[row() + i].configure(image=img['dark'])

                else:
                    #not a match
                    btns[word[i]].configure(style='SemiDisable.TButton')
                    labs[row() + i].configure(image=img['dark'])

    if check_var.get() == True:
        show_var.set(f'{known[0]} {known[1]} {known[2]} {known[3]} {known[4]}')


def get_word():
    word = ''
    for i in range(0, 5):
        n = row() + i
        word += text_vars[n].get().lower()

    return word


def show_vis():
    global show_var

    if check_var.get() == True:
        show_var.set(f'{known[0]} {known[1]} {known[2]} {known[3]} {known[4]}')
    else:
        show_var.set('_ _ _ _ _')


def move_pointer(go='forward'):
    if pointer[0] != -1:
        if go == 'forward':
            if pointer[0]  < 4:
                pointer[0] += 1
                #print(f'{pointer} ->')

        elif go == 'backward':
            if pointer[0] > 0:
                pointer[0] -= 1
                #print(f'{pointer} <-')

        elif go == 'next line':
            if pointer[1] < 5:
                pointer[0] = 0
                pointer[1] += 1
                #print(f'{pointer} V')

        elif go == 'end':
            pointer[0] = -1
            pointer[1] = -1


def row():
    return pointer[1] * 5


def pos():
    return (pointer[1] * 5) + pointer[0]


def reset():
    global word_shown
    global rand_word
    global known

    if not word_shown:
        messagebox.showerror(message=f"The word was {rand_word}")

    word_shown = False
    rand_word = random.choice(reasonable_words)
    print(f'random word is {rand_word}')

    known = ['_', '_', '_', '_', '_']
    show_var.set(f'_ _ _ _ _')

    for i in range(0, 30):
        pointer[0] = 0
        pointer[1] = 0

        text_vars[i].set('')
        labs[i].configure(image=img['light'])

    for b in btns.values():
        b.configure(style='TButton')

#---------------------------------------------------------

turd_dir = os.path.dirname(__file__)

all_words = load_words('all')
reasonable_words = load_words('some')
rand_word = random.choice(reasonable_words)

print(f'choosing from {len(reasonable_words)} words')
print(f'random word is {rand_word}')

labs = []
btns = {}
known = ['_', '_', '_', '_', '_']
text_vars = []
pointer = [0, 0]
word_shown = False

root = Tk()

ttk.Style().configure('SemiDisable.TButton', )

img = {}
for name in ['dark', 'light', 'green', 'yellow', 'red', 'empty', 'empty_wide']:
    img.update({name : PhotoImage(file=f'{turd_dir}/Resources/{name}.gif')})

load_gui(root)
root.mainloop()


    





