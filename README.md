# Grade Assistant Proof of Concept (PoC)
Use AI to grade open-response questions on a Google Forms Quiz or Application

Upload projected grades and grade book to Google Sheets

## Usage

1. Update your credentials to use this code. (step-by-step walkthrough found [here](#Update-Your-Credentials))
2. Update your environment. (step-by-step walkthrough found [here](#Setting-Up-Your-Environment))
3. Run `python3 main.py` in a python-equipped terminal.

<br>

_____________________________________________________

<br>

<br>

<br>

## Setting Up Your Environment

In a Linux shell/terminal: follow the lines in the `update.bash` file:
1. `pip install -r requirements.txt`
2. `pip install apiclient (1.0.4)`
3. `pip install getpass`
4. `pip install replicate`

<br>

_____________________________________________________

<br>

<br>

<br>

## Common Errors

### Unknown Module
1. If the unknown module is 'replicate'
   1. Try running `pip install replicate` again
   2. Try running `pip install --upgrade --force-reinstall replicate` if the above does not work
2. If the unknown module is 'getpass'
   1. Try running `pip install getpass` again
   2. Try running `pip install --upgrade --force-reinstall getpass` if the above does not work


<br>

_____________________________________________________

<br>

<br>

<br>

## Update Your Credentials

1. Download the `credentials.json` file
2. Update the `client-ID` and `client-secret` with your own, given to you by Google when you register an OAuth 2.0 client with Google via Google API Dashboard's [credential manager]([https://console.cloud.google.com/apis/dashboard](https://console.cloud.google.com/apis/credentials)). Go to the [Getting an OAuth Token section](#Getting-an-OAuth-Token) of this readme for a walkthrough.
   1. You are required to pass an OAuth Consent Screen. (Walkthrough found [here](#OAuth-consent-screen))
3. Update the AI token
   1. Go to [replicate's website](https://replicate.com/docs/get-started/python#authenticate) to create a free account (by linking your GitHub account). NOTE: you get 10 free API calls to the AI. You may wish to add a payment method. This will charge you approx $0.000021 per API call using the default settings. Feel free to set a monthly "Spend Limit" on [their billing page](https://replicate.com/account/billing). Supported models and pricing can be found on [their pricing page, in the language models section](https://replicate.com/pricing#language-models)
      1. Model Options:
         1. llama-2-13b
         2. *llama-2-70b* (**default**)
         3. llama-2-7b
         4. meta-llama-3-70b
         5. meta-llama-3-8b
         6. mistral-7b-v0.1
   2. Once you have an API token from [replicate's token section on their website](https://replicate.com/account/api-tokens): copy the token and run the following in a Python-enabled terminal.
      1. `python3 update.py`
      2. `update_token`
      3. `my_API_token` (make sure to replace `my_API_token` with the token from [replicate's token section on their website](https://replicate.com/account/api-tokens).
4. Update the Google Form ID
   1. Run the update script using the following code in a Python-enabled terminal. 
      1. `python3 update.py [OPTIONAL: Google_Form_URL]` (make sure to replace `[OPTIONAL: Google_Form_URL]` with the URL of your Google form **AND** *skip the 3rd step if you choose to do this*)
      2. `update_form`
      3. `Google_Form_URL` (make sure to replace `Google_Form_URL` with the URL of your Google form **ONLY IF** *you did not add the optional URL in the first step*)
         1. NOTE: you will not see an update as this will be read in as a password and will therefore be invisible.
6. Update the Google Sheets ID
   1. Run the update script using the following code in a Python-enabled terminal. 
      1. `python3 update.py [OPTIONAL: Google_Sheet_URL]` (make sure to replace `[OPTIONAL: Google_Sheet_URL]` with the URL of your Google sheet **AND** *skip the 3rd step if you choose to do this*)
      2. `update_spreadsheet`
      3. `Google_Sheet_URL` (make sure to replace `Google_Sheet_URL` with the URL of your Google sheet **ONLY IF** *you did not add the optional URL in the first step*)
         1. NOTE: you will not see an update as this will be read in as a password and will therefore be invisible.

<br>

_________________________

<br>

<br>

## Getting an OAuth Token

Go to [Google Cloud Consol's](https://console.cloud.google.com/) website and select the `APIs & Services` button.

Navigate to the `credentials` tab and select the `+ CREATE CREDENTIALS` button to reveal a drop-down of 4 items. 

Select the second item (`OAuth client ID`, sub-text: "Requests user consent so your app can access the user's data")

This will bring you to the "Create OAuth client ID" page. **However**, to be able to continue you need to fill out the `OAuth consent screen` and pass the screening process. The step-by-step process is in the [OAuth consent screen](#OAuth-consent-screen) section.

Finally, click the application type dropdown, select `Desktop app`, and name it whatever you'd like.

Click the blue `CREATE` button at the bottom of the page.

A pop-up window will appear with your `client-ID` and `client-secret`. Save both somewhere secure.

<br>

_________________________

<br>

<br>

## OAuth consent screen

Click on External and hit the blue `CREATE` button.

![image](readme_images/OAuthConcentScreen.png)

____________________________________________

<br>

<br>

## Edit app registration - OAuth consent screen

Enter a name in the "App Name" text-entry box and enter your email in the "User Support Email" text-entry box.

Scroll down to the "Developer contact information" section. 
Enter your email again into the "Email Address" text-entry box with the subtext: "*These email addresses are for Google to notify you about any changes to your project.*"

**Leave everything else blank.**

✔️ Select the `Save and Continue` button at the bottom of the page, **leaving everything else blank**.

____________________________________________

<br>

<br>

## Edit app registration - Scopes

Select the `ADD OR REMOVE SCOPES` button to open a table of scopes. The following table can be found on page 3. (results 22-27)

|add scope| API | Scope | User-facing description |
|---------|-----|-------|-------------------------|
|☐|Google Forms API | .../auth/drive | See, edit, create, and delete all of your Google Drive files|
|☐|Google Forms API | .../auth/drive.file | See, edit, create, and delete only the specific Google Drive files you use with this app|
|☐|Google Forms API | .../auth/forms.body | See, edit, create, and delete all your Google Forms forms|
|☐|Google Forms API | .../auth/drive.readonly | See and download all your Google Drive files|
|☑️|Google Forms API | .../auth/forms.body.readonly | See all your Google Forms forms|
|☑️|Google Forms API | .../auth/forms.responses.readonly | See all responses to your Google Forms forms|

Select the two rows above (26: `forms.body.readonly` and 27: `forms.responses.readonly`)

Scroll down and select the blue `UPDATE` button at the bottom to close the table and return to the previous page (Edit app registration - Scopes)

✔️ Select the `SAVE AND CONTINUE` button at the bottom of the page.

____________________________________________

<br>

<br>

## Edit app registration - Test users

Click the `+ ADD USERS` button. 

Add the Gmail account that owns the Google Form OR has viewing access to the Google Form's results.

✔️ Scroll to the bottom and select the `SAVE AND CONTINUE` button.

____________________________________________

<br>

<br>

## Edit app registration - Summary

Here you will find a summary of the previous selections. 

✔️ Select the `BACK TO DASHBOARD` button to return to your dashboard and create an OAuth token. You can read more about creating an OAuth token in the [Getting an OAuth Token](#Getting-an-OAuth-Token) section of the README.

<br>

<br>

👏 Congradulations 🎉🎊

You have completed the OAuth Consent Screen and **PASSED**!

<br>
