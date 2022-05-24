# Synthetics-Cards-Generation

<!-- PROJECT SHIELDS -->
<!--
*** This template uses markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url] [![Forks][forks-shield]][forks-url] [![Stargazers][stars-shield]][stars-url] [![Issues][issues-shield]][issues-url]

**Structured synthetic French data generation system with Python for CNN**

<!-- ABOUT THE PROJECT -->
## About The Project

This project allows the generation of procedurally structured data to train a CNN image classification model.

### Built With

* 🖊️ OpenCV
* 🐙 Github
* 💻 Python

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Dowload the project and extract.

Install requeriments :

```
OpenCV
PIL
Numpy
Pandas
Tqdm
```

### Installation
 
1. Clone the repo
```sh
git clone [https://github.com/NicolasBrondin/basic-readme-template](https://github.com/darkphenix/Synthetics-Cards-Generation)
```

2. Open the README.md file and execute the following command


<!-- USAGE EXAMPLES -->
## Usage

3. Generated the files

Arguments :
```
Structure :

    0 : CNI OLD
    1 : CNI OLD verso
    2 : CNI
    3 : CNI verso
    4 : Permis conduire
    5 : Permis conduire verso
    6 : PASSPORT
    
    
iteration : Generation number

path_fold : Path destination of generations

name_structure : Name file structure xlsx
```
```sh
python <structure> <iteration> <path_fold> <name_structure>
```

4. Generated noise

Arguments :

Structure :

    0 : CNI OLD
    1 : CNI OLD verso
    2 : CNI
    3 : CNI verso
    4 : Permis conduire
    5 : Permis conduire verso
    6 : PASSPORT
    
path : Path destination of generations noise

name : Name file structure noise xlsx

```
--rezize_min | --rezize_max = size of picture (400px - 1200px)
--blur_back = Background blur (1-10)
--line_back = Generate n lines on background (1 - 1000)
--noise =  Noise on document (1-15)
--blur =  Blur on document (0-2.0)

--color =  Color on document (0-2.0)
--constrast_max | --constrast_min =  Contrast maximum and constrast minimum on document (0-2.0)
--brightness_max | --brightness_min =  Brightness maximum and brightness minimum on document (0-2.0)
 ``` 

```sh
python <structure> <path_fold> <name_structure> <--optional> 
```

<!-- CONTACT -->
## Contact
- D@RK PH3N!X -
