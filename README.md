# BXER Usability Accessibility Testing App

![App Logo](BXER.png)

**Table of Contents**

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Introduction](#introduction)
- [Getting Involved](#getting-involved)
- [Versioning strategy](#versioning-strategy)
- [Git pull strategy](#git-pull-strategy)
    - [Merging](#merging)
    - [Git flow](#git-flow)
    - [Summary Information](#summary-information)
    - [Adding a New Algorithm](#adding-a-new-algorithm)
    - [Future Goals](#future-goals)
- [Usage](#usage)
    - [Prerequisites](#prerequisites)
        - [Note](#note)
    - [How to run app](#how-to-run-app)
- [Team Information](#team-information)
    - [Current Team members](#current-team-members)
- [Algorithms information](#algorithms-information)
    - [Gifdroid](#gifdroid)
    - [Owleye](#owleye)
    - [StoryDistiller](#storydistiller)
    - [Xbot](#xbot)
    - [Tappable/Tapshoe](#tappabletapshoe)
    - [Venus](#venus)
- [Known Issues](#known-issues)
- [Sources & References](#sources--references)
    - [Related Git Repositories](#related-git-repositories)

<!-- markdown-toc end -->

[![Flask Backend Test](https://github.com/luyangliuable/Usability-Accessibility-Testing-App/actions/workflows/python-app.yaml/badge.svg)](https://github.com/luyangliuable/Usability-Accessibility-Testing-App/actions/workflows/python-app.yaml)

## Introduction
This application was built as part of a university project to develop a toolkit that would allow for the automatic testing of **usability and accessibility of target Android apps**. The purpose of this project is to allow developers to further improve their applications by addressing possible accessibility and usability flaws. This application utilises algorithms from previous research projects, some with initial source code and prototypes, and integrates them for more detailed output.

## Getting Involved
This application is currently open source.

## Versioning strategy
The Versioning strategy for this app is **SemVer**.
* For example
* when going from 1.2 to 1.3 you are adding in non-breaking improvements.
* when going from 1.2 to 2.0, then something is probably going to break. 

This is important because there are Api endpoints involved in this application meaning that when there is a significant change the app may break but improvement and fixes can does not have to increment the digit value of the version.


## Git pull strategy

### Merging
* Creator document change in a merge request.
* All change to main branch go through a pull/merge request.
* At least 2 reviewer must agree to the merge before it can proceed.
* If a comment is declined the person must comment what the issue with the code is.

### Git flow
* Release branch
  * Contains release versions of the code
  * Naming convention: release@ver##.##
* Feature branch
  * Development branch on wor:wking on a new feature
  * Naming convention: feature/<new_feature>
* Main branch
  * Contains the most up to date and stable code.
  * Deployment will be performed using ci/cd on main branch
* Temporary branches
  * Contains spikes or act as a placeholder for possible changes
  * Naming convention: #<branch_name>
* Hotfix
  * When a major fault occurs in the main and deployed application. The branch is spun off to hotfix to be fixed immediately and put back

![git flow](https://www.gitkraken.com/wp-content/uploads/2021/03/git-flow-4.svg)

### Summary Information
The goal is to provide a convenient way for both software developers and ui/ux designers alike to identify for display bugs and ui issues. The app combines various machine learning algorithms to provide an comprehensive overview of ui issues.

Current the application is able to:
* Identify display bugs
* Identify UI accessibility issues.
* Identify buttons that are deemed with a low capability rating.

### Adding a New Algorithm

1. Place the source code of the new machine learning algorithm into the algorithms folder.
```
.
├── algorithms
│   ├── app
│   │   └── ~
│   ├── archive_docker_apps
│   │   └── gifdroid_app
│   ├── droidbot
│   ├── gifdroid
│   ├── owleye
│   ├── storydistiller
│   ├── tappability
│   ├── ui-checker
│   └── xbot
```

2. Add the execution command of the code and environment variables into docker compose. For example, Tappability is a an algorithm the rates tappable UI elements on how tappable they are. It's docker-compose segment is:

```yaml
  tappability:
    build:
      context: ./algorithms/tappability/
    command: python3.8 app.py
    container_name: bxer.tappability
    ports:
      - '3007:3007'
    volumes:
      - './.data:/home/data'
    cpu_percent: 30
```

3. Add a dockerfile in the algorithm folder that configures the docker container.
```
FROM ubuntu:18.04 AS builder

RUN apt-get update
RUN apt upgrade -y

# Installing basic linux tools and build tools here...
RUN apt install curl -y
RUN apt-get install unzip -y

# Installing Python 3.8 and pip3 here...

# Install Dependencies here...

# Copy Source Code and Run Script here...
```

### Future Goals
* Make API endpoints be assessible allowing to run algorithms.
* Continue adding more algorithms to detect accessibility issues.
* Give recommendation on how to address raised accessibility issues in the App.

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


### How to run entire app
1. Git pull and go into project directory
```
git pull https://github.com/luyangliuable/Usability-Accessibility-Testing-App.git ~/

cd ~/FIT3170_Usability_Accessibility_Testing_App/
```

3. build

```bash
docker-compose build
```
3.  Run
```bash
docker-compose up --build
```

4. Navigate to 
```
http://127.0.0.1:3001/
```

## Team Information
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

## Algorithms information

### Gifdroid
Gifdroid is a light-weight image-processing approach to automatically replay the video
(GIF) based bug reports for Android apps
### Owleye
Owleye is a tool to automatically detect and localize UI display issues in the screenshots of the
application under test.
### StoryDistiller
StoryDistiller automatically generates the storyboard for an application with rich kinds of features through reverse engineering, and assists different roles to review and analyze apps efficiently.
### Xbot
Xbot is a page exploration tool which outputs a file of accessibility issues. 
### Tappable/Tapshoe
Tappable explores how tappable a button is perceived by a user. Given an image and .xml file, the model will output a heatmap and tappability rating on clickable objects that the model perceives as untappable. The model is a modified ResNet18 which accepts the input image and a binary mask of the tappable object.

### Venus
Venus explores accessibility issues in an application and requires a .dl file and produces a .csv document. 


## Known Issues
Please refer to the [issues section](https://github.com/luyangliuable/Usability-Accessibility-Testing-App/issues) of this Github repository.


## Sources & References
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
