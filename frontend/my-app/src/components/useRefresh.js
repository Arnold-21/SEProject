import { useState } from 'react';

export default function useRefresh() {
  const getRefresh = () => {
    const refreshString = localStorage.getItem('refresh');
    const userRefresh = JSON.parse(refreshString);
    return userRefresh;
  };

  const [refresh, setRefresh] = useState(getRefresh());

  const saveRefresh = userRefresh => {
    localStorage.setItem('refresh', JSON.stringify(userRefresh));
    setRefresh(userRefresh.refresh);
  };

  return {
    setRefresh: saveRefresh,
    refresh
  }
}