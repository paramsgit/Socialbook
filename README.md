 
 <img src="sclone/static/logo.png" alt="logo" width="100" height="100" align="right" style="margin-top:15px" /> 

# Socialbook 


Socialbook is a web application built with Django that allows users to connect and share their memories with others. It provides features such for profile management, photo posting, liking, making friends and chat functionality.

## Features

- **Signup with Email OTP Verification**: Users can sign up for an account using their email address and complete the verification process using a One-Time Password (OTP) sent to their email.

- **Profile Section**: Once registered, users have their own profile section where they can manage their personal information, such as username, profile picture, bio, and other details.

- **Photo Posting**: Users can upload and share their photos with the community. They can provide captions, add tags, and select privacy settings for their posts.

- **Likes**: Users can express their appreciation for posts by liking them. The number of likes is displayed on each post, and users can also view a list of users who liked a particular post.

- **Follow/Unfollow**: Users can follow other users to stay updated with their posts. They can also unfollow users if they no longer wish to see their content.

- **Chat**: The website provides a real-time chat feature that allows users to communicate with each other. Users can send text messages, share photos, and have private conversations.

## Installation

To run the project locally, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-social-media-website.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-social-media-website
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv env
   source env/bin/activate
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

7. Access the website locally by visiting [http://localhost:8000](http://localhost:8000) in your web browser.

## Configuration

The application requires some configuration settings to function correctly. You can modify these settings in the `settings.py` file located in the project's root directory. Here are some important settings you might want to customize:

- `EMAIL_BACKEND`: Specify the email backend for sending verification emails. You can use SMTP, a transactional email service like SendGrid, or any other supported backend.

- `DATABASES`: Configure the database settings according to your setup (e.g., PostgreSQL, MySQL, SQLite).

- `MEDIA_ROOT` and `MEDIA_URL`: Set the path where user-uploaded media files will be stored and served.

- `SECRET_KEY`: Update the secret key used for cryptographic signing. Generate a secure key and keep it secret.

Please make sure to secure sensitive information, such as secret keys, database credentials, and API tokens, by using environment variables or other secure methods.

## Contributing

Contributions to this project are welcome. If you have any ideas, suggestions, or bug reports, please open an issue on the project's GitHub repository and describe your proposal. You can also submit a pull request to contribute code improvements.

When contributing, please adhere to the project's code style and follow the guidelines specified in the CONTRIBUTING.md file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowled

gements

This project was developed using the Django web framework. We would like to acknowledge the Django community for their excellent work and documentation that helped us build this application.

## Contact

If you have any questions or need further assistance, feel free to contact us at your-email@example.com.

---

You can use this README file as a starting point and customize it according to your specific project requirements. Remember to update the installation instructions, configuration details, and contact information with your own relevant information.