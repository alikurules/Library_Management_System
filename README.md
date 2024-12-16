# 📚 **Library Management System API**

### **Overview**  
Welcome to the Library Management System API! This backend application allows seamless management of a library, including book inventory, user profiles, and book borrowing/returning functionality.

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
- Optional filters: Search by Title, Author, or ISPN.  

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
| `book_id`           | AutoField             | Unique book identifier       |
| `title`             | CharField             | Book title                   |
| `author`            | CharField             | Book author                  |
| `ispn`              | CharField             | Unique identifier for books  |
| `published_year`    | DateField             | Date of publication          |
| `availability_status`| PositiveIntegerField  | Number of copies available   |

### **Users**  
| Field               | Type          | Description                  |
|---------------------|---------------|------------------------------|
| `user_id`           | AutoField     | Unique user identifier       |
| `username`          | CharField     | User’s unique name           |
| `email`             | EmailField    | User’s email                 |
| `date_of_membership`| DateField     | Membership start date        |
| `borrowed_book`     | BooleanField  | Borrowed books by user       |

### **Transactions**  
| Field               | Type          | Description                  |
|---------------------|---------------|------------------------------|
| `transaction_id`    | AutoField     | Unique transaction identifier |
| `user_id`           | ForeignKey    | User performing the transaction |
| `book_id`           | ForeignKey    | Book involved in the transaction |
| `borrow_date`       | DateTimeField | Date and time of checkout    |
| `return_date`       | DateTimeField | Date and time of return      |

---

## 🚀 **Deployment**

### **Live API Access**  
- **Primary Platform**: Heroku  
- **Optional Alternative**: PythonAnywhere  

---


