# Live Link: [Food Shop Backend](https://assignment-twelfth.web.app)

## Overview

The **YUMMY TUMMY** Food Shop Project Backend serves as a comprehensive backend platform tailored for efficient management of a food ordering system. Built with **Django** and **Django REST Framework**, it supports smooth interactions between `customer` (Customer) and `shop admin` (Admin) roles, ensuring a user-friendly and feature-rich experience.

he project allows shop admins to create, update, and manage menu items, handle orders, and oversee customer feedback, while customers can browse the menu, place orders, and track their purchases. Key features include role-based access control, order tracking, and notification functionalities, enhancing the overall user experience for both customers and admins.

Powered by **PostgreSQL** the backend offers robust data management and scalability, preparing it for future expansions and upgrades. This architecture makes **YUMMY TUMMY**  a reliable solution for managing a dynamic and growing food shop business.

---

<br>

## Features

- **Admin Capabilities**:
  - Create, update, and manage menu items.
  - Process and track customer orders.
  - View and respond to customer feedback.

- **Customer Capabilities**:
  - Browse the menu and view item details.
  - Place orders and track order status.
  - Access account details and order history.

- **Additional Features**:
  - Role-based access control to secure different user operations.
  - Real-time order tracking and notifications.
  - Support for future feature enhancements.

 ---

 <br>

 ## Tech Stack

- **Backend Framework**: Django, Django REST Framework
- **Database**: PostgreSQL(Using Supabse Deployment)
  - Ensures reliable data handling, scalability, and flexibility for future improvements.

---

<br>

## Instructions to Run Locally

### Prerequisites

- Python 3.12.2
- Django 4.2.4
- Django REST Framework 3.15.2
- PostgreSQL

### Packages used:

- **Django**: v5.1.2
- **Django REST Framework**: v3.15.2 
- **PostgreSQL**: v2.9.10 (psycopg2-binary)
- **django-cors-headers**: v4.5.0 
- **django-environ**: v0.11.2 
- **requests**: v2.32.3 
- **whitenoise**: v6.7.0
- **sslcommerz-lib**: v1.0 - Payment integration with SSLCommerz
- **pillow**: v11.0.0 
- **JWT**: v8.5.1 


## Getting Started

1. Open `command prompt` in the folder directory where you want to create & run the project locally

2. Copy the `repository_url` to **Clone the repository**

   ```bash
   git clone https://github.com/SunjidaAkter/food_backend.git
   cd food_backend
   ```

3. **Create a virtual environment**

   ```bash
   python -m venv food_venv
   cd food_venv
   Scripts\activate.bat
   cd ..
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   code .
   ```

<br>


5. **Then, add the `SECRET_KEY` in that `.env` file:**

- SECRET_KEY=(Your SECRET_KEY)

       **to get the `SECRET_KEY`, Temporarily `Create a new project` named `food_backend` anywhere `outside the current project directory` (may be in the `desktop`, `documents` or `downloads`, wherever you want, just outside the current project directory)**

- Copy the `secret key` from the temporarily created project's `temp_settings.py` file

<br>

6. **Add the supabase postgreeSQL database credentials** in `.env` file:

- DB_NAME=(Your database name)
- DB_USER=(Your database username)
- DB_PASSWORD=(Your database password)
- DB_HOST=(The host for your database)
- DB_PORT=(The port for your database)



<br>

7. **Also, Add the email sending accessibility credentials** in `.env` file:

- EMAIL: (Your email address for sending emails)
- EMAIL_PASSWORD: (Your email password or an app-specific password)

 
<br>

8. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

9. **Creating superuser**

```bash
python manage.py createsuperuser
```

10. **Run the development server**

```bash
python manage.py runserver
```

<br>

11. **Finally, Access the application**

- Local: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/login/

---

<br>


## API Endpoints

| Endpoint            | Method | Description                     |
|-----------------------------|--------|---------------------------------|
| `/menu/list/`               | POST   | Create Menu Item                |
| `/menu/list/`               | GET    | List all menu items             |
| `/menu/list/<id>/`          | GET    | Retrieve a specific menu item   |
| `/menu/list/<id>/`          | DELETE | Delete a specific menu item     |
| `/menu/list/<id>/`          | PATCH  | Update a specific menu item     |
| `/order/`                   | POST   | Place a new order               |
| `/order/<id>/`              | PATCH  | Update an existing order        |
| `/order/<id>/`              | DELETE | Delete an existing order        |
| `/users/<id>/`              | GET    | Retrieve user details           |
| `/users/`                   | GET    | Retrieve all users              |
| `/user_accounts/list/`      | POST   | Create useraccount              |
| `/user_accounts/list/`      | GET    | Retrieve all useraccounts       |
| `/user_accounts/list/<id>/` | GET    | Retrieve useraccount Detail     |
| `/user_accounts/list/<id>/` | DELETE | Delete useraccount              |
| `/user_accounts/list/<id>/` | PATCH  | Update a specific useraccount   |

---

<br>


###Conclusion###
In developing the Yummy Tummy Food Shop backend, the aim was to build a seamless, secure platform for managing food orders and customer interactions efficiently. Using Django and PostgreSQL ensures a reliable and scalable system, allowing smooth operations between customers and the food shop.

With features like role-based access, order tracking, and menu management, I believe this platform will enhance the customer experience and streamline shop management. I look forward to seeing the value it can add, and if you have any questions or would like to contribute, please reach out!
