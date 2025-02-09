
// src/pages/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';

const Dashboard = () => {
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState({
    totalExpenses: 0,
    totalIncome: 0,
    totalLent: 0,
  });
  const { toast } = useToast();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [transactionsRes] = await Promise.all([
          api.get('/view-transactions'),
        ]);

        setTransactions(transactionsRes.data);

        // Calculate summary
        const expenses = transactionsRes.data
          .filter(t => t.type === 'expense')
          .reduce((sum, t) => sum + t.amount, 0);
        const income = transactionsRes.data
          .filter(t => t.type === 'income')
          .reduce((sum, t) => sum + t.amount, 0);
        const lent = transactionsRes.data
          .filter(t => t.type === 'lent' && !t.reimbursed)
          .reduce((sum, t) => sum + t.amount, 0);

        setSummary({
          totalExpenses: expenses,
          totalIncome: income,
          totalLent: lent,
        });
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to fetch dashboard data',
          variant: 'destructive',
        });
      }
    };

    fetchData();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Total Income</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-green-600">
              ${summary.totalIncome.toFixed(2)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Total Expenses</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-red-600">
              ${summary.totalExpenses.toFixed(2)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Money Lent</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-blue-600">
              ${summary.totalLent.toFixed(2)}
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Transactions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {transactions.slice(0, 5).map((transaction) => (
              <div
                key={transaction.id}
                className="flex justify-between items-center p-4 border rounded"
              >
                <div>
                  <p className="font-medium">{transaction.description}</p>
                  <p className="text-sm text-gray-500">{transaction.category}</p>
                </div>
                <p className={`font-bold ${
                  transaction.type === 'income' ? 'text-green-600' :
                  transaction.type === 'expense' ? 'text-red-600' :
                  'text-blue-600'
                }`}>
                  ${transaction.amount.toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;