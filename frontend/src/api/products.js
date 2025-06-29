import axiosInstance from './axios';

export const getProducts = async () => {
  const response = await axiosInstance.get('products/');
  return response.data;
};
