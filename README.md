
# Cumin Dashboard – A Jira Clone

Cumin Dashboard is a full-stack Jira-inspired project management tool built with **Flask**, **React (Vite)**, and **PostgreSQL**. It supports firm-level collaboration with task tracking, role-based access control, reports, and more.

---

## 📁 Project Structure


cumin-dashboard/
├── backend/        # Flask API with PostgreSQL
├── frontend/       # React + Vite frontend
├── README.md



---

## 🚀 Features

- Role-based access: Firm admin, project-level, and team-level roles
- Task & project management with types, priorities, and progress tracking
- Team creation and member assignment
- Activity logging and real-time notifications
- Project reports and visual analytics
- User onboarding via join requests

---

## 🧰 Tech Stack

- **Frontend**: React + Vite, Tailwind CSS
- **Backend**: Flask (Python), Flask-JWT-Extended, SQLAlchemy
- **Database**: PostgreSQL
- **Hosting**: Render (Free Tier for demo)

---

## 🖥️ Local Development Setup

### ⚙️ Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL
- Git

---

## 🐍 Backend Setup (Flask)

1. Navigate to the backend directory:


   cd backend


2. Create and activate a virtual environment:


   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate


3. Install dependencies:

   pip install -r requirements.txt


4. Create a `.env` file in the `backend/` directory with the following:

   CORS_ORIGINS=*
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://username:password@localhost:5432/your_db_name
   JWT_SECRET_KEY=your-jwt-secret-key
   JWT_HEADER_NAME=Authorization
   JWT_HEADER_TYPE=Bearer


6. Set up the database:


   flask db init
   flask db migrate
   flask db upgrade


7. Start the development server:


   flask run


---

## ⚛️ Frontend Setup (React + Vite)

1. Open a new terminal and navigate to the frontend directory:


   cd frontend


2. Install dependencies:

   npm install

3. Create a `.env` file in the `frontend/` directory:

   VITE_API_URL=http://localhost:5000/api

4. Start the Vite dev server:

   npm run dev

---

## 🌐 Access

* Frontend: [http://localhost:5173](http://localhost:5173)
* Backend API: [http://localhost:5000/api](http://localhost:5000/api)

Ensure PostgreSQL is running and that your `.env` files match your local configuration.

---

## 🧪 Live Demo

* 🔗 **Live App**: [https://cumin-dashboard.onrender.com](https://flask-frontend-ge56.onrender.com/)
* 💻 **GitHub**: [https://github.com/yourusername/cumin-dashboard](https://github.com/abhishek12221732/cumin-dashboard)

> ⚠️ *Note: Initial loading may be slow due to Render’s free-tier hosting (cold starts).*

---

## 📬 Contact

Want to explore admin features or contribute to the project?
📩 Message me on [LinkedIn](https://www.linkedin.com/in/abhishekkumar1732/) or open an issue on GitHub.

---

## 📝 License

This project is intended for educational and demo purposes. Licensing can be added based on future requirements.


