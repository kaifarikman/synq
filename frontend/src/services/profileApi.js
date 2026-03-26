import { getAccessToken, request } from './api';

export const profileAPI = {
  getMyProfile() {
    return request('/profile/me', {
      method: 'GET',
      token: getAccessToken(),
    });
  },

  updateMyProfile(payload) {
    return request('/profile/me', {
      method: 'PUT',
      token: getAccessToken(),
      body: payload,
    });
  },
};
