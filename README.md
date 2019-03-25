# Setting Up the Environment
## Install Python 3.6
- Check if you already have Python 3.6 installed. Type `python3 --version` on Terminal. If you see 3.6.*, then you're all set and can skip this section and proceed to "Install Python3 Virtual Environment Module" section.
- Otherwise, go to [this link](https://www.python.org/downloads/release/python-367/ "this link") to download and run the Python 3.6 install file. Note: Although latest Python version is 3.7 and is usually installed conveniently with `brew` in OSX, Python 3.7 is currently imcompatible with Tensorflow which powers the neural network backend of our application. Since `brew` doesn't let you install a specific Python3 version, you have to install specifically Python 3.6 by downloading the installation file above.
- Verify your installation by again typing `python3 --version` on Terminal.  You should now see Python 3.6.*

## Install Python3 Virtual Environment Module, then Create and Activate Virtual Environment
- First, install the virtual environment module for Python3. In terminal, simply type `pip3 install virtualenv`
- In Terminal, navigate to the directory where you'd like to create the virtual environment folder. Use any name for the virtual environent folder. We will use the folder name `virtual-env-folder` in this example.
- Enter `python3 -m virtualenv virtual-env-folder`
- Then, activate the virtual environment for your current shell process by running `source virtual-env-folder/bin/activate`. Note: every time you open a new Terminal window, you need to perform this step to activate the virtual environment for the current shell process before you can run the application.

## Install Package Dependencies within Virtual Environment
- Make sure you've activated your virtual environment by executing
`source virtual-env-folder/bin/activate`
in your current shell process.
- In Terminal, navigate to the folder of the application repository. Then, run
`pip install -r requirements.txt`
This will install all the package dependencies needed for our application as outlined in *requirements.txt*

# Folder Structure
Folder structure is as follows:  
| miicloud_sandbox_apis.py   
| requirements.txt   
| input/persons/   
| _ _ _ _ _ _ will_smith/   
| _ _ _ _ _ _ _ _ _ _ will_smith_001.jpg   
| _ _ _ _ _ _ _ _ _ _ will_smith_002.jpg   
| _ _ _ _ _ _ _ _ _ _ will_smith_003.jpg   
| _ _ _ _ _ _ tom_hanks/   
| _ _ _ _ _ _ _ _ _ _ tom_hanks_001.jpg   
| _ _ _ _ _ _ _ _ _ _ tom_hanks_002.jpg   
| input/test_images/   
| _ _ _ _ _ _ test_001.jpg   
| _ _ _ _ _ _ test_002.png   
| _ _ _ _ _ _ test_003.jpg   
| _ _ _ _ _ _ test_004.jpg   
| output/persons/   
| _ _ _ _ _ _ will_smith_001_<timestamp>.jpg   
| _ _ _ _ _ _ will_smith_002_<timestamp>.jpg   
| _ _ _ _ _ _ will_smith_003_<timestamp>.jpg   
| _ _ _ _ _ _ tom_hanks_001_<timestamp>.jpg   
| _ _ _ _ _ _ tom_hanks_002_<timestamp>.jpg   
| output/test_images/   
| _ _ _ _ _ _ output_test_001_<timestamp>.jpg   
| _ _ _ _ _ _ output_test_002_<timestamp>.jpg   
| _ _ _ _ _ _ output_test_003_<timestamp>.jpg   
| _ _ _ _ _ _ output_test_004_<timestamp>.jpg   

# Running the sample code
- In Terminal, make sure you've activated the virtual environment in the current shell process by running `source virtual-env-folder/bin/activate`. 
- Simply run: `python3 miicloud_sandbox_apis.py`
- Now look in the `output/persons` and `output/test_images` folder.  It should have images with bounding boxes around each face with tags of "known" faces in the `output/test_images` folder.
