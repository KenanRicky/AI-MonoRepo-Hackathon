import { useEffect, useState } from 'react';
import axios from 'axios';

export default function App() {
  const [expenses, setExpenses] = useState([]);
  const [desc, setDesc] = useState('');
  const [amt, setAmt] = useState('');

  const fetchExpenses = async () => {
    const res = await axios.get('http://localhost:5000/expenses');
    setExpenses(res.data);
  };

  const addExpense = async () => {
    if (!desc || !amt) return;
    await axios.post('http://localhost:5000/expenses', { description: desc, amount: amt });
    setDesc(''); setAmt('');
    fetchExpenses();
  };

  useEffect(() => { fetchExpenses() }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Expense Tracker</h1>
      <input placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)} />
      <input placeholder="Amount" value={amt} type="number" onChange={e => setAmt(e.target.value)} />
      <button onClick={addExpense}>Add</button>
      <ul>
        {expenses.map(e => (
          <li key={e.id}>{e.description} - ${e.amount} - {e.category}</li>
        ))}
      </ul>
    </div>
  );
}
