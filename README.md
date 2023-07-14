# BreachCheck

## Introduction

We strongly advise users to only utilize BreachCheck for their own emails and usernames. Do not misuse this tool or exploit it for malicious purposes. Respect the privacy and security of others by refraining from attempting to check passwords that do not belong to you.

Our aim is to promote responsible and ethical use of BreachCheck to empower individuals in securing their online presence. By adhering to these principles, we can collectively contribute to a safer digital environment for everyone.

## Usage

Fisrt clone and install
```bash
git clone https://github.com/v4resk/BreachCheck
cd BreachCheck
pip install -r requirements.txt
```

Before running BreachCheck, make sure to configure your API Key in the `conf.json` file. If you don't have one, sign-up on RapidAPI and choose the **Basic** plan (It's free) or Pro Plan (not free) for the [BreachDirectory API](https://rapidapi.com/rohan-patra/api/breachdirectory/)


To use BreachCheck, run the following command:
```bash
#Simple use, target can be username or email
python BreachCheck.py -t <target>

#Output passwords to a file
python BreachCheck.py -t <target> -oN target_passwords.txt
```

# Exemples 

![Email Target](/assets/screenshot_email_target.png)
