# ChEMBL Explorer
#### Explore the ChEMBL platform and download customized bioactivity datasets

## Features

- Search for diseases and genes in ChEMBL platform
- See a summary of targets and bioactivity data available for your search query 
- Create a custom dataset by selecting your desired specific columns of bioactivity data
- Download the dataset as a CSV file

## Live Demo

Not only you can use this repo as a GUI in your local development enviroment, but a live demo is also available at https://chemblxplore.herokuapp.com

## Development

Want to contribute? That is so nice!

**Step 1**: Be sure that you use python version 3.7.10 and you have installed pip package manager properly

**step 2**: Install streamlit via this command

```sh
pip install streamlit
```


**Step 3**: Clone this repository
```sh
git clone https://github.com/AramDonyaee/ChEMBL-Explorer.git
```
**Step 4**: Download Miniconda for better development experience and virtual environment management from https://docs.conda.io/en/latest/miniconda.html  

**Step 5**: Install Miniconda and launch Anaconda Propmt  

**Step 6**: Navigate to the directory in which you have cloned this repository  

**Step 7**: Create a virtual environment and then activate it:  

```sh
conda create -n <your_environment_name> python=3.7.10
conda activate <your_environment_name>
```
**Step 8**: While you are in your activated conda environment run this command:
```sh
pip install -r requirements.txt
```
**Step 9**: After installing the requirements, navigate to my_component directory and use this command to run your stremlit app:
```sh
streamlit run Main.py
```
## License
MIT