# FIT3170 Usability Accessibility Testing App

**Table of Contents**
<!-- TOC -->

- [FIT3170 Usability Accessibility Testing App](#fit3170-usability-accessibility-testing-app)
    - [Introduction](#introduction)
        - [Current Team members](#current-team-members)
    - [Usage](#usage)
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

<!-- /TOC -->

## Introduction

This application was built as part of a university project to develop a toolkit that would allow for the automatic testing of **usability and accessibility of target Android apps**. The purpose of this project is to allow developers to further improve their applications by addressing possible accessibility and usability flaws. This application utilises algorithms from previous research projects, some with initial source code and prototypes, and integrates them for more detailed output. 

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

## Usage 

Given an APK file, the app automatically explores all the different screens and, through the implementation of accessibility algorithms [2, 3, 4, 5], outputs accessibility and usability issues found. The website also has a login functionality that allows users to store and revisit their results. 

### Gifdroid
Gifdroid is an image-processing algorithm which generates a UTG from a video input and apk file. 
### Owleye 
OwlEye is a tool which automatically detects and localizes UI display issues in the screenshots of the application under test.
### StoryDistiller
StoryDistiller automatically generates the storyboard for an application with rich kinds of features through reverse engineering, and assists different roles to review and analyze apps efficiently.
### Xbot
Xbot is a page exploration tool which outputs a file of accessibility issues. 
### Tappable/Tapshoe
Tappable explores how tappable a button is perceived by a user. Given an image and .xml file, the model will output a heatmap and tappability rating on clickable objects that the model perceives as untappable. 
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

