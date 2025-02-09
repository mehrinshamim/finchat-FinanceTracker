
// src/components/TransactionList.jsx
import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { useToast } from '@/components/ui/use-toast';
import { api } from '../utils/api';

const TransactionList = ({ transactions, onUpdate }) => {
  const { toast } = useToast();

  const handleDelete = async (id) => {
    try {
      await api.post('/delete-entry', { id });
      toast({
        title: 'Success',
        description: 'Transaction deleted successfully',
      });
      if (onUpdate) onUpdate();
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to delete transaction',
        variant: 'destructive',
      });
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Transactions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {transactions.map((transaction) => (
            <div
              key={transaction.id}
              className="flex justify-between items-center p-4 border rounded"
            >
              <div>
                <p className="font-medium">{transaction.description}</p>
                <p className="text-sm text-gray-500">{transaction.category}</p>
              </div>
              <div className="flex items-center space-x-4">
                <p className={`font-bold ${
                  transaction.type === 'income' ? 'text-green-600' :
                  transaction.type === 'expense' ? 'text-red-600' :
                  'text-blue-600'
                }`}>
                  ${transaction.amount.toFixed(2)}
                </p>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => handleDelete(transaction.id)}
                >
                  Delete
                </Button>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default TransactionList;