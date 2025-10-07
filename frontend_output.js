Here is a basic implementation of the React component code implementing the specified requirements using functional components, Tailwind CSS, and React Router. This includes the routing setup, form component with validation, and a list displaying contacts:

```javascript
// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Form from './components/Form';
import ContactList from './components/ContactList';

function App() {
  return (
    <Router>
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold">Contact Manager</h1>
        <Routes>
          <Route path="/" element={<Form />} />
          <Route path="/contacts" element={<ContactList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

// components/Form.js
import React, { useState } from 'react';

function Form() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [errorMessage, setErrorMessage] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !email) {
      setErrorMessage('Name and email are required.');
      return;
    }
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
      setErrorMessage('Invalid email format.');
      return;
    }
    setErrorMessage(null);
    // Handle form submission (e.g., to the API)
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4">
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700" htmlFor="name">
          Name
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
          placeholder="Enter your name"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700" htmlFor="email">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
          placeholder="Enter your email"
        />
      </div>
      {errorMessage && (
        <div className="mb-4 text-red-500 text-sm">{errorMessage}</div>
      )}
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Submit
      </button>
    </form>
  );
}

export default Form;

// components/ContactList.js
import React, { useEffect, useState } from 'react';

function ContactList() {
  const [contacts, setContacts] = useState([]);

  useEffect(() => {
    // Fetch contacts from API
    setContacts([
      { id: 1, name: 'John Doe', email: 'john@example.com', createdAt: '2023-10-10' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com', createdAt: '2023-10-11' },
    ]);
  }, []);

  return (
    <div className="mt-4">
      <h2 className="text-xl font-bold">Contact List</h2>
      <table className="mt-2 min-w-full bg-white shadow-md rounded-lg overflow-hidden">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b">Name</th>
            <th className="py-2 px-4 border-b">Email</th>
            <th className="py-2 px-4 border-b">Created At</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map(contact => (
            <tr key={contact.id}>
              <td className="py-2 px-4 border-b">{contact.name}</td>
              <td className="py-2 px-4 border-b">{contact.email}</td>
              <td className="py-2 px-4 border-b">{new Date(contact.createdAt).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ContactList;
```

To run this code, make sure you have set up a React project with Tailwind CSS and React Router. You can adjust the `useEffect` hook in `ContactList.js` to fetch contacts from an actual API once the backend is ready.