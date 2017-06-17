# CPP 480 Cyber Attack Detection

Review Status: Not Reviewed

## Introduction
Currently, rule-based detection is being used to detect cyber-attack patterns within server/web
logs. This is a great solution for identifying potential security risks, however unless the rules
 specifically target a type of cyber attack, that particular pattern will not get detected. It
 may seem impossible to detect a pattern before acknowledging it, however it is possible through
 the use of unsupervised machine learning. Through the use of unsupervised machine learning
 patterns and grouping of the logs can get discovered and identified. As a stepping stone towards
  migrating the rule-based system to a machine learning system, a supervised learning will be
  used to replace the current existing rules.

## User Stories

U1. As a user, I want to be able to input server/web logs into CAD.

U2. As a user, for logs I have inputted, I want to be able to view classifications of cyber attacks
 in accordance to patterns in the logs.

## Common Terminologies

* Cyber attack - an attempt to damage, disrupt, or gain unauthorized access to a computer,
computer system, or electronic communications network.

* Server log - file automatically created and maintained by a server consisting of a list of
activities it performed.

* Neural networks - a computer system modeled on the human brain and nervous system.

* Supervised learning - machine learning task of inferring a function from labeled training data

* Unsupervised learning - machine learning algorithm used to draw inferences from datasets
consisting of
input data without labeled responses.

* DOS - Denial of Service; above normal network requests originating from specific or set of IP
Addresses.

* R2L - Remote to Local (User) Attacks; Attempt to gain login access as local user via FTP, SSH or
other protocols.

* U2R - User to Root Attack; When a logged in user tries to gain root or system access.

* Probing - Scanning for open ports on the network.

## Solution
Neural networks can be used to detect and identify DOS, R2L, U2R and Probing that may have
happened for a given server log. These discoveries can be used to figure out a better safety
measure of protecting our servers and data from harm.

A cyber-attack specific trained neural network model will be used to identify each cyber attack.
One for DOS, one for R2L, one for U2R and one for Probing Attacks.

There are many machine learning libraries that can be used to train our models.

We considered using Google Cloud Platform's Machine Learning Platform as it abstracts away the
overhead of managing infrastructure, provisioning servers and configuring networks.

We were also considering using AWS Machine Learning, however they don't support Neural Network
model training as of now and only support.

Ultimately we decided to use scikit-learn's Naive bayes to detect the cyber attacks. Naive bayes
is based on applying Bayes' theorem.

### Architecture

CAD will compose of four major components.

- Preprocessor - In charge of formatting the log files into serializable objects that can be
easily understood by the classifier.

- Classifier - Identify and mark all objects that categorize as DOS, R2L, U2R and Probing attacks.

- S3 - AWS S3 will be used to the store the marked and identified server logs.

- User Interface - Provide the user the ability to the view the marked file.

#### Data Flow

![Data Flow](images/DataFlow.png)

### Milestones

1. Properly pre-process the log data.

2. Successfully implement detection of DOS.

3. Successfully implement detection of R2L.

4. Successfully implement detection of U2R.

5. Successfully implement detection of Probing Attacks.

6. Create a user interface that allows users to provide a log and returns a classified log.

### Stretch Goals

1. Implement a neural network for either DOS, R2L, U2R or Probing Attacks.

### Out of Scope

1. CAD should be able to retrieve server logs from the local host.

2. CAD should be able to work with real time log data.

## Risks

1. New technology - My team is not familiar with security and also the plethora of new concepts
such as technologies, libraries, frameworks and working in a group. Neural networks is also a
topic that is still being researched today and hasn't been taught at our instutition.

2. Not full time - We are students that aren't able to dedicate 40 hours / week for this project. Students will also have
other obligations such as classes, jobs and etc. It is also expected that getting everyone up to speed on the topic and
development process will cause a lot of time to be invested early on. It is expected that progress will be slow in the
beginning.

3. Training Data - Unfortunately, we have not been provided with any training data. This will
definitely delay and potentially create an inaccurate neural network. This also adds a lot more
complexity and burden to the team, as we have to create our training data.

## Open Questions

## Post-Review

## Reference

1. [Cyber Attack](https://en.wikipedia.org/wiki/Cyber-attack)
2. [DOS](https://en.wikipedia.org/wiki/Denial-of-service_attack)
3. [Detection of DOS, Probing and R2L](https://pdfs.semanticscholar.org/060d/0c18c3f490720b62e40e7003aa7f75d50941.pdf)
4. [Efficient Classifiers for R2L and U2R attack](https://pdfs.semanticscholar.org/bbf5/bfe8c4fc238405df91f54849eabb2aadf1cb.pdf)
5. [Detecting U2R using ML](http://www.ijarcce.com/upload/2014/april/IJARCCE4J%20a%20revathi%20EPCglobal%20Gen-2%20RFID.pdf)
6. [Detecting Cyber Attacks with various IDS](https://www.idosi.org/wasj/wasj27(11)13/13.pdf)
7. [PortScan Detection](https://community.sophos.com/kb/en-us/115153)
