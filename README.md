# 📚 **Library Management System API**

### **Overview**  
Welcome to the Library Management System API! This backend application allows seamless management of a library, including book inventory, user profiles, and book borrowing/returning functionality. Built with Django and Django REST Framework, the API is scalable, user-friendly, and production-ready.

---

## 🎯 **Features**
### 📖 **Books Management**  
- CRUD operations for books.  
- Attributes: Title, Author, Genre, Published Year, and Availability Status.  

### 👤 **Users Management**  
- CRUD operations for users.  
- Attributes: Name, Email, Membership ID, and Borrowed Books.  

### 🔄 **Borrow & Return**  
- **Check-Out Books**:  
  - Reduces book availability and logs checkout date.  
- **Return Books**:  
  - Updates availability status and logs return date.  

### 🔍 **View Available Books**  
- Filter books by availability.  
- Optional filters: Search by Title, Author, or Genre.  

---

## 🛠️ **Tech Stack**
- **Framework**: Django + Django REST Framework  
- **Database**:  
  - Development: SQLite  
  - Production: PostgreSQL  
- **Deployment**:  
  - **Primary**: Heroku  
  - **Optional**: PythonAnywhere  

---

## 🌐 **API Endpoints**

### 📖 **Books Endpoints**
| Method | Endpoint         | Description              |
|--------|------------------|--------------------------|
| GET    | `/books/`        | List all books           |
| POST   | `/books/`        | Add a new book           |
| GET    | `/books/<id>/`   | Get details of a book    |
| PUT    | `/books/<id>/`   | Update a book            |
| DELETE | `/books/<id>/`   | Delete a book            |

### 👤 **Users Endpoints**
| Method | Endpoint         | Description              |
|--------|------------------|--------------------------|
| GET    | `/users/`        | List all users           |
| POST   | `/users/`        | Add a new user           |
| GET    | `/users/<id>/`   | Get details of a user    |
| PUT    | `/users/<id>/`   | Update a user            |
| DELETE | `/users/<id>/`   | Delete a user            |

### 🔄 **Checkout & Return Endpoints**
| Method | Endpoint        | Description              |
|--------|-----------------|--------------------------|
| POST   | `/checkout/`    | Check out a book         |
| POST   | `/return/`      | Return a book            |

---

## 🗂️ **Data Models**

### **Books**  
| Field               | Type                  | Description                  |
|---------------------|-----------------------|------------------------------|
| `id`                | AutoField             | Unique book identifier       |
| `title`             | CharField             | Book title                   |
| `author`            | CharField             | Book author                  |
| `published_date`    | DateField             | Date of publication          |
| `copies_available`  | PositiveIntegerField  | Number of copies available   |

### **Users**  
| Field               | Type          | Description                  |
|---------------------|---------------|------------------------------|
| `id`                | AutoField     | Unique user identifier       |
| `username`          | CharField     | User’s unique name           |
| `email`             | EmailField    | User’s email                 |
| `date_of_membership`| DateField     | Membership start date        |
| `is_active`         | BooleanField  | Active status of the user    |

### **Transactions**  
| Field               | Type          | Description                  |
|---------------------|---------------|------------------------------|
| `id`                | AutoField     | Unique transaction identifier |
| `user`              | ForeignKey    | User performing the transaction |
| `book`              | ForeignKey    | Book involved in the transaction |
| `checkout_date`     | DateTimeField | Date and time of checkout    |
| `return_date`       | DateTimeField | Date and time of return      |

---


