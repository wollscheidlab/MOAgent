![MOAgent logo](./Figures/MOAgent_Logo.png)
MOAgent is a graphical user interface which enables searching for biomarker candidates without coding skills in MS data by using Artificial Intelligence. An early version of the used algorithms from [MOBiceps](https://github.com/JensSettelmeier/MOBiceps) within [MOAgent](https://github.com/JensSettelmeier/MOAgent) was applied in [Nature Communications, 2023](https://www.nature.com/articles/s41467-023-42101-z) to identify phenotype-specific proteins of myeloproliferative neoplasms (blood cancer).

Quick links:
- [MOAgent Installation Instructions](#moagent-installation-instructions)
- [Get started in three steps](#get-started-in-three-steps)
- [Advanced installation outside of a Virtual Machine (VM)](#advanced-installation-outside-of-a-virtual-machine-vm)
- [MOAgent Tutorial](#moagent-tutorial)
- [Demo](#demo)
- [Example files and file requirements](#example-files-and-file-requirements)
- [General notes](#general-notes)


# MOAgent Installation Instructions

## Minimal System Requirements

| Requirement     | Specification                                             |
|-----------------|-----------------------------------------------------------|
| **Operating System** | Ubuntu 18.04/20.04/22.04<br> Windows 8.1/10/11<br> MacOS 10.15 - 14 |
| **CPU Architecture** | x86_64 (64-bit Intel or AMD CPUs with Virtualization support)                     |
| **CPU Cores**        | 4 cores                                             |
| **RAM**              | 8 GB RAM   
| **Storage**              | 50 GB     

Follow the steps below to install and use MOAgent:
## Get started in three steps

1. Install [VirtualBox](https://www.virtualbox.org/)

2. Download and extract [MOAgentVM](https://zenodo.org/records/10715409?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjAwMDY3MGFlLWZkY2YtNGU5OC1hODlkLTRiMTIyMjA4NDJkNSIsImRhdGEiOnt9LCJyYW5kb20iOiI0OGFlZmZkZjEzYWY3N2Q0ODllNDI4OGExNDc2ZTA1OSJ9.sDMnyH-ZpRNI33_hEe7sHvJAe1xD_D_4gfSeK1xEOwV0mjk_-jASbw9RI7a2WiRXJ2tY3-sqEXYRFuzkvdpsSw)

3. Open MOAgentVM.vbox file with VirtualBox
   (Default username: moagent, password: 123)

After login MOAgent will start automatically. If not, use the desktop shortcut MOAgent.


## Advanced installation outside of a Virtual Machine (VM)  
### Prerequisites

- [MOBiceps](https://github.com/wollscheidlab/MOBiceps)
- [Anaconda](https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh) (We recommend to use conda or other virtual python environments)
- [docker](https://docs.docker.com/engine/install/ubuntu/) (If you want to convert raw data)


### Installation Instructions:
1. Install Anaconda

    Download  and install Anaconda 23.3.1 from [here](https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh).

    For Ubuntu 20.04 LTS users:
    In the download folder where the downloaded anaconda file is located, open a terminal and execute:

    ```bash
    $ bash Anaconda3-2023.03-1-Linux-x86_64.sh
    $ yes       # to install
    $ enter     # for default path
    $ yes       # to init anaconda and make changes in your bash
    ```

2. Create the Conda Environment

    Open a terminal within the git folder where the .yml file is located and execute the following command:

    ```bash
    $ conda env create -f moagent.yml
    ```

3. Install the iq R package.

    ```bash
    $ conda activate MOAgent
    $ R
    $ install.packages("iq")
    ```

4. Start MOAgent
    Open a terminal
    ```bash
    $ conda activate MOAgent
    $ python MOAgent.py
    ```


# MOAgent Tutorial
For Spectronaut users, you need to use the [iq.rs](https://github.com/tvpham/iq/releases/download/v1.1/iq.rs) report schema in the repo to extract the needed columns for MOAgent.
For Fragpipe users, we tested functionality with diann and ionquant output of the LF-MBR and DIA_SpecLib_Quant workflow. In general you can use any feature expression matrix where rows represent samples and columns features. This tutorial will guide you through using the MOAgent graphical user interface (GUI). This GUI allows you to convert data formats, generate feature tables, and use RFE++ for feature selection.

## GUI Layout

The GUI is organized into three main sections, which are accessible through the "Workflow" dropdown menu:

- **Data Convert**: This section is used for converting data from one format to another.
- **Feature ML Table**: This section is used for generating a feature table.
- **RFE++**: This section is used for Recursive Feature Elimination (RFE).

### Data Convert

MOAgent GUI currently offers a data conversion functionality that can convert raw, mzXML and mzML into png, mzML or mzXML format. 
Alternatively, you can use the conversion functionality from the command line using the MOBiceps `expression_table.py` function directly. 

#### GUI

To use the data conversion workflow in the GUI:

![Screenshot: Data Convert section](./Figures/data_convert.png)

1. Select "Data Convert" from the "Workflow" menu. This will open the Data Convert section.
2. Chose the input format (for example mzML)
3. Chose the output format (for example mzXML)
4. Specify the number of processing threads (optional)
5. Hit the Start button
You will find two directories in the specified *Input directory* folder. One containing the original files, the other the conversions. 


#### Command Line

Alternatively, you can execute the MOBiceps `convertRAWMP.py` in the terminal. The following parameters are accepted:

- `--p` or `--path_to_folder`: Absolute path to the folder containing all files to be converted. (Default: Current working directory)
- `--s` or `--orig_format`: Source file format. (Default: 'raw')
- `--f` or `--file_format`: Target file format. (Default: 'mzML')
- `--c` or `--core_number`: Specifies the number of threads to be used to convert all files. -1 corresponds to all possible. (Default: -1)

To execute the script, navigate to its location in your terminal and use the following command:

```bash
python /path/to/MOBiceps/convertRAWMP.py --p /path/to/folder --s original_format --f target_format --c number_of_cores
```

or within your code if you installed MOBiceps via pip

```bash
import MOBiceps as mob
mob.convertRAWMP(original_format,target_format,number_of_cores)
```

### Feature ML Table

The "Feature ML Table" functionality allows for the conversion of search output data into a feature expression table that is compatible with the machine learning (ML) process. It also provides the option to perform imputation of missing values. You can access this functionality via the MOAgent GUI or the command line through the `expression_table.py` script.

#### GUI

To use the "Feature ML Table" feature in the GUI:

![Screenshot: Feature ML Table section](./Figures/feature_table.png)

1. Select "Feature ML Table" from the "Workflow" menu. This will open the Feature ML Table section.
2. In the 'Search output' field, specify the file containing your search output. You can use the 'Browse' button to navigate to the file.
3. In the 'Class annotations' field, specify the file that contains your class annotations. You can use the 'Browse' button to navigate to the file.
4. In the 'Output path' field, specify the directory where you want to save your output. You can use the 'Browse' button to navigate to the directory.
5. In the 'Imputation' dropdown menu, select the imputation method to be used. Currently "mean", "median", "zero", "gaussian" are supported. We recommend to use no imputation or your more sophisticated approaches from dedicated imputation packages.
6. In the 'Feature level' dropdown menu, select if the feature table should be constructed for peptide or protein level.
7. Click the 'Start' button to start the data conversion process.

#### Command Line

Alternatively, you can use the "Feature ML Table" function from the command line by executing the MOBiceps `expression_table.py`. The following parameters are accepted:

- `--s`: Path to search output. Currently Spectronaut and DIA-NN output is supported. (Default: Current working directory)
- `--c`: Path to class annotation file. (Default: Current working directory)
- `--o`: Output path. (Default: Current working directory)
- `--m`: Imputation method. Currently "mean", "median", "zero", "gaussian" are supported. (Default: "none")
- `--f`: Feature level. "peptide" and "protein" are supported. (Default: "peptide")

To execute the script, navigate to its location in your terminal and use the following command:

```bash
python /path/to/MOBiceps/expression_table.py --s /path/to/search/output --c /path/to/class/annotation --o /path/to/output
```

or within your code if you installed MOBiceps via pip

```bash
from MOBiceps.expression_table import create_rfe_expression_table
feature_expression_table = create_rfe_expression_table(path_to_search_output, path_to_class_annotation, path_to_output) 
```

### RFE++

You can use the RFE++ feature through the MOAgent GUI or directly from the command line.

#### GUI

To use the RFE++ feature in the GUI:

1. Select "RFE++" from the "Workflow" menu. This will open the RFE++ section.
    ![Screenshot: RFE++ section](./Figures/rfePP.png)
2. In the 'Search output or expression table' field, specify the file you want to use. You can use the 'Browse' button to navigate to the file.
3. In the 'Class annotations' field, specify the file that contains your class annotations. You can use the 'Browse' button to navigate to the file.
4. In the 'Replicate annotations' field, specify the file that contains your replicate annotations. You can use the 'Browse' button to navigate to the file.
5. In the 'Output directory' field, specify the directory where you want to save your output. You can use the 'Browse' button to navigate to the directory.
6. In the 'Bootstrap augmentation' check box, specify if bootstrap should be applied to augment the samples. The 'Noisy augmentation' check box specifies, if class-dependent Gaussian noise learned from the data should be applied during augmentation. 
7. In the 'Feature level' dropdown menu, select if the analyses should be done on peptide or protein level.
8. In the 'GPU support' check box, specify if a GPU should be used. By default, a GPU is not used. (Not available in VM. Only available if a GPU is installed - for experienced users)
9. In the 'Force handalbe amount of features' check box it can be specified, if up to less than 30 features should be filtered, even if the optimal phenotype classification is achieved with far more than 30 features. 
10. In the considered Classes field write in comma separated which classes should be considered in the analysis. If the field is empty, all available classes will be considered. 
10. Click the 'Start' button to estimate the most contributing phenotype-specific features.

#### Command Line

Alternatively, you can use the RFE++ feature from the command line by executing the `rfePlusPlusWF.py` script. The script accepts the following parameters:

- `--i`: Path to the folder containing the search output of Spectronaut or DIA-NN. (Default: Current working directory)
- `--c`: Path to the class annotation file.
- `--s`: Path to the sample annotation file. (Optional)
- `--o`: Output path. (Default: Current working directory)
- `--b`: Use bootstrapping augmentation. (Default: False)
- `--m`: Imputation method. Currently "mean", "median", "zero", "frequent" and "none" are supported. (Default: 'none')
- `--f`: Feature level. "peptide" and "protein" are supported. (Default: 'peptide')
- `--g`: Support for GPU if set to True. (Default: False)
- `--n`: Bootstrapping with noisy resampling. (Default: False)
- `--h`: Force the reduction to a handable  amount of features. (Default: True)
- `--p`: specify which classes should be considered. 

To execute the script, navigate to its location in your terminal and use the following command:

```bash
python /path/to/MOBiceps/rfePlusPlusWF.py --i /path/to/search/output --c /path/to/class/annotation --o /path/to/output --p classA classB classC
```

or within your code if you installed MOBiceps via pip

```bash
from MOBiceps.rfePlusPlusWF import execute_rfePP
most_contributing_features = execute_rfePP(path_to_search_output, path_to_class_annotation, path_to_output, phenotype_class_list) 
```

## Demo
To test MOAgent outside of the provided MOAgentVM hosted on Zenodo, you can use the provided input files in the Demo folder.
1. Therefore, make sure to set `--i` parameter of RFE++ function `rfePlusPlusWF.py` or `path_to_search_output` parameter of `execute_rfePP` of the `MOBiceps` package to `MOAgent/Demo/input/metabolite_expression_table.csv` or select this file for the `Search output or expression table` field in the GUI via the `Browse` button.
2. Additionally, set the `--c` parameter of RFE++ function `rfePlusPlusWF.py` or `path_to_class_annotation` of `execute_rfePP` of the `MOBiceps` package to `MOAgent/Demo/input/class_annotations.csv` or select this file for the `Class annotations` field in the GUI via the `Browse` button. 
3. Finally, set the `--o` parameter of RFE++ function `rfePlusPlusWF.py` or `path_to_output` of `execute_rfePP` of the `MOBiceps` package to `MOAgent/Demo/output` or select this path for the `Output directory` field in the GUI via the `Browse` button and hit the `Start` button.

The results of the MOAgent analysis will be available in the folder “<..>/Demo/output/”. They will be similar to the reported results which can be found here [More case studies](https://polybox.ethz.ch/index.php/s/IoEnfcmmIkqletP).  


# Example files and file requirements

The class annotation and sample annotation files need to have a specific structure as shown in the following.

#### Class annotation file
Make sure the column names are **files** and **class**. The file type should be **.csv**. The classes should not just be numerical. 
![Screenshot: class annotation file](./Figures/example_class_annotation_file.png)

#### Sample annotation file
Make sure the column names are **files** and **PatientID**. The file type should be **.csv**. 

![Screenshot: sample annotation file](./Figures/example_file_annotation_file_patient.png)

#### Spectronaut search output 
Spectronaut supports report exports in csv and tsv format. Change the file ending by renaming the file to **.txt**.

#### DIANN report from fragpipe
The DIANN main report file in a label free quantification default workflow from Fragpipe is **.tsv** and should be used. 

#### Output examples
![example output](./Figures/output_moagent.png)
[More case studies](https://polybox.ethz.ch/index.php/s/IoEnfcmmIkqletP)

# General notes
1. General help about VirtualBox (e.g. how to mount local drives to MOAgent) you can find in the [UserManual](http://download.virtualbox.org/virtualbox/UserManual.pdf)
2. We recommend accessing your data using [FileZilla](https://wiki.filezilla-project.org/Documentation), ssh (scp, sftp) and if necessary the VPN functionality within the VM in combination with the file browser. 
3. Have fun and please leave a star if you find this repo helpful!
4. If you have any questions, please do not hesitate to contact [jsettelmeier@ethz.ch](jsettelmeier@ethz.ch).
