Below is an example of a React project using functional components, React Router for routing, and Tailwind CSS for styling. The code snippet focuses on the main components and structure according to the requirements you provided:

```javascript
// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import ContactForm from './components/ContactForm';
import ContactList from './components/ContactList';
import './App.css';

function App() {
  return (
    <Router>
      <div className="container mx-auto px-4">
        <Header />
        <Routes>
          <Route path="/" element={<ContactList />} />
          <Route path="/add" element={<ContactForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

// components/Header.js

import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="py-4 mb-4 border-b">
      <h1 className="text-2xl font-bold"><Link to="/">Contact Management</Link></h1>
      <nav>
        <Link className="mr-4 text-blue-500" to="/">View Contacts</Link>
        <Link className="text-blue-500" to="/add">Add Contact</Link>
      </nav>
    </header>
  );
};

export default Header;

// components/ContactForm.js

import React, { useState } from 'react';

const ContactForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);

    try {
      // Implement API submit logic here
    } catch (error) {
      console.error(error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="max-w-md mx-auto" onSubmit={handleSubmit}>
      <div className="mb-4">
        <label className="block text-sm font-bold mb-2" htmlFor="name">
          Name
        </label>
        <input
          className="border rounded w-full py-2 px-3"
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-bold mb-2" htmlFor="email">
          Email
        </label>
        <input
          className="border rounded w-full py-2 px-3"
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <button
        className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
        type="submit"
        disabled={submitting}
      >
        {submitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
};

export default ContactForm;

// components/ContactList.js

import React, { useEffect, useState } from 'react';

const ContactList = () => {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContacts = async () => {
      setLoading(true);
      try {
        // Implement fetch logic here
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchContacts();
  }, []);

  return (
    <div className="max-w-xl mx-auto">
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul className="divide-y divide-gray-200">
          {contacts.map((contact) => (
            <li key={contact.id} className="py-2">
              {contact.name} - {contact.email}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ContactList;
```

### Explanation:
- **App.js**: This is the main component that handles the routes to `ContactList` and `ContactForm`.
- **Header.js**: Renders a simple header with navigation links to `ContactList` and `ContactForm`.
- **ContactForm.js**: A form for adding a new contact with controlled components and basic validation.
- **ContactList.js**: Fetches and displays contacts, handling the loading state.
- **Tailwind CSS**: Used for styling with utility classes.

Make sure you have Tailwind CSS properly set up in your project (e.g., `tailwindcss` and `postcss` configured) to utilize the styles given in the snippets.

Additionally, you would need to handle API integrations intelligently by using an API Client Module based on the earlier requirements and ensure that HTTP responses are managed effectively as suggested in the "API integration layer" portion of the tasks.