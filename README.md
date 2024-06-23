# Grade Assistant Proof of Concept (PoC)
Use AI to grade open-response questions on a Google Forms Quiz or Application

Upload Google Form responses, projected grades, and resulting grade book to Google Sheets

###### Please note this readme's [Possible Considerations for Enterprise Use section](#Chapter-3:-Possible-Considerations-for-Enterprise-Use) before implementing this codebase for enterprise use. With that in mind, this is a Proof of Concept: we have taken shortcuts that you may wish to fix before using this codebase directly for enterprise use.

<br>

## Table of Contents

### **Contains:**

- [Usage](#Usage)
   - [Run the Code](#Run-the-Code)
   - [Setting Up Your Environment](#Setting-Up-Your-Environment)
   - [Update Your Credentials](#Update-Your-Credentials)
      - [Startup Endpoints](#Startup-Endpoints)
      - [Getting an OAuth Token](#Getting-an-OAuth-Token)
      - [Passing Google's OAuth Consent Screen](#OAuth-consent-screen)
   - [Common Errors](#Common-Errors)
- [Expected Output](#Expected-Output)
   - [Expected Local Output Files](#Expected-Local-Output-Files)
   - [Expected Google Output Files](#Expected-Google-Output-Files)
   - [What Do The Columns Mean?](#What-Do-The-Columns-Mean?)
- [Possible Considerations for Enterprise Use](#Possible-Considerations-for-Enterprise-Use)
   - [Security](#Security)
   - [Better AI training](#Better-AI-training)
   - [Improving API call speed (Multithreading)](#Improving-API-call-speed-Multithreading)

<br>

_____________________________________________________

<br>

<br>

<br>

<br>

<br>

# Usage

<br>

## Run the Code
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

1. Update your credentials to use this code. (step-by-step walkthrough found [here](#Update-Your-Credentials))
2. Set up your environment. (step-by-step walkthrough found [here](#Setting-Up-Your-Environment))
3. Run `python3 main.py` in a python-equipped terminal.

<br>

_____________________________________________________

<br>

<br>

<br>

<br>

<br>

## Setting Up Your Environment
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

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

<br>

<br>

## Common Errors
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

### Unknown Module
1. If the unknown module is 'replicate'
   1. Try running `pip install replicate` again
   2. Try running `pip install --upgrade --force-reinstall replicate` if the above does not work
2. If the unknown module is 'getpass'
   1. Try running `pip install getpass` again
   2. Try running `pip install --upgrade --force-reinstall getpass` if the above does not work

<br>

### 400 Error When Uploading Local CSV to Google Sheets
###### Error will look like this:
```cmd
<HttpError 400 when requesting https://sheets.googleapis.com/v4/spreadsheets/$Sheet_ID:batchUpdate?alt=json returned "Invalid requests[0].updateCells: Attempting to write column: 26, beyond the last requested column of: 25". Details: "Invalid requests[0].updateCells: Attempting to write column: 26, beyond the last requested column of: 25">
```
This is caused by the default maximum limit of columns imposed by Google Sheets on your Google Spreadsheet. Make sure you don't have unintended commas in your CSV. You may want to add columns manually if this error persists.

<br>

_____________________________________________________

<br>

<br>

<br>

<br>

<br>

## Update Your Credentials
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

1. Download the `credentials.json` file
2. Update the `client-ID` and `client-secret` with your own, given to you by Google when you register an OAuth 2.0 client with Google via Google API Dashboard's [credential manager](https://console.cloud.google.com/apis/credentials). Go to the [Startup Endpoints section](#Startup-Endpoints) of this readme for a walkthrough on setting up your Google Project credentials.
3. Update the AI token
   1. Go to [replicate's website](https://replicate.com/docs/get-started/python#authenticate) to create a free account (by linking your GitHub account). NOTE: you get 10 free API calls to the AI. You may wish to add a payment method. This will charge you approx $0.000021 per API call using the default settings. Feel free to set a monthly "Spend Limit" on [their billing page](https://replicate.com/account/billing). Supported models and pricing can be found on [their pricing page, in the language models section](https://replicate.com/pricing#language-models)
      1. Model Options:
         1. meta/llama-2-13b
         2. meta/llama-2-13b-chat
         3. meta/llama-2-70b
         4. *meta/llama-2-70b-chat* (**default**)
         5. meta/llama-2-7b
         6. meta/llama-2-7b-chat
         7. meta/meta-llama-3-70b
         8. meta/meta-llama-3-70b-instruct
         9. meta/meta-llama-3-8b
         10. meta/meta-llama-3-8b-instruct
         11. mistralai/mistral-7b-instruct-v0.2
         12. mistralai/mistral-7b-v0.1
         13. mistralai/mixtral-8x7b-instruct-v0.1
      2. Model option is set in the `auto_grader_ai.py` file in the `ai` class, in the `generate_response` static method as the first parameter of the `replicate.stream()` function. Change it to any other model if you'd like.
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

<br>

<br>

<br>

## Startup Endpoints
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

To learn about setting up your endpoints for Google Sheets and Google Forms look at their "Python quickstart guides." ([Python quickstart | Google Sheets link](https://developers.google.com/sheets/api/quickstart/python), [Python quickstart | Google Forms link](https://developers.google.com/forms/api/quickstart/python))

The short version is a 3-step process for both. 
1. Enable the API - must be completed separately for Google Sheets and Google Forms
   1. [Enable Google Sheets Endpoint link](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com)
   2. [Enable Google Forms Endpoint link](https://console.cloud.google.com/flows/enableapi?apiid=forms.googleapis.com)
2. Configure the OAuth consent screen (step-by-step guide in the [OAuth consent screen section](#OAuth-consent-screen))
3. Authorize credentials for a desktop application (step-by-step guide in the [Getting an OAuth Token section](#Getting-an-OAuth-Token))

<br>

_________________________

<br>

<br>

<br>

<br>

<br>

## Getting an OAuth Token
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

Go to [Google Cloud Consol's](https://console.cloud.google.com/) website and select the `APIs & Services` button.

Navigate to the `credentials` tab and select the `+ CREATE CREDENTIALS` button to reveal a drop-down of 4 items. 

Select the second item (`OAuth client ID`, sub-text: "Requests user consent so your app can access the user's data")

This will bring you to the "Create OAuth client ID" page.

Finally, click the application type dropdown, select `Desktop app`, and name it whatever you'd like.

Click the blue `CREATE` button at the bottom of the page.

A pop-up window will appear with your `client-ID` and `client-secret`. Save both somewhere secure.

<br>

_________________________

<br>

<br>

<br>

<br>

<br>

## OAuth consent screen
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

[Navigate to Google's OAuth Consent Screen's website](https://console.cloud.google.com/apis/credentials/consent){:target="_blank"}

**Make sure the correct Google Project is selected in the top left!**

Click on External and hit the blue `CREATE` button.

![image](readme_images/OAuthConcentScreen.png)

<br>

<br>

## Edit app registration - OAuth consent screen

Enter a name in the "App Name" text-entry box and enter your email in the "User Support Email" text-entry box.

Scroll down to the "Developer contact information" section. 
Enter your email again into the "Email Address" text-entry box with the subtext: "*These email addresses are for Google to notify you about any changes to your project.*"

**Leave everything else blank.**

✔️ Select the `Save and Continue` button at the bottom of the page, **leaving everything else blank**.

<br>

<br>

## Edit app registration - Scopes

Select the `ADD OR REMOVE SCOPES` button to open a table of scopes. The following table can be found on page 3. (results 22-27)

|add scope| API             | Scope                             | User-facing description                                                                  |
|---------|-----------------|-----------------------------------|------------------------------------------------------------------------------------------|
|☐|Google Forms API        | .../auth/drive                    | See, edit, create, and delete all of your Google Drive files                             |
|☐|Google Forms API        | .../auth/drive.file               | See, edit, create, and delete only the specific Google Drive files you use with this app |
|☐|Google Forms API        | .../auth/forms.body               | See, edit, create, and delete all your Google Forms forms                                |
|☐|Google Forms API        | .../auth/drive.readonly           | See and download all your Google Drive files                                             |
|☑️| Google Forms API      | .../auth/forms.body.readonly      | See all your Google Forms forms                                                          |
|☑️| Google Forms API      | .../auth/forms.responses.readonly | See all responses to your Google Forms forms                                             |
|☑️| Google Sheets API     | .../auth/spreadsheets             | See, edit, create, and delete all your Google Sheets spreadsheets                        |
|☑️| Google Sheets API     | .../auth/spreadsheets.readonly    | See all your Google Sheets spreadsheets                                                  |
|☐| Service Management API | .../auth/service.management       | Manage your Google API service configuration                                             |

Select the four rows above (28: `forms.body.readonly`, 29: `forms.responses.readonly`, 30: `spreadsheets`, and 31: `service.management`)

Scroll down and select the blue `UPDATE` button at the bottom to close the table and return to the previous page (Edit app registration - Scopes)

Note: *if these rows are missing, you may need to enable these endpoints for your Google Project. Learn more in the [Startup Endpoints Section](#Startup-Endpoints)*

✔️ Select the `SAVE AND CONTINUE` button at the bottom of the page.

<br>

<br>

## Edit app registration - Test users

Click the `+ ADD USERS` button. 

Add the Gmail account that owns the Google Form OR has viewing access to the Google Form's results.

✔️ Scroll to the bottom and select the `SAVE AND CONTINUE` button.

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

<br>

_____________________________________________________

<br>

<br>

<br>

<br>

<br>

# Expected Output
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

<br>

## Expected Local Output Files

## Expected Google Output Files

## What Do The Columns Mean?

<br>

_____________________________________________________

<br>

<br>

<br>

<br>

<br>

##  Possible Considerations for Enterprise Use
###### [back to top](#Grade-Assistant-Proof-of-Concept-PoC)

1. ### Security
   1. ###### Please Note: We do not believe this to be a consideration if you run this code on a local machine in your physical possession. 
   2. We save your `Replicate` token locally in the `token.vault` file using a strong encryption scheme (see `secureparsing.py` for more info). Every time the token is read, it is re-encrypted based on the time. The time is never saved. If this security scheme breaks your corporation's "secure storage standards" (SSS) you may want to consider other solutions for this part. 
      1. A possible solution may be writing it to your operating system's environment variables instead of a local file. This may obfuscate the retrieval process and make it difficult to accidentally leak the token.
      2. Alternatively, if you are running this code on a cloud provider's automation account (AWS, Google Cloud, Microsoft Azure, etc) you may want to look into their secret storage manager (SSM). They do this for you.
   3. We save your Google `Client ID` and `Client Secret` in an unencrypted json file (`credentials.json`). You may wish to change this depending on your corporation's "secure storage standards" (SSS).
   4. The Google OAuth 2.0 token is saved locally in `json` form during runtime. It is never deleted after code execution. In theory, an attacker could leverage this old token to generate a new one, but it is unlikely and reduces the general load if saved like we have it set up to be. The most viable mitigation tactic would be to remove the file after runtime if you do not project the use of this code for longer then an hour.
2. ### Better AI training
   1. We send all data (background, rubric, question, submission) in one single message. This can open up the system to malicious prompt engineering attacks and may reduce the quality of responses from the AI. A potential mitigation/improvement would be training the AI with the background, sending the rubric and question in separate messages, and sending the submission in a final message for grading.
3. ### Improving API call speed (Multithreading)
   1. While grading each question, our code calls the Replicate API. When calling the API: our code waits for a response before grading the next question. On average: Replicate takes 3 - 5 seconds to reply. Running multiple threads or processes may decrease runtime by 80% - 95% depending on the multithreading scheme.
   2. A simpler solution may be to run the code at night or over weekends.

<br>

<br>

<br>

<br>

<br>

<br>
