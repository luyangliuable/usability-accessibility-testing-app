# FIT3170 Usability Accessibility Testing App

**Table of Contents**

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**
<!-- TOC -->

- [FIT3170 Usability Accessibility Testing App](#fit3170-usability-accessibility-testing-app)
    - [Introduction](#introduction)
    - [Usage](#usage)
        - [Prerequisites](#prerequisites)
            - [Note](#note)
        - [How to run app](#how-to-run-app)
        - [Current Team members](#current-team-members)
        - [Gifdroid](#gifdroid)
        - [Owleye](#owleye)
        - [StoryDistiller](#storydistiller)
        - [Xbot](#xbot)
        - [Tappable/Tapshoe](#tappabletapshoe)
        - [Venus](#venus)
    - [Pre-requisites](#pre-requisites)
    - [Environment & Setup](#environment--setup)
    - [Running the application](#running-the-application)
    - [Known Issues](#known-issues)
    - [Sources & References](#sources--references)
        - [Algorithm Papers](#algorithm-papers)
        - [Related Git Repositories](#related-git-repositories)

<!-- markdown-toc end -->

[![Flask Backend Test](https://github.com/luyangliuable/Usability-Accessibility-Testing-App/actions/workflows/python-app.yaml/badge.svg)](https://github.com/luyangliuable/Usability-Accessibility-Testing-App/actions/workflows/python-app.yaml)

## Introduction
This application was built as part of a university project to develop a toolkit that would allow for the automatic testing of **usability and accessibility of target Android apps**. The purpose of this project is to allow developers to further improve their applications by addressing possible accessibility and usability flaws. This application utilises algorithms from previous research projects, some with initial source code and prototypes, and integrates them for more detailed output.

## Usage

Given an APK file, the app automatically explores all the different screens and, through the implementation of accessibility algorithms [2, 3, 4, 5], outputs accessibility and usability issues found. The website also has a login functionality that allows users to store and revisit their results.

### Prerequisites
* Docker
    * [mac os](https://docs.docker.com/desktop/install/mac-install/)
    * [mac os w/ m1 chip](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64)
    * [windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)


* Docker-compose
    * mac os
    ```bash
        brew install docker-compose
    ```

    * [windows](https://docs.docker.com/compose/install/)

#### Note
* Ensure port 3001-3006 and 5005 is not taken
* No instance of redis or mongodb should be running already on your local environment


### How to run app
1. Go into project directory
2. build

```bash
docker-compose build
```
3. run
```bash
docker-compose up --build
```

4. Navigate to http://127.0.0.1:3001/


### Current Team members

System Architecture | RTE Scrum Masters | Product Managers
--- | --- | --- |
Ansh Bajpai | Arragon Prosser | Benjamin Woang
Dale Thomas Beniga | Emily Lam | Jimmy Tran
Dhanushka Perera | Javeriya Nadaf | Joshua Jaden
Eric Chen | Sifan Mao | Pooja Seshadri
Leonardo Prasetyo
Luyang Liu
Mark Diedericks
Trevin Dilhan Wadugodapitiya
Zhongxun Pan


### Gifdroid
### Owleye
### StoryDistiller
StoryDistiller automatically generates the storyboard for an application with rich kinds of features through reverse engineering, and assists different roles to review and analyze apps efficiently.
### Xbot
Xbot is a page exploration tool which outputs a file of accessibility issues. 
### Tappable/Tapshoe
Tappable explores how tappable a button is perceived by a user. Given an image and .xml file, the model will output a heatmap and tappability rating on clickable objects that the model perceives as untappable. The model is a modified ResNet18 which accepts the input image and a binary mask of the tappable object.

### Venus
Venus explores accessibility issues in an application and requires a .dl file and produces a .csv document. 

## Pre-requisites

## Environment & Setup

## Running the application

## Known Issues


## Sources & References

### Algorithm Papers
[1] Chen, S., Fan, L., Chen, C., Su, T., Li, W., Liu, Y., & Xu, L. (2019, May). Storydroid: Automated generation of storyboard for Android apps. In 2019 IEEE/ACM 41st International Conference on Software Engineering (ICSE) (pp. 596-607). IEEE. <br />
[2] Chen, S., Chen, C., Fan, L., Fan, M., Zhan, X., & Liu, Y. (2021). Accessible or Not An Empirical Investigation of Android App Accessibility. IEEE Transactions on Software Engineering. [3] Liu, Z., Chen, C., Wang, J., Huang, Y., Hu, J., & Wang, Q. (2020, September). Owl eyes: Spotting ui display issues via visual understanding. In 2020 35th IEEE/ACM International Conference on Automated Software Engineering (ASE) (pp. 398-409). IEEE. <br />
[4] E. Schoop, X. Zhou, G. Li, Z. Chen, B. Hartmann and Y. Li, "Predicting and Explaining Mobile UI Tappability with Vision Modeling and Saliency Analysis", CHI Conference on Human Factors in Computing Systems, 2022. Available: 10.1145/3491102.3517497. <br />
[5] Zhang, Z., Feng, Y., Ernst, M. D., Porst, S., & Dillig, I. (2021, August). Checking conformance of applications against GUI policies. In Proceedings of the 29th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (pp. 95-106). [6] Feng, S., & Chen, C. (2021). GIFdroid: Automated Replay of Visual Bug Reports for Android Apps. arXiv preprint arXiv:2112.04128. <br />

### Related Git Repositories
https://github.com/sidongfeng/gifdroid <br>
https://github.com/tjusenchen/StoryDistiller <br>
https://github.com/20200501/OwlEye <br>
https://github.com/MulongXie/UIED <br>
https://github.com/chenjshnn/WAE <br>
https://github.com/GUIDesignResearch/GUIGAN <br>
https://github.com/budtmo/docker-android
