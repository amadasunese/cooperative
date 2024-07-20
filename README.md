# Cooperative Society Web Application

## Overview
The Cooperative Society Web Application is designed to support the operations of a cooperative society, providing features such as member management, financial services, announcements, news, and more. This application aims to enhance the engagement and financial well-being of the society's members.

## Features
- **Member Management**: Add and manage members, including their personal details, savings, and loans.
- **Financial Services**: Offer savings accounts, loans, and investment opportunities to members.
- **Announcements**: Post announcements for upcoming events, meetings, and polls.
- **News Section**: Share the latest news and updates with members.
- **Services and Products**: Highlight the various services and products offered by the cooperative society.
- **Contact and About Us**: Provide detailed information about the cooperative society and how to get in touch.

## Installation

### Prerequisites
- Python 3.x
- Flask
- Other dependencies listed in `requirements.txt`

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/cooperative-society.git
    cd cooperative-society
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```bash
    export FLASK_APP=run.py
    export FLASK_ENV=development
    ```

5. Initialize the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. Run the application:
    ```bash
    flask run
    ```

## Usage
- Navigate to `http://127.0.0.1:5000` in your web browser to access the application.
- Use the various sections of the application to manage members, post announcements, share news, and more.

## Contributing
We welcome contributions to improve the application. Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any questions or inquiries, please contact us at [amadasunese@gmail.com](mailto:amadasunese@gmail.com).

