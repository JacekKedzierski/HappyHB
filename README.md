# HappyHB

**Description:**

HappyHB is a program designed to analyze a given molecular structure, identify hydrogen bond donors and build a hydrogen bond network. It accepts the molecular structure in PDB (Protein Data Bank) format. This README provides an overview of how to install and use the program.

**Installation:**

To use HappyHB, you will need to have Python 3 installed on your system. If you haven't already installed Python 3, you can download it from the official Python website (https://www.python.org/).

Once you have Python 3 installed, you can follow these steps to obtain the HappyHB program files:

1. Open your terminal.

2. Use the `git` command to clone the HappyHB repository from GitHub. Run the following command:

    ```bash
    $ git clone https://github.com/lillgroup/HappyHB.git
    ```

This will download the program files to your local machine.

**Example Usage:**

Here is a simple example of how you can use HappyHB:

1. Navigate to the directory where you have the HappyHB program files.

2. Place your molecular structure in PDB format in the same directory or provide the path to your PDB file.

3. Run the program using the command:

    ```bash
    $ python HappyLoop.py --directory Input/Development
    ```

4. HappyHB will process your PDB file and provide you with information about the hydrogen bond donors and their interactions.

**Note:**

- Ensure that your PDB file is correctly formatted and contains the necessary structural information for hydrogen bond analysis.
- For more advanced usage and customization options, please refer to the program's documentation.
