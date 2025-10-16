olaf-admin/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── utils/
│   │   │   ├── security.py
│   │   │   └── billing.py
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── admins.py
│   │       ├── users.py
│   │       └── transactions.py
│   └── requirements.txt
│
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── index.jsx
│       ├── services/
│       │   └── api.js
│       └── components/
│           ├── Dashboard.jsx
│           ├── UsersTable.jsx
│           └── Transactions.jsx
│
├── docker-compose.yml
├── .env.example
└── README.md