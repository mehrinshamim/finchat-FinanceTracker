
// src/components/CategoryForm.jsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { api } from '../utils/api';

const CategoryForm = ({ onSuccess }) => {
  const { register, handleSubmit, reset } = useForm();
  const { toast } = useToast();

  const onSubmit = async (data) => {
    try {
      const endpoint = data.type === 'income' ? '/add-income-category' : '/add-expense-category';
      await api.post(endpoint, { name: data.name });
      toast({
        title: 'Success',
        description: 'Category added successfully',
      });
      reset();
      if (onSuccess) onSuccess();
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.message || 'Failed to add category',
        variant: 'destructive',
      });
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Add Category</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Select {...register('type')} required>
              <option value="">Select Type</option>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </Select>
          </div>
          <div className="space-y-2">
            <Input
              {...register('name')}
              placeholder="Category Name"
              required
            />
          </div>
          <Button type="submit" className="w-full">
            Add Category
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default CategoryForm;
