# Author: Jens Settelmeier
# Created on 26.02.24 15:05
# File Name: MOAgent.py
# Contact: jenssettelmeier@gmail.com
# License: Apache License 2.0
# You can't climb the ladder of success
# with your hands in your pockets (A. Schwarzenegger)

import os
import sys
import subprocess
import joblib
import glob
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from MOBiceps import convertRawMP, rfePlusPlusWF
from MOBiceps import convert_mzXML2img
from MOBiceps import expression_table
from ttkthemes import ThemedTk

# ToDO: Add button for manifestfile for rfePlusPlusWF


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

        # Converter
        self.input_dir = tk.StringVar()
        self.input_format = tk.StringVar()
        # self.output_dir_conv = tk.StringVar()
        self.output_format = tk.StringVar()
        self.num_threads = tk.IntVar()

        # RFE feature tabel
        self.input_to_search_output = tk.StringVar()
        self.path_to_class_annotation = tk.StringVar()
        self.feature_table_output_path = tk.StringVar()
        self.impute_method = tk.StringVar()
        self.feature_level = tk.StringVar()

        # RFE++
        self.input_file_rfe = tk.StringVar()
        self.class_annotation_path = tk.StringVar()
        self.replicate_annotation_path = tk.StringVar()
        self.manifest_path = tk.StringVar()
        self.bootstrap = tk.BooleanVar()
        self.noisy_aug = tk.BooleanVar()
        self.output_dir_rfe = tk.StringVar()
        self.impute_method_rfe = tk.StringVar()
        self.feature_level_rfe = tk.StringVar()
        self.gpu = tk.BooleanVar()
        self.force_selection = tk.BooleanVar()
        self.considered_classes = tk.StringVar()

        self.create_menu()
        self.convert()
        self.feature_table()
        self.rfe()

        # Gui menu

    def create_menu(self):
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        # Convert
        self.filemenu.add_command(label="Data Convert", command=self.convert)
        # RFE++
        self.filemenu.add_command(label="RFE++", command=self.rfe)
        # Feature_table
        self.filemenu.add_command(label="Feature ML Table", command=self.feature_table)
        # Cascade menu
        self.menubar.add_cascade(label="Workflow", menu=self.filemenu)
        self.master.config(menu=self.menubar)

    # converter
    def convert(self):
        # Clear the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Input directory
        ttk.Label(self, text="Input directory").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.input_dir).grid(row=1, column=1)
        ttk.Button(self, text="Browse", command=self.browse_input_conv).grid(
            row=1, column=2
        )

        # Input format
        ttk.Label(self, text="Input format").grid(row=2, column=0)
        formats = ["raw", "mzXML", "mzML"]
        tk.OptionMenu(self, self.input_format, *formats).grid(row=2, column=1)

        # Output format
        ttk.Label(self, text="Output format").grid(row=3, column=0)
        out_formats = ["mzXML", "mzML", "png"]
        tk.OptionMenu(self, self.output_format, *out_formats).grid(row=3, column=1)

        # Number of threads
        ttk.Label(self, text="Number of threads").grid(row=4, column=0)
        threads = list(range(1, joblib.cpu_count()))
        tk.OptionMenu(self, self.num_threads, *threads).grid(row=4, column=1)

        # Start button
        ttk.Button(self, text="Start", command=self.start_conversion).grid(
            row=5, column=1
        )
        ttk.Label(self, text="Convert files").grid(row=5, column=0)

        # update button
        ttk.Button(
            self, text="Exit and update Platform", command=self.start_update
        ).grid(row=5, column=2)

    # converter
    def browse_input_conv(self):
        self.input_dir.set(filedialog.askdirectory())

    def start_conversion(self):
        # Call function with the arguments from the GUI
        print("start file conversion...")
        if self.output_format.get() == "png":

            convertRawMP.convertRAWMP(
                self.input_dir.get(),
                self.input_format.get(),
                "mzXML",
                self.num_threads.get(),
            )
            mzXML_folders = glob.glob(
                os.path.join(self.input_dir.get(), "results_mzXML_*")
            )
            input_path = mzXML_folders[0]
            convert_mzXML2img.mzXML2DIAimg(input_path)
        else:
            convertRawMP.convertRAWMP(
                self.input_dir.get(),
                self.input_format.get(),
                self.output_format.get(),
                self.num_threads.get(),
            )
        messagebox.showinfo("Information", "Conversion done!")

    # Feature table

    def feature_table(self):
        # Clear the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Input file
        ttk.Label(self, text="Search result file").grid(row=0, column=0)
        ttk.Entry(self, textvariable=self.input_to_search_output).grid(row=0, column=1)
        ttk.Button(self, text="Browse", command=self.browse_input_ftable).grid(
            row=0, column=2
        )

        # Path to class annotaion
        ttk.Label(self, text="Class annotation file").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.path_to_class_annotation).grid(
            row=1, column=1
        )
        ttk.Button(self, text="Browse", command=self.browse_class_annotation).grid(
            row=1, column=2
        )

        # Output path
        ttk.Label(self, text="Output path").grid(row=2, column=0)
        ttk.Entry(self, textvariable=self.feature_table_output_path).grid(
            row=2, column=1
        )
        ttk.Button(
            self, text="Browse", command=self.browse_feature_table_output_path
        ).grid(row=2, column=2)

        # Imputation method
        ttk.Label(self, text="Impute method").grid(row=3, column=0)
        methods = [
            "zero",
            "gaussian",
            "median",
            "mean",
            "none",
        ]
        tk.OptionMenu(self, self.impute_method, *methods).grid(row=3, column=1)

        # Feature level
        ttk.Label(self, text="Feature level").grid(row=4, column=0)
        feature_lvl = [
            "peptide",
            "protein",
        ]
        tk.OptionMenu(self, self.feature_level, *feature_lvl).grid(row=4, column=1)

        # Start button
        ttk.Button(self, text="Start", command=self.start_feature_table).grid(
            row=5, column=1
        )
        ttk.Label(self, text="Build feature table").grid(row=5, column=0)

        # update button
        ttk.Button(
            self, text="Exit and update Platform", command=self.start_update
        ).grid(row=5, column=2)

    def browse_input_ftable(self):
        self.input_to_search_output.set(filedialog.askopenfilename())

    def browse_manifest_file(self):
        self.manifest_path.set(filedialog.askopenfilename())

    def browse_class_annotation(self):
        self.path_to_class_annotation.set(filedialog.askopenfilename())

    def browse_feature_table_output_path(self):
        self.feature_table_output_path.set(filedialog.askdirectory())

    def start_feature_table(self):
        # Call function with the arguments from the GUI

        if self.feature_table_output_path.get() == "":
            ftop = os.path.dirname(self.input_to_search_output.get())
        else:
            ftop = self.feature_table_output_path.get()

        print("start feature table computation...")
        expression_table.create_rfe_expression_table(
            self.input_to_search_output.get(),
            self.path_to_class_annotation.get(),
            ftop,
            self.impute_method.get(),
            self.feature_level.get(),
        )
        messagebox.showinfo("Information", "Feature table done!")

    # RFE
    def rfe(self):
        # Clear the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Input directory
        ttk.Label(self, text="Search output or expression table").grid(row=0, column=0)
        ttk.Entry(self, textvariable=self.input_file_rfe).grid(row=0, column=1)
        ttk.Button(self, text="Browse", command=self.browse_input_file).grid(
            row=0, column=2
        )

        # Class annotation
        ttk.Label(self, text="Class annotations").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.class_annotation_path).grid(row=1, column=1)
        ttk.Button(self, text="Browse", command=self.browse_annotation_file).grid(
            row=1, column=2
        )

        # Replicate annotation
        ttk.Label(self, text="Replicate annotations").grid(row=2, column=0)
        ttk.Entry(self, textvariable=self.replicate_annotation_path).grid(
            row=2, column=1
        )
        ttk.Button(self, text="Browse", command=self.browse_replicate_file).grid(
            row=2, column=2
        )

        # Manifest file for DDA
        ttk.Label(self, text="Fragpipe manifest (DDA)").grid(row=3, column=0)
        ttk.Entry(self, textvariable=self.manifest_path).grid(row=3, column=1)
        ttk.Button(self, text="Browse", command=self.browse_manifest_file).grid(
            row=3, column=2
        )

        # Output directory
        ttk.Label(self, text="Output directory").grid(row=4, column=0)
        ttk.Entry(self, textvariable=self.output_dir_rfe).grid(row=4, column=1)
        ttk.Button(self, text="Browse", command=self.browse_output_rfe).grid(
            row=4, column=2
        )

        # bootstrapping
        ttk.Checkbutton(
            self, text="Bootstrap augmentation", variable=self.bootstrap
        ).grid(row=5, column=0, sticky="W")
        ttk.Checkbutton(self, text="Noisy augmentation", variable=self.noisy_aug).grid(
            row=5, column=1, sticky="W"
        )

        # ToDo
        # Imputation method
        # ttk.Label(self, text='Imputation method').grid(row=5, column=0)
        # methods = ['zero', 'frequent', 'median', 'mean', 'none', 'try_all']
        # tk.OptionMenu(self, self.impute_method_rfe, *methods).grid(row=5, column=1)

        # Feature level
        ttk.Label(self, text="Feature level").grid(row=6, column=0)
        feature_lvl_r = ["peptide", "protein"]
        tk.OptionMenu(self, self.feature_level_rfe, *feature_lvl_r).grid(
            row=6, column=1
        )

        # GPU support
        ttk.Checkbutton(self, text="GPU support", variable=self.gpu).grid(
            row=7, column=0, sticky="W"
        )

        # force selection
        ttk.Checkbutton(
            self,
            text="Force handable amount of features",
            variable=self.force_selection,
        ).grid(row=8, column=0, sticky="W")
        # considered classes
        ttk.Label(self, text="Considered Classes").grid(row=9, column=0)
        ttk.Entry(self, textvariable=self.considered_classes).grid(row=9, column=1)

        # Start button
        ttk.Button(self, text="Start", command=self.start_rfe).grid(row=10, column=1)
        ttk.Label(self, text="Estimate most phenotype-specific features").grid(
            row=10, column=0
        )
        # update button
        ttk.Button(
            self, text="Exit and update Platform", command=self.start_update
        ).grid(row=10, column=2)

    # Update
    def start_update(self):
        def execute_command(command):
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            output, error = process.communicate()
            if process.returncode != 0:
                print(f"Error executing command: {command}")
                print(error.decode("utf-8"))
            return output.decode("utf-8")

        # Define the commands
        commands = [
            "#!/bin/bash",
            "cd ~/Desktop/MOAgent && git pull",
            "cd ~/Desktop/MOBiceps && git pull",
            ". /home/moagent/anaconda3/etc/profile.d/conda.sh && conda activate moagent",
            "pip uninstall MOBiceps -y",  # Add -y to automatically confirm uninstall
            "cd ~/Desktop/MOBiceps && pip install .",
        ]

        # Execute the commands
        for cmd in commands:
            subprocess.run(cmd, shell=True)
        sys.exit()

    # RFE
    def browse_input_file(self):
        self.input_file_rfe.set(filedialog.askopenfilename())

    def browse_annotation_file(self):
        self.class_annotation_path.set(filedialog.askopenfilename())

    def browse_replicate_file(self):
        self.replicate_annotation_path.set(filedialog.askopenfilename())

    def browse_output_rfe(self):
        self.output_dir_rfe.set(filedialog.askdirectory())

    def start_rfe(self):
        # Call function with the arguments from the GUI
        # In the start_rfe method:
        considered_classes = (
            self.considered_classes.get().strip()
        )  # .strip() removes leading/trailing whitespace
        considered_classes_list = (
            None
            if considered_classes == ""
            else [cls.strip() for cls in considered_classes.split(",")]
        )
        print("considered_classes_list", considered_classes_list)
        if self.output_dir_rfe.get() == "":
            odr = os.path.dirname(self.input_file_rfe.get())
        else:
            odr = self.output_dir_rfe.get()

        if self.replicate_annotation_path.get() == "":
            rap = None
        else:
            rap = self.replicate_annotation_path.get()

        if self.manifest_path.get() == "":
            mp = None
        else:
            mp = self.manifest_path.get()

        print("start rfe++")
        print("gpu", self.gpu.get())
        rfePlusPlusWF.execute_rfePP(
            path_to_search_file=self.input_file_rfe.get(),
            path_to_class_annotation_file=self.class_annotation_path.get(),
            path_to_output=odr,
            path_to_manifest_file=mp,
            path_to_sample_annotation_file=rap,
            bootstrapping_augmentation=self.bootstrap.get(),
            feature_lvl=self.feature_level_rfe.get(),
            gpu=self.gpu.get(),
            noisy_augmentation=self.noisy_aug.get(),
            force_selection=self.force_selection.get(),
            phenotype_class=considered_classes_list,
        )
        messagebox.showinfo("Information", "RFE++ done!")


root = ThemedTk(theme="ubuntu")

root.title("MOAgent")
app = Application(master=root)
app.mainloop()
