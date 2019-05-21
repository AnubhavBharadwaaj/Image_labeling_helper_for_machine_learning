import tkinter as tk
from tkinter import *
import tkinter.filedialog as fdialog
import csv
import os
import glob
from PIL import Image, ImageTk

class Frame_header_class(Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)


    def show(self):
        self.lift()

class Frame_1_directory_and_class_labels(Frame_header_class):
    def __init__(self, *args, **kwargs):
        Frame_header_class.__init__(self, *args, **kwargs)
        # self.pack()
        # self.pack(side = "top", fill = tk.BOTH, expand = True)
        for arg in args:
            self.frame_2_image_view = arg

        self.label_button_1 = Label(self, text="Select directory for picking images")
        self.label_button_1.grid(row = 0, column = 0, columnspan = 1, sticky = W)

        self.button_1 = tk.Button(self, text="CLICK HERE", width=25, command=self.open_dialog_box_to_select_folder)
        self.button_1.grid(row=0, column=1, columnspan=2, sticky=W)

        self.label_for_label_directory = Label(self, text="Current chosen directory")
        self.label_for_label_directory.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W)

        self.entryText = StringVar()
        self.label_directory = Entry(self, textvariable=self.entryText, state="readonly")
        self.label_directory.grid(row=1, column=1, rowspan=1, columnspan=2, sticky=W)

        self.label_for_entry_for_class_label_values = Label(self, text="Enter (+) seperated class labels\nto be assigned to the images")
        self.label_for_entry_for_class_label_values.grid(row = 2, column = 0, rowspan = 1, columnspan = 2, sticky = W)

        self.entry_for_class_label_values = Entry(self)
        self.entry_for_class_label_values.grid(row = 2, column = 1, rowspan = 1, columnspan = 1, sticky = W)

        self.button_for_submitting_class_labels = Button(self, text = "Submit", width = 10, command = self.submit_class_labels)
        self.button_for_submitting_class_labels.grid(row = 2, column = 2, rowspan = 1, columnspan = 2, sticky = W)


    def open_dialog_box_to_select_folder(self):
        self.chosen_directory_name = fdialog.askdirectory()
        self.entryText.set(self.chosen_directory_name)

    def update_option_menu_of_class_labels(self):
        menu = self.frame_2_image_view.list_of_class_labels_option_view["menu"]
        menu.delete(0, "end")
        for string in self.list_of_class_labels:
            menu.add_command(label=string, command=lambda value=string: self.frame_2_image_view.variable_showing_list_of_class_labels.set(value))

    def submit_class_labels(self):
        self.class_labels = self.entry_for_class_label_values.get()
        self.list_of_class_labels = self.class_labels.split("+")
        self.frame_2_image_view.chosen_directory_name = self.chosen_directory_name
        self.frame_2_image_view.list_of_class_labels = self.list_of_class_labels
        numerical_class_label = 0
        for class_label in self.list_of_class_labels:
            self.frame_2_image_view.numerical_labels_corresponding_to_class_labels_provided[class_label] = numerical_class_label
            self.frame_2_image_view.class_labels_corresponding_to_numerical_labels[numerical_class_label] = class_label
            numerical_class_label += 1
        self.update_option_menu_of_class_labels()
        self.frame_2_image_view.show()

class Frame_2_image_view(Frame_header_class):

    def __init__(self, *args, **kwargs):
        Frame_header_class.__init__(self, *args, **kwargs)
        self.chosen_directory_name = [1]
        self.list_of_class_labels = ["Select a class label"]
        self.numerical_labels_corresponding_to_class_labels_provided = dict({})
        self.class_label_corresponding_to_any_image = dict({})
        self.class_labels_corresponding_to_numerical_labels = dict({})
        self.current_class_label_selected = self.list_of_class_labels[0]
        self.check_if_image_has_already_been_updated_on_click = dict({})
        self.variable_showing_list_of_class_labels = StringVar(self)
        self.variable_showing_list_of_class_labels.set(self.list_of_class_labels[0])
        self.list_of_class_labels_option_view = OptionMenu(self, self.variable_showing_list_of_class_labels, *self.list_of_class_labels, command = self.list_of_class_labels_option_view_updated)
        self.list_of_class_labels_option_view.grid(row = 0, column = 0, rowspan = 1, columnspan = 1)
        button_to_select_images = Button(self, text='Open Image Viewer', command=self.dataset_image_viewer)
        button_to_select_images.grid(row = 1, column = 0, rowspan = 1, columnspan = 1)

        button_to_generate_csv = Button(self, text = "Download CSV", command = self.generate_csv_of_class_labels)
        button_to_generate_csv.grid(row = 2, column = 0, rowspan = 1, columnspan = 1)

    def generate_csv_of_class_labels(self):
        with open("csv_class_labels_and_corresponding_image_files.csv", "w") as f:
            for key in self.class_label_corresponding_to_any_image:
                f.write("%s,%d,%s\n"%(key, self.class_label_corresponding_to_any_image[key], self.class_labels_corresponding_to_numerical_labels[self.class_label_corresponding_to_any_image[key]]))


    def list_of_class_labels_option_view_updated(self, event):
        self.current_class_label_selected = self.variable_showing_list_of_class_labels.get()

    def getting_information_of_image_selected_and_updating_class_label_information_of_the_corresponding_image(self, event):

        selected_image_id = event.widget.find_withtag(CURRENT)[0]

        if self.check_if_image_has_already_been_updated_on_click[selected_image_id] == 0:
            # print('selected_image_id: ', selected_image_id)
            # print('file_name: ', self.image_id_mapped_to_file_name[selected_image_id])
            path_of_the_selected_image_id = self.image_id_mapped_to_file_name[selected_image_id]
            class_label_being_provided = self.variable_showing_list_of_class_labels.get()
            self.class_label_corresponding_to_any_image[path_of_the_selected_image_id] = self.numerical_labels_corresponding_to_class_labels_provided[class_label_being_provided]
            # self.container.itemconfig(selected_image_id, image = Image.open(self.image_id_mapped_to_file_name[selected_image_id]).resize((100, 100), Image.ANTIALIAS).convert('1'))
            self.container.delete(selected_image_id)
            self.check_if_image_has_already_been_updated_on_click[selected_image_id] = 1




    def dataset_image_viewer(self):

        self.win = Toplevel()
        self.vbar = tk.Scrollbar(self.win, orient = VERTICAL)
        self.vbar.grid(row = 0, column = 1, sticky = "ns")

        self.hbar = tk.Scrollbar(self.win, orient = HORIZONTAL)
        self.hbar.grid(row = 1, column = 0, sticky = "we")

        self.container = tk.Canvas(self.win, height=778, width=1516, scrollregion=(0, 0, 778, 1516))
        self.container.grid(row = 0, column = 0, sticky = "nsew")


        self.container.img_list = []
        self.vbar.config(command=self.container.yview)
        self.hbar.config(command = self.container.xview)
        self.container.config(yscrollcommand=self.vbar.set)
        self.container.config(xscrollcommand = self.hbar.set)

        path = self.chosen_directory_name
        COLUMNS = 10
        image_count = 0
        r = 0
        c = 0
        self.image_id_mapped_to_file_name = dict({})
        self.file_name_mapped_to_image_id = dict({})
        self.image_id_mapped_to_just_read_image = dict({})
        for infile in glob.glob(os.path.join(path, '*.jpg')):
            image_count += 1

            im = Image.open(infile)
            resized = im.resize((100, 100), Image.ANTIALIAS)
            img_part = ImageTk.PhotoImage(resized)
            self.container.img_list.append(img_part)

            image_in_canvas = self.container.create_image(r, c, image = img_part, anchor = 'nw')
            self.check_if_image_has_already_been_updated_on_click[image_in_canvas] = 0
            self.image_id_mapped_to_file_name[image_in_canvas] = infile
            self.image_id_mapped_to_just_read_image[image_in_canvas] = resized
            self.file_name_mapped_to_image_id[infile] = image_in_canvas
            self.container.tag_bind(image_in_canvas, "<Button-1>", self.getting_information_of_image_selected_and_updating_class_label_information_of_the_corresponding_image)
            r += 105
            if r >= 1440:
                r = 0
                c += 105

        self.container.bind('<Configure>', lambda e: self.container.configure(scrollregion=self.container.bbox('all')))

    # win.rowconfigure(0, weight=1)
    # win.columnconfigure(0, weight=1)

class Label_helper_main_page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # self.master.title("Image Label Helper")
        # self.master.wm_geometry("500x500")
        # self.master.resizable(0, 0)
        # self.master.pack_propagate(0)
        frame_2_image_view = Frame_2_image_view(self)
        frame_1_directory_and_class_labels = Frame_1_directory_and_class_labels(self, frame_2_image_view)

        container = tk.Frame(self, bg = "red")
        container.pack(side="top", fill="both", expand=True)

        frame_1_directory_and_class_labels.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        frame_2_image_view.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        frame_1_directory_and_class_labels.show()

if __name__ == '__main__':
    root = tk.Tk()
    label_helper_main = Label_helper_main_page(root)
    label_helper_main.pack(side="top", fill="both", expand=True)
    root.title("Galaxy Dominator Ultra Omega: Image Label Helper Mark 2")
    root.wm_geometry("500x500")
    root.resizable(0, 0)
    root.pack_propagate(0)

    label_helper_main.mainloop()
