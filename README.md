# Apex - Graphical Password Authentication System

**SIH 2022 - DR705 - Graphical Password Authentication (AICTE)**

A Django-based web application implementing a secure graphical password authentication system using cryptocurrency-themed images. This system combines traditional text-based passwords with visual authentication for enhanced security.

## 🎯 Features

- **Dual Authentication**: Combines traditional username/password with graphical password
- **Visual Security**: Select 4-6 images in a specific sequence as your visual password
- **Secure Storage**: Image sequences are hashed with salt using SHA-256
- **Interactive UI**: Modern, responsive interface with real-time visual feedback
- **User-Friendly**: Clear selection indicators showing the order of selected images
- **50+ Images**: Large pool of cryptocurrency-themed images to choose from

## 🚀 How It Works

### Registration
1. Enter username, email, and traditional password
2. Select 4-6 images from the grid in a specific order
3. Visual feedback shows your selection order with numbers
4. The image sequence is securely hashed and stored in the database

### Login
1. Enter username and traditional password
2. Select the SAME images in the SAME order as during registration
3. System validates both text and graphical passwords
4. Access granted only if both match

## 📋 Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## 🛠️ Installation & Setup

### 1. Clone or Download the Repository

```bash
cd /Users/himanshunimonkar/Downloads/Apex_SIH-main/apex-main
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Create a Superuser (Optional - for Admin Access)

```bash
python3 manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Run the Development Server

```bash
python3 manage.py runserver
```

### 7. Access the Application

Open your web browser and navigate to:
- **Registration Page**: http://127.0.0.1:8000/register
- **Login Page**: http://127.0.0.1:8000/login
- **Admin Panel**: http://127.0.0.1:8000/admin (requires superuser account)

## 📱 Usage Guide

### Creating an Account

1. Navigate to the registration page
2. Fill in your details:
   - Username (unique)
   - Email address
   - Text password
3. Scroll down to the image grid
4. Click on 4-6 images in a specific order
   - Selected images show a green border and a number
   - The number indicates the selection order
5. Click "SUBMIT" to create your account
6. You'll be redirected to the login page upon successful registration

### Logging In

1. Navigate to the login page
2. Enter your username and text password
3. Select the SAME images in the SAME order as during registration
   - Selected images show a blue border and numbers
4. Click "LOGIN"
5. If both passwords match, you'll be logged in successfully

### Important Notes

- ⚠️ **Order Matters**: The sequence of selected images is part of your password
- ⚠️ **Remember Your Pattern**: Choose a memorable pattern or sequence
- ⚠️ **No Password Recovery**: Currently, there's no password recovery feature
- ✅ **Security**: Image sequences are hashed and cannot be retrieved

## 🔒 Security Features

1. **Salted Hashing**: Each user's graphical password is hashed with a unique salt
2. **SHA-256**: Industry-standard cryptographic hash function
3. **CSRF Protection**: Django's built-in CSRF protection enabled
4. **No Plain Storage**: Image sequences are never stored in plain text
5. **Secure Comparison**: Uses cryptographic hash comparison for validation

## 📁 Project Structure

```
apex-main/
├── accounts/                   # Main application
│   ├── migrations/            # Database migrations
│   ├── templates/accounts/    # HTML templates
│   │   ├── register.html     # Registration page with graphical password
│   │   ├── login.html        # Login page with graphical password
│   │   └── ...
│   ├── admin.py              # Admin configuration
│   ├── models.py             # Database models (User, GraphicalPassword)
│   ├── views.py              # Business logic and controllers
│   └── urls.py               # URL routing
├── apex/                      # Project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── ...
├── static/                    # Static files
│   └── images/               # 50+ cryptocurrency images
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## 🎨 Technologies Used

- **Backend**: Django 4.0.3
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Security**: hashlib (SHA-256), secrets module
- **UI Framework**: Bootstrap 4

## 🐛 Troubleshooting

### Module Not Found Error
```bash
# Ensure virtual environment is activated and dependencies are installed
pip install -r requirements.txt
```

### Database Errors
```bash
# Delete db.sqlite3 and migrations, then recreate
rm db.sqlite3
rm -rf accounts/migrations/
python3 manage.py makemigrations accounts
python3 manage.py migrate
```

### Images Not Loading
- Ensure all images are in `static/images/` directory
- Check that `STATICFILES_DIRS` is correctly configured in `settings.py`

## 🔮 Future Enhancements

- [ ] Image randomization (different image order each session)
- [ ] Password strength indicator
- [ ] Multi-factor authentication
- [ ] Password recovery mechanism
- [ ] User profile management
- [ ] Session timeout
- [ ] Rate limiting for login attempts
- [ ] Mobile-responsive improvements

## 👥 Team

This project was developed for Smart India Hackathon 2022 (SIH 2022)
- **Problem Statement**: DR705 - Graphical Password Authentication
- **Organization**: AICTE

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

This is an academic project developed for SIH 2022. Contributions, issues, and feature requests are welcome!

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation: https://docs.djangoproject.com/
3. Open an issue in the repository

---

**Note**: This is a demonstration project for educational purposes. For production use, additional security measures and testing should be implemented.
