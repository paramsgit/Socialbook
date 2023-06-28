 
 <img src="sclone/static/logo.png" alt="logo" width="100" height="100" align="right"  /> 

# Socialbook 


Socialbook is a web application built with Django that allows users to connect and share their memories with others. It provides features such for profile management, photo posting, liking, making friends and chat functionality.

 <img src="sclone/static/imgs/img1.png" alt="demo"  style="margin:20px 0 40px 0" /> 

## Features

- **Signup with Email OTP Verification**: Users can sign up for an account using their email address and complete the verification process using a One-Time Password (OTP) sent to their email.

<img src="sclone/static/imgs/sig.png" alt="signin"  style="margin:20px 0 40px 0" /> 

- **Profile Section**: Once registered, users have their own profile section where they can manage their personal information, such as username, profile picture, bio, and other details.

<img src="sclone/static/imgs/profilesec.png" alt="profile"  style="margin:20px 0 40px 0" /> 


- **Posts**: Users can upload and share their photos with the community. They can provide captions and even can delete any time their posts.

<img src="sclone/static/imgs/upload.png" alt="profile"  style="margin:20px 0 40px 0" /> 

- **Likes**: Users can express their appreciation for posts by liking them. The number of likes is displayed on each post, Date and time of post is shown in right side of likes.

<img src="sclone/static/imgs/likes.png" alt="profile"  style="margin:20px 0 40px 0" /> 

- **Follow/Unfollow**: Users can follow other users to stay updated with their posts. They can also unfollow users if they no longer wish to see their content.

<img src="sclone/static/imgs/follow.png" alt="profile"  style="margin:20px 0 40px 0" /> 

- **Chat**: The website provides a real-time chat feature that allows users to communicate with each other. Users can send text messages, share photos, and have private conversations.

<img src="sclone/static/imgs/chat.png" alt="profile"  style="margin:20px 0 40px 0" />


# Installation

To run the project locally, follow these steps:

## Requirements
Before running the application, make sure you have the following requirements met:

`Python 3.9` or higher: Ensure that Python is installed on your system. You can download Python from the official Python website: https://www.python.org/ .

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/paramsgit/Socialbook.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Socialbook\sclone
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   pip install virtualenv 
   python -m venv env
   \env\Scripts\activate
   ```

4. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the website locally by visiting [http://localhost:8000](http://localhost:8000) in your web browser. Complete configurations first to avoid any errors.

## Configuration

The application requires some configuration settings to function correctly. You can modify these settings in the `settings.py` file located in the project's root directory. Here are some important settings you might want to customize:


- `DATABASES`: Configure the database settings according to your setup (e.g., PostgreSQL, MySQL, SQLite).
You can download my database file and media here : https://drive.google.com/file/d/1SpW0uBAvFXn5lKZlhkka-hgBomCtOq-h/view?usp=sharing/ . Update database and media path in `settings.py` file.


- `EMAIL_BACKEND`: Specify the email backend for sending verification emails. You can use SMTP, a transactional email service like SendGrid, or any other supported backend.



- `MEDIA_ROOT` and `MEDIA_URL`: Set the path where user-uploaded media files will be stored and served.



Please make sure to secure sensitive information, such as secret keys, database credentials, and API tokens, by using environment variables or other secure methods.

## Contributing

Contributions to this project are welcome. If you have any ideas, suggestions, or bug reports, please open an issue on the project's GitHub repository and describe your proposal. You can also submit a pull request to contribute code improvements.





## Acknowledgements



This project was developed using the Django web framework. We would like to acknowledge the Django community for their excellent work and documentation that helped us build this application.

## Contact

If you have any questions or need further assistance, feel free to contact us at your-email@example.com.
