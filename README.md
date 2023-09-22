<p align="center">
  <img width="579" alt="Screenshot 2023-08-14 at 8 54 47 PM" src="https://github.com/gangula-karthik/KAKI-App/assets/56480632/4886c3cf-e10f-4aed-9f65-89bd9da6e702">
</p>

<p align="center">
  <strong>KAKI</strong><br>
  HARNESSING THE POWER OF COMMUNITY BUILDING & SUSTAINABILITY
</p>

<p align="center">
  Demo Link: https://youtu.be/GGYOT-R8A7s
</p>

## Testing User View
You may create your own account using your gmail to test this out. (you will receive a verification link to your email)

## Sample Credentials for Testing Admin View
Note: These are sample credentials for testing purposes only. Do not use these in production or for any real transactions. Always keep real credentials private and secure.

### Kaki website 
```
Email: kaki.w3bapp@gmail.com
Password: test123
```

### Gmail for verification link
```
Email: kaki.w3bapp@gmail.com
Password: Trashminator
```

## Prerequisites
Before you proceed, ensure you obtain the following:
```
HUGGINGFACEHUB_API_TOKEN
PYREBASE_API_TOKEN
PYREBASE_APP_ID
RECAPTCHA_SECRET_KEY 
```

### Obtaining HUGGINGFACEHUB_API_TOKEN:
1. Create an account or sign in to your existing account on HuggingFace.
2. Navigate to your profile (usually found in the top-right corner).
3. Click on 'Settings'.
4. In the 'API Tokens' section, you should see your token. If not, there's an option to generate one.
5. Copy this token for the setup process.
   
### Obtaining PYREBASE_API_TOKEN and PYREBASE_APP_ID:
1. Visit the Firebase Console.
2. Click on your project or create a new one.
3. In the Project Overview, click on the gear icon and select 'Project settings'.
4. Under 'Your apps', select the appropriate app type (Web, Android, iOS).
5. You'll find a code snippet that includes your "apiKey" (PYREBASE_API_TOKEN) and "appId" (PYREBASE_APP_ID).
6. Copy these values for the setup process.
   
### Obtaining RECAPTCHA_SECRET_KEY :
1. Go to the reCAPTCHA website.
2. Sign in using your Google account.
3. Click on the title of your website or register a new site.
4. Once registered, you'll find the "SECRET KEY". This is your RECAPTHA_SECRET_KEY.
5. Note it down for the setup.


## Setup
Clone this repository:

```
git clone https://github.com/gangula-karthik/KAKI-App.git
```

Navigate to the project directory:
```
cd KAKI-App
```

In your .env file, fill in the details:
```
HUGGINGFACEHUB_API_TOKEN=YOUR_HUGGINGFACE_TOKEN
PYREBASE_API_TOKEN=YOUR_PYREBASE_TOKEN
PYREBASE_APP_ID=YOUR_PYREBASE_APP_ID
RECAPTCHA_SECRET_KEY =YOUR_RECAPTCHA_SECRET_KEY 
```

Save the .env file at the root of the project and follow any additional setup instructions...


## Contributions
#### Karthik
- Homepage: Designed and implemented the main landing page, ensuring responsive design and user-friendly interface.
- Customer Support: Developed the customer support module, integrated live chat functionality, and ensured timely response mechanisms.
#### Jay
- Account Management: Oversaw the creation and management of user accounts. Implemented features like password reset, profile editing, and two-factor authentication for enhanced security.
#### Jun Ming
- Report Generation: Engineered the report generation system, allowing users to obtain detailed insights and analytics. Ensured data accuracy and provided multiple export formats.
#### Pin Shien
- Transaction Handling: Spearheaded the transaction module, ensuring secure and swift financial transactions. Integrated with multiple payment gateways and implemented fraud detection mechanisms.
