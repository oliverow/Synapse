import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
import random


COLOR_SCHEME = ['#90ee90', 'YELLOW', 'ORANGE', 'MAGENTA', 'RED', 'BLACK']


class gui_app(tk.Tk):
    def __init__(self, database, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.database = database

        # config app
        self.minsize(640, 480)

        # building main container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # creating pages in the main container
        self.frames = {}
        for pageClass in (HomePage, EntryPage, ReviewPage, SimilarReviewPage):
            frame = pageClass(container, self)
            self.frames[pageClass] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
            frame.grid_columnconfigure(1, weight = 1)
            frame.grid_rowconfigure(1, weight = 1)

        # start with home page
        self.show_frame(HomePage)

    def show_frame(self, pageName, *args):
        self.frames[pageName].tkraise()
        self.frames[pageName].prepare(*args)


class Page(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

    def prepare(self):
        return


class HomePage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
        self.grid(ipady = 50)
        title = tk.Label(self, text = "Synapse", font = ("Arial", 44))
        title.pack()
        menu = tk.PanedWindow(self)
        menu.pack()
        entryPageButton = tk.Button(menu, text = "Learn", command=lambda: controller.show_frame(EntryPage))
        entryPageButton.grid(row = 0, column = 0, pady = 50)
        reviewPageButton = tk.Button(menu, text = "Review", command=lambda: controller.show_frame(ReviewPage))
        reviewPageButton.grid(row = 0, column = 1)


class EntryPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        main_panel = tk.PanedWindow(self)
        main_panel.grid(row = 1, column = 1, columnspan = 2, sticky = "nsew")
        main_panel.grid_columnconfigure(2, weight = 1)
        main_panel.grid_rowconfigure(0, weight = 1)
        main_panel.grid_rowconfigure(2, weight = 1)
        main_panel.grid_rowconfigure(5, weight = 1)

        word_label = tk.Label(main_panel, text = "word:")
        word_label.grid(row = 1, column = 0, pady = 10)
        self.word_input = tk.Entry(main_panel)
        self.word_input.grid(row = 1, column = 1)
        hint_label = tk.Label(main_panel, text = "hint:")
        hint_label.grid(row = 2, column = 0, pady = 10)
        self.hint_input = tk.Entry(main_panel)
        self.hint_input.grid(row = 2, column = 1)
        add_button = tk.Button(main_panel, text = "add", command = self.add_entry)
        add_button.grid(row = 4, column = 0, columnspan = 2, pady = 20)

        self.status_var = tk.StringVar()
        status_label = tk.Label(main_panel, textvariable = self.status_var)
        status_label.grid(row = 5, column = 0, columnspan = 2, pady = 10)

        self.list_data = []
        self.list_panel = tk.Listbox(main_panel, selectmode = "SINGLE")
        self.list_panel.yview()
        self.list_panel.grid(row = 0, column = 2, rowspan = 10, padx = 20, pady = 20, sticky = "nsew")

        back_button = tk.Button(self, text = "⬅︎", command = self.exit)
        back_button.grid(row = 0, column = 0)

    def prepare(self):
        self.list_panel.delete(0, self.list_panel.size())
        self.list_data = []
        result = self.controller.database.list()
        result = sorted(result)
        for index, line in enumerate(result):
            self.list_data.append(line[0])
            s = ' '.join(list(map(lambda x: x.word, line)))
            self.list_panel.insert(index, s)

    def add_entry(self):
        word = self.word_input.get()
        hint = self.hint_input.get()
        try:
            selected = self.list_data[self.list_panel.curselection()[0]]
            suffix = " with " + selected.word
        except Exception as e:
            selected = None
            suffix = " as an independent word"
        self.controller.database.create_entry(word, hint, selected)
        self.status_var.set(word + " entered successfully" + suffix)
        self.prepare()

    def exit(self):
        self.controller.show_frame(HomePage)
        self.list_panel.delete(0, self.list_panel.size())
        self.list_data = []


class ReviewPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
        back_button = tk.Button(self, text = "⬅︎", command=lambda: controller.show_frame(HomePage))
        back_button.grid(row = 0, column = 0)

        menu = tk.PanedWindow(self)
        menu.grid(row = 1, column = 1, sticky = "nsew")
        menu.grid_columnconfigure(0, weight = 1)

        similar_review_menu = tk.PanedWindow(menu)
        similar_review_menu.grid(row = 0, column = 0, pady = 50)
        similar_review_label = tk.Label(similar_review_menu, text = "Similar Words")
        similar_review_label.grid(row = 0, column = 1)
        wrong_similar_review_button = tk.Button(similar_review_menu, text = "Hard Words", command = lambda: controller.show_frame(SimilarReviewPage, "Hard"))
        wrong_similar_review_button.grid(row = 1, column = 0, pady = 30)
        all_similar_review_button = tk.Button(similar_review_menu, text = "All Words", command = lambda: controller.show_frame(SimilarReviewPage, "All"))
        all_similar_review_button.grid(row = 1, column = 1)
        memorized_similar_review_button = tk.Button(similar_review_menu, text = "Memorized Words", command = lambda: controller.show_frame(SimilarReviewPage, "Memorized"))
        memorized_similar_review_button.grid(row = 1, column = 2)


class SimilarReviewPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent)
        self.controller = controller
        self.mode = "All"

        back_button = tk.Button(self, text = "Quit️", command = self.exit)
        back_button.grid(row = 0, column = 0)

        main_panel = tk.PanedWindow(self)
        main_panel.grid(row = 1, column = 1, sticky = "nsew")
        main_panel.grid_columnconfigure(1, weight = 1)

        self.progress_bar = ttk.Progressbar(main_panel, orient = "horizontal", mode = "determinate")
        self.progress_bar.grid(row = 0, column = 1, sticky = "nsew", pady = 20)
        self.progress_label = tk.StringVar()
        self.progress_display = tk.Label(main_panel, textvariable = self.progress_label)
        self.progress_display.grid(row = 0, column = 2)

        self.count_var = tk.IntVar()
        self.counter_display = tk.Label(main_panel, textvariable = self.count_var)
        self.counter_display.grid(row = 1, column = 2, ipadx = 20, padx = 30, sticky = "nsew")

        inspect_button = tk.Button(main_panel, text = "Toggle full set", command = self.toggle_inspect)
        inspect_button.grid(row = 2, column = 0)
        self.inspect_list = tk.Listbox(main_panel)
        self.inspect_list.yview()
        self.inspect_list.grid_forget()
        self.inspect_list_visible = False
        self.inspect_list.bind("<<ListboxSelect>>", self.jump_to_word)

        self.iter_index = 0                     # the current position in normal iteration
        self.current_word = None
        self.jump_back_word = None                   # to store the current word in case of manual jump
        word_font = tkfont.Font(size = 32)
        self.word_var = tk.StringVar()
        word_display = tk.Label(main_panel, textvariable = self.word_var, font = word_font)
        word_display.grid(row = 1, column = 1, pady = 15)
        word_display.bind("<Button-1>", self.toggle_meaning)
        self.meaning_var = tk.StringVar()
        self.meaning_display = tk.Message(main_panel, textvariable = self.meaning_var, aspect = 500)
        self.meaning_display.grid_forget()
        self.meaning_visible = False

        selection_panel = tk.PanedWindow(main_panel)
        selection_panel.grid(row = 5, column = 1, sticky = "s")
        yes_button = tk.Button(selection_panel, text = "✓", command = self.remembered)
        yes_button.grid(row = 0, column = 1)
        no_button = tk.Button(selection_panel, text = "✕", command = self.forgotten)
        no_button.grid(row = 0, column = 0)
        next_button = tk.Button(selection_panel, text = "→", command = self.iterate_word)
        next_button.grid(row = 0, column = 2)
        mark_panel = tk.PanedWindow(main_panel)
        mark_panel.grid(row = 6, column = 1, rowspan = 4, sticky = "s")
        self.memorized_flag = tk.BooleanVar()
        selection_font1 = tkfont.Font(size = 32)
        memorized_check = tk.Checkbutton(mark_panel, text = "☺︎", font = selection_font1, variable = self.memorized_flag, command = self.memorized)
        memorized_check.grid(row = 1, column = 1)
        self.starred_flag = tk.BooleanVar()
        selection_font2 = tkfont.Font(size = 20)
        starred_check = tk.Checkbutton(mark_panel, text = "☆", font = selection_font2, variable = self.starred_flag, command = self.starred)
        starred_check.grid(row = 1, column = 0)

    def prepare(self, *args):
        self.mode = args[0]
        result = self.controller.database.list()
        random.shuffle(result)
        self.vocab_list = []
        for line in result:
            random.shuffle(line)
            self.vocab_list.append(line)
        self.current_set = self.vocab_list.pop(0)
        for index, word in enumerate(self.current_set):
            self.inspect_list.insert(index, word.word)
        self.progress_bar.config(maximum = len(self.vocab_list))
        self.progress_label.set(str(self.progress_bar['value'])+"/"+str(self.progress_bar['maximum']))
        self.iter_index = 0
        self.current_word = self.current_set[self.iter_index]
        self.update_word()

    def exit(self):
        self.controller.show_frame(ReviewPage)
        self.inspect_list.delete(0, self.inspect_list.size())

    def update_word(self, word = None):
        if word is None: word = self.current_word
        if self.mode == "Hard" and word.memorized and word.wrongtimes == 0:
            self.iterate_word()
            return
        if self.mode == "Memorized" and (not word.memorized or word.wrongtimes != 0):
            self.iterate_word()
            return
        self.word_var.set(word.word)
        self.meaning_var.set(word.meaning)
        self.count_var.set(word.wrongtimes)
        self.counter_display.config(bg = COLOR_SCHEME[word.wrongtimes])
        self.memorized_flag.set(word.memorized)
        self.starred_flag.set(word.starred)

    def iterate_word(self):
        if len(self.vocab_list) == 0 and len(self.current_set) == self.iter_index:
            self.exit()
            return
        if len(self.current_set) == self.iter_index:
            self.current_set = self.vocab_list.pop(0)
            self.iter_index = 0
            self.inspect_list.delete(0, self.inspect_list.size())
            for index, word in enumerate(self.current_set):
                self.inspect_list.insert(index, word.word)
            self.progress_bar['value'] = self.progress_bar['maximum'] - len(self.vocab_list)
            self.progress_label.set(str(self.progress_bar['value'])+"/"+str(self.progress_bar['maximum']))
        if self.jump_back_word is None:
            self.current_word = self.current_set[self.iter_index]
            self.iter_index += 1
        else:
            self.inspect_list.selection_clear(0, 'end')
            self.jump_back_word = None
        self.update_word()

    def remembered(self):
        self.current_word.get_right()
        self.controller.database.update_entry(self.current_word.word, "wrongtimes", self.current_word.wrongtimes)
        self.iterate_word()

    def forgotten(self):
        self.current_word.get_wrong()
        self.controller.database.update_entry(self.current_word.word, "wrongtimes", self.current_word.wrongtimes)
        self.iterate_word()

    def memorized(self):
        self.current_word.memorized = self.memorized_flag.get()
        self.controller.database.update_entry(self.current_word.word, "memorized", self.current_word.memorized)

    def starred(self):
        self.current_word.starred = self.starred_flag.get()
        self.controller.database.update_entry(self.current_word.word, "starred", self.current_word.starred)

    def toggle_inspect(self):
        if self.inspect_list_visible:
            self.inspect_list.grid_forget()
            self.inspect_list_visible = False
        else:
            self.inspect_list.grid(row = 3, column = 0, rowspan = 5)
            self.inspect_list_visible = True

    def toggle_meaning(self, event):
        if self.meaning_visible:
            self.meaning_display.grid_forget()
            self.meaning_visible = False
        else:
            self.meaning_display.grid(row = 4, column = 1, sticky = "nsew", pady = 25)
            self.meaning_visible = True

    def jump_to_word(self, event):
        word_index = self.inspect_list.curselection()[0]
        if self.iter_index == word_index:
            return
        self.jump_back_word = self.current_word
        self.update_word(self.current_set[word_index])
