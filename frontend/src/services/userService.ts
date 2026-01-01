import api from './api';

export const userService = {
  async getProfile(): Promise<any> {
    const response = await api.get('/user/profile');
    return response.data;
  },

  async updateProfile(data: { name: string; username: string }): Promise<any> {
    const response = await api.put('/user/profile', data);
    return response.data;
  },

  async changePassword(data: { currentPassword: string; newPassword: string }): Promise<any> {
    const response = await api.post('/user/change-password', data);
    return response.data;
  },

  async deleteAccount(password: string): Promise<any> {
    const response = await api.delete('/user/account', {
      data: { password },
    });
    return response.data;
  },

  async getAccountStats(): Promise<any> {
    const response = await api.get('/user/stats');
    return response.data;
  },

  async exportData(): Promise<any> {
    const response = await api.get('/user/export');
    return response.data;
  },
};
