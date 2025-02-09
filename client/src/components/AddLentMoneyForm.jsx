
// src/components/AddLentMoneyForm.jsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/input';
import { useToast } from '@/components/ui/use-toast';
import { api } from '../utils/api';

const AddLentMoneyForm = ({ onSuccess }) => {
  const { register, handleSubmit, reset } = useForm();
  const { toast } = useToast();

  const onSubmit = async (data) => {
    try {
      await api.post('/add-lent-money', data);
      toast({
        title: 'Success',
        description: 'Lent money record added successfully',
      });
      reset();
      if (onSuccess) onSuccess();
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to add lent money record',
        variant: 'destructive',
      });
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Add Lent Money</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Input
              {...register('borrower')}
              placeholder="Borrower Name"
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
            <Input
              {...register('description')}
              placeholder="Description"
              required
            />
          </div>
          <Button type="submit" className="w-full">
            Add Lent Money
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default AddLentMoneyForm;
