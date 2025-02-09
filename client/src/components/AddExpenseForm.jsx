
// src/components/AddExpenseForm.jsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { api } from '../utils/api';

const AddExpenseForm = ({ onSuccess }) => {
  const { register, handleSubmit, reset } = useForm();
  const { toast } = useToast();

  const onSubmit = async (data) => {
    try {
      await api.post('/add-expense', data);
      toast({
        title: 'Success',
        description: 'Expense added successfully',
      });
      reset();
      if (onSuccess) onSuccess();
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to add expense',
        variant: 'destructive',
      });
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Add Expense</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Input
              {...register('description')}
              placeholder="Description"
              required
            />
          </div>
          <div className="space-y-2">
            <Input
              {...register('amount')}
              type="number"
              step="0.01"
              placeholder="Amount"
              required
            />
          </div>
          <div className="space-y-2">
            <Select {...register('category')} required>
              <option value="">Select Category</option>
              <option value="food">Food</option>
              <option value="transport">Transport</option>
              <option value="utilities">Utilities</option>
              <option value="entertainment">Entertainment</option>
              <option value="other">Other</option>
            </Select>
          </div>
          <Button type="submit" className="w-full">
            Add Expense
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default AddExpenseForm;
